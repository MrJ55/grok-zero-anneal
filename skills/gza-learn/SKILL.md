---
name: gza-learn
description: Append a dated operational learning to grok-zero-anneal docs/learnings-log.md covering throughput, cost, and failures. Use after a run, when logging learnings, or recording scale or auth incidents.
---

# gza-learn

## Steps

1. Read the end of `docs/learnings-log.md` to avoid duplicates.
2. Append a new section (newest at bottom) using:

```markdown
## YYYY-MM-DD — <short title>
**Goal / phase:**
**Worker model ($):** e.g. Muse free / paid
**Manager work:** orchestrate only? or rewrote code?
**K / wall / pass rate:**
**Cost note:** worker $; strong-model tokens used for what
**Problems / solutions:**
```

3. Commit/push when the session can update the GitHub repo.
4. Keep entries factual and short. No API keys.

## When to log

- New failure mode (auth, extract, rate limit)
- Parallelism measurement (K, wall time, pass rate)
- Manager had to rewrite worker code (cost thesis break)
