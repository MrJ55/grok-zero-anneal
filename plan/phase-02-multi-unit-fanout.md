# Phase 2 — Multi-unit fan-out (2–5 workers)

## Goals

Sequencer (or manager loop) executes a **task graph**: ready tasks = deps satisfied; dispatch up to K workers (K=2..5).

## Manager-only tasks

- [ ] **M2.1** Task schema: `id`, `target`, `deps[]`, `pytest_args`, `status`.
- [ ] **M2.2** Ready-set algorithm (deterministic): topological waves.
- [ ] **M2.3** Placement policy: one writer to a given `target` path (no parallel writers on same file).
- [ ] **M2.4** Integration gate after each wave (full pytest or subset).
- [ ] **M2.5** Design a **demo goal** with 3–5 independent pure-Python units (see playbook).

## Worker-eligible units (sequencer features — 3–5)

| ID | Target | Brief | Deps |
|----|--------|-------|------|
| **W2.1** | `scripts/task_graph.py` | `ready_tasks(tasks, completed) -> list` | none |
| **W2.2** | `scripts/task_graph.py` or tests | Cycle detection / validate deps | W2.1 |
| **W2.3** | `scripts/sequencer.py` | Wave loop: for ready in waves: run unit (sequential first) | W2.1, Phase 0 client |
| **W2.4** | `tests/test_task_graph.py` | Graph fixtures | W2.1 |
| **W2.5** | optional `scripts/parallel_dispatch.py` | Concurrent futures for **independent** targets only; K from env | W2.3 |

**Recommended first multi-worker coding session (product dogfood):**  
After sequencer can run waves, manager defines demo tasks D1–D4 (below) and fans **3–4 workers** on independent modules.

### Demo goal (dogfood) — suggested units

Implement a tiny `workspace/pkg/` library with independent modules:

| ID | Module | Contract |
|----|--------|----------|
| D1 | `slugify(text) -> str` | ASCII slug |
| D2 | `clamp(x, lo, hi)` | numeric |
| D3 | `parse_kv(line) -> dict` | `k=v` pairs |
| D4 | `merkle_hash(parts: list[str]) -> str` | sha256 hex of joined parts |

Manager writes tests first; workers implement; no cross-deps → **4-way fan-out**.

## Exit criteria

- [ ] One run completes ≥3 units with K≥2 without manager rewriting successful units.
- [ ] Same-file parallel dispatch refused or serialized.
