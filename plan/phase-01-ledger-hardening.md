# Phase 1 — Run ledger hardening (STATUS: modules landed)

## Goals

Production-grade run directory helpers so multi-unit work does not corrupt state.

## Done

- [x] `scripts/state_store.py` — atomic state save
- [x] `scripts/task_graph.py` — validate, ready-set, parallel wave
- [x] `scripts/brief_format.py` — structured → brief markdown
- [x] Unit tests for the above
- [x] Wiki / handoff / custom instructions / learnings log

## Remaining

- [ ] Wire sequencer.py to import state_store + task_graph (thin refactor)
- [ ] Expand codegen_parse edge-case tests from run-001 sample
- [ ] templates/run refresh pointing at new helpers

## Exit criteria

- [x] State helpers + graph + brief formatter tested
- [ ] Sequencer uses shared modules (next small commit if not done same day)
