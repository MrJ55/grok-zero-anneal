# grok-zero-anneal

**Grok-as-manager** + pure no-tool workers + restartable sequencer with anneal stages.

**v0 complete** (phases 0–5). Start: [WIKI.md](./WIKI.md) · Playbook: [docs/manager-playbook.md](./docs/manager-playbook.md)

## Quick start

```bash
pip install -e ".[dev]"   # optional; or: pip install pytest

export OPENCODE_API_KEY=...   # OpenCode Zen; never commit
export WORKER_BACKEND=zen_responses
export WORKER_MODEL=muse-spark-1.2-contributor-free

python -m scripts.cli init-run runs/demo --goal "my goal"
# add tasks.json entries, briefs/, workspace/tests/

export RUN_DIR=$PWD/runs/demo
python -m scripts.cli run --parallel 4
pytest tests -q
python -m scripts.cli check-auth   # optional smoke
```

Workers default to **OpenCode Zen Muse** (`POST /zen/v1/responses`, **`x-api-key`**).  
Chat-completions backends (MiMo, OpenCode Go): `WORKER_BACKEND=openai_chat` + base URL/model.

## Custom instructions

Paste [docs/CUSTOM_INSTRUCTIONS.md](./docs/CUSTOM_INSTRUCTIONS.md) into the Grok project so blank sessions keep manager role.

## Layout

```text
plan/  docs/  adr/  scripts/  tests/  templates/run/  examples/
```

## License

MIT for code in this repo unless noted.
