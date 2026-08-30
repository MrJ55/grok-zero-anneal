"""Unit tests for rebrief helpers."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.rebrief import append_extract_failure, append_pytest_failure


def test_append_pytest_failure_includes_tail():
    out = append_pytest_failure("brief body", "FAILED tests/foo.py::test_x")
    assert "brief body" in out
    assert "FAILED tests/foo.py::test_x" in out
    assert "mechanical verify" in out


def test_append_pytest_truncates():
    long = "x" * 5000
    out = append_pytest_failure("b", long, max_tail=100)
    assert len(out) < len(long) + 200


def test_append_extract_failure():
    out = append_extract_failure("b")
    assert "## code" in out
