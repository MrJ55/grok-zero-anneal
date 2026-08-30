# grok-zero-anneal

**Grok-as-manager** orchestration: pure **no-tool** codegen workers + a restartable Python sequencer.

Combines ideas from:

- **Zero-shot ledger control** ([GVS5H](https://github.com/slee-persis/GVS5H) / [arXiv:2608.26480](https://arxiv.org/abs/2608.26480)) — short worker contexts, shared durable state, external gates
- **Anneal-style stages** — plan → implement → verify → retry, deterministic controller

**Not** a [Pi](https://github.com/earendil-works/pi) extension. For the Pi-oriented port, see **[pi-zero-shot](https://github.com/MrJ55/pi-zero-shot)**.

## Roles

| Role | Who |
|------|-----|
| User | States a goal (“implement this plan in repo X”) |
| **Manager** | **Grok**: plans, writes briefs/sequencer, places code, runs tests, rewrites strategy |
| **Sequencer** | Python — deterministic loop, **0 LLM tokens** |
| **Workers** | **Provider-agnostic** chat completions (**no tools**). **Default next backend: [OpenCode Go](https://opencode.ai/go)** |

OpenRouter was used only for an early smoke test (`examples/run-001/`). Runtime code should not require it ([ADR 0004](./adr/0004-provider-agnostic-workers.md)).

## Implementation plan

Manager-driven phases and **2–5 worker** task lists:

**→ [`plan/`](./plan/)**

| Phase | Focus |
|-------|--------|
| 0 | Provider-agnostic `WorkerClient` + OpenCode Go adapter |
| 1 | Ledger / parse / state hardening |
| 2 | Multi-unit fan-out (2–5 workers) + dogfood demo |
| 3 | Anneal stages |
| 4 | Manager playbooks |
| 5 | Packaging / v0 done |

Cheatsheet: [`docs/manager-decomposition-cheatsheet.md`](./docs/manager-decomposition-cheatsheet.md).

## First smoke (historical)

- Worker via OpenRouter Laguna free; unit `parse_worker_response`; manager integration after extract bug; pytest green.
- Artifacts: [`examples/run-001/`](./examples/run-001/).

## Quick start (target shape)

```bash
export WORKER_BACKEND=opencode_go   # after Phase 0
export WORKER_API_KEY=...           # OpenCode Go key
export WORKER_MODEL=...             # a Go lineup model
export RUN_DIR=$PWD/runs/<id>
python scripts/sequencer.py         # name after Phase 0 refactor
```

Until Phase 0 lands, see `scripts/openrouter_sequencer.py` as the prototype loop (replace backend, do not treat OpenRouter as required).

```bash
pytest tests/test_codegen_parse.py -q
```

## Layout

```text
grok-zero-anneal/
├── plan/              ← phased task lists for Grok-as-manager
├── docs/
├── adr/
├── scripts/
├── tests/
├── templates/run/
└── examples/run-001/
```

## Relationship to pi-zero-shot

| Repo | Focus |
|------|--------|
| **grok-zero-anneal** (this) | Grok manager + sequencer + pure workers (OpenCode Go default) |
| [pi-zero-shot](https://github.com/MrJ55/pi-zero-shot) | Pi extension / skill; pi-subagents |

## License

MIT for code in this repo unless noted. Paper content remains under upstream licenses.
