# -*- coding: utf-8 -*-
"""Fail-closed JSON parsing for ChatGPT function_call service requests."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional, Tuple


def parse_function_call_request(
    request_text: Any,
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]], Optional[str]]:
    """Parse LLM function-call JSON into (ok, name, args, error)."""
    if request_text is None:
        return False, None, None, "request_text is empty"
    if isinstance(request_text, bytes):
        try:
            request_text = request_text.decode("utf-8")
        except Exception as exc:  # noqa: BLE001
            return False, None, None, f"request_text decode failed: {exc}"
    if not isinstance(request_text, str):
        request_text = str(request_text)
    text = request_text.strip()
    if not text:
        return False, None, None, "request_text is empty"

    try:
        req = json.loads(text)
    except json.JSONDecodeError as exc:
        return False, None, None, f"invalid JSON: {exc}"

    if not isinstance(req, dict):
        return False, None, None, "request JSON must be an object"

    name = req.get("name")
    if not isinstance(name, str) or not name.strip():
        return False, None, None, "missing or invalid function name"
    name = name.strip()

    raw_args = req.get("arguments", {})
    if isinstance(raw_args, str):
        raw_args = raw_args.strip()
        if not raw_args:
            args: Dict[str, Any] = {}
        else:
            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError as exc:
                return False, None, None, f"invalid arguments JSON: {exc}"
    elif isinstance(raw_args, dict):
        args = raw_args
    elif raw_args is None:
        args = {}
    else:
        return False, None, None, "arguments must be object or JSON string"

    if not isinstance(args, dict):
        return False, None, None, "arguments must decode to an object"

    return True, name, args, None
