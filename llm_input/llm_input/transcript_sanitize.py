#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok / contributors (transcript bounds)
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
# Fail-closed sanitizer for ASR/Whisper transcripts before ROS publish.

"""Sanitize transcript text before publishing to /llm_input_audio_to_text."""

from __future__ import annotations

DEFAULT_MAX_CHARS = 4000


def sanitize_transcript_text(text, max_chars=DEFAULT_MAX_CHARS):
    """
    Return a cleaned transcript string, or None if unusable.

    - None / bool / non-str → None
    - strip ends; empty → None
    - drop C0 controls except newline and tab; empty after → None
    - truncate to max_chars (positive int; bad max → default)
    """
    if text is None or isinstance(text, bool) or not isinstance(text, str):
        return None

    cleaned_chars = []
    for ch in text:
        code = ord(ch)
        if code < 32 and ch not in ("\n", "\t"):
            continue
        cleaned_chars.append(ch)
    cleaned = "".join(cleaned_chars).strip()
    if not cleaned:
        return None

    try:
        limit = int(max_chars)
    except (TypeError, ValueError):
        limit = DEFAULT_MAX_CHARS
    if isinstance(max_chars, bool) or limit <= 0:
        limit = DEFAULT_MAX_CHARS

    if len(cleaned) > limit:
        cleaned = cleaned[:limit]
    return cleaned
