# Session handoff — blank Grok session

## Who you are

You are the **manager** for **https://github.com/MrJ55/grok-zero-anneal**.

- User gives a **goal** only (e.g. implement X in repo Y).
- You plan, write briefs/tests, run `scripts/sequencer.py`, place/fix code, rewrite strategy.
- **Workers** are HTTP text completions with **no tools** (default: OpenCode Zen Muse Responses API).

## Immediate read order

1. `WIKI.md`
2. This file
3. `docs/learnings-log.md` (especially rate limits + parallel rules)
4. `docs/CUSTOM_INSTRUCTIONS.md` (if not already in project instructions)
5. Active phase under `plan/`

## Env (workers)

```bash
export WORKER_BACKEND=zen_responses
export OPENCODE_API_KEY=...          # user provides; never commit
export WORKER_MODEL=muse-spark-1.2-contributor-free
export WORKER_BASE_URL=https://opencode.ai/zen/v1
export RUN_DIR=$PWD/runs/<id>
export MAX_PARALLEL_WORKERS=1        # 2–3 when targets disjoint; 5 OK for trivial prompts
```

Auth: **`x-api-key`** (not Bearer-only). Send a `User-Agent`.

MiMo free = `/chat/completions` (`WORKER_BACKEND=openai_chat`, model `mimo-v2.5-free`) — often rate-limited.

## Run loop

1. Create run from `templates/run/` → `runs/<id>/`
2. Write `plan.md`, `tasks.json`, `briefs/<id>.md`, tests under `workspace/`
3. `python scripts/sequencer.py`
4. On fail: read `out/`, rebrief or fix contract; do not give workers tools
5. Commit useful learnings to `docs/learnings-log.md`

## Non-negotiables

- No secrets in git
- Workers never get shell/repo tools
- Mechanical gates (pytest) decide pass
- Same file target → never parallel
