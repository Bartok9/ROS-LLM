# -*- coding: utf-8 -*-
"""Resolve and unlink demo temp audio paths under /tmp only."""

from __future__ import annotations

import os
from typing import Optional

DEFAULT_TMP_AUDIO = "/tmp/user_audio_input.flac"
_ALLOWED_SUFFIXES = (".flac", ".wav")
_MAX_PATH_LEN = 180


def resolve_tmp_audio_path(path: Optional[str] = None) -> str:
    """
    Return a sanitized absolute path under /tmp for temp audio.

    Falls back to DEFAULT_TMP_AUDIO when input is missing or unsafe.
    """
    candidate = DEFAULT_TMP_AUDIO if path is None else str(path).strip()
    if not candidate:
        candidate = DEFAULT_TMP_AUDIO
    if len(candidate) > _MAX_PATH_LEN:
        return os.path.realpath(DEFAULT_TMP_AUDIO)
    # No null bytes or obvious path tricks before resolve
    if "\x00" in candidate or ".." in candidate.split(os.sep):
        return os.path.realpath(DEFAULT_TMP_AUDIO)
    expanded = os.path.expanduser(candidate)
    # Prefer absolute; if relative, join under /tmp basename only
    if not os.path.isabs(expanded):
        expanded = os.path.join("/tmp", os.path.basename(expanded))
    real = os.path.realpath(expanded)
    tmp_root = os.path.realpath("/tmp")
    if real != tmp_root and not real.startswith(tmp_root + os.sep):
        return os.path.realpath(DEFAULT_TMP_AUDIO)
    lower = real.lower()
    if not lower.endswith(_ALLOWED_SUFFIXES):
        return os.path.realpath(DEFAULT_TMP_AUDIO)
    base = os.path.basename(real)
    if not base or base in (".", ".."):
        return os.path.realpath(DEFAULT_TMP_AUDIO)
    return real


def safe_unlink(path: Optional[str]) -> bool:
    """Unlink path only if it resolves as an allowed tmp audio path."""
    if path is None:
        return False
    try:
        resolved = resolve_tmp_audio_path(path)
    except Exception:
        return False
    # Only unlink if caller path canonicalizes to the same allowed target
    try:
        caller_real = os.path.realpath(os.path.expanduser(str(path)))
    except Exception:
        return False
    if caller_real != resolved:
        # Still allow unlink of default if resolve remapped unsafe → default
        # but never unlink a path that is not under /tmp with audio suffix
        tmp_root = os.path.realpath("/tmp")
        if not (
            caller_real.startswith(tmp_root + os.sep)
            and caller_real.lower().endswith(_ALLOWED_SUFFIXES)
        ):
            return False
        target = caller_real
    else:
        target = resolved
    try:
        os.unlink(target)
        return True
    except FileNotFoundError:
        return True
    except OSError:
        return False
