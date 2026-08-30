# ADR 0004: Provider-agnostic workers (OpenCode Go default)

## Status

Accepted

## Context

The first smoke used OpenRouter + Laguna free. The product must not depend on OpenRouter. Next runs use **OpenCode Go** (low-cost open models via OpenCode’s Go endpoint).

## Decision

1. Workers are **any OpenAI-compatible chat completion** API (no tools).
2. Runtime configuration: base URL, API key env, model id.
3. **Default backend for upcoming work:** OpenCode Go.
4. OpenRouter examples are historical only.

## Consequences

- Sequencer refactored behind `WorkerClient`.
- Docs and plans reference Go, not OpenRouter, as primary.
- Local or alternate compatible endpoints remain valid.
