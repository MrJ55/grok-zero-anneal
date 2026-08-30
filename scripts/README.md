# scripts/

| File | Role |
|------|------|
| `worker_client.py` | Provider-agnostic pure-text workers |
| `codegen_parse.py` | Parse `## code` / `## notes` |
| `sequencer.py` | Restartable run loop (+ optional parallel wave) |
| `openrouter_sequencer.py` | Historical prototype (OpenRouter) |

## Worker env

```bash
export WORKER_BACKEND=zen_responses          # default: Muse via /responses
export WORKER_API_KEY=...                    # or OPENCODE_API_KEY
export WORKER_MODEL=muse-spark-1.2-contributor-free
export WORKER_BASE_URL=https://opencode.ai/zen/v1

# chat-completions path (MiMo, Go, etc.)
# export WORKER_BACKEND=openai_chat
# export WORKER_MODEL=mimo-v2.5-free

export RUN_DIR=/path/to/run
export MAX_PARALLEL_WORKERS=1                # set 2-5 when targets disjoint
python scripts/sequencer.py
```

Auth header used: `x-api-key` (Zen). Include `User-Agent`.
