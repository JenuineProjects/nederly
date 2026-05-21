"""Shared LLM client for all Nederly agents.

Every agent is a thin wrapper around `call_claude(system, user)` that returns
parsed JSON. Keeping this tiny on purpose — the interesting logic lives in
each agent's system prompt and the orchestration in `manager.py`.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def call_claude(system: str, user: str, *, max_tokens: int = 2048) -> str:
    msg = _get_client().messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in msg.content if block.type == "text")


def call_claude_json(system: str, user: str, *, max_tokens: int = 2048) -> Any:
    """Same as call_claude but extracts and parses the first JSON object/array.

    Agents are told to wrap output in a ```json block; we tolerate raw JSON too.
    """
    raw = call_claude(system, user, max_tokens=max_tokens)
    return _extract_json(raw)


_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", re.DOTALL)


def _extract_json(raw: str) -> Any:
    m = _FENCE_RE.search(raw)
    candidate = m.group(1) if m else raw.strip()

    if not (candidate.startswith("{") or candidate.startswith("[")):
        start = min(
            (i for i in (candidate.find("{"), candidate.find("[")) if i != -1),
            default=-1,
        )
        if start == -1:
            raise ValueError(f"No JSON found in model output:\n{raw}")
        candidate = candidate[start:]

    return json.loads(candidate)
