---
name: gza-run-init
description: Initialize a grok-zero-anneal run directory from templates/run and print Muse worker env exports. Use when the user or manager needs a new ledger run, init run dir, or runs/slug scaffold for grok-zero-anneal.
---

# gza-run-init

## Preconditions

- Working with repo https://github.com/MrJ55/grok-zero-anneal (clone or GitHub tools).
- You are the manager. User only supplies goal/slug if any.

## Steps

1. Choose destination `runs/<slug>/` (slug from user or derived from goal).
2. Prefer CLI when repo is on disk:

```bash
python -m scripts.cli init-run runs/<slug> --goal "<goal text>"
```

3. If CLI unavailable, copy `templates/run/` to `runs/<slug>/` and ensure dirs `briefs/`, `out/`, `workspace/tests/`, plus `plan.md`, `tasks.json`, `state.json`.
4. Print (do not invent secrets):

```bash
export RUN_DIR=<absolute path to run>
export WORKER_BACKEND=zen_responses
export WORKER_MODEL=muse-spark-1.2-contributor-free
export WORKER_BASE_URL=https://opencode.ai/zen/v1
export OPENCODE_API_KEY=...   # user-provided; never commit
export MAX_PARALLEL_WORKERS=1
```

5. Stop. Next is briefing/tests, not dispatch, until briefs and tests exist.

## Do not

- Commit API keys.
- Start workers until tasks, briefs, and tests exist.
