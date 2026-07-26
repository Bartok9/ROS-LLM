"""Clamp OpenAI client request timeout for ROS-LLM model node."""
from __future__ import annotations

import math


def clamp_openai_request_timeout(
    value,
    *,
    default: float = 30.0,
    minimum: float = 1.0,
    maximum: float = 120.0,
) -> float:
    """Return a finite request timeout in seconds within [minimum, maximum]."""
    if value is None:
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    if number < minimum:
        return minimum
    if number > maximum:
        return maximum
    return number
