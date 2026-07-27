# -*- coding: utf-8 -*-
"""Fail-closed helpers when OpenAI ChatCompletion raises or returns unusable payloads."""

EMPTY_COMPLETION = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": None,
            }
        }
    ]
}


def empty_chat_completion():
    """Return a shallow-safe empty ChatCompletion-like dict (no function_call)."""
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": None,
                }
            }
        ]
    }


def is_usable_chat_completion(response):
    """True if response has choices[0].message as a mapping."""
    if not isinstance(response, dict):
        return False
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        return False
    first = choices[0]
    if not isinstance(first, dict):
        return False
    message = first.get("message")
    return isinstance(message, dict)


def completion_or_empty(response, error=None):
    """Prefer usable response; otherwise return empty completion."""
    if error is not None:
        return empty_chat_completion()
    if is_usable_chat_completion(response):
        return response
    return empty_chat_completion()
