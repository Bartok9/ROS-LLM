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
"""Sanitize AWS Transcribe LanguageCode values from config."""

from __future__ import annotations

ALLOWED_AWS_TRANSCRIBE_LANG = frozenset(
    {
        "en-US",
        "en-GB",
        "en-AU",
        "en-IN",
        "en-IE",
        "en-NZ",
        "en-AB",
        "en-WL",
        "zh-CN",
        "zh-TW",
        "ja-JP",
        "ko-KR",
        "de-DE",
        "de-CH",
        "fr-FR",
        "fr-CA",
        "es-US",
        "es-ES",
        "pt-BR",
        "pt-PT",
        "it-IT",
        "hi-IN",
        "ar-SA",
        "ar-AE",
        "nl-NL",
        "ru-RU",
        "tr-TR",
        "th-TH",
        "vi-VN",
        "id-ID",
        "ms-MY",
        "ta-IN",
        "te-IN",
        "he-IL",
        "fa-IR",
        "sv-SE",
        "no-NO",
        "da-DK",
        "fi-FI",
        "pl-PL",
        "uk-UA",
        "cs-CZ",
        "ro-RO",
        "hu-HU",
        "el-GR",
        "ca-ES",
        "af-ZA",
    }
)


def sanitize_aws_transcribe_language(raw, default="en-US"):
    """Return an allowed Transcribe LanguageCode or *default*."""
    if default not in ALLOWED_AWS_TRANSCRIBE_LANG:
        default = "en-US"
    if raw is None:
        return default
    if not isinstance(raw, str):
        return default
    text = raw.strip()
    if not text:
        return default
    if any(ch in text for ch in ("/", "\\", "\x00", "\n", "\r", "\t", " ", "..")):
        return default
    if text not in ALLOWED_AWS_TRANSCRIBE_LANG:
        return default
    return text
