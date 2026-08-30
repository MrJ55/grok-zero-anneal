# Session handoff (cold-start Grok)

## Identity

You are the **sole manager** for https://github.com/MrJ55/grok-zero-anneal.
User gives goals only. See [CUSTOM_INSTRUCTIONS.md](./CUSTOM_INSTRUCTIONS.md).

## Bootstrap

1. Read [WIKI.md](../WIKI.md) and [learnings-log.md](./learnings-log.md) (last entries).
2. Check [plan/README.md](../plan/README.md) for active phase.
3. Confirm worker env (Zen Muse defaults). **Never commit keys.**
4. Continue phase tasks; log new learnings.

## Proven stack

- `scripts/worker_client.py` — Muse `/responses`, **x-api-key only**
- `scripts/sequencer.py` — waves via `task_graph.wave_for_parallel`
- `scripts/state_store.py`, `brief_format.py`, `codegen_parse.py`
- Dogfood: [examples/run-002/](../examples/run-002/) — 4 parallel Muse workers, all pass

## Do not

- Mix with [pi-zero-shot](https://github.com/MrJ55/pi-zero-shot) control plane
- Give workers tools
- Parallelize same target path
