"""Augment worker briefs after mechanical verify failures."""
from __future__ import annotations


def append_pytest_failure(brief: str, output: str, *, max_tail: int = 3000) -> str:
    """Append pytest failure tail and fix instructions to a brief."""
    tail = (output or "")[-max_tail:]
    addition = (
        "\n\nPrevious attempt failed tests (mechanical verify):\n\n"
        + tail
        + "\n\nFix the implementation. Avoid triple-backtick sequences inside docstrings.\n"
    )
    return (brief or "").rstrip() + addition


def append_extract_failure(brief: str, *, reason: str = "no code section extracted") -> str:
    return (
        (brief or "").rstrip()
        + "\n\nPrevious attempt failed parsing: "
        + reason
        + ". Respond with ## code and ## notes sections only.\n"
    )
