# Run directory template

Copy this folder to `runs/<id>/` then:

1. Edit `plan.md` and `tasks.json`
2. Add `briefs/<task-id>.md` for each task
3. Put tests (and any seed code) under `workspace/`
4. `export RUN_DIR=...` and run `python scripts/openrouter_sequencer.py` from the repo root (or any cwd with RUN_DIR set)
