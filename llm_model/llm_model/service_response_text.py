# -*- coding: utf-8 -*-
"""Normalize ChatGPT function-call service responses for chat history."""

from __future__ import annotations

from typing import Any, Optional

_MAX_LEN = 4000


def normalize_function_call_response_text(
    response: Any = None, error: Optional[BaseException] = None
) -> str:
    """Return a short string safe to store in OpenAI chat history.

    On RPC failure, prefer an explicit error marker. On success, use
    ``response.response_text`` when present. Empty/missing becomes ``\"null\"``.
    """
    if error is not None:
        msg = str(error).strip() or type(error).__name__
        if len(msg) > 500:
            msg = msg[:500]
        return f"error: {msg}"

    if response is None:
        return "null"

    text = None
    if isinstance(response, dict):
        text = response.get("response_text")
    else:
        text = getattr(response, "response_text", None)

    if text is None:
        return "null"
    if not isinstance(text, str):
        if isinstance(text, bytes):
            text = text.decode("utf-8", errors="replace")
        else:
            text = str(text)
    text = text.strip()
    if not text:
        return "null"
    if len(text) > _MAX_LEN:
        return text[:_MAX_LEN]
    return text
