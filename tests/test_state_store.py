import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.state_store import bump_attempt, load_state, mark_complete, save_state


def test_roundtrip(tmp_path: Path):
    p = tmp_path / "state.json"
    st = load_state(p)
    assert st["completed"] == []
    bump_attempt(st, "t1")
    mark_complete(st, "t1")
    save_state(p, st)
    st2 = load_state(p)
    assert st2["completed"] == ["t1"]
    assert st2["attempts"]["t1"] == 1
    assert p.read_text().endswith("\n")
