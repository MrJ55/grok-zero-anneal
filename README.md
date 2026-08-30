# grok-zero-anneal

**Grok-as-manager** + pure no-tool HTTP workers + restartable sequencer.

**Start here:** **[WIKI.md](./WIKI.md)** — handoff, custom instructions, learnings, skills proposals, plan.

Default worker: OpenCode Zen **Muse** (`zen_responses` / `/responses`). Parallel K=2–5 measured on trivial prompts; use K=2–3 for real codegen.

```bash
export WORKER_BACKEND=zen_responses
export OPENCODE_API_KEY=...
export WORKER_MODEL=muse-spark-1.2-contributor-free
export RUN_DIR=$PWD/runs/<id>
export MAX_PARALLEL_WORKERS=1
python scripts/sequencer.py
pytest tests -q
```

Sibling: [pi-zero-shot](https://github.com/MrJ55/pi-zero-shot) (Pi path — separate).

## License

MIT for code in this repo unless noted.
