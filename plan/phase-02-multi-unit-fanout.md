# Phase 2 — Multi-unit fan-out dogfood

## Goals

Prove **cost model in practice:** free Muse workers implement 3–4 independent units; Grok only briefs, tests, gates, fixes contracts.

## Demo library (`workspace/pkg/`)

| ID | Target | Contract |
|----|--------|----------|
| D1 | `pkg/textutil.py` | `slugify(text: str) -> str` |
| D2 | `pkg/numutil.py` | `clamp(x: float, lo: float, hi: float) -> float` |
| D3 | `pkg/parseutil.py` | `parse_kv(line: str) -> dict[str, str]` |
| D4 | `pkg/hashutil.py` | `merkle_join(parts: list[str]) -> str` sha256 hex of `"\\x00".join(parts)` |

All deps empty → one parallel wave with `MAX_PARALLEL_WORKERS=3` or `4`.

## Manager-only

- [x] Task graph + tests authored by manager
- [ ] Dispatch Muse workers (not manager-written implementations)
- [ ] Log cost note: worker $≈0; manager rewrites count as cost leak

## Exit criteria

- [ ] ≥3 units green without manager rewriting successful units
- [ ] Entry in learnings-log with K and cost note
