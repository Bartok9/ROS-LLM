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
"""Fail-closed helpers for AWS Polly synthesize_speech audio streams."""

from __future__ import annotations

from typing import Any, Tuple, Union

_DEFAULT_MAX = 5_000_000
_MIN_MAX = 1_000
_MAX_MAX = 20_000_000


def clamp_polly_audio_max_bytes(value: Any, default: int = _DEFAULT_MAX) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        n = int(default)
    if n < _MIN_MAX:
        return _MIN_MAX
    if n > _MAX_MAX:
        return _MAX_MAX
    return n


def safe_read_audio_stream(
    stream: Any, max_bytes: Any = _DEFAULT_MAX
) -> Tuple[bool, Union[bytes, str]]:
    """Read Polly AudioStream with a hard byte cap.

    Returns (True, bytes) on success, (False, error_message) otherwise.
    """
    limit = clamp_polly_audio_max_bytes(max_bytes)
    if stream is None:
        return False, "missing AudioStream"
    read = getattr(stream, "read", None)
    if not callable(read):
        return False, "AudioStream has no read()"
    try:
        # read one extra byte to detect overflow without loading unbounded
        data = read(limit + 1)
    except Exception as exc:  # noqa: BLE001 — fail-closed network/SDK errors
        return False, "AudioStream read failed: %s" % exc
    if data is None:
        return False, "AudioStream returned None"
    if not isinstance(data, (bytes, bytearray)):
        try:
            data = bytes(data)
        except Exception:
            return False, "AudioStream did not return bytes"
    data = bytes(data)
    if len(data) > limit:
        return False, "AudioStream exceeds max_bytes=%s" % limit
    if len(data) == 0:
        return False, "AudioStream empty"
    return True, data
