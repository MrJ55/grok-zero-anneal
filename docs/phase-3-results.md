# Phase 3 results — Anneal stages

**Date:** 2026-08-30

## Delivered

| Module | Role |
|--------|------|
| `scripts/stages.py` | `Stage` enum + `next_stage` + state history helpers |
| `scripts/rebrief.py` | `append_pytest_failure` / `append_extract_failure` |
| `scripts/sequencer.py` | Explicit implement → verify → done / manager_fix; transcript stage events |
| Tests | `tests/test_stages.py`, `tests/test_rebrief.py` |

## Stage policy

```text
implement (worker, no tools)
    → place code
    → verify (pytest only)
         → pass → done
         → fail → rebrief → implement (until MAX_ATTEMPTS)
              → still fail → manager_fix (sequencer stops; Grok intervenes)
```

Optional: `"ideation": true` on a task runs a notes-only worker into `notes.md` before implement.

## Transcript

Events include `stage` field: `implement` | `verify` | `done` | `manager_fix` | `ideation`.

Per-task history also under `state.json` → `stages.<task_id>.history`.

## Exit criteria

- [x] Transcript records stage transitions
- [x] Manager fix path only after N worker/verify failures
- [x] Unit tests for pure stage/rebrief helpers
