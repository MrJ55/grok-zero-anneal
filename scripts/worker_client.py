"""Provider-agnostic pure-text worker client (no tools)."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol


class WorkerError(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None, body: str | None = None):
        super().__init__(message)
        self.status = status
        self.body = body


class WorkerClient(Protocol):
    def generate(self, system: str, user: str, *, model: str | None = None) -> str:
        """Return assistant text only."""


@dataclass
class WorkerConfig:
    api_key: str
    base_url: str
    model: str
    backend: str  # zen_responses | openai_chat
    timeout: float = 120.0
    user_agent: str = "grok-zero-anneal/0.1"

    @classmethod
    def from_env(cls) -> "WorkerConfig":
        backend = os.environ.get("WORKER_BACKEND", "zen_responses").strip().lower()
        key = (
            os.environ.get("WORKER_API_KEY")
            or os.environ.get("OPENCODE_API_KEY")
            or os.environ.get("OPENCODE_GO_API_KEY")
            or ""
        ).strip()
        if not key:
            raise WorkerError("WORKER_API_KEY or OPENCODE_API_KEY not set")

        if backend in ("zen_responses", "muse", "opencode_zen_responses"):
            base = os.environ.get("WORKER_BASE_URL", "https://opencode.ai/zen/v1").rstrip("/")
            model = os.environ.get("WORKER_MODEL", "muse-spark-1.2-contributor-free")
            return cls(api_key=key, base_url=base, model=model, backend="zen_responses")

        if backend in ("openai_chat", "zen_chat", "mimo", "opencode_zen_chat", "opencode_go"):
            default_base = (
                "https://opencode.ai/zen/go/v1"
                if backend == "opencode_go"
                else "https://opencode.ai/zen/v1"
            )
            base = os.environ.get("WORKER_BASE_URL", default_base).rstrip("/")
            model = os.environ.get("WORKER_MODEL", "mimo-v2.5-free")
            return cls(api_key=key, base_url=base, model=model, backend="openai_chat")

        raise WorkerError(f"unknown WORKER_BACKEND={backend!r}")


def _http_json(
    url: str,
    payload: dict,
    *,
    api_key: str,
    timeout: float,
    user_agent: str,
    auth_style: str = "x-api-key",
) -> dict:
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": user_agent,
    }
    # Zen rejects Bearer (401 Invalid API key). Use x-api-key only for Zen.
    if auth_style == "bearer":
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        headers["x-api-key"] = api_key
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise WorkerError(f"HTTP {e.code} from {url}: {body[:400]}", status=e.code, body=body) from e


def extract_responses_text(data: dict) -> str:
    """Parse OpenAI-style Responses API JSON for assistant text."""
    parts: list[str] = []
    for item in data.get("output") or []:
        if item.get("type") != "message":
            continue
        for c in item.get("content") or []:
            if c.get("type") in ("output_text", "text") and c.get("text"):
                parts.append(c["text"])
    if parts:
        return "\n".join(parts).strip()
    if isinstance(data.get("output_text"), str) and data["output_text"].strip():
        return data["output_text"].strip()
    raise WorkerError("no assistant text in responses payload", body=json.dumps(data)[:500])


def extract_chat_text(data: dict) -> str:
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise WorkerError("no choices[0].message.content", body=json.dumps(data)[:500]) from e
    if content is None:
        raise WorkerError("empty chat content", body=json.dumps(data)[:500])
    if isinstance(content, list):
        texts = [c.get("text", "") for c in content if isinstance(c, dict)]
        return "\n".join(t for t in texts if t).strip()
    return str(content).strip()


@dataclass
class HttpWorker:
    config: WorkerConfig

    def generate(self, system: str, user: str, *, model: str | None = None) -> str:
        model = model or self.config.model
        auth_style = "x-api-key" if self.config.backend == "zen_responses" else "bearer"
        if self.config.backend == "zen_responses":
            prompt = user if not system else f"{system.rstrip()}\n\n{user}"
            url = f"{self.config.base_url}/responses"
            data = _http_json(
                url,
                {"model": model, "input": prompt},
                api_key=self.config.api_key,
                timeout=self.config.timeout,
                user_agent=self.config.user_agent,
                auth_style=auth_style,
            )
            return extract_responses_text(data)

        url = f"{self.config.base_url}/chat/completions"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        data = _http_json(
            url,
            {"model": model, "messages": messages, "temperature": 0.2},
            api_key=self.config.api_key,
            timeout=self.config.timeout,
            user_agent=self.config.user_agent,
            auth_style=auth_style,
        )
        return extract_chat_text(data)


def make_worker(config: WorkerConfig | None = None) -> HttpWorker:
    return HttpWorker(config or WorkerConfig.from_env())
