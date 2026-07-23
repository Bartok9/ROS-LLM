#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2026 Bartok / contributors
# Licensed under the Apache License, Version 2.0

import unittest

from llm_input.transcript_sanitize import (
    DEFAULT_MAX_CHARS,
    sanitize_transcript_text,
)


class TestTranscriptSanitize(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(sanitize_transcript_text("Hello"), "Hello")
        self.assertEqual(sanitize_transcript_text("  hi  "), "hi")
        self.assertEqual(sanitize_transcript_text("a\nb\tc"), "a\nb\tc")

    def test_empty(self):
        self.assertIsNone(sanitize_transcript_text(""))
        self.assertIsNone(sanitize_transcript_text("   "))
        self.assertIsNone(sanitize_transcript_text(None))

    def test_types(self):
        self.assertIsNone(sanitize_transcript_text(True))
        self.assertIsNone(sanitize_transcript_text(False))
        self.assertIsNone(sanitize_transcript_text(12))

    def test_controls(self):
        self.assertIsNone(sanitize_transcript_text("\x00\x01\x02"))
        self.assertEqual(sanitize_transcript_text("a\x00b"), "ab")

    def test_truncate(self):
        long = "a" * 5000
        out = sanitize_transcript_text(long)
        self.assertEqual(len(out), DEFAULT_MAX_CHARS)
        self.assertEqual(len(sanitize_transcript_text(long, max_chars=10)), 10)

    def test_bad_limit_falls_back(self):
        s = "x" * (DEFAULT_MAX_CHARS + 5)
        out = sanitize_transcript_text(s, max_chars=0)
        self.assertEqual(len(out), DEFAULT_MAX_CHARS)
        out2 = sanitize_transcript_text(s, max_chars=True)
        self.assertEqual(len(out2), DEFAULT_MAX_CHARS)
        out3 = sanitize_transcript_text(s, max_chars="nope")
        self.assertEqual(len(out3), DEFAULT_MAX_CHARS)


if __name__ == "__main__":
    unittest.main()
