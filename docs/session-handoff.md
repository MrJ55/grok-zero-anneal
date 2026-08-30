# Session handoff (for a new Grok session)

## What this project is

**grok-zero-anneal**: You (Grok) are the **manager**. The user only gives goals. You create briefs, run `scripts/openrouter_sequencer.py`, place/fix code, and iterate. Workers are OpenRouter completions with **no tools**.

Sibling project **pi-zero-shot** is a different direction (Pi extension). Do not conflate them.

## Repo

https://github.com/MrJ55/grok-zero-anneal

## Already proven

- Sandbox can reach OpenRouter; chat needs `OPENROUTER_API_KEY`.
- Laguna free model can implement a small pure-Python unit from a tight brief.
- Failure mode seen: nested ``` in worker docstring + naive extract → truncated file; **fixed** outer-fence extract in sequencer.
- Free tier **429** rate limits — backoff / manager escalate.
- Example artifacts: `examples/run-001/`.

## Env

```bash
export OPENROUTER_API_KEY=...   # user provides; never commit
export WORKER_MODEL=poolside/laguna-s-2.1:free
export RUN_DIR=/path/to/runs/my-run
export MAX_ATTEMPTS=3
```

## Next experiments worth doing

1. Multi-unit run (3–5 **independent** tasks) with parallel or sequential workers.
2. Manager never hand-edits code unless gate fails twice.
3. Optional: anneal-style explicit stages in sequencer (implement vs verify metadata).

## Do not

- Commit API keys.
- Give workers tools “just this once.”
- Paste full monorepos into worker prompts — excerpts only.
