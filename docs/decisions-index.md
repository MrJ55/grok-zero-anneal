# Decisions index

## ADRs

| ADR | Title |
|-----|--------|
| [0001](../adr/0001-grok-is-manager.md) | Grok is the sole manager |
| [0002](../adr/0002-pure-workers-openrouter.md) | Pure workers (historical OpenRouter note) |
| [0003](../adr/0003-separate-from-pi-zero-shot.md) | Separate from pi-zero-shot |
| [0004](../adr/0004-provider-agnostic-workers.md) | Provider-agnostic; Zen Muse default |

## Running decisions (not full ADRs)

- **Default worker:** Muse `muse-spark-1.2-contributor-free` via Zen `/responses`
- **Auth:** `x-api-key` only for Zen Responses
- **Parallel default for dogfood:** K=4 when 4 independent targets
- **Cost goal:** worker codegen on free/cheap; strong model for orchestration only
- **Tests before workers:** manager authors gates when possible
