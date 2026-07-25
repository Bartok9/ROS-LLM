# -*- coding: utf-8 -*-
"""Timeout helpers for multi_robot ros2 service call subprocesses."""

from __future__ import annotations

import subprocess
from typing import List, Sequence, Union

DEFAULT_TIMEOUT_SEC = 15.0
MIN_TIMEOUT_SEC = 1.0
MAX_TIMEOUT_SEC = 60.0


def clamp_timeout(value: object, default: float = DEFAULT_TIMEOUT_SEC) -> float:
    """Clamp optional timeout to [MIN, MAX]; invalid → default."""
    try:
        if value is None:
            return float(default)
        t = float(value)
    except (TypeError, ValueError):
        return float(default)
    if t != t:  # NaN
        return float(default)
    if t < MIN_TIMEOUT_SEC:
        return MIN_TIMEOUT_SEC
    if t > MAX_TIMEOUT_SEC:
        return MAX_TIMEOUT_SEC
    return t


def run_ros2_service_call(
    command: Sequence[str], timeout_sec: float = DEFAULT_TIMEOUT_SEC
) -> str:
    """Run argv list with timeout; never shell=True. Return stdout/stderr text."""
    try:
        out = subprocess.check_output(
            list(command),
            stderr=subprocess.STDOUT,
            timeout=float(timeout_sec),
        )
        return out.decode("utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return f"error: ros2 service call timed out after {timeout_sec}s"
    except subprocess.CalledProcessError as command_error:
        raw = command_error.output or b""
        return raw.decode("utf-8", errors="replace")
    except OSError as e:
        return f"error: failed to run ros2 service call: {e}"
