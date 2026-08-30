#!/usr/bin/env python3
"""Restartable sequencer: pure workers + anneal stages (implement/verify/manager_fix)."""
from __future__ import annotations

import concurrent.futures
import json
import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from scripts.codegen_parse import parse_worker_response  # noqa: E402
from scripts.rebrief import append_extract_failure, append_pytest_failure  # noqa: E402
from scripts.stages import Stage, next_stage, record_stage  # noqa: E402
from scripts.state_store import bump_attempt, load_state, mark_complete, save_state  # noqa: E402
from scripts.task_graph import ready_tasks, validate_tasks, wave_for_parallel  # noqa: E402
from scripts.worker_client import WorkerError, make_worker  # noqa: E402

if os.environ.get("RUN_DIR"):
    RUN = Path(os.environ["RUN_DIR"]).resolve()
else:
    RUN = Path.cwd().resolve()

WORK = RUN / "workspace"
STATE_PATH = RUN / "state.json"
TRANSCRIPT = RUN / "transcript.jsonl"
MAX_WORKERS = int(os.environ.get("MAX_PARALLEL_WORKERS", "1"))


def log(event: dict) -> None:
    TRANSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    with TRANSCRIPT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


SYSTEM = (
    "You are a codegen worker with no tools and no repository access. "
    "Implement only what the brief asks. Respond with exactly two sections:\n"
    "## code\n\n```python\n# implementation\n```\n\n## notes\n\n...\n"
    "Avoid triple-backtick sequences inside docstrings; use plain quotes."
)

IDEATION_SYSTEM = (
    "You are an ideation worker with no tools. Propose approaches only. "
    "Do not write full implementation code. Respond with markdown notes."
)


def place_module(code: str, rel: str) -> Path:
    target = WORK / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    init = target.parent / "__init__.py"
    if not init.exists():
        init.write_text("# package\n", encoding="utf-8")
    target.write_text(code.rstrip() + "\n", encoding="utf-8")
    return target


def run_tests(pytest_args: list[str] | None = None) -> tuple[int, str]:
    import subprocess

    args = pytest_args or ["tests", "-q"]
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", *args],
        cwd=str(WORK),
        capture_output=True,
        text=True,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def maybe_ideation(task: dict, worker) -> None:
    """Optional notes-only worker into run notes.md when task.ideation is true."""
    if not task.get("ideation"):
        return
    brief_path = RUN / "briefs" / f"{task['id']}.md"
    brief = brief_path.read_text(encoding="utf-8") if brief_path.exists() else task.get("title", "")
    prompt = (
        "Propose 2-3 approaches for this unit. No full code.\n\n" + brief
    )
    try:
        notes = worker.generate(IDEATION_SYSTEM, prompt)
    except WorkerError as e:
        log({"task": task["id"], "stage": "ideation", "error": str(e)})
        return
    notes_path = RUN / "notes.md"
    prev = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
    block = f"\n\n## ideation:{task['id']}\n\n{notes.strip()}\n"
    notes_path.write_text(prev + block, encoding="utf-8")
    log({"task": task["id"], "stage": "ideation", "chars": len(notes)})


