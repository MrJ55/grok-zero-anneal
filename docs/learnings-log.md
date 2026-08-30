# Learnings log

Append-only operational memory. Newest at bottom.

**Cost thesis:** savings = **free/cheap workers for code** + **strong model for orchestration only**. See [cost-model.md](./cost-model.md).

---

## 2026-08-30 — First OpenRouter / Laguna smoke (historical)

**Setup:** OpenRouter Laguna free; unit `parse_worker_response`.

**Cost:** Worker free tier; manager (Grok) paid for harness + integration after extract bug.

**Lesson:** Worker can own implementation $; extract/harness bugs shift work back to strong model — fix plumbing so manager stays orchestrator.

**Artifact:** `examples/run-001/`

---

## 2026-08-30 — OpenCode Zen auth and models

- MiMo chat: `x-api-key` works; Bearer 401; free **429** common.
- Muse Responses: works; parse `output_text`; no `messages` field on `/responses`.

**Cost decision:** Prefer Muse free for workers; keep strong model off the codegen path.

---

## 2026-08-30 — Parallel Muse throughput

| K | Success | Wall (approx) |
|---|---------|----------------|
| 2–5 | OK | K=5 ~2.4s trivial prompts |

**Wall-clock:** parallel helps.  
**Token cost:** total worker tokens still ~×K.  
**$ cost:** still ~$0 on free Muse if within limits.

**Real savings vs frontier single-agent:** not “fewer tokens,” but **$0 (or cents) per unit** of codegen + fewer frontier tokens on bulk code.

---

## 2026-08-30 — Phase 0–1 cost posture

| Phase | Worker $ | Manager role |
|-------|----------|--------------|
| 0 | ~$0 Muse smokes | Client + docs |
| 1 | ~$0 | Ledger modules mostly manager-written (infra; acceptable) |

Phase 2 target: **workers write the demo library; manager only tests/briefs/gates.**

---

## Template

```markdown
## YYYY-MM-DD — title
**Goal / phase:**
**Worker model ($):** free Muse / …
**Manager work:** orchestrate only? or rewrote code?
**K / wall / pass rate:**
**Cost note:** worker $≈0; strong model used for …
**Problems / solutions:**
```
