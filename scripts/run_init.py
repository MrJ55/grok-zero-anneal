"""Create a new run directory from templates/run."""
from __future__ import annotations

import json
import shutil
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def init_run(
    dest: Path | str,
    *,
    force: bool = False,
    plan_goal: str | None = None,
) -> Path:
    """Copy templates/run into dest. Returns dest path."""
    dest_p = Path(dest).resolve()
    template = repo_root() / "templates" / "run"
    if not template.is_dir():
        raise FileNotFoundError(f"missing template: {template}")

    if dest_p.exists():
        if any(dest_p.iterdir()) and not force:
            raise FileExistsError(f"destination not empty (use force=True): {dest_p}")
    else:
        dest_p.mkdir(parents=True)

    for item in template.iterdir():
        target = dest_p / item.name
        if item.is_dir():
            if target.exists() and force:
                shutil.rmtree(target)
            shutil.copytree(item, target, dirs_exist_ok=force)
        else:
            if target.exists() and not force:
                continue
            shutil.copy2(item, target)

    # ensure standard dirs
    for sub in ("briefs", "out", "workspace", "workspace/tests"):
        (dest_p / sub).mkdir(parents=True, exist_ok=True)

    plan_path = dest_p / "plan.md"
    if plan_goal:
        plan_path.write_text(
            f"# Plan\n\nGoal: {plan_goal}\n\nUnits:\n1. ...\n\nDone when: gates green\n",
            encoding="utf-8",
        )
    elif not plan_path.exists():
        plan_path.write_text(
            "# Plan\n\nGoal: <one sentence>\n\nUnits:\n1. ...\n\nDone when: <gate>\n",
            encoding="utf-8",
        )

    tasks_path = dest_p / "tasks.json"
    if not tasks_path.exists():
        tasks_path.write_text(
            json.dumps({"tasks": []}, indent=2) + "\n",
            encoding="utf-8",
        )

    state_path = dest_p / "state.json"
    if not state_path.exists():
        state_path.write_text(
            json.dumps({"completed": [], "attempts": {}, "stages": {}}, indent=2) + "\n",
            encoding="utf-8",
        )

    return dest_p


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Initialize a grok-zero-anneal run directory")
    p.add_argument("dest", help="Destination path, e.g. runs/my-run")
    p.add_argument("--force", action="store_true", help="Overwrite template files")
    p.add_argument("--goal", default=None, help="Seed plan.md goal line")
    args = p.parse_args(argv)
    path = init_run(args.dest, force=args.force, plan_goal=args.goal)
    print(path)
    print("# exports:")
    print(f"export RUN_DIR={path}")
    print("export WORKER_BACKEND=zen_responses")
    print("export OPENCODE_API_KEY=...  # never commit")
    print("export WORKER_MODEL=muse-spark-1.2-contributor-free")
    print("export MAX_PARALLEL_WORKERS=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