def run_one_task(task: dict, state: dict, max_attempts: int) -> bool:
    tid = task["id"]
    brief_path = RUN / "briefs" / f"{tid}.md"
    brief = brief_path.read_text(encoding="utf-8")
    target_rel = task.get("target", "module.py")
    pytest_args = task.get("pytest_args")
    worker = make_worker()

    maybe_ideation(task, worker)

    record_stage(state, tid, Stage.IMPLEMENT, detail="start")
    log({"task": tid, "stage": Stage.IMPLEMENT.value, "event": "start"})
    save_state(STATE_PATH, state)

    while True:
        attempts = int(state.get("attempts", {}).get(tid, 0))
        stage = next_stage(
            code_placed=False,
            implement_attempts=attempts,
            max_implement_attempts=max_attempts,
        )
        if stage == Stage.MANAGER_FIX:
            record_stage(state, tid, Stage.MANAGER_FIX, detail="max implement attempts")
            save_state(STATE_PATH, state)
            log({"task": tid, "stage": Stage.MANAGER_FIX.value})
            print(f"MANAGER_FIX {tid} — exhausted worker attempts; manager must intervene")
            return False

        attempts = bump_attempt(state, tid)
        attempts = int(state["attempts"][tid])
        save_state(STATE_PATH, state)
        print(
            f"== stage=implement task={tid} attempt={attempts} "
            f"model={worker.config.model} backend={worker.config.backend}"
        )
        log({"task": tid, "stage": Stage.IMPLEMENT.value, "attempt": attempts})

        try:
            raw = worker.generate(SYSTEM, brief)
        except WorkerError as e:
            log(
                {
                    "task": tid,
                    "stage": Stage.IMPLEMENT.value,
                    "attempt": attempts,
                    "error": str(e),
                    "status": e.status,
                }
            )
            print("worker error:", e)
            if attempts >= max_attempts:
                record_stage(state, tid, Stage.MANAGER_FIX, detail="worker errors")
                save_state(STATE_PATH, state)
                print(f"MANAGER_FIX {tid}")
                return False
            continue

        out_dir = RUN / "out"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{tid}-a{attempts}.md").write_text(raw, encoding="utf-8")
        log({"task": tid, "stage": Stage.IMPLEMENT.value, "attempt": attempts, "chars": len(raw)})

        code, _notes = parse_worker_response(raw)
        if not code:
            print("no code extracted; rebrief")
            brief = append_extract_failure(brief)
            log({"task": tid, "stage": Stage.IMPLEMENT.value, "event": "extract_fail"})
            if attempts >= max_attempts:
                record_stage(state, tid, Stage.MANAGER_FIX, detail="extract failed")
                save_state(STATE_PATH, state)
                print(f"MANAGER_FIX {tid}")
                return False
            continue

        place_module(code, target_rel)
        record_stage(state, tid, Stage.VERIFY, detail="code placed")
        log({"task": tid, "stage": Stage.VERIFY.value, "attempt": attempts})
        save_state(STATE_PATH, state)

        print(f"== stage=verify task={tid} attempt={attempts}")
        rc, tout = run_tests(pytest_args)
        (out_dir / f"{tid}-a{attempts}-pytest.txt").write_text(tout, encoding="utf-8")
        print(tout)

        nxt = next_stage(
            verify_ok=(rc == 0),
            implement_attempts=attempts,
            max_implement_attempts=max_attempts,
            code_placed=True,
        )
        if nxt == Stage.DONE:
            record_stage(state, tid, Stage.DONE, detail="verify ok")
            mark_complete(state, tid)
            save_state(STATE_PATH, state)
            log({"task": tid, "stage": Stage.DONE.value, "attempt": attempts})
            print(f"PASS {tid}")
            return True

        print(f"FAIL verify attempt {attempts} -> {nxt.value}")
        log(
            {
                "task": tid,
                "stage": Stage.VERIFY.value,
                "attempt": attempts,
                "ok": False,
                "next": nxt.value,
            }
        )
        if nxt == Stage.MANAGER_FIX:
            record_stage(state, tid, Stage.MANAGER_FIX, detail="verify exhausted")
            save_state(STATE_PATH, state)
            print(f"MANAGER_FIX {tid}")
            return False

        # Back to implement with augmented brief
        record_stage(state, tid, Stage.IMPLEMENT, detail="rebrief after verify fail")
        brief = append_pytest_failure(brief, tout)
        save_state(STATE_PATH, state)


def main() -> int:
    tasks_path = RUN / "tasks.json"
    if not tasks_path.exists():
        raise SystemExit(f"missing {tasks_path}; set RUN_DIR")
    tasks = json.loads(tasks_path.read_text(encoding="utf-8"))["tasks"]
    validate_tasks(tasks)
    state = load_state(STATE_PATH)
    max_attempts = int(os.environ.get("MAX_ATTEMPTS", "3"))
    completed = set(state.get("completed") or [])

    while True:
        ready = ready_tasks(tasks, completed)
        if not ready:
            pending = [t["id"] for t in tasks if t["id"] not in completed]
            if pending:
                # Surface manager_fix tasks clearly
                stages = state.get("stages") or {}
                for pid in pending:
                    cur = (stages.get(pid) or {}).get("current")
                    if cur == Stage.MANAGER_FIX.value:
                        print(f"pending manager_fix: {pid}")
                print("stuck pending:", pending)
                return 1
            print("ALL DONE")
            return 0

        wave = wave_for_parallel(ready, MAX_WORKERS)

        if len(wave) == 1 or MAX_WORKERS <= 1:
            ok = run_one_task(wave[0], state, max_attempts)
            if not ok:
                save_state(STATE_PATH, state)
                return 1
            completed = set(state.get("completed") or [])
            continue

        print(f"== parallel wave size={len(wave)} max={MAX_WORKERS}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(wave)) as ex:
            futs = {
                ex.submit(
                    run_one_task,
                    t,
                    {
                        "completed": list(completed),
                        "attempts": dict(state.get("attempts") or {}),
                        "stages": json.loads(json.dumps(state.get("stages") or {})),
                    },
                    max_attempts,
                ): t
                for t in wave
            }
            for fut in concurrent.futures.as_completed(futs):
                t = futs[fut]
                ok = fut.result()
                if ok:
                    mark_complete(state, t["id"])
                    record_stage(state, t["id"], Stage.DONE, detail="parallel wave")
                else:
                    record_stage(state, t["id"], Stage.MANAGER_FIX, detail="parallel wave fail")
                    save_state(STATE_PATH, state)
                    return 1
            save_state(STATE_PATH, state)
            completed = set(state.get("completed") or [])


if __name__ == "__main__":
    raise SystemExit(main())
