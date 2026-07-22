#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline tests for OpenAI sampling clamps in user_config."""
import math
import unittest
import sys
import os
import types
import importlib.util

_PKG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_LLM_CFG = os.path.join(_PKG_DIR, "llm_config")

pkg = types.ModuleType("llm_config")
pkg.__path__ = [_LLM_CFG]
sys.modules["llm_config"] = pkg
rb_mod = types.ModuleType("llm_config.robot_behavior")

class RobotBehavior:
    robot_functions_list = []

rb_mod.RobotBehavior = RobotBehavior
sys.modules["llm_config.robot_behavior"] = rb_mod
spec = importlib.util.spec_from_file_location(
    "llm_config.user_config",
    os.path.join(_LLM_CFG, "user_config.py"),
    submodule_search_locations=[_LLM_CFG],
)
uc = importlib.util.module_from_spec(spec)
sys.modules["llm_config.user_config"] = uc
spec.loader.exec_module(uc)


class TestOpenAISamplingClamps(unittest.TestCase):
    def test_temperature(self):
        self.assertEqual(uc.clamp_openai_temperature(1), 1.0)
        self.assertEqual(uc.clamp_openai_temperature(-1), 0.0)
        self.assertEqual(uc.clamp_openai_temperature(9), 2.0)
        self.assertEqual(uc.clamp_openai_temperature(float("nan")), 1.0)
        self.assertEqual(uc.clamp_openai_temperature("x"), 1.0)

    def test_top_p(self):
        self.assertEqual(uc.clamp_openai_top_p(0.5), 0.5)
        self.assertEqual(uc.clamp_openai_top_p(0), 1.0)
        self.assertEqual(uc.clamp_openai_top_p(2), 1.0)
        self.assertTrue(math.isfinite(uc.clamp_openai_top_p(float("inf"))))

    def test_n_and_tokens(self):
        self.assertEqual(uc.clamp_openai_n(3), 3)
        self.assertEqual(uc.clamp_openai_n(0), 1)
        self.assertEqual(uc.clamp_openai_n(100), 16)
        self.assertEqual(uc.clamp_openai_max_tokens(100), 100)
        self.assertEqual(uc.clamp_openai_max_tokens(0), 1)
        self.assertEqual(uc.clamp_openai_max_tokens(999999), 128000)

    def test_penalties_and_history(self):
        self.assertEqual(uc.clamp_openai_penalty(0), 0.0)
        self.assertEqual(uc.clamp_openai_penalty(-5), -2.0)
        self.assertEqual(uc.clamp_openai_penalty(5), 2.0)
        self.assertEqual(uc.clamp_chat_history_max_length(10), 10)
        self.assertEqual(uc.clamp_chat_history_max_length(0), 1)
        self.assertEqual(uc.clamp_chat_history_max_length(10**9), 100000)


if __name__ == "__main__":
    unittest.main()
