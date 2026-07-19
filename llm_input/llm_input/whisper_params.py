#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Daniel Pike / Bartok9 contributors
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
"""Fail-closed helpers for OpenAI Whisper model size and language."""

from __future__ import annotations

import re

ALLOWED_WHISPER_SIZES = frozenset(
    {
        "tiny",
        "base",
        "small",
        "medium",
        "large",
        "tiny.en",
        "base.en",
        "small.en",
        "medium.en",
        "large-v1",
        "large-v2",
        "large-v3",
    }
)

_LANG_RE = re.compile(r"^[a-z]{2}(-[a-z]{2})?$")
_CTRL = re.compile(r"[\x00-\x1f\x7f]")


def sanitize_whisper_model_size(raw, default: str = "base") -> str:
    """Return an allowlisted Whisper model size name."""
    if default not in ALLOWED_WHISPER_SIZES:
        default = "base"
    if raw is None:
        return default
    if not isinstance(raw, str):
        return default
    size = raw.strip().lower()
    if not size or _CTRL.search(size):
        return default
    if any(sep in size for sep in ("/", "\\", " ", "\t", ";", "|", "&", "$", "`", "..")):
        return default
    if size not in ALLOWED_WHISPER_SIZES:
        return default
    return size


def sanitize_whisper_language(raw, default: str = "en") -> str:
    """Return a safe short language code for whisper.transcribe."""
    if not isinstance(default, str) or not default:
        default = "en"
    default = default.strip().lower()
    if default != "auto" and not _LANG_RE.match(default):
        default = "en"
    if raw is None:
        return default
    if not isinstance(raw, str):
        return default
    lang = raw.strip().lower().replace("_", "-")
    if not lang or _CTRL.search(lang) or len(lang) > 8:
        return default
    if any(sep in lang for sep in ("/", "\\", " ", "\t", ";", "|", "&", "$", "`", "..")):
        return default
    if lang == "auto":
        return "auto"
    if not _LANG_RE.match(lang):
        return default
    return lang
