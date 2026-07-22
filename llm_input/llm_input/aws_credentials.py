#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
# Copyright 2026 Bartok / contributors (AWS credential fail-closed, input)
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

"""AWS credential validation helpers for audio input (pure, testable offline)."""


def aws_credentials_ok(access_key_id, secret_access_key) -> bool:
    """Return True only when both AWS IAM credentials are non-empty strings."""
    if not isinstance(access_key_id, str) or not isinstance(secret_access_key, str):
        return False
    if not access_key_id.strip() or not secret_access_key.strip():
        return False
    return True
