# Cost and throughput model

## What “savings” means here

Not primarily “fewer total tokens.”  
Primary win: **move bulk codegen tokens to free/cheap workers** while the **strong model (Grok) spends tokens only on orchestration** (briefs, gates, integration).

| Path | Token locus | Typical $ |
|------|-------------|-----------|
| Frontier single-agent does all code | Strong model | High |
| Grok manager + Muse workers | Strong: briefs/judgment; Muse: code | Strong ↓; Muse ~$0 on free tier |

## Parallelism

| Effect | Parallel K workers |
|--------|---------------------|
| **Wall-clock** | Often ~1/K for independent units (network-bound) |
| **Worker token volume** | Still ~×K (each unit pays its own prompt+completion) |
| **$ on free Muse** | Still ~$0 until rate limits |
| **Manager tokens** | Slightly higher (merge/verify wave) but << K full agent sessions |

### Measured (2026-08-30)

**Trivial prompts (ok0…ok4):** K=5 wall ~2.4s (all success).

**Real codegen dogfood (run-002):** 4 independent pure-Python units, Muse, **K=4**, **first-try pass all**, wall **~38s**, manager did **not** rewrite implementations.

Approx worker output sizes (chars of raw reply): slugify ~389, clamp ~264, merkle ~287, parse_kv larger — order of hundreds of tokens per unit, not tens of thousands.

## When parallel does not save

- Dependent tasks (must sequence)
- Shared file targets
- Rate limits turning K into retries (manager time + wall up)
- Bad briefs → manager rewrites code (destroys the thesis)
