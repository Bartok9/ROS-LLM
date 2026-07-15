#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2023 Herman Ye @Auromix (package); sanitize helper 2026 contrib
# Licensed under the Apache License, Version 2.0
"""Sanitize LLM-supplied cmd_vel scalars for ROS-LLM demos."""

from __future__ import annotations

import math
from typing import Any


DEFAULT_MAX_ABS = 2.0
DEFAULT_MAX_DURATION = 30.0


def sanitize_cmd_vel_float(
    value: Any,
    name: str,
    *,
    max_abs: float = DEFAULT_MAX_ABS,
) -> float:
    """Coerce to float; reject non-finite; clamp to [-max_abs, max_abs]."""
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"cmd_vel field {name!r} must be a number, got {value!r}"
        ) from exc
    if not math.isfinite(number):
        raise ValueError(f"cmd_vel field {name!r} must be finite, got {number!r}")
    if max_abs < 0:
        raise ValueError("max_abs must be non-negative")
    if number > max_abs:
        return float(max_abs)
    if number < -max_abs:
        return float(-max_abs)
    return number


def sanitize_duration(
    value: Any,
    *,
    max_sec: float = DEFAULT_MAX_DURATION,
    default: float = 0.0,
) -> float:
    """Coerce duration seconds; non-finite/negative → default; clamp to max_sec."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return float(default)
    if not math.isfinite(number) or number < 0:
        return float(default)
    if max_sec < 0:
        raise ValueError("max_sec must be non-negative")
    if number > max_sec:
        return float(max_sec)
    return number
