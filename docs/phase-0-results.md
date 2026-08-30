# Phase 0 results (2026-08-30)

## Delivered

- `scripts/worker_client.py`, `scripts/sequencer.py`, unit tests
- Default: Zen Muse Responses (`muse-spark-1.2-contributor-free`)
- Parallel probe K=2..5 on trivial prompts — see [learnings-log.md](./learnings-log.md)

## Cost posture

| Item | Estimate |
|------|----------|
| Worker smoke / parallel probe | **$0** (Muse free tier) |
| Manager (Grok) | Design, integration, docs (strong model) |
| OpenRouter | Historical only; not required |

**Intent:** validate that **cheap/free models can be the workforce** while the strong model only orchestrates.

## Exit criteria

- [x] No OpenRouter hard dependency
- [x] Live Muse + parallel probe
- [x] Cost thesis documented in [cost-model.md](./cost-model.md)
