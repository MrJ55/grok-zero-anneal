"""Unit tests for anneal stage transitions."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.stages import Stage, next_stage, record_stage, task_stage_view


def test_initial_implement():
    assert next_stage(code_placed=False) == Stage.IMPLEMENT


def test_after_place_verify():
    assert next_stage(code_placed=True) == Stage.VERIFY


def test_verify_ok_done():
    assert next_stage(verify_ok=True, code_placed=True) == Stage.DONE


def test_verify_fail_retry():
    assert (
        next_stage(verify_ok=False, implement_attempts=1, max_implement_attempts=3)
        == Stage.IMPLEMENT
    )


def test_verify_fail_exhausted_manager_fix():
    assert (
        next_stage(verify_ok=False, implement_attempts=3, max_implement_attempts=3)
        == Stage.MANAGER_FIX
    )


def test_record_stage_history():
    state: dict = {}
    record_stage(state, "t1", Stage.IMPLEMENT)
    record_stage(state, "t1", Stage.VERIFY, detail="pytest")
    entry = task_stage_view(state, "t1")
    assert entry["current"] == "verify"
    assert len(entry["history"]) == 2
