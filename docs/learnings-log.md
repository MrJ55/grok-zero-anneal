# Learnings log

Append-only. Newest at bottom.

---

## 2026-08-30 — Laguna smoke / Zen auth / parallel / Phase 2–3

See prior entries in git history for full detail. Highlights:

- x-api-key only for Muse; Bearer → 401
- K=4 dogfood ~38s, 4/4 first-try pass (`examples/run-002/`)
- Stages: implement → verify → manager_fix

---

## 2026-08-30 — Phase 4–5 v0 close

**Goal / phase:** Playbooks + packaging  
**Manager work:** `manager-playbook.md`, `run_init`, `cli`, `pyproject.toml`, handoff refresh  
**Cost note:** no worker spend  
**Outcome:** v0 definition of done met; CLI `python -m scripts.cli init-run|run|check-auth`  
**Artifact:** `docs/phase-4-5-results.md`

---

## Template

```markdown
## YYYY-MM-DD — title
**Goal / phase:**
**Worker model ($):**
**Manager work:**
**K / wall / pass rate:**
**Cost note:**
**Problems / solutions:**
```
