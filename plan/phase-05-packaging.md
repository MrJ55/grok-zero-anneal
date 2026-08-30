# Phase 5 — Packaging & completion bar

## Goals

Repo is “complete” for v0: installable helpers, clear CLI, CI-able tests, no provider lock-in.

## Manager-only tasks

- [ ] **M5.1** `pyproject.toml` or minimal package layout; `pytest` in CI if available.
- [ ] **M5.2** README quick start: OpenCode Go only (OpenRouter demoted to appendix).
- [ ] **M5.3** ADR: provider-agnostic workers; OpenCode Go default.
- [ ] **M5.4** Final acceptance: demo D1–D4 green in one managed run with ≥2 concurrent-capable units.

## Worker-eligible (2–3)

| ID | Target | Brief |
|----|--------|-------|
| **W5.1** | `README` sections via manager preferred | — often manager-written |
| **W5.2** | `scripts/cli.py` | `python -m scripts.cli init-run|run` thin wrapper |
| **W5.3** | tests for cli | subprocess |

## Definition of done (project v0)

- [ ] Provider-agnostic worker client + OpenCode Go path documented and smoked.
- [ ] Multi-unit task graph with 2–5 pure workers proven on demo library.
- [ ] Restartable state + mechanical gates.
- [ ] Session handoff sufficient for cold-start Grok manager.
