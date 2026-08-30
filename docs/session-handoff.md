# Session handoff (cold-start Grok)

## Identity

You are the **sole manager** for https://github.com/MrJ55/grok-zero-anneal.
User gives goals only. Paste [CUSTOM_INSTRUCTIONS.md](./CUSTOM_INSTRUCTIONS.md) into project instructions.

## Bootstrap

1. Read [WIKI.md](../WIKI.md) and latest [learnings-log.md](./learnings-log.md).
2. Check [plan/README.md](../plan/README.md) — v0 phases 0–5 complete; extend as needed.
3. Follow [manager-playbook.md](./manager-playbook.md).

## Env (workers)

```bash
export WORKER_BACKEND=zen_responses          # default Muse
export OPENCODE_API_KEY=...                  # Zen key; x-api-key auth
export WORKER_MODEL=muse-spark-1.2-contributor-free
export WORKER_BASE_URL=https://opencode.ai/zen/v1

# Optional chat-completions (MiMo / OpenCode Go):
# export WORKER_BACKEND=openai_chat
# export WORKER_BASE_URL=https://opencode.ai/zen/go/v1   # if using Go endpoint
# export WORKER_MODEL=<model-id>
```

Never commit keys. Auth for Zen Responses: **x-api-key only** (not Bearer).

## CLI

```bash
python -m scripts.cli init-run runs/foo --goal "..."
python -m scripts.cli check-auth
python -m scripts.cli run --run-dir runs/foo --parallel 4
pytest tests -q
```

## Proven

- Muse parallel K=4 dogfood: [examples/run-002/](../examples/run-002/)
- Stages: implement / verify / manager_fix

## Do not

- Mix with [pi-zero-shot](https://github.com/MrJ55/pi-zero-shot)
- Give workers tools
- Parallelize same target path
