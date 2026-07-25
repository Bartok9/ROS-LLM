# -*- coding: utf-8 -*-
"""Fail-closed extraction of OpenAI ChatCompletion choice message fields."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


def extract_choice_message(
    chatgpt_response: Any,
) -> Tuple[Dict[str, Any], Optional[Any], Any, int]:
    """
    Return (message, content, function_call, function_flag).

    function_flag = 0 for text (or unknown / failure), 1 for function_call.
    Missing/malformed payloads yield empty message, content None, flag 0.
    """
    empty: Dict[str, Any] = {}
    if not isinstance(chatgpt_response, dict):
        return empty, None, None, 0

    choices = chatgpt_response.get("choices")
    if not isinstance(choices, list) or not choices:
        return empty, None, None, 0

    first = choices[0]
    if not isinstance(first, dict):
        return empty, None, None, 0

    message = first.get("message")
    if not isinstance(message, dict):
        return empty, None, None, 0

    content = message.get("content")
    function_call = message.get("function_call", None)

    if content is not None:
        function_flag = 0
    else:
        function_flag = 1 if function_call is not None else 0

    return message, content, function_call, function_flag
