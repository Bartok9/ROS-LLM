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
"""Bounded HTTP fetch helpers for AWS Transcribe transcript JSON."""

from __future__ import annotations

import json
from typing import Any, Tuple, Union

_DEFAULT_TIMEOUT = 15.0
_MIN_TIMEOUT = 1.0
_MAX_TIMEOUT = 120.0

_DEFAULT_MAX_BYTES = 1_000_000
_MIN_MAX_BYTES = 1024
_MAX_MAX_BYTES = 10_000_000


def clamp_transcript_http_timeout(value: Any, default: float = _DEFAULT_TIMEOUT) -> float:
    try:
        n = float(value)
    except (TypeError, ValueError):
        n = float(default)
    if n < _MIN_TIMEOUT:
        return _MIN_TIMEOUT
    if n > _MAX_TIMEOUT:
        return _MAX_TIMEOUT
    return n


def clamp_transcript_http_max_bytes(value: Any, default: int = _DEFAULT_MAX_BYTES) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        n = int(default)
    if n < _MIN_MAX_BYTES:
        return _MIN_MAX_BYTES
    if n > _MAX_MAX_BYTES:
        return _MAX_MAX_BYTES
    return n


def extract_transcript_text(payload: Any) -> Tuple[bool, str]:
    """Fail-closed navigate Transcribe transcript JSON."""
    if not isinstance(payload, dict):
        return False, "transcript payload is not an object"
    results = payload.get("results")
    if not isinstance(results, dict):
        return False, "missing results object"
    transcripts = results.get("transcripts")
    if not isinstance(transcripts, list) or not transcripts:
        return False, "missing transcripts list"
    first = transcripts[0]
    if not isinstance(first, dict):
        return False, "transcript entry is not an object"
    text = first.get("transcript")
    if text is None:
        return False, "missing transcript field"
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception:
            return False, "transcript not coercible to str"
    return True, text


def parse_transcript_http_body(
    body: Union[bytes, bytearray, str], max_bytes: Any = _DEFAULT_MAX_BYTES
) -> Tuple[bool, str]:
    """Decode + JSON-parse bounded body; return (ok, transcript_or_err)."""
    limit = clamp_transcript_http_max_bytes(max_bytes)
    if body is None:
        return False, "empty body"
    if isinstance(body, str):
        raw = body.encode("utf-8", errors="replace")
    else:
        raw = bytes(body)
    if len(raw) > limit:
        return False, "transcript body exceeds max_bytes=%s" % limit
    try:
        text = raw.decode("utf-8")
    except Exception as exc:  # noqa: BLE001
        return False, "utf-8 decode failed: %s" % exc
    try:
        payload = json.loads(text)
    except Exception as exc:  # noqa: BLE001
        return False, "json parse failed: %s" % exc
    return extract_transcript_text(payload)
