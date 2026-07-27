# -*- coding: utf-8 -*-
"""Bounds AWS Transcribe job polling so a stuck job cannot hang the node forever."""

DEFAULT_MAX_WAIT_SEC = 60.0
ABS_MAX_WAIT_SEC = 300.0
MIN_WAIT_SEC = 1.0


def clamp_transcribe_wait_sec(value, default=DEFAULT_MAX_WAIT_SEC):
    """Return a finite poll budget in seconds within [MIN_WAIT_SEC, ABS_MAX_WAIT_SEC]."""
    if value is None:
        raw = default
    else:
        try:
            raw = float(value)
        except (TypeError, ValueError):
            raw = default
    if raw != raw:  # NaN
        raw = default
    if raw < MIN_WAIT_SEC:
        return MIN_WAIT_SEC
    if raw > ABS_MAX_WAIT_SEC:
        return ABS_MAX_WAIT_SEC
    return raw


def should_stop_poll(elapsed_sec, max_wait_sec):
    """True when polling must stop because the wait budget is exhausted."""
    try:
        elapsed = float(elapsed_sec)
        budget = float(max_wait_sec)
    except (TypeError, ValueError):
        return True
    if elapsed != elapsed or budget != budget:
        return True
    return elapsed >= budget
