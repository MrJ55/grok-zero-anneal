# Phase 2 results — multi-unit Muse dogfood

**Date:** 2026-08-30  
**Run dir:** `examples/run-002/`

## Setup

- Backend: `zen_responses` / `muse-spark-1.2-contributor-free`
- `MAX_PARALLEL_WORKERS=4`
- Four independent targets under `workspace/pkg/`
- Manager-authored pytest per module

## Outcome

| Task | Attempts | Result |
|------|----------|--------|
| d1-slugify | 1 | PASS |
| d2-clamp | 1 | PASS |
| d3-parsekv | 1 | PASS |
| d4-merkle | 1 | PASS |

- Wall clock: **~38.4s** for full wave + gates  
- Final `pytest tests`: **8 passed**  
- Manager code edits on implementations: **0**

## Auth incident

First attempt with dual `Authorization: Bearer` + `x-api-key` → all 401.  
After **x-api-key only**: full green.

## Exit criteria (phase 2)

- [x] ≥3 units in one run with K≥2  
- [x] No same-file parallel writers  
- [x] Workers wrote the library code  
