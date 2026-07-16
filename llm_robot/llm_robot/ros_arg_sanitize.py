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
# Fail-closed validators for ros2 service call argv pieces from LLM function args.

from __future__ import annotations

import re
from typing import Tuple, Union

# Optional leading slash; one or more [A-Za-z0-9_]+ segments joined by /
_ROS_NAME = re.compile(r"^/?[A-Za-z][A-Za-z0-9_]*(?:/[A-Za-z][A-Za-z0-9_]*)*$")
# package/Type or package/srv/Type style (1–3 slash segments after package)
_ROS_TYPE = re.compile(
    r"^[A-Za-z][A-Za-z0-9_]*(?:/[A-Za-z][A-Za-z0-9_]*){1,3}$"
)


def is_valid_ros_name(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if any(c.isspace() or c in ";|&$`\\\"'<>" for c in value):
        return False
    return bool(_ROS_NAME.match(value))


def is_valid_ros_type(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if any(c.isspace() or c in ";|&$`\\\"'<>" for c in value):
        return False
    return bool(_ROS_TYPE.match(value))


def sanitize_service_call_args(
    service_name: object, service_type: object
) -> Tuple[bool, str, str]:
    """
    Returns (ok, name_or_err, type_or_err).
    When ok is False, second element is the error message.
    """
    if not is_valid_ros_name(service_name):
        return False, "invalid service_name", ""
    if not is_valid_ros_type(service_type):
        return False, "invalid service_type", ""
    return True, str(service_name), str(service_type)
