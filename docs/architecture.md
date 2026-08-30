# Architecture

## Control flow

```text
User goal
    │
    ▼
Grok (manager) ── tools: files, shell, git, browser as needed
    │  writes plan, tasks.json, briefs/, sequencer config
    │  runs: python scripts/openrouter_sequencer.py
    ▼
Sequencer (deterministic)
    │  for each pending task:
    │    load brief → OpenRouter completion (worker) → parse ## code
    │    write workspace file → pytest / gate → update state.json
    │  on fail: augment brief with gate output, retry up to MAX_ATTEMPTS
    ▼
Grok reads out/, state.json, notes
    │  escalate: fix extractors, place code, split tasks, rewrite sequencer
    └─ loop until done or budget stop
```

## Invariants

1. **Workers have no tools** — HTTP chat only; no repo, no shell.
2. **Manager owns the tree** — only Grok (or sequencer under Grok’s scripts) writes project files.
3. **Shared state is on disk** — `tasks.json`, `state.json`, `plan.md`, `notes.md`, `transcript.jsonl`, `workspace/`.
4. **Gates are mechanical** when possible — pytest/tsc, not an LLM with tools claiming PASS.
5. **Restartable** — completed task ids in `state.json` are skipped.

## Worker contract

Workers must answer with:

```markdown
## code

```python
...
```

## notes

...
```

Avoid triple-backtick sequences inside docstrings (breaks naive fence parsers). Prefer plain quotes in docstrings.

Parser: `scripts/codegen_parse.py` and sequencer `extract_code` (outer-fence aware).

## Models

- Default worker experiment: `poolside/laguna-s-2.1:free` via OpenRouter.
- Manager is whatever hosts Grok (not billed as worker tokens).
- Asymmetric setups are encouraged (cheap bulk codegen, strong manager judgment).
