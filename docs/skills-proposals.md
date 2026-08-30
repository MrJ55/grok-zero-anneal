# Proposed Grok Skills (user-created)

Grok’s skill system can package repeatable manager behaviors. These are **proposals** — implement as project skills when the platform allows.

## 1. `gza-run-init`

**Trigger:** “new run”, “init run dir”, “start ledger run”

**Does:**
- Copy `templates/run/` → `runs/<slug>/`
- Skeleton `plan.md`, `tasks.json`, empty `briefs/`
- Print env exports for Muse Zen

## 2. `gza-brief`

**Trigger:** “write worker brief”, “brief for task”

**Does:**
- From task id + signature + tests path, emit `briefs/<id>.md` using the standard template (path, signature, allowed imports, must-not, acceptance, excerpts only)
- Enforce no whole-repo dumps; no nested triple-backticks in docstring examples

## 3. `gza-dispatch`

**Trigger:** “run sequencer”, “dispatch workers”

**Does:**
- Verify `RUN_DIR`, `OPENCODE_API_KEY` / `WORKER_API_KEY`
- Set `MAX_PARALLEL_WORKERS` from ready-set size (cap 3 default)
- Run `python scripts/sequencer.py`
- Summarize `state.json` + failed `out/*-pytest.txt`

## 4. `gza-learn`

**Trigger:** “log learning”, “record throughput”

**Does:**
- Append a dated entry to `docs/learnings-log.md` with: goal, K workers, wall time, approx tokens if known, failure mode, fix

## 5. `gza-phase`

**Trigger:** “continue phase”, “phase status”

**Does:**
- Read `plan/README.md` + current phase file
- List open manager vs worker-eligible tasks
- Propose next wave of 2–5 briefs

## Skill vs custom instructions

| Mechanism | Use for |
|-----------|--------|
| **Custom instructions** | Always-on identity (manager, no tools for workers, repo URLs) |
| **Skills** | Optional procedural bundles (init run, brief, dispatch, log) |

Until skills exist, follow playbooks in `docs/` and `plan/` manually as manager.
