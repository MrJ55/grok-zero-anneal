import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.brief_format import format_brief


def test_format_contains_sections():
    text = format_brief(
        {
            "unit_id": "t1",
            "target": "pkg/x.py",
            "implement": "Add clamp",
            "signature": "def clamp(x, lo, hi): ...",
            "allowed_imports": ["none"],
            "acceptance": ["clamp(5,0,3)==3"],
        }
    )
    assert "Unit id: t1" in text
    assert "Target path: pkg/x.py" in text
    assert "def clamp" in text
    assert "## code" in text
