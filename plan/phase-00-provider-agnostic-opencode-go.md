# Phase 0 — Provider-agnostic worker + OpenCode Go

## Goals

- Remove hard dependency on OpenRouter.
- One `WorkerClient` interface; OpenCode Go as default adapter for the next real run.
- Sequencer calls the interface only.

## Manager-only tasks

- [ ] **M0.1** Define `WorkerClient.generate(system: str, user: str, *, model: str) -> str` in `scripts/worker_client.py`.
- [ ] **M0.2** Implement `OpenAICompatibleWorker` (base URL, API key env, model id).
- [ ] **M0.3** Implement `OpenCodeGoWorker` defaults:
  - Base URL: `https://opencode.ai/zen/go/v1` (chat completions path as documented for Go)
  - Auth: `OPENCODE_API_KEY` or `OPENCODE_GO_API_KEY` (document exact env after one live probe)
  - Model: configurable (e.g. a Go lineup coding model — pick after `models` list probe)
- [ ] **M0.4** Refactor `openrouter_sequencer.py` → `sequencer.py` (or keep name, inject client via env `WORKER_BACKEND=opencode_go|openai_compatible`).
- [ ] **M0.5** Env matrix in docs: `WORKER_BASE_URL`, `WORKER_API_KEY`, `WORKER_MODEL`, `WORKER_BACKEND`.
- [ ] **M0.6** Live smoke: one completion through OpenCode Go; record model id in `examples/` or notes (no secrets).
- [ ] **M0.7** Deprecate OpenRouter-only naming in README; keep example run as historical.

## Worker-eligible units (2–4 pure codegen briefs)

Fan out after M0.1 interface is sketched by manager:

| ID | Target | Brief focus | Deps |
|----|--------|-------------|------|
| **W0.1** | `scripts/worker_client.py` | Dataclass/config + abstract `generate`; raise clear errors on missing key | none |
| **W0.2** | `scripts/backends/openai_compatible.py` | urllib or stdlib HTTP POST chat/completions; parse `choices[0].message.content` | W0.1 |
| **W0.3** | `scripts/backends/opencode_go.py` | Thin wrapper setting Go base URL + headers | W0.1, W0.2 |
| **W0.4** | `tests/test_worker_client_parse.py` | Unit tests with **mocked** HTTP (no network) for JSON parse / error paths | W0.2 |

If only **2 workers**: merge W0.2+W0.3 into one “HTTP backend” unit; keep W0.1 and W0.4.

## Exit criteria

- [ ] Sequencer runs a mocked worker in CI/tests without network.
- [ ] Documented one-command smoke against OpenCode Go when key present.
- [ ] Zero required references to OpenRouter in runtime code paths.

## Verification

- pytest for parse + mock client.
- Manual: one Go completion returns non-empty text.
