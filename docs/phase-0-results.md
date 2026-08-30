# Phase 0 results (2026-08-30)

## Delivered

- `scripts/worker_client.py` — `WorkerConfig`, `HttpWorker`, Responses + chat extractors
- `scripts/sequencer.py` — uses WorkerClient; optional `MAX_PARALLEL_WORKERS`
- Tests: `tests/test_worker_client_parse.py`, `tests/test_worker_config.py` (no network)
- Default backend: **OpenCode Zen Responses** + `muse-spark-1.2-contributor-free`
- OpenRouter not required

## Live Muse smoke

- Single `POST /zen/v1/responses` → `pong` (x-api-key)
- MiMo `/chat/completions` was rate-limited earlier; Muse preferred

## Parallelism probe (Muse, independent tiny prompts)

| Concurrency | Result | Notes |
|-------------|--------|-------|
| 2 | OK | texts `ok0`/`ok1` |
| 3 | OK | wall ~3s class |
| 5 | OK | wall ~2.4s; all five texts correct |

**Conclusion:** API allows **at least 5 concurrent** Muse Responses calls from this sandbox for trivial prompts. Real codegen units will be slower and may hit free-tier limits; sequencer should keep `MAX_PARALLEL_WORKERS` conservative (2–3) until gates prove stable.

**Caveats**

- Do not parallelize writers to the same `target` path (sequencer collapses wave).
- Avoid tiny `max_output_tokens` — reasoning can consume the budget before `output_text`.
- Use `User-Agent`; missing UA correlated with odd 403s in one probe.

## Exit criteria

- [x] No OpenRouter hard dependency in new runtime path
- [x] Mock/unit tests without network
- [x] Documented Muse smoke + parallel probe
- [ ] Full multi-unit coding run with K>1 (Phase 2 dogfood)
