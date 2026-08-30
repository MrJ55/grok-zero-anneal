# Manager cheatsheet: 2–5 worker decomposition

## Always manager-owned

- Goal interpretation, task graph, dependency edges
- Writing **failing tests** (or reviewing worker tests)
- Repo exploration, git, secrets, provider config
- Placing code if extract fails; integration across files
- Rewriting sequencer / briefs when contracts were wrong

## Safe to give pure workers

- Single-file (or single-function) implementation against a fixed signature
- Pure functions with tests already in tree
- Parsers, formatters, small algorithms
- Mock-based unit tests for HTTP JSON parsing (no live network in worker)

## Fan-out rules

| K | Use when |
|---|----------|
| 2 | Default; two independent modules or impl+tests if tests don’t need impl source |
| 3–4 | Demo library style (slugify / clamp / parse_kv / hash) |
| 5 | Only if all five targets are disjoint and briefs are ≤ ~1–2k tokens |

Never parallelize two writers to the same path.

## Brief minimum viable content

1. Target path  
2. Full signature / types  
3. Allowed imports  
4. Must-not list  
5. Acceptance bullets or examples  
6. Only necessary code excerpts  

## After worker returns

1. Parse `## code`  
2. Write target  
3. Run gate  
4. Pass → mark complete  
5. Fail → rebrief with pytest tail (worker) or fix contract (manager)  
