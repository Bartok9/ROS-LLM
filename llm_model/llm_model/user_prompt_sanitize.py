#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok / contributors (user prompt bounds)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Fail-closed sanitizer for user prompts before OpenAI chat completion.

"""Sanitize user prompt text before chat history / OpenAI API calls."""

from __future__ import annotations

DEFAULT_MAX_CHARS = 8000


def sanitize_user_prompt(text, max_chars=DEFAULT_MAX_CHARS):
    """
    Return a cleaned user prompt string, or None if unusable.

    - None / bool / non-str → None
    - strip whitespace; empty → None
    - drop C0 control bytes except newline and tab
    - truncate to max_chars (must be positive int; bad max → default)
    """
    if text is None or isinstance(text, bool) or not isinstance(text, str):
        return None
    # Keep wtsp semantics simple: strip ends, then filter controls
    cleaned_chars = []
    for ch in text:
        code = ord(ch)
        if code < 32 and ch not in ("\n", "\t"):
            continue
        if code == 127:
            continue
        cleaned_chars.append(ch)
    cleaned = "".join(cleaned_chars).strip()
    if not cleaned:
        return None
    try:
        limit = int(max_chars)
    except (TypeError, ValueError):
        limit = DEFAULT_MAX_CHARS
    if isinstance(max_chars, bool):
        limit = DEFAULT_MAX_CHARS
    if limit <= 0:
        limit = DEFAULT_MAX_CHARS
    if len(cleaned) > limit:
        cleaned = cleaned[:limit]
    return cleaned
