import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.task_graph import ready_tasks, validate_tasks, wave_for_parallel


def test_ready_and_wave():
    tasks = [
        {"id": "a", "target": "a.py", "deps": []},
        {"id": "b", "target": "b.py", "deps": []},
        {"id": "c", "target": "c.py", "deps": ["a"]},
    ]
    validate_tasks(tasks)
    r = ready_tasks(tasks, set())
    assert {t["id"] for t in r} == {"a", "b"}
    w = wave_for_parallel(r, 2)
    assert len(w) == 2
    r2 = ready_tasks(tasks, {"a", "b"})
    assert [t["id"] for t in r2] == ["c"]


def test_cycle():
    tasks = [
        {"id": "a", "deps": ["b"]},
        {"id": "b", "deps": ["a"]},
    ]
    with pytest.raises(ValueError):
        validate_tasks(tasks)
