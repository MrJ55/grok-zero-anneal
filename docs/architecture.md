# Architecture

## Cost split

**Strong model (Grok)** = manager. **Free/cheap models** = workers. Sequencer = $0.  
Details: [cost-model.md](./cost-model.md).

## Control flow

```text
User goal
    │
    ▼
Grok (manager) — plan, brief, test, gate, replan
    │
    ▼
Sequencer → WorkerClient (Muse free / cheap chat) × K parallel if disjoint targets
    │
    ▼
Mechanical pytest → state.json
```

## Worker backends

| Backend | Env | Endpoint | Default model |
|---------|-----|----------|---------------|
| Zen Responses | `zen_responses` | `/responses` | `muse-spark-1.2-contributor-free` |
| OpenAI chat | `openai_chat` | `/chat/completions` | `mimo-v2.5-free` |

Auth: `x-api-key`. Base: `https://opencode.ai/zen/v1`.

## Modules

`worker_client`, `codegen_parse`, `state_store`, `task_graph`, `brief_format`, `sequencer`.
