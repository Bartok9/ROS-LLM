#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2023 Herman Ye @Auromix (package); sanitize helper 2026 contrib
# Licensed under the Apache License, Version 2.0
"""Sanitize LLM-supplied target pose for arx5 arm demo (workspace soft limits)."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Mapping


# Soft demo workspace clamps (meters / radians) — not a substitute for real FK limits.
DEFAULT_MAX_ABS_XYZ = 2.0
DEFAULT_MAX_ABS_RPY = math.pi


def sanitize_pose_component(
    value: Any,
    name: str,
    *,
    default: float,
    max_abs: float,
) -> float:
    """Coerce to finite float; clamp to [-max_abs, max_abs]; bad type → default then clamp."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = float(default)
    if not math.isfinite(number):
        number = float(default)
    if max_abs < 0:
        raise ValueError("max_abs must be non-negative")
    if number > max_abs:
        return float(max_abs)
    if number < -max_abs:
        return float(-max_abs)
    return number


def sanitize_target_pose(
    kwargs: Mapping[str, Any],
    *,
    max_abs_xyz: float = DEFAULT_MAX_ABS_XYZ,
    max_abs_rpy: float = DEFAULT_MAX_ABS_RPY,
) -> List[float]:
    """Return [x, y, z, roll, pitch, yaw] sanitized from kwargs."""
    defaults = {
        "x": 0.2,
        "y": 0.2,
        "z": 0.2,
        "roll": 0.2,
        "pitch": 0.2,
        "yaw": 0.2,
    }
    out: List[float] = []
    for key in ("x", "y", "z"):
        out.append(
            sanitize_pose_component(
                kwargs.get(key, defaults[key]),
                key,
                default=defaults[key],
                max_abs=max_abs_xyz,
            )
        )
    for key in ("roll", "pitch", "yaw"):
        out.append(
            sanitize_pose_component(
                kwargs.get(key, defaults[key]),
                key,
                default=defaults[key],
                max_abs=max_abs_rpy,
            )
        )
    return out
