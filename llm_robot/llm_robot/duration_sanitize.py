# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok / contributors (duration helper)
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
# Fail-closed / clamped duration for LLM cmd_vel publish loops.

from __future__ import annotations

import math
from typing import Union

Number = Union[int, float]

DEFAULT_MAX_DURATION_SEC = 30.0


def sanitize_duration(
    value: object, max_sec: float = DEFAULT_MAX_DURATION_SEC
) -> float:
    """
    Return a non-negative duration in seconds, clamped to [0, max_sec].

    Raises ValueError for non-numeric / non-finite / bool inputs.
    """
    if isinstance(value, bool) or value is None:
        raise ValueError(f"duration must be a number, got {value!r}")
    try:
        duration = float(value)
    except (TypeError, ValueError) as err:
        raise ValueError(f"duration must be numeric: {value!r}") from err
    if not math.isfinite(duration):
        raise ValueError(f"duration must be finite: {value!r}")
    if duration < 0:
        raise ValueError(f"duration must be >= 0: {duration}")
    if max_sec < 0 or not math.isfinite(max_sec):
        raise ValueError(f"max_sec must be a finite non-negative number: {max_sec!r}")
    if duration > max_sec:
        return float(max_sec)
    return float(duration)
