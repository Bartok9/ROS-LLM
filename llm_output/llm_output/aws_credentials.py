#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AWS credential validation helpers (pure, testable offline)."""


def aws_credentials_ok(access_key_id, secret_access_key) -> bool:
    """Return True only when both AWS IAM credentials are non-empty strings."""
    if not isinstance(access_key_id, str) or not isinstance(secret_access_key, str):
        return False
    if not access_key_id.strip() or not secret_access_key.strip():
        return False
    return True
