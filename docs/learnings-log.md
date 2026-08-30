# Learnings log

Append-only operational memory. Newest at bottom.

See also [cost-model.md](./cost-model.md), [problems-and-solutions.md](./problems-and-solutions.md).

---

## 2026-08-30 — First OpenRouter / Laguna smoke (historical)

**Goal / phase:** Smoke parse helper  
**Worker ($):** Laguna free via OpenRouter  
**Manager work:** Harness + integration after extract bug  
**Problems / solutions:** Nested ``` in docstring truncated extract → outer-fence + prompt hygiene  
**Artifact:** `examples/run-001/`

---

## 2026-08-30 — Zen auth and models

- Bearer → 401; **`x-api-key` → OK**
- Sending **both** Bearer + x-api-key caused sequencer 401s in parallel dogfood
- **Fix:** x-api-key only for `zen_responses`
- MiMo free: 429 common; Muse Responses preferred

---

## 2026-08-30 — Parallel Muse throughput (trivial)

| K | Success | Wall |
|---|---------|------|
| 5 | 5/5 | ~2.4s |

Wall-clock scales; token volume still ×K; $ ~0 on free.

---

## 2026-08-30 — Phase 2 dogfood (real codegen, K=4)

**Goal / phase:** Phase 2 multi-unit  
**Worker model ($):** Muse free  
**Manager work:** tests + briefs + sequencer only; **no implementation rewrites**  
**K / wall / pass rate:** K=4, **~38.4s**, **4/4 first attempt**  
**Cost note:** worker $≈0; strong model not used for bulk code  
**Artifact:** `examples/run-002/`

---

## 2026-08-30 — Phase 3 anneal stages

**Goal / phase:** Explicit implement → verify → manager_fix  
**Worker model ($):** N/A for pure unit tests; runtime uses Muse as before  
**Manager work:** Implemented `stages.py`, `rebrief.py`, sequencer integration  
**Behavior:** Transcript + `state.stages` record transitions; after MAX_ATTEMPTS verify fails → `manager_fix` (no silent give-up)  
**Optional:** `task.ideation: true` notes-only worker  
**Artifact:** `docs/phase-3-results.md`

---

## Template

```markdown
## YYYY-MM-DD — title
**Goal / phase:**
**Worker model ($):**
**Manager work:** orchestrate only? or rewrote code?
**K / wall / pass rate:**
**Cost note:**
**Problems / solutions:**
```
