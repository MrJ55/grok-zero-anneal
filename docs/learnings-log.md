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
**Units:** slugify, clamp, parse_kv, merkle_join  
**Problems / solutions:** Initial 401 from dual auth headers → x-api-key only  
**Artifact:** `examples/run-002/`

**Throughput takeaway:** Independent micro-units + tight tests → parallel workers deliver full feature slice in <1 minute wall without manager coding.

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
