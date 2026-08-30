---
name: gza-brief
description: Write a tight pure-worker brief for grok-zero-anneal under briefs/id.md. Use when creating or fixing worker briefs, task prompts, or codegen unit contracts for the sequencer.
---

# gza-brief

## Contract

Workers are HTTP text only (no tools). Briefs must be self-contained and small.

## Required fields

Write `briefs/<id>.md` including:

1. Unit id and target path
2. Language
3. Implement (1-5 sentences)
4. Signature / shape (code fence OK)
5. Allowed imports (list)
6. Must-not list (network, undeclared deps, claiming files written)
7. Acceptance bullets or 1-3 examples
8. Context excerpts only (never whole repo)

Prefer `scripts.brief_format.format_brief` when the package is importable.

## Output format reminder (in every brief)

Workers must answer with `## code` and `## notes` only. Ban nested triple-backticks inside docstrings.

## Quality bar

- Fail the brief if it asks the worker to explore the repo or run tests.
- Prefer manager-authored failing pytest first, then brief against those tests.
