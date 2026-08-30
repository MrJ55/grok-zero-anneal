# Cost model — strong manager + cheap/free workers

## Thesis

**Cost (and effective token) savings** come primarily from:

1. **Cheap or free models doing bulk codegen** (OpenCode Zen Muse free, MiMo free when available, later Go/low-tier chat models).
2. **A stronger model (Grok) doing orchestration only** — decompose, brief, place, gate, replan — not writing every line.

Secondary benefits: **wall-clock** reduction from parallel workers (K=2–5); **context efficiency** from micro-briefs vs one long tool-using agent session.

Parallelism does **not** reduce total worker tokens (≈ K × brief work). It reduces time-to-green when units are independent.

## Roles vs spend

| Role | Model class | Pays for | Should stay small |
|------|-------------|----------|-------------------|
| Manager (Grok) | Strong / frontier | Planning, contracts, integration, failures | Avoid pasting full worker transcripts; don’t re-implement easy units |
| Worker | Free / cheap | Code text for one unit | Tight briefs; no tools; no repo crawl |
| Sequencer | None (Python) | 0 model $ | — |

## Rough estimate template (fill per run)

```text
Manager turns:     ~M  (strong model)
Worker calls:      ~W  (free/cheap)
Worker tokens:     ~Tw_in + Tw_out  (often $0 on free tier)
Manager tokens:    ~Tm_in + Tm_out  (main $ if any)
Wall time:         sequential sum vs parallel max of wave
```

**Break-even vs single strong agent:** when worker pass rate is high enough that manager tokens + free worker tokens &lt; one large strong-model coding session with tools.

## Per-phase cost intent

| Phase | Manager (strong) | Workers (free/cheap) | Expected $ pattern |
|-------|------------------|----------------------|---------------------|
| **0** Client + Muse path | Design/integration | Smoke + parallel probe | Near-$0 workers; manager docs/code |
| **1** Ledger helpers | Mostly manager-authored infra | Optional | Near-$0 |
| **2** Multi-unit dogfood | Tests, briefs, gates, fixes | **3–4 codegen units** on Muse | Workers $0; manager = orchestration only if units pass |
| **3** Stages | Policy code | Small pure functions | Low |
| **4–5** Playbooks / package | Docs + thin CLI | Optional | Low |

## Recording rule

After each meaningful run, append `docs/learnings-log.md` with:

- K, model, backend
- Worker calls / pass rate
- Whether manager rewrote code (bad — cost leaks to strong model)
- Wall time vs sequential estimate
- Explicit note: **worker $ ≈ 0 (free tier)** or measured spend
