#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline tests for UserConfig OPENAI_API_KEY normalization."""

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

# package lives at llm_config/llm_config
_ROOT = Path(__file__).resolve().parents[1]
_PKG_PARENT = _ROOT  # contains package dir llm_config/
if str(_PKG_PARENT) not in sys.path:
    sys.path.insert(0, str(_PKG_PARENT))


class TestUserConfigApiKey(unittest.TestCase):
    def test_missing_env(self):
        from llm_config.user_config import UserConfig

        def fake_getenv(k, default=None):
            if k == "OPENAI_API_KEY":
                return None
            return os.environ.get(k, default)

        with mock.patch.object(os, "getenv", side_effect=fake_getenv):
            cfg = UserConfig()
        self.assertIsNone(cfg.openai_api_key)

    def test_whitespace_only(self):
        from llm_config.user_config import UserConfig

        def fake_getenv(k, default=None):
            if k == "OPENAI_API_KEY":
                return "   "
            return os.environ.get(k, default)

        with mock.patch.object(os, "getenv", side_effect=fake_getenv):
            cfg = UserConfig()
        self.assertIsNone(cfg.openai_api_key)

    def test_valid_key(self):
        from llm_config.user_config import UserConfig

        def fake_getenv(k, default=None):
            if k == "OPENAI_API_KEY":
                return "sk-test"
            return os.environ.get(k, default)

        with mock.patch.object(os, "getenv", side_effect=fake_getenv):
            cfg = UserConfig()
        self.assertEqual(cfg.openai_api_key, "sk-test")


if __name__ == "__main__":
    unittest.main()
