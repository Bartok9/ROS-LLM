# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok / contributors (audio recording param clamp)
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
# Fail-closed clamps for sounddevice recording parameters.

from __future__ import annotations

import math
from typing import Any, Tuple, Union

_COMMON_RATES = frozenset({8000, 11025, 16000, 22050, 32000, 44100, 48000})
_MIN_RATE = 8000
_MAX_RATE = 48000
_MAX_DURATION = 60.0
_MAX_GAIN = 10.0


def _as_finite_float(value: Any, label: str) -> Tuple[bool, Union[float, str]]:
    if isinstance(value, bool):
        return False, f"{label} must not be bool"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False, f"{label} must be a number"
    if not math.isfinite(number):
        return False, f"{label} must be finite"
    return True, number


def sanitize_recording_params(
    duration: Any,
    sample_rate: Any,
    volume_gain_multiplier: Any,
) -> Tuple[bool, float, int, float, str]:
    """
    Validate recording knobs before allocating audio buffers.

    Returns (ok, duration, sample_rate, gain, err). On failure ok is False and
    err explains why; numeric fields may be placeholders.
    """
    ok_d, duration_or_err = _as_finite_float(duration, "duration")
    if not ok_d:
        return False, 0.0, 0, 0.0, str(duration_or_err)
    duration_f = float(duration_or_err)
    if duration_f <= 0.0 or duration_f > _MAX_DURATION:
        return (
            False,
            0.0,
            0,
            0.0,
            f"duration must be in (0, {_MAX_DURATION:g}] seconds",
        )

    if isinstance(sample_rate, bool):
        return False, 0.0, 0, 0.0, "sample_rate must not be bool"
    try:
        # reject non-integer floats like 16000.5
        if isinstance(sample_rate, float) and not sample_rate.is_integer():
            return False, 0.0, 0, 0.0, "sample_rate must be an integer Hz value"
        rate_i = int(sample_rate)
    except (TypeError, ValueError):
        return False, 0.0, 0, 0.0, "sample_rate must be an integer"

    if rate_i in _COMMON_RATES:
        pass
    elif _MIN_RATE <= rate_i <= _MAX_RATE:
        pass
    else:
        return (
            False,
            0.0,
            0,
            0.0,
            f"sample_rate must be between {_MIN_RATE} and {_MAX_RATE} Hz",
        )

    ok_g, gain_or_err = _as_finite_float(volume_gain_multiplier, "volume_gain_multiplier")
    if not ok_g:
        return False, 0.0, 0, 0.0, str(gain_or_err)
    gain_f = float(gain_or_err)
    if gain_f <= 0.0 or gain_f > _MAX_GAIN:
        return (
            False,
            0.0,
            0,
            0.0,
            f"volume_gain_multiplier must be in (0, {_MAX_GAIN:g}]",
        )

    return True, duration_f, rate_i, gain_f, ""
