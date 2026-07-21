#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sanitize LLM feedback strings before TTS / String publish."""

DEFAULT_MAX_CHARS = 3000


def sanitize_feedback_text(text, max_chars=DEFAULT_MAX_CHARS):
    """
    Return a cleaned feedback string, or None if unusable.

    - None / non-str → None (bool is rejected)
    - strip whitespace; empty → None
    - truncate to max_chars (must be positive int)
    """
    if text is None or isinstance(text, bool) or not isinstance(text, str):
        return None
    cleaned = text.strip()
    if not cleaned:
        return None
    try:
        limit = int(max_chars)
    except (TypeError, ValueError):
        limit = DEFAULT_MAX_CHARS
    if limit <= 0:
        limit = DEFAULT_MAX_CHARS
    if len(cleaned) > limit:
        cleaned = cleaned[:limit]
    return cleaned
