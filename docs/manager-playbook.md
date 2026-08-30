# Manager playbook

End-to-end process for Grok as sole manager.

## 1. Intake

- Capture goal, constraints, definition of done.
- Confirm worker credentials exist in env (never in git).

## 2. Decompose

- Split into **2–5** pure-codegen units when independent.
- Draw deps in `tasks.json` (`deps` arrays).
- Prefer one target path per task.

### When to parallelize

| Parallelize | Do not |
|-------------|--------|
| Disjoint `target` paths | Same file / package init races |
| No unmet deps | Dependent units |
| Briefs ≤ ~2k tokens | Huge context dumps |
| K=2–4 typical | K>5 until rate limits known |

## 3. Brief quality bar

Each `briefs/<id>.md` must include:

1. Target path  
2. Full signature / types  
3. Allowed imports  
4. Must-not list  
5. Acceptance bullets or 1–3 examples  
6. Only necessary excerpts (no whole repo)  
7. No nested triple-backticks in docstring examples  

Use `scripts.brief_format.format_brief`.

## 4. Gates first

- Write **failing** pytest modules under `workspace/tests/` before dispatch when possible.

## 5. Dispatch

```bash
python -m scripts.cli init-run runs/my-run --goal "..."
# add tasks, briefs, tests
export RUN_DIR=$PWD/runs/my-run
export OPENCODE_API_KEY=...
export WORKER_BACKEND=zen_responses
export MAX_PARALLEL_WORKERS=4
python -m scripts.cli run --parallel 4
```

## 6. Stages

Sequencer: **implement** → **verify** (pytest) → rebrief loop → **manager_fix** if exhausted.

## 7. Escalate

On `manager_fix` or stuck pending:

1. Read `out/<id>-aN.md` and pytest tail  
2. Fix contract/tests or place corrected code  
3. Reset task attempts in `state.json` if re-dispatching  
4. Log learning if new failure mode  

## 8. Close

- All ids in `state.completed`  
- Full pytest green  
- Optional: copy run into `examples/` without secrets  
