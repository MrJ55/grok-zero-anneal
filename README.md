# grok-zero-anneal

**Grok-as-manager** orchestration: pure **no-tool** codegen workers + a restartable Python sequencer.

**Default worker (Phase 0):** [OpenCode Zen](https://opencode.ai/docs/zen/) **Muse** via `POST /zen/v1/responses` (`muse-spark-1.2-contributor-free`).  
Not tied to OpenRouter. Chat-completions backends (MiMo, OpenCode Go) supported via `WORKER_BACKEND=openai_chat`.

## Roles

| Role | Who |
|------|-----|
| User | Goal only |
| **Manager** | **Grok** — plan, brief, place, gate, replan |
| **Sequencer** | `scripts/sequencer.py` |
| **Workers** | HTTP text only — Muse Responses by default |

## Phase 0 status

Done: provider-agnostic client, Muse smoke, **parallel K=2..5** probe on trivial prompts.  
Details: [`docs/phase-0-results.md`](./docs/phase-0-results.md) · plan: [`plan/`](./plan/).

```bash
export WORKER_BACKEND=zen_responses
export OPENCODE_API_KEY=...          # Zen key
export WORKER_MODEL=muse-spark-1.2-contributor-free
export RUN_DIR=$PWD/runs/<id>
export MAX_PARALLEL_WORKERS=1        # raise when targets are disjoint
python scripts/sequencer.py
pytest tests -q
```

## Plan overview

| Phase | Focus | Status |
|-------|--------|--------|
| 0 | WorkerClient + Zen/Muse | **Done** |
| 1 | Ledger hardening | Next |
| 2 | Multi-unit fan-out dogfood | Pending |
| 3–5 | Stages, playbooks, package | Pending |

Sibling: [pi-zero-shot](https://github.com/MrJ55/pi-zero-shot) (Pi extension path).

## License

MIT for code in this repo unless noted.
