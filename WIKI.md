# grok-zero-anneal — Session Wiki (start here)

Live workflow for **Grok-as-manager** + pure HTTP codegen workers + Python sequencer.

## Read order (new session)

1. This file (map)
2. [docs/CUSTOM_INSTRUCTIONS.md](./docs/CUSTOM_INSTRUCTIONS.md) — paste into project instructions
3. [docs/session-handoff.md](./docs/session-handoff.md) — operational cold-start
4. [docs/learnings-log.md](./docs/learnings-log.md) — what broke, what scaled, cost notes
5. [docs/ops-playbook.md](./docs/ops-playbook.md) — day-to-day manager loop (includes stages)
6. [plan/README.md](./plan/README.md) — phase status

## Doc index

| Doc | Purpose |
|-----|--------|
| [docs/architecture.md](./docs/architecture.md) | Control plane diagram |
| [docs/cost-model.md](./docs/cost-model.md) | Token vs $ savings; parallel economics |
| [docs/problems-and-solutions.md](./docs/problems-and-solutions.md) | Failure catalog |
| [docs/decisions-index.md](./docs/decisions-index.md) | ADR pointers + running decisions |
| [docs/phase-0-results.md](./docs/phase-0-results.md) | Phase 0 evidence |
| [docs/phase-2-results.md](./docs/phase-2-results.md) | 4-worker dogfood evidence |
| [docs/phase-3-results.md](./docs/phase-3-results.md) | Anneal stages |
| [docs/manager-decomposition-cheatsheet.md](./docs/manager-decomposition-cheatsheet.md) | 2–5 worker split rules |
| [docs/skills-proposals.md](./docs/skills-proposals.md) | Optional Grok Skills |
| [adr/](./adr/) | Architecture Decision Records |
| [examples/run-001/](./examples/run-001/) | Historical Laguna parse unit |
| [examples/run-002/](./examples/run-002/) | Muse ×4 parallel dogfood |

## One-screen status (2026-08-30)

| Phase | Status |
|-------|--------|
| 0 WorkerClient + Muse | **Done** |
| 1 Ledger helpers | **Done** |
| 2 Multi-unit fan-out | **Done** (run-002) |
| 3 Anneal stages | **Done** |
| 4–5 Playbooks / package | Partial docs; next |

**Sibling:** [pi-zero-shot](https://github.com/MrJ55/pi-zero-shot) — Pi extension; separate control plane.
