# grok-zero-anneal

**Grok-as-manager** orchestration: pure no-tool codegen workers (OpenRouter) + a restartable Python sequencer.

Combines ideas from:

- **Zero-shot ledger control** ([GVS5H](https://github.com/slee-persis/GVS5H) / [arXiv:2608.26480](https://arxiv.org/abs/2608.26480)) — short worker contexts, shared durable state, external gates
- **Anneal-style stages** — plan → implement → verify → retry, deterministic controller

**Not** a [Pi](https://github.com/earendil-works/pi) extension. For the Pi-oriented port, see **[pi-zero-shot](https://github.com/MrJ55/pi-zero-shot)**.

## Roles

| Role | Who |
|------|-----|
| User | States a goal (“implement this plan in repo X”) |
| **Manager** | **Grok** (this class of agent): plans, writes briefs/sequencer, places code, runs tests, rewrites strategy |
| **Sequencer** | Python in a sandbox — deterministic loop, **0 LLM tokens** |
| **Workers** | OpenRouter chat completions only — **no tools**, micro-briefs in / code text out |

## First successful smoke (2026-08-30)

- Worker: `poolside/laguna-s-2.1:free`
- Unit: `scripts/codegen_parse.parse_worker_response`
- Laguna produced the implementation; sequencer truncated on nested fences in a docstring; manager integrated + fixed extractor; **4 pytest tests passed**
- Example run tree: [`examples/run-001/`](./examples/run-001/)

## Quick start (new session)

1. Clone this repo.
2. Set `OPENROUTER_API_KEY` (never commit it).
3. Optional: `WORKER_MODEL=poolside/laguna-s-2.1:free`
4. Copy [`templates/run/`](./templates/run/) to a new `runs/<id>/`, fill briefs, put tests under `workspace/`.
5. Manager (Grok) runs:

```bash
export RUN_DIR=$PWD/runs/<id>
export OPENROUTER_API_KEY=...
python scripts/openrouter_sequencer.py
```

6. On failure: manager reads `out/`, `state.json`, patches code and/or sequencer/tasks, re-runs (restartable).

Library helper used by managers and sequencers:

```python
from scripts.codegen_parse import parse_worker_response
code, notes = parse_worker_response(raw)
```

```bash
pytest tests/test_codegen_parse.py -q
```

## Layout

```text
grok-zero-anneal/
├── README.md
├── docs/           architecture, session handoff
├── adr/            decisions
├── scripts/        sequencer + parse helper
├── tests/
├── templates/run/  empty run skeleton
└── examples/run-001/  first real Laguna run (artifacts)
```

## Relationship to pi-zero-shot

| Repo | Focus |
|------|--------|
| **grok-zero-anneal** (this) | Grok manager + sandbox sequencer + OpenRouter workers |
| [pi-zero-shot](https://github.com/MrJ55/pi-zero-shot) | Pi extension / skill; pi-subagents spawn path |

Do not merge the two control planes; share ideas (ledger, pure workers, gates) only.

## License

MIT for code in this repo unless noted. Paper content remains under upstream licenses.
