# -*- coding: utf-8 -*-
"""Helpers for best-effort AWS Transcribe job cleanup."""

from __future__ import annotations

import re
from typing import Optional

_JOB_NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,200}$")
_DELETE_STATUSES = frozenset({"COMPLETED", "FAILED"})


def sanitize_transcribe_job_name(name: Optional[str]) -> Optional[str]:
    """Return job name if safe for delete_transcription_job; else None."""
    if name is None:
        return None
    if not isinstance(name, str):
        return None
    stripped = name.strip()
    if not stripped or not _JOB_NAME_RE.match(stripped):
        return None
    if ".." in stripped or "/" in stripped or "\\" in stripped:
        return None
    return stripped


def should_attempt_job_delete(status: Optional[str]) -> bool:
    """True when the Transcribe job is in a terminal state worth deleting."""
    if not isinstance(status, str):
        return False
    return status.strip().upper() in _DELETE_STATUSES
