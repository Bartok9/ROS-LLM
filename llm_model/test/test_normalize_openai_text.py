#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1] / "llm_model"
sys.path.insert(0, str(PKG))

from text_content import normalize_openai_text  # noqa: E402


class TestNormalizeOpenAIText(unittest.TestCase):
    def test_none(self):
        self.assertEqual(normalize_openai_text(None), "")

    def test_str_passthrough(self):
        self.assertEqual(normalize_openai_text("hello"), "hello")

    def test_empty_str(self):
        self.assertEqual(normalize_openai_text(""), "")

    def test_bytes(self):
        self.assertEqual(normalize_openai_text(b"hi"), "hi")

    def test_int(self):
        self.assertEqual(normalize_openai_text(42), "42")


if __name__ == "__main__":
    unittest.main()
