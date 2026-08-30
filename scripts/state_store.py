"""Load/save run state.json with simple atomic replace."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def default_state() -> dict[str, Any]:
    return {"completed": [], "attempts": {}}


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return default_state()
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("completed", [])
    data.setdefault("attempts", {})
    return data


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(state, indent=2, ensure_ascii=False) + "\n"
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".state.", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(raw)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def mark_complete(state: dict[str, Any], task_id: str) -> None:
    if task_id not in state["completed"]:
        state["completed"].append(task_id)


def bump_attempt(state: dict[str, Any], task_id: str) -> int:
    n = int(state["attempts"].get(task_id, 0)) + 1
    state["attempts"][task_id] = n
    return n
