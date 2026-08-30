# Implementation plan (manager-owned)

**Manager = Grok.** User supplies goals only. This plan is the breakdown Grok uses to fan work to **2–5 pure codegen workers** and drive **grok-zero-anneal** to a usable product.

## Provider stance

- **Not** tied to OpenRouter.
- Workers are **OpenAI-compatible chat completions** (prompt in → text out, **no tools**).
- **Next run default backend:** [OpenCode Go](https://opencode.ai/go) (`https://opencode.ai/zen/go/v1/...` + Go API key / OpenCode auth).
- Adapters are swappable: OpenCode Go, any Zen/compatible endpoint, local OpenAI-compatible server.

OpenRouter remains only as a historical example in `examples/run-001/`.

## North star

A new Grok session can:

1. Accept a user goal (“implement X in repo Y”).
2. Create a run dir (ledger + briefs + gates).
3. Dispatch **2–5 independent** pure-worker units (OpenCode Go models).
4. Place code, run mechanical gates, rebrief failures, optionally rewrite the sequencer.
5. Stop on green gates or budget exhaust — with inspectable `state.json` / transcript.

## Phase overview

| Phase | Name | Outcome |
|-------|------|--------|
| 0 | Provider-agnostic worker + OpenCode Go | `WorkerClient` API; Go adapter; no OpenRouter hard dep |
| 1 | Run ledger hardening | Robust parse, state, gates, brief templates |
| 2 | Multi-unit fan-out (2–5) | Dependency-aware ready set; sequential MVP; optional parallel |
| 3 | Anneal stages in sequencer | plan → implement → verify → fix metadata |
| 4 | Manager playbooks | Checklists + example multi-unit goal |
| 5 | Packaging & handoff | Docs, CLI entry, “new session” green path |

Detailed lists: `phase-0` … `phase-5` below.

## How Grok uses this

For each phase:

1. Mark phase active in `notes.md` of the current run (or project board).
2. Split **worker-eligible** tasks (pure codegen, tight contract) into 2–5 briefs.
3. Keep **manager-only** tasks (git, API design, adapter wiring, test authorship when needed, integration).
4. Run sequencer / place / gate; escalate only when workers fail twice or contracts were wrong.
