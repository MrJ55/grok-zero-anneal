# Learnings log

Append-only operational memory. Newest at bottom.

---

## 2026-08-30 — First OpenRouter / Laguna smoke (historical)

**Setup:** OpenRouter `poolside/laguna-s-2.1:free`; single unit `parse_worker_response`.

**What worked:** Worker produced correct algorithm structure on attempt 1.

**What failed:**
- Sequencer used naive fence extract → truncated on nested ` ``` ` inside docstring.
- Attempts 2–3: HTTP **429** free rate limit.

**Fix:** Manager re-integrated full module; later outer-fence extract; instruct workers to avoid backticks in docstrings.

**Who wrote the code:** ~90–95% worker logic; manager integration + harness.

**Token / context:**
- Worker: brief-sized (~1k) in / short out.
- Manager paid for tests, sequencer, diagnosis (most of session tokens).

**Artifact:** `examples/run-001/`

---

## 2026-08-30 — OpenCode Zen auth and models

**MiMo** `mimo-v2.5-free`: `POST /zen/v1/chat/completions`.
- `Authorization: Bearer` → **401** Invalid API key.
- `x-api-key` → accepted; then **429** FreeUsageLimitError.

**Muse** `muse-spark-1.2-contributor-free`: `POST /zen/v1/responses`.
- Body: `{"model","input": "..."}` (string or message list). **`messages` field invalid** on `/responses`.
- Parse: `output[]` → `type==message` → `content[]` `output_text.text`.
- Often includes a `reasoning` item first.

**Decision:** Default worker = Muse Responses; chat path retained for MiMo/Go.

---

## 2026-08-30 — Parallel Muse throughput

**Method:** concurrent `urllib` POSTs, independent prompts `ok0`…`okN`, `User-Agent: grok-zero-anneal/0.1`.

| K | Success | Wall time (approx) | Notes |
|---|---------|----------------------|-------|
| 2 | 2/2 | ~20s (high variance) | Correct texts |
| 3 | 3/3 | ~3.2s | |
| 5 | 5/5 | **~2.4s** | All texts correct |

**Throughput gain (trivial prompts):**
- Sequential 5 × ~1.5–2s ≈ 7.5–10s class vs parallel ~2.4s → roughly **3–4× wall-clock** on this probe (not a promise for codegen).
- Parallelism is **latency hiding**, not fewer total model tokens: **token cost scales ~K** if all K units run; savings vs one giant agent are in **smaller contexts per call** and cheaper/free models, not in fewer total worker tokens.

**Token savings framing:**
| Approach | Context per call | Total worker tokens | Manager tokens |
|----------|------------------|---------------------|----------------|
| Single strong agent whole feature | Large | 1× large | Low |
| K pure workers micro-briefs | Small × K | ~K × small | Medium (integrate) |
| Parallel K workers | Same as sequential K | Same as sequential K | Same integrate; **less wall time** |

**Savings show up when:** micro-briefs << full-repo agent context; free/cheap worker $/token; high pass rate so manager does not rewrite everything.

**Problems:**
- Without `User-Agent`, saw **403** on some urllib bursts.
- `max_output_tokens: 48` → status OK but **empty visible text** (reasoning consumed budget).

**Solutions:** Always set UA; do not starve `max_output_tokens` on reasoning models; cap real codegen parallel at 2–3 until measured.

---

## 2026-08-30 — Phase 0 product decisions

- Provider-agnostic `WorkerClient`; no OpenRouter runtime dependency.
- Sequencer: `MAX_PARALLEL_WORKERS`; collapse wave if targets collide.
- Docs over tribal memory: this log + handoff + custom instructions.

---

## Template for new entries

```markdown
## YYYY-MM-DD — title

**Goal:**
**K workers / model / backend:**
**Wall time / pass rate:**
**Approx tokens (if known):**
**Throughput vs sequential:**
**Problems:**
**Solutions:**
**Decisions:**
```
