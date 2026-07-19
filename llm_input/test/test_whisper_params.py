#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline tests for Whisper model/language sanitizers."""

import unittest

from llm_input.whisper_params import (
    sanitize_whisper_language,
    sanitize_whisper_model_size,
)


class TestWhisperParams(unittest.TestCase):
    def test_model_size(self):
        self.assertEqual(sanitize_whisper_model_size("medium"), "medium")
        self.assertEqual(sanitize_whisper_model_size("LARGE-V3"), "large-v3")
        self.assertEqual(sanitize_whisper_model_size("turbo"), "base")
        self.assertEqual(sanitize_whisper_model_size("../x"), "base")
        self.assertEqual(sanitize_whisper_model_size(None, default="small"), "small")
        self.assertEqual(sanitize_whisper_model_size("  Base  "), "base")

    def test_language(self):
        self.assertEqual(sanitize_whisper_language("en"), "en")
        self.assertEqual(sanitize_whisper_language("EN-US"), "en-us")
        self.assertEqual(sanitize_whisper_language("zh"), "zh")
        self.assertEqual(sanitize_whisper_language("auto"), "auto")
        self.assertEqual(sanitize_whisper_language("english"), "en")
        self.assertEqual(sanitize_whisper_language("en;rm"), "en")
        self.assertEqual(sanitize_whisper_language(None, default="zh"), "zh")


if __name__ == "__main__":
    unittest.main()
