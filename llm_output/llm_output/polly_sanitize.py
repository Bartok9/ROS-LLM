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
"""Fail-closed helpers for AWS Polly voice ids and TTS feedback text."""

from __future__ import annotations

import re
from typing import Tuple

# Common Polly standard / neural voices used in ROS-LLM and docs (Ivy, Zhiyu - zh).
ALLOWED_POLLY_VOICES = frozenset(
    {
        "Ivy",
        "Joanna",
        "Joey",
        "Justin",
        "Kendra",
        "Kimberly",
        "Matthew",
        "Salli",
        "Amy",
        "Emma",
        "Brian",
        "Aditi",
        "Raveena",
        "Zhiyu",
        "Laura",
        "Ruth",
        "Stephen",
        "Lucia",
        "Lea",
        "Vicki",
        "Hans",
        "Marlene",
        "Mizuki",
        "Takumi",
        "Seoyeon",
        "Camila",
        "Lupe",
        "Mia",
        "Pedro",
        "Andres",
        "Sergio",
        "Bianca",
        "Carla",
        "Giorgio",
        "Celine",
        "Mathieu",
        "Chantal",
        "Vitória",
        "Camila",
        "Ricardo",
        "Ines",
        "Cristiano",
        "Carmen",
        "Enrique",
        "Conchita",
        "Naja",
        "Mads",
        "Ruben",
        "Lotte",
        "Astrid",
        "Filiz",
        "Jacek",
        "Jan",
        "Ewa",
        "Maja",
        "Karl",
        "Dora",
        "Liv",
        "Tatyana",
        "Maxim",
        "Gwyneth",
        "Geraint",
        "Nicole",
        "Russell",
        "Olivia",
        "Aria",
        "Ayanda",
        "Kajal",
        "Hiujin",
        "Zayd",
        "Hala",
        "Arlet",
        "Hannah",
        "Sofie",
        "Ida",
        "Niamh",
        "Danielle",
        "Gregory",
        "Kevin",
        "Arthur",
        "Kajal",
        "Ola",
        "Suvi",
        "Lisa",
        "Adriano",
        "Thiago",
        "Andres",
        "Sergio",
        "Lucia",
        "Sergio",
        "Isabelle",
        "Kazuha",
        "Tomoko",
        "Jihye",
        "Seoyeon",
    }
)

_CTRL = re.compile(r"[\x00-\x1f\x7f]")


def sanitize_polly_voice_id(raw, default: str = "Ivy") -> str:
    """Return an allowlisted Polly VoiceId or ``default``."""
    if default not in ALLOWED_POLLY_VOICES:
        default = "Ivy"
    if raw is None:
        return default
    if not isinstance(raw, str):
        return default
    voice = raw.strip()
    if not voice or _CTRL.search(voice):
        return default
    if any(sep in voice for sep in ("/", "\\", " ", "\t", ";", "|", "&", "$", "`")):
        return default
    if voice not in ALLOWED_POLLY_VOICES:
        return default
    return voice


def sanitize_feedback_text(raw, max_len: int = 3000) -> Tuple[bool, str]:
    """Require non-empty user-facing TTS text; cap length; reject NUL."""
    if raw is None:
        return False, "empty_feedback"
    if not isinstance(raw, str):
        try:
            raw = str(raw)
        except Exception:
            return False, "invalid_feedback_type"
    text = raw.replace("\x00", "").strip()
    if not text:
        return False, "empty_feedback"
    if max_len is not None and max_len > 0 and len(text) > max_len:
        text = text[:max_len]
    return True, text
