---
name: gza-dispatch
description: Run the grok-zero-anneal sequencer for a prepared RUN_DIR, set parallel workers for disjoint targets, and summarize state and failures. Use when dispatching workers, running the sequencer, or starting a ledger wave.
---

# gza-dispatch

## Preconditions

- `RUN_DIR` has `tasks.json`, `briefs/<id>.md` for pending tasks, and tests under `workspace/`.
- `OPENCODE_API_KEY` or `WORKER_API_KEY` available in the environment (never echo full key).

## Parallelism

- Default `MAX_PARALLEL_WORKERS=1`.
- Raise to 2-4 only when ready tasks have **distinct** `target` paths and no unmet deps.
- Cap at 4 unless user asks higher and rate limits allow.

## Run

```bash
export RUN_DIR=<absolute run path>
export WORKER_BACKEND=zen_responses
export WORKER_MODEL=muse-spark-1.2-contributor-free
export MAX_PARALLEL_WORKERS=<1-4>
export MAX_ATTEMPTS=3
python -m scripts.cli run --run-dir "$RUN_DIR" --parallel "$MAX_PARALLEL_WORKERS"
```

Zen Muse auth is **x-api-key only** (client sets this). Do not send Bearer for Zen Responses.

## After

1. Read `state.json` (`completed`, `stages`, `attempts`).
2. On failure or `manager_fix`, open `out/<id>-aN.md` and `out/<id>-aN-pytest.txt`.
3. Summarize pass/fail per task for the user.
4. Escalate as manager (fix code/contracts) only after worker attempts exhausted or contracts were wrong.
