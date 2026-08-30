# Grok Skills for grok-zero-anneal

Full skill packages live under [`skills/`](../skills/). Each folder is a standard Grok skill (`SKILL.md` frontmatter + body).

| Skill | When to use |
|-------|-------------|
| [gza-run-init](../skills/gza-run-init/SKILL.md) | New run directory / ledger scaffold |
| [gza-brief](../skills/gza-brief/SKILL.md) | Write or fix pure-worker briefs |
| [gza-dispatch](../skills/gza-dispatch/SKILL.md) | Run sequencer / parallel wave |
| [gza-learn](../skills/gza-learn/SKILL.md) | Append learnings-log entry |
| [gza-phase](../skills/gza-phase/SKILL.md) | Phase status / what next |
| [gza-auth-check](../skills/gza-auth-check/SKILL.md) | Verify Zen Muse auth (no key echo) |

## How to install in Grok

1. Open Grok **Custom skills** (or project skills) for the grok-zero-anneal project.
2. For each skill folder, create a skill named exactly as `name:` in frontmatter.
3. Paste the full `SKILL.md` contents (including YAML frontmatter).
4. Keep [docs/CUSTOM_INSTRUCTIONS.md](./CUSTOM_INSTRUCTIONS.md) as always-on manager identity; skills are procedural add-ons.

| Mechanism | Use for |
|-----------|--------|
| Custom instructions | Always-on identity (manager, Muse defaults, no worker tools) |
| Skills | On-demand procedures above |
