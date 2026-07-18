# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok / contributors (function_call payload sanitize)
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
# Fail-closed sanitizer for OpenAI-style function_call objects before ROS RPC.

from __future__ import annotations

import json
from typing import Any, Dict, Tuple, Union

_Ok = bool
_Normalized = Dict[str, str]
_Err = str


def _get_field(obj: Any, key: str) -> Any:
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(key)
    # openai SDK objects often support mapping-style or attribute access
    try:
        if hasattr(obj, "get"):
            return obj.get(key)
    except Exception:
        pass
    return getattr(obj, key, None)


def sanitize_function_call(obj: Any) -> Tuple[_Ok, Union[_Normalized, _Err]]:
    """
    Validate and normalize a ChatCompletions function_call payload.

    Returns (True, {"name": str, "arguments": str}) where arguments is a JSON object
    string, or (False, error_message).
    """
    if obj is None:
        return False, "function_call is required"

    name_raw = _get_field(obj, "name")
    if name_raw is None:
        return False, "function_call.name is required"
    if not isinstance(name_raw, str):
        return False, "function_call.name must be a string"

    name = name_raw.strip()
    if not name:
        return False, "function_call.name is empty"

    if any(ch in name for ch in (".", "/", "\\", " ", "\t", "\n", "\r")):
        return False, f"invalid function_call.name: {name_raw!r}"

    if name.startswith("_"):
        return False, f"function_call.name not allowed: {name!r}"

    args_raw = _get_field(obj, "arguments")
    if args_raw is None:
        args_str = "{}"
    elif isinstance(args_raw, dict):
        try:
            args_str = json.dumps(args_raw)
        except (TypeError, ValueError) as err:
            return False, f"function_call.arguments not JSON-serializable: {err}"
    elif isinstance(args_raw, str):
        text = args_raw.strip()
        if not text:
            args_str = "{}"
        else:
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError as err:
                return False, f"function_call.arguments is not valid JSON: {err}"
            if not isinstance(parsed, dict):
                return False, "function_call.arguments JSON must be an object"
            args_str = json.dumps(parsed)
    else:
        return False, "function_call.arguments must be a string or object"

    return True, {"name": name, "arguments": args_str}
