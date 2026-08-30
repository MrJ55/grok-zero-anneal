"""WorkerConfig.from_env without network."""
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.worker_client import WorkerConfig, WorkerError


def test_zen_responses_defaults(monkeypatch):
    monkeypatch.setenv("WORKER_API_KEY", "test-key")
    monkeypatch.setenv("WORKER_BACKEND", "zen_responses")
    monkeypatch.delenv("WORKER_MODEL", raising=False)
    cfg = WorkerConfig.from_env()
    assert cfg.backend == "zen_responses"
    assert cfg.model == "muse-spark-1.2-contributor-free"
    assert cfg.base_url.endswith("/zen/v1")


def test_missing_key(monkeypatch):
    monkeypatch.delenv("WORKER_API_KEY", raising=False)
    monkeypatch.delenv("OPENCODE_API_KEY", raising=False)
    monkeypatch.delenv("OPENCODE_GO_API_KEY", raising=False)
    with pytest.raises(WorkerError):
        WorkerConfig.from_env()
