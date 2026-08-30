# Phase 4 — Manager playbooks

## Goals

Grok can operate without rediscovering process each session.

## Manager-only tasks (no pure workers required)

- [ ] **M4.1** Write `docs/manager-playbook.md`: intake goal → decompose → brief → dispatch → gate → escalate.
- [ ] **M4.2** Checklist: “when to parallelize” (independent targets only).
- [ ] **M4.3** Checklist: brief quality bar (signature, allowed imports, 1–3 examples, no whole-repo dump).
- [ ] **M4.4** Update `docs/session-handoff.md` for OpenCode Go env vars.
- [ ] **M4.5** Record one successful multi-unit run under `examples/run-002/` (artifacts, no secrets).

## Worker-eligible (optional 2)

| ID | Target | Brief |
|----|--------|-------|
| **W4.1** | `scripts/run_init.py` | CLI: create run dir from template |
| **W4.2** | tests for run_init | temp dir assertions |

## Exit criteria

- [ ] New Grok session can follow playbook + handoff only.
