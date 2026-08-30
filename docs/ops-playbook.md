# Ops playbook (manager)

## Intake

1. User states goal (+ optional constraints, repo, done criteria).
2. You explore only as needed (tools OK for manager).
3. Write `plan.md` + `tasks.json` with **small** units and deps.
4. Write **failing tests** under `workspace/tests/` (or verify existing).
5. Write one brief per task under `briefs/<id>.md` via `brief_format.format_brief` or template.

## Stages (Phase 3)

Per task the sequencer runs:

1. **implement** — pure worker
2. **verify** — pytest only
3. On fail — **rebrief** and implement again until `MAX_ATTEMPTS`
4. Then **manager_fix** — sequencer returns non-zero; **you** edit code/contracts

Optional: `"ideation": true` on a task for notes-only worker output in `notes.md`.

Watch `transcript.jsonl` for `"stage"` and `state.json` → `stages`.

## Dispatch

```bash
export WORKER_BACKEND=zen_responses
export OPENCODE_API_KEY=...          # never commit; x-api-key auth
export WORKER_MODEL=muse-spark-1.2-contributor-free
export RUN_DIR=/absolute/path/to/run
export MAX_PARALLEL_WORKERS=4        # only if targets disjoint
export MAX_ATTEMPTS=3
export PYTHONPATH=/path/to/grok-zero-anneal
python scripts/sequencer.py
```

## After run

1. Read `state.json` — all task ids in `completed`?
2. On `manager_fix`: read `out/<id>-aN.md` + pytest tail; fix as manager
3. Append learning to `docs/learnings-log.md` if new failure mode or scale data

## Parallel rules

- Same `target` path → never parallel
- Prefer K=2–3 for heavy codegen; K=4–5 OK for tiny independent units (proven)
- Free-tier 429/403: backoff; do not burn manager tokens rewriting all units

## Auth reminder (Zen)

- Header: **`x-api-key` only** (not Bearer) for Muse `/responses`
- Always send `User-Agent`
