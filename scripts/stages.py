"""Anneal-style stage machine for a single task unit."""
from __future__ import annotations

from enum import Enum
from typing import Any


class Stage(str, Enum):
    IMPLEMENT = "implement"
    VERIFY = "verify"
    MANAGER_FIX = "manager_fix"
    DONE = "done"


def next_stage(
    *,
    verify_ok: bool | None = None,
    implement_attempts: int = 0,
    max_implement_attempts: int = 3,
    code_placed: bool = False,
) -> Stage:
    """Pure transition helper for one task lifecycle step.

    Typical flow:
      implement (worker) -> verify (pytest) -> done
      verify fail -> implement again until max -> manager_fix
    """
    if verify_ok is True:
        return Stage.DONE
    if verify_ok is False:
        if implement_attempts >= max_implement_attempts:
            return Stage.MANAGER_FIX
        return Stage.IMPLEMENT
    # No verify result yet
    if not code_placed:
        return Stage.IMPLEMENT
    return Stage.VERIFY


def task_stage_view(state: dict[str, Any], task_id: str) -> dict[str, Any]:
    """Read per-task stage fields from run state (defaults)."""
    stages = state.setdefault("stages", {})
    entry = stages.setdefault(
        task_id,
        {"current": Stage.IMPLEMENT.value, "history": []},
    )
    return entry


def record_stage(
    state: dict[str, Any],
    task_id: str,
    stage: Stage | str,
    *,
    detail: str | None = None,
) -> None:
    entry = task_stage_view(state, task_id)
    name = stage.value if isinstance(stage, Stage) else str(stage)
    entry["current"] = name
    hist = entry.setdefault("history", [])
    event: dict[str, Any] = {"stage": name}
    if detail:
        event["detail"] = detail
    hist.append(event)
