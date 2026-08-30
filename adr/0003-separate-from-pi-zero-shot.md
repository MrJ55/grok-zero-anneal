# ADR 0003: Separate repository from pi-zero-shot

## Status

Accepted

## Context

[pi-zero-shot](https://github.com/MrJ55/pi-zero-shot) targets a Pi extension / skill and pi-subagents. This project targets Grok-as-manager + sandbox Python sequencer + OpenRouter workers.

## Decision

Maintain **grok-zero-anneal** as its own repo. Cross-link in READMEs; do not merge codepaths.

## Consequences

- Clearer session context and less ADR conflict.
- Shared ideas (ledger, pure workers) can be copied deliberately either way.
