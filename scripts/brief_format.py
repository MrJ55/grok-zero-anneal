"""Format structured task fields into a worker brief."""
from __future__ import annotations

from typing import Any


def format_brief(fields: dict[str, Any]) -> str:
    """Build a standard pure-worker brief.

    Expected keys (all optional except unit_id/target/implement):
      unit_id, target, language, implement, signature, allowed_imports (list),
      must_not (list), acceptance (list), context (str)
    """
    unit = fields.get("unit_id") or fields.get("id") or "unit"
    target = fields.get("target") or "module.py"
    lang = fields.get("language") or "python"
    implement = fields.get("implement") or fields.get("title") or ""
    signature = fields.get("signature") or ""
    allowed = fields.get("allowed_imports") or ["stdlib only as needed"]
    must_not = fields.get("must_not") or [
        "use network, filesystem, or subprocess",
        "add dependencies not listed",
        "claim files were written or tests were run",
    ]
    acceptance = fields.get("acceptance") or []
    context = fields.get("context") or ""

    def bullets(items: list[str]) -> str:
        return "\n".join(f"- {x}" for x in items)

    parts = [
        f"Unit id: {unit}",
        f"Target path: {target}",
        f"Language: {lang}",
        "",
        "Implement:",
        implement.strip(),
        "",
    ]
    if signature:
        parts += ["Signature / shape:", signature.strip(), ""]
    parts += ["Allowed imports:", bullets(list(allowed)), ""]
    parts += ["Must not:", bullets(list(must_not)), ""]
    if acceptance:
        parts += ["Acceptance:", bullets(list(acceptance)), ""]
    if context:
        parts += ["Context (read-only excerpts):", context.strip(), ""]
    parts += [
        "Output format:",
        "## code",
        "",
        f"```{lang}",
        "# implementation only",
        "```",
        "",
        "## notes",
        "",
        "Short notes or none. Avoid triple-backtick sequences inside docstrings.",
    ]
    return "\n".join(parts).rstrip() + "\n"
