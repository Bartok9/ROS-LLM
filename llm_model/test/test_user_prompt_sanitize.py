#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from llm_model.user_prompt_sanitize import (
    DEFAULT_MAX_CHARS,
    sanitize_user_prompt,
)


class TestUserPromptSanitize(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(sanitize_user_prompt("Hello"), "Hello")
        self.assertEqual(sanitize_user_prompt("  hi  "), "hi")
        self.assertEqual(
            sanitize_user_prompt("line1\nline2"), "line1\nline2"
        )

    def test_reject_empty_and_types(self):
        self.assertIsNone(sanitize_user_prompt(""))
        self.assertIsNone(sanitize_user_prompt("   "))
        self.assertIsNone(sanitize_user_prompt(None))
        self.assertIsNone(sanitize_user_prompt(True))
        self.assertIsNone(sanitize_user_prompt(12))
        self.assertIsNone(sanitize_user_prompt("\x00\x01"))

    def test_truncate(self):
        long_text = "a" * 9000
        out = sanitize_user_prompt(long_text)
        self.assertEqual(len(out), DEFAULT_MAX_CHARS)
        self.assertEqual(sanitize_user_prompt("abcdef", max_chars=3), "abc")

    def test_bad_max_chars(self):
        self.assertEqual(sanitize_user_prompt("hello", max_chars=0), "hello")
        self.assertEqual(sanitize_user_prompt("hello", max_chars=-5), "hello")
        self.assertEqual(sanitize_user_prompt("hello", max_chars="nope"), "hello")
        self.assertEqual(sanitize_user_prompt("hello", max_chars=True), "hello")


if __name__ == "__main__":
    unittest.main()
