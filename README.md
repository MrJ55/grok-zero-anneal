# grok-zero-anneal

**Grok-as-manager** + pure no-tool workers + restartable sequencer.

**Start here:** [WIKI.md](./WIKI.md)

| Phase | Status |
|-------|--------|
| 0 Muse WorkerClient | Done |
| 1 Ledger helpers | Done |
| 2 4-worker dogfood | **Done** (~38s, 4/4 pass) |
| 3 Anneal stages | Next |

```bash
export WORKER_BACKEND=zen_responses
export OPENCODE_API_KEY=...   # x-api-key auth; never commit
export RUN_DIR=$PWD/runs/<id>
export MAX_PARALLEL_WORKERS=4
PYTHONPATH=. python scripts/sequencer.py
pytest tests -q
```

Paste [docs/CUSTOM_INSTRUCTIONS.md](./docs/CUSTOM_INSTRUCTIONS.md) into project instructions for blank sessions.
