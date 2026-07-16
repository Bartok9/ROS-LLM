#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok9 (Aerial OSS campaign)
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
# Fail-closed robot_name for cmd_vel topic construction from LLM args.

from __future__ import annotations

import re
from typing import Optional, Tuple

# Empty string is allowed (maps to /cmd_vel). Non-empty: single ROS graph token.
_ROBOT = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,63}$")


def sanitize_robot_name(name: object) -> Tuple[bool, Optional[str], str]:
    """
    Returns (ok, sanitized_or_None, error_or_empty).
    empty / None-like → ok with "" (default robot).
    """
    if name is None:
        return True, "", ""
    if not isinstance(name, str):
        return False, None, "invalid robot_name"
    if name == "":
        return True, "", ""
    if name.strip() == "" and name != "":
        return False, None, "invalid robot_name"
    if any(c.isspace() or c in "/;|&$`\\\"'<>." for c in name):
        return False, None, "invalid robot_name"
    if not _ROBOT.match(name):
        return False, None, "invalid robot_name"
    return True, name, ""
