#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from llm_output.feedback_text import sanitize_feedback_text, DEFAULT_MAX_CHARS


class TestFeedbackText(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(sanitize_feedback_text("  hello  "), "hello")

    def test_empty(self):
        self.assertIsNone(sanitize_feedback_text(""))
        self.assertIsNone(sanitize_feedback_text("   "))
        self.assertIsNone(sanitize_feedback_text(None))

    def test_types(self):
        self.assertIsNone(sanitize_feedback_text(True))
        self.assertIsNone(sanitize_feedback_text(12))

    def test_truncate(self):
        long = "a" * 50
        self.assertEqual(len(sanitize_feedback_text(long, max_chars=10)), 10)

    def test_bad_limit_falls_back(self):
        s = "x" * (DEFAULT_MAX_CHARS + 5)
        out = sanitize_feedback_text(s, max_chars=0)
        self.assertEqual(len(out), DEFAULT_MAX_CHARS)


if __name__ == "__main__":
    unittest.main()
