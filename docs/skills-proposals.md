# Proposed Grok Skills (user-created)

Package these when the platform allows project skills.

## 1. `gza-run-init`
Copy `templates/run/` → `runs/<slug>/`; print Muse env exports.

## 2. `gza-brief`
Emit `briefs/<id>.md` from structured fields via `brief_format` rules (no repo dumps, no nested fences).

## 3. `gza-dispatch`
Verify env; set `MAX_PARALLEL_WORKERS` from ready-set (cap 4); run sequencer; summarize state + failures.

## 4. `gza-learn`
Append dated entry to `docs/learnings-log.md` (K, wall, pass rate, $, problems).

## 5. `gza-phase`
Read plan status; list open manager vs worker tasks; propose next wave.

## 6. `gza-auth-check`
One-shot Muse `pong` with x-api-key; report 200 vs 401/429 (no key echo).

| Mechanism | Use |
|-----------|-----|
| Custom instructions | Always-on manager identity |
| Skills | Procedural bundles above |
