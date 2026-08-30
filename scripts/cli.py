"""Thin CLI: python -m scripts.cli <command>"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def cmd_init_run(args: argparse.Namespace) -> int:
    from scripts.run_init import init_run

    path = init_run(args.dest, force=args.force, plan_goal=args.goal)
    print(path)
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir or os.environ.get("RUN_DIR") or "").resolve()
    if not run_dir.is_dir():
        print("RUN_DIR missing; pass --run-dir or export RUN_DIR", file=sys.stderr)
        return 2
    env = os.environ.copy()
    env["RUN_DIR"] = str(run_dir)
    if args.parallel is not None:
        env["MAX_PARALLEL_WORKERS"] = str(args.parallel)
    if args.attempts is not None:
        env["MAX_ATTEMPTS"] = str(args.attempts)
    seq = _repo_root() / "scripts" / "sequencer.py"
    proc = subprocess.run([sys.executable, str(seq)], env=env)
    return proc.returncode


def cmd_check_auth(args: argparse.Namespace) -> int:
    """One-shot Muse/chat pong without printing secrets."""
    try:
        from scripts.worker_client import make_worker

        w = make_worker()
        text = w.generate("", "Reply with exactly one word: pong")
        ok = "pong" in (text or "").lower()
        print("ok" if ok else f"unexpected: {text[:80]!r}")
        print(f"backend={w.config.backend} model={w.config.model}")
        return 0 if ok else 1
    except Exception as e:
        print(f"fail: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scripts.cli", description="grok-zero-anneal CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init-run", help="Create run dir from template")
    p_init.add_argument("dest")
    p_init.add_argument("--force", action="store_true")
    p_init.add_argument("--goal", default=None)
    p_init.set_defaults(func=cmd_init_run)

    p_run = sub.add_parser("run", help="Run sequencer on RUN_DIR")
    p_run.add_argument("--run-dir", default=None)
    p_run.add_argument("--parallel", type=int, default=None)
    p_run.add_argument("--attempts", type=int, default=None)
    p_run.set_defaults(func=cmd_run)

    p_auth = sub.add_parser("check-auth", help="Smoke worker completion")
    p_auth.set_defaults(func=cmd_check_auth)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
