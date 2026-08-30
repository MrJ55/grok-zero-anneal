# Phase 1 — Ledger hardening — DONE

## Delivered

- `scripts/state_store.py` — atomic state.json
- `scripts/task_graph.py` — ready set, cycle check, parallel wave
- `scripts/brief_format.py` — structured briefs
- Sequencer imports the above
- Tests: `test_state_store`, `test_task_graph`, `test_brief_format`

## Exit criteria

- [x] Restartable state
- [x] Unique-target parallel waves
- [x] Standard brief formatter
