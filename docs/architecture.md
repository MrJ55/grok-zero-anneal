# Architecture

## Control flow

```text
User goal
    │
    ▼
Grok (manager) — tools: files, shell, git
    │  plan, tasks, briefs, tests
    │  python scripts/sequencer.py
    ▼
Sequencer (deterministic)
    │  ready-set from deps → wave (1..MAX_PARALLEL_WORKERS)
    │  WorkerClient.generate (no tools) → parse ## code → place → pytest
    ▼
Grok reads out/, state.json → rebrief / fix / replan
```

## Worker backends

| Backend | Env `WORKER_BACKEND` | Endpoint | Default model |
|---------|----------------------|----------|---------------|
| Zen Responses | `zen_responses` | `{base}/responses` | `muse-spark-1.2-contributor-free` |
| OpenAI chat | `openai_chat` | `{base}/chat/completions` | `mimo-v2.5-free` |

Base default: `https://opencode.ai/zen/v1`. Auth: `x-api-key`.

## Invariants

1. Workers: no tools, no repo access.
2. Manager owns tree and gates.
3. State on disk: `tasks.json`, `state.json`, `transcript.jsonl`, `workspace/`.
4. Parallel only for disjoint targets.
5. No secrets in git.

## Key modules

| Module | Role |
|--------|------|
| `scripts/worker_client.py` | HTTP workers |
| `scripts/codegen_parse.py` | Parse worker markdown |
| `scripts/state_store.py` | Atomic state helpers |
| `scripts/task_graph.py` | Ready-set / deps |
| `scripts/brief_format.py` | Brief text from structured fields |
| `scripts/sequencer.py` | Orchestration loop |
