#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok / contributors (chat role allowlist)
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
# Fail-closed allowlist for OpenAI chat history message roles.

"""Allowlist chat-history message roles before append / OpenAI replay."""

from __future__ import annotations

ALLOWED_CHAT_ROLES = frozenset(
    {
        "system",
        "user",
        "assistant",
        "function",
        "tool",
    }
)


def sanitize_chat_role(role):
    """
    Return a normalized role string, or None if not allowlisted.

    - None / bool / non-str → None
    - strip + casefold to lower
    - empty → None
    - must be in ALLOWED_CHAT_ROLES
    """
    if role is None or isinstance(role, bool) or not isinstance(role, str):
        return None
    cleaned = role.strip().lower()
    if not cleaned:
        return None
    if cleaned not in ALLOWED_CHAT_ROLES:
        return None
    return cleaned
