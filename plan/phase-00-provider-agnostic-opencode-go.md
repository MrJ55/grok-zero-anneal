# Phase 0 — Provider-agnostic worker + Zen/Muse (STATUS: largely done)

Originally titled OpenCode Go; **executed with OpenCode Zen + Muse** because Muse `/responses` worked and MiMo free was rate-limited.

## Goals

- Remove hard dependency on OpenRouter.
- One `WorkerClient` interface; Zen Muse as default adapter.
- Sequencer calls the interface only.

## Manager tasks

- [x] **M0.1** `WorkerClient.generate` in `scripts/worker_client.py`
- [x] **M0.2** OpenAI chat-completions path (`openai_chat`)
- [x] **M0.3** Zen Responses path for Muse (`zen_responses`)
- [x] **M0.4** `scripts/sequencer.py` injects client via env
- [x] **M0.5** Env matrix in `scripts/README.md`
- [x] **M0.6** Live Muse smoke + parallel 2–5 probe → `docs/phase-0-results.md`
- [x] **M0.7** OpenRouter demoted (legacy script kept)

## Worker-eligible units

Implemented primarily by manager for speed/correctness on infra; parsers covered by unit tests.

## Exit criteria

- [x] Mocked parse tests without network
- [x] Live Muse completion
- [x] Zero required OpenRouter references in new path
- [ ] Optional: live Go endpoint smoke when user switches subscription
