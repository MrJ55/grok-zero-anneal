"""Unit tests for worker response parsers (no network)."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.worker_client import WorkerError, extract_chat_text, extract_responses_text


def test_extract_responses_message():
    data = {
        "output": [
            {"type": "reasoning", "encrypted_content": "x"},
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": "pong"}],
            },
        ]
    }
    assert extract_responses_text(data) == "pong"


def test_extract_responses_missing():
    with pytest.raises(WorkerError):
        extract_responses_text({"output": [{"type": "reasoning"}]})


def test_extract_chat():
    data = {"choices": [{"message": {"content": "hello"}}]}
    assert extract_chat_text(data) == "hello"


def test_extract_chat_missing():
    with pytest.raises(WorkerError):
        extract_chat_text({})
