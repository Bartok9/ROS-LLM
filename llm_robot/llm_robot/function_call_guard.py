# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok / contributors (allowlist helper)
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
# Fail-closed allowlist for LLM-chosen function names before getattr.

from __future__ import annotations

from typing import Dict, FrozenSet, Set, Tuple

# Methods the LLM may invoke via ChatGPT function-call JSON "name"
ALLOWED_FUNCTIONS: Dict[str, FrozenSet[str]] = {
    "multi": frozenset({"publish_cmd_vel", "call_service"}),
    "turtle": frozenset({"publish_cmd_vel", "reset_turtlesim"}),
    "arm": frozenset({"publish_target_pose"}),
}


def resolve_function(
    robot_kind: str, function_name: object
) -> Tuple[bool, str]:
    """
    Return (True, name) if function_name is an allowed action for robot_kind.
    Otherwise (False, error_message).
    """
    if robot_kind not in ALLOWED_FUNCTIONS:
        return False, f"unknown robot_kind for function allowlist: {robot_kind!r}"

    if function_name is None:
        return False, "function name is required"

    if not isinstance(function_name, str):
        return False, "function name must be a string"

    name = function_name.strip()
    if not name:
        return False, "function name is empty"

    # Path/self-injection / attribute walk
    if any(ch in name for ch in (".", "/", "\\", " ", "\t", "\n", "\r")):
        return False, f"invalid function name: {function_name!r}"

    if name.startswith("_"):
        return False, f"function name not allowed: {name!r}"

    allowed: Set[str] = set(ALLOWED_FUNCTIONS[robot_kind])
    if name not in allowed:
        return False, f"function not in allowlist: {name!r}"

    return True, name
