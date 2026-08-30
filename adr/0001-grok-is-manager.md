# ADR 0001: Grok is the manager

## Status

Accepted

## Context

We need an orchestration path that does not depend on Pi subagents or the user driving a checklist. The user supplies a goal; an agent in the chat window should own planning, briefing, integration, and gates.

## Decision

**Grok (chat agent) is the sole manager.** The user does not act as manager. Grok writes the sequencer, briefs, and ledger files and runs the process.

## Consequences

- Session handoff docs must tell the next Grok instance to take ownership immediately.
- UX is “give a goal,” not “run these steps.”
- Manager token use is real and should stay on judgment/integration, not bulk codegen.
