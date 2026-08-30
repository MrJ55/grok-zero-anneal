# Run directory template

```bash
python -m scripts.cli init-run runs/my-run --goal "..."
# or: python scripts/run_init.py runs/my-run
```

Then:

1. Edit `plan.md` and `tasks.json`
2. Add `briefs/<task-id>.md` for each task
3. Put tests under `workspace/tests/`
4. Dispatch:

```bash
export RUN_DIR=$PWD/runs/my-run
export OPENCODE_API_KEY=...
export WORKER_BACKEND=zen_responses
python -m scripts.cli run --parallel 2
```
