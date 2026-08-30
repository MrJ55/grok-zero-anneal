# Problems and solutions

| Problem | Symptom | Solution |
|---------|---------|----------|
| Nested ``` in worker docstring | Truncated module, SyntaxError | Outer-fence extract; ban nested fences in system prompt |
| OpenRouter free 429 | Worker HTTP 429 | Backoff; switch provider; manager escalate |
| Zen Bearer auth | HTTP 401 Invalid API key | Use **`x-api-key` only**; do not send Bearer |
| MiMo free rate limit | 429 FreeUsageLimitError | Prefer Muse; retry later |
| Muse tiny max_output_tokens | HTTP 200 but empty text | Reasoning ate budget; omit low max or raise |
| Parallel same target | Race / overwrite | `wave_for_parallel` unique targets only |
| Missing User-Agent | Intermittent 403 | Always set UA in worker client |
| Manager rewrites all code | No savings | Tighten briefs; fix harness; only escalate after N fails |
| Key in chat/git | Leak | Env only; rotate; `.gitignore` |
