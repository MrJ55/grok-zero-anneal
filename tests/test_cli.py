"""CLI smoke tests (no network)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_init_run(tmp_path: Path):
    dest = tmp_path / "runx"
    proc = subprocess.run(
        [sys.executable, "-m", "scripts.cli", "init-run", str(dest), "--goal", "g"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert (dest / "plan.md").exists()


def test_cli_help():
    proc = subprocess.run(
        [sys.executable, "-m", "scripts.cli", "--help"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "init-run" in proc.stdout
