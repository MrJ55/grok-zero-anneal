# ADR 0002: Pure workers via OpenRouter

## Status

Accepted

## Context

Workers should match the zero-shot insight: short, generation-shaped calls. Toolful workers reintroduce context bloat and races.

## Decision

Workers are **OpenRouter chat completions** with no tools. Default experimental model: `poolside/laguna-s-2.1:free`. Manager places code and runs mechanical gates.

## Consequences

- Requires `OPENROUTER_API_KEY` in the environment.
- Rate limits on free models are expected; sequencer retries + manager escalation.
- Brief quality dominates success.
