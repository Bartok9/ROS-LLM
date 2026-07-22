#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok / contributors (AWS region + S3 bucket sanitize)
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
# Fail-closed sanitizers for AWS region ids and S3 bucket names (pure/offline).

"""Sanitize AWS region and S3 bucket names before boto3/S3 URI construction."""

from __future__ import annotations

import re

# Standard AWS region shape: us-east-1, ap-southeast-1, eu-central-1, etc.
_REGION_RE = re.compile(r"^[a-z]{2}(?:-[a-z]+)+-\d+$")

# DNS-style S3 bucket subset (AWS rules tightened for safety).
_BUCKET_RE = re.compile(r"^[a-z0-9][a-z0-9.\-]{1,61}[a-z0-9]$")


def sanitize_aws_region(raw):
    """
    Return a normalized AWS region id, or None if invalid.

    Accepts lowercase region strings matching the common AWS pattern
    (e.g. ``us-east-1``, ``ap-southeast-1``). Rejects None/bool/non-str,
    empty/whitespace, path fragments, and non-region garbage.
    """
    if raw is None or isinstance(raw, bool) or not isinstance(raw, str):
        return None
    text = raw.strip()
    if not text:
        return None
    if ".." in text or "/" in text or "\\" in text or " " in text:
        return None
    if any(ord(ch) < 32 for ch in text):
        return None
    # Force lowercase compare; reject mixed case by requiring exact lower
    if text != text.lower():
        return None
    if not _REGION_RE.match(text):
        return None
    # Bound length (AWS regions are short)
    if len(text) > 32:
        return None
    return text


def sanitize_s3_bucket_name(raw):
    """
    Return a safe S3 bucket name, or None if invalid.

    Applies a strict DNS-compatible subset of AWS bucket naming:
    3–63 chars, lowercase letters/digits/hyphen/dot, start/end alnum,
    no adjacent periods, no ``.-`` / ``-.`` pairs, no IP-looking 4-octet forms.
    """
    if raw is None or isinstance(raw, bool) or not isinstance(raw, str):
        return None
    text = raw.strip()
    if not text:
        return None
    if ".." in text or "/" in text or "\\" in text or " " in text:
        return None
    if any(ord(ch) < 32 for ch in text):
        return None
    if text != text.lower():
        return None
    if len(text) < 3 or len(text) > 63:
        return None
    if not _BUCKET_RE.match(text):
        return None
    if ".-" in text or "-." in text:
        return None
    # Reject IPv4-shaped names (AWS disallows)
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", text):
        return None
    return text
