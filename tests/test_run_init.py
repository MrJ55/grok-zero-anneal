"""Tests for run_init."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_init import init_run


def test_init_run_creates_layout(tmp_path: Path):
    dest = tmp_path / "r1"
    path = init_run(dest, plan_goal="demo goal")
    assert path == dest.resolve()
    assert (dest / "plan.md").exists()
    assert "demo goal" in (dest / "plan.md").read_text()
    assert (dest / "tasks.json").exists()
    assert (dest / "briefs").is_dir()
    assert (dest / "workspace" / "tests").is_dir()
    state = json.loads((dest / "state.json").read_text())
    assert "completed" in state


def test_init_run_refuses_nonempty(tmp_path: Path):
    dest = tmp_path / "r2"
    dest.mkdir()
    (dest / "junk.txt").write_text("x")
    with pytest.raises(FileExistsError):
        init_run(dest)
    init_run(dest, force=True)
