# ADR 0004: Provider-agnostic workers (Zen Muse default)

## Status

Accepted (updated 2026-08-30)

## Context

First smoke used OpenRouter + Laguna. Product must not depend on OpenRouter. OpenCode Zen free **Muse Spark contributor** works via **Responses API**; MiMo free uses chat completions but hit rate limits.

## Decision

1. Workers are pure text over HTTP (no tools).
2. Config: `WORKER_BACKEND`, `WORKER_API_KEY` / `OPENCODE_API_KEY`, `WORKER_MODEL`, `WORKER_BASE_URL`.
3. **Default:** `zen_responses` + `muse-spark-1.2-contributor-free` + `https://opencode.ai/zen/v1`.
4. **Alt:** `openai_chat` for MiMo / OpenCode Go-style `/chat/completions`.
5. Auth: send **`x-api-key`** (Zen); also send Bearer for compatible gateways.
6. OpenRouter examples are historical only.

## Consequences

- Sequencer uses `scripts/worker_client.py`.
- Parallel waves allowed when task targets are disjoint (`MAX_PARALLEL_WORKERS`).
