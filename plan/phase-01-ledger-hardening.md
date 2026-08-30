# Phase 1 — Run ledger hardening

## Goals

Production-grade run directory behavior so multi-unit work does not corrupt state.

## Manager-only tasks

- [ ] **M1.1** Standardize run layout in `templates/run/` (tasks, briefs, out, workspace, state, transcript).
- [ ] **M1.2** Gate runner abstraction: pytest argv from `tasks.json`; capture exit code + tail.
- [ ] **M1.3** Brief template generator (manager skill): path, signature, allowed imports, acceptance, excerpts only.
- [ ] **M1.4** Policy: workers must not use triple-backticks inside docstrings; encoder in system prompt.

## Worker-eligible units (2–4)

| ID | Target | Brief | Deps |
|----|--------|-------|------|
| **W1.1** | `scripts/codegen_parse.py` | Harden outer-fence + section parse; edge cases from `examples/run-001` | none |
| **W1.2** | `tests/test_codegen_parse.py` | Expand cases: nested noise, missing sections, CRLF | W1.1 or parallel if manager writes failing tests first |
| **W1.3** | `scripts/state_store.py` | load/save `state.json`; mark complete; attempt counters; atomic write | none |
| **W1.4** | `scripts/brief_format.py` | `format_brief(task_dict) -> str` from structured fields | none |

**Fan-out tip:** W1.1+W1.3+W1.4 can run as **3 parallel** workers if interfaces are fixed by manager first; W1.2 after W1.1 or manager-authored tests first (red) then W1.1 (green).

## Exit criteria

- [ ] Parse never truncates the run-001 worker sample when outer-fence rules apply.
- [ ] State survives kill mid-run (restart skips completed).
- [ ] Brief formatter used by manager when creating new runs.
