---
name: gza-auth-check
description: Smoke-test OpenCode Zen worker auth for grok-zero-anneal without printing secrets. Use when verifying API keys, Muse connectivity, or diagnosing 401 or 429 worker errors.
---

# gza-auth-check

## Steps

1. Confirm `OPENCODE_API_KEY` or `WORKER_API_KEY` is set in the runtime (do not print the value).
2. Run:

```bash
python -m scripts.cli check-auth
```

Or equivalent one-shot Muse Responses call with header `x-api-key` (not Bearer) to `https://opencode.ai/zen/v1/responses`, model `muse-spark-1.2-contributor-free`, input `Reply with exactly one word: pong`.

3. Report only HTTP/outcome (ok, 401, 429, other), backend and model id, and whether text contained pong.
4. On 401, remind Zen needs **x-api-key only**.
5. On 429, recommend backoff or alternate model — do not tight-loop.

## Do not

- Echo API keys into chat, logs, or git.
