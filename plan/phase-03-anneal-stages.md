# Phase 3 — Anneal-style stages in the sequencer

## Goals

Encode explicit stages without toolful workers: implement vs mechanical verify vs manager fix policy.

## Manager-only tasks

- [ ] **M3.1** Stage enum: `implement` | `verify` | `manager_fix` (verify = pytest only).
- [ ] **M3.2** Retry policy: on verify fail → rebrief same worker (implement) up to N; then `manager_fix`.
- [ ] **M3.3** Optional “ideation” worker: notes-only, no code (ledger `notes.md`).

## Worker-eligible units (2–3)

| ID | Target | Brief |
|----|--------|-------|
| **W3.1** | `scripts/stages.py` | Pure functions: next_stage(state) → stage |
| **W3.2** | `scripts/rebrief.py` | `append_pytest_failure(brief, output) -> str` |
| **W3.3** | tests for stages/rebrief | fixtures |

## Exit criteria

- [ ] Transcript records stage transitions.
- [ ] Manager fix path documented and used only after N worker fails.
