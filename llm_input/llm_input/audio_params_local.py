"""Bounded recording parameters for local Whisper ASR path."""
from __future__ import annotations

import math
from typing import Tuple


def _finite_number(value, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a number") from exc
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def clamp_local_recording_params(
    duration,
    sample_rate,
    volume_gain_multiplier,
    *,
    min_duration: float = 0.1,
    max_duration: float = 60.0,
    min_sample_rate: int = 8000,
    max_sample_rate: int = 48000,
    min_gain: float = 0.0,
    max_gain: float = 10.0,
) -> Tuple[float, int, float]:
    """
    Fail-closed bounds for sounddevice buffer allocation on the local ASR path.

    Returns (duration_s, sample_rate_hz, gain).
    """
    duration_f = _finite_number(duration, "duration")
    if duration_f < min_duration or duration_f > max_duration:
        raise ValueError(
            f"duration must be in [{min_duration}, {max_duration}] seconds"
        )

    rate_f = _finite_number(sample_rate, "sample_rate")
    rate_i = int(round(rate_f))
    if rate_i < min_sample_rate or rate_i > max_sample_rate:
        raise ValueError(
            f"sample_rate must be in [{min_sample_rate}, {max_sample_rate}] Hz"
        )

    gain_f = _finite_number(volume_gain_multiplier, "volume_gain_multiplier")
    if gain_f < min_gain or gain_f > max_gain:
        raise ValueError(
            f"volume_gain_multiplier must be in [{min_gain}, {max_gain}]"
        )

    return duration_f, rate_i, gain_f
