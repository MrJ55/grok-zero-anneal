#!/usr/bin/env python3
"""Restartable sequencer: pure workers via WorkerClient (Zen Muse default)."""
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


def run_one_task(task: dict, state: dict, max_attempts: int) -> bool:
    tid = task["id"]
    brief_path = RUN / "briefs" / f"{tid}.md"
    brief = brief_path.read_text(encoding="utf-8")
    attempts = int(state["attempts"].get(tid, 0))
    target_rel = task.get("target", "module.py")
    pytest_args = task.get("pytest_args")
    worker = make_worker()

    while attempts < max_attempts:
        attempts = bump_attempt(state, tid)
        # bump_attempt already incremented; sync loop var
        attempts = int(state["attempts"][tid])
        save_state(STATE_PATH, state)
        print(
            f"== worker {tid} attempt {attempts} "
            f"model={worker.config.model} backend={worker.config.backend}"
        )
        try:
            raw = worker.generate(SYSTEM, brief)
        except WorkerError as e:
            log({"task": tid, "attempt": attempts, "error": str(e), "status": e.status})
            print("worker error:", e)
            continue

        out_dir = RUN / "out"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{tid}-a{attempts}.md").write_text(raw, encoding="utf-8")
        log({"task": tid, "attempt": attempts, "chars": len(raw)})

        code, _notes = parse_worker_response(raw)
        if not code:
            print("no code extracted; retry")
            continue

        place_module(code, target_rel)
        rc, tout = run_tests(pytest_args)
        (out_dir / f"{tid}-a{attempts}-pytest.txt").write_text(tout, encoding="utf-8")
        print(tout)
        if rc == 0:
            mark_complete(state, tid)
            save_state(STATE_PATH, state)
            print(f"PASS {tid}")
            return True
        print(f"FAIL tests attempt {attempts}")
        brief = (
            brief
            + "\n\nPrevious attempt failed tests:\n\n"
            + tout[-3000:]
            + "\n\nFix the implementation. Avoid backticks inside docstrings.\n"
        )
    print(f"GAVE UP {tid}")
    return False


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
                print("stuck pending (deps?):", pending)
                return 1
            print("ALL DONE")
            return 0

        wave = wave_for_parallel(ready, MAX_WORKERS)

        if len(wave) == 1 or MAX_WORKERS <= 1:
            ok = run_one_task(wave[0], state, max_attempts)
            if not ok:
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
                else:
                    save_state(STATE_PATH, state)
                    return 1
            save_state(STATE_PATH, state)
            completed = set(state.get("completed") or [])


if __name__ == "__main__":
    raise SystemExit(main())
