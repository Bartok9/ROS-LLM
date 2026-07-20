#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
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
"""Sanitize OpenAI model ids and chat-history write bounds."""

from __future__ import annotations

import math
import re

_MODEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._\-]{0,63}$")
_TS_RE = re.compile(r"^[0-9A-Za-z_\-]{1,64}$")


def sanitize_openai_model_id(raw, default="gpt-3.5-turbo-0613"):
    """Return a safe OpenAI model id string or *default*."""
    if not isinstance(default, str) or not _MODEL_RE.match(default or ""):
        default = "gpt-3.5-turbo-0613"
    if raw is None:
        return default
    if not isinstance(raw, str):
        return default
    text = raw.strip()
    if not text or ".." in text or "/" in text or "\\" in text:
        return default
    if any(ord(ch) < 32 for ch in text):
        return default
    if not _MODEL_RE.match(text):
        return default
    return text


def clamp_chat_history_max_length(raw, default=4000, min_v=1, max_v=16000):
    """Clamp chat history max length to a positive int window."""
    if isinstance(raw, bool) or raw is None:
        return int(default)
    try:
        if isinstance(raw, float) and (math.isnan(raw) or math.isinf(raw)):
            return int(default)
        value = int(raw)
    except (TypeError, ValueError):
        return int(default)
    if value < int(min_v):
        return int(min_v)
    if value > int(max_v):
        return int(max_v)
    return value


def safe_chat_history_filename(prefix_ts: str, prefix="chat_history_", suffix=".json"):
    """Build a basename-only chat history file name from a timestamp fragment."""
    if not isinstance(prefix_ts, str):
        prefix_ts = "unknown"
    frag = prefix_ts.strip().replace(" ", "-")
    if not frag or ".." in frag or "/" in frag or "\\" in frag:
        frag = "unknown"
    if any(ord(ch) < 32 for ch in frag):
        frag = "unknown"
    if not _TS_RE.match(frag):
        frag = "unknown"
    return f"{prefix}{frag}{suffix}"
