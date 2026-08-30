Unit id: t1-parse
Target path: scripts/codegen_parse.py
Language: python

Implement a module `scripts/codegen_parse.py` with exactly this public API:

```python
def parse_worker_response(text: str) -> tuple[str | None, str]:
    """Parse no-tool worker output into (code, notes).

    Expect markdown with sections:
      ## code
      optional fenced block (use fences; avoid fences inside docstrings)
      ## notes
      free text

    Returns:
      code: inner fence content, or raw section body if no fence;
            None if section missing or only whitespace.
      notes: notes section body stripped; empty string if missing.
    """
```

Allowed imports:
- re (stdlib only)
- typing if needed

Must not:
- use network, filesystem, or subprocess
- depend on third-party packages

Acceptance:
- Supports ## code / ## notes headers
- Strips language tag from fence opener
- Empty code section => None preferred
