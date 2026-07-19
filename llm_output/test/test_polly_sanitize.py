#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline tests for Polly TTS sanitizers."""

import unittest

from llm_output.polly_sanitize import (
    sanitize_feedback_text,
    sanitize_polly_voice_id,
)


class TestPollySanitize(unittest.TestCase):
    def test_voice_allowlist(self):
        self.assertEqual(sanitize_polly_voice_id("Ivy"), "Ivy")
        self.assertEqual(sanitize_polly_voice_id("Zhiyu"), "Zhiyu")
        self.assertEqual(sanitize_polly_voice_id("not-a-voice"), "Ivy")
        self.assertEqual(sanitize_polly_voice_id("../etc"), "Ivy")
        self.assertEqual(sanitize_polly_voice_id("Ivy; rm -rf"), "Ivy")
        self.assertEqual(sanitize_polly_voice_id(None, default="Matthew"), "Matthew")
        self.assertEqual(sanitize_polly_voice_id("  Joanna  "), "Joanna")

    def test_feedback_text(self):
        ok, t = sanitize_feedback_text("Hello robot")
        self.assertTrue(ok)
        self.assertEqual(t, "Hello robot")
        ok, err = sanitize_feedback_text("   ")
        self.assertFalse(ok)
        self.assertEqual(err, "empty_feedback")
        ok, t = sanitize_feedback_text("x" * 5000, max_len=10)
        self.assertTrue(ok)
        self.assertEqual(len(t), 10)
        ok, t = sanitize_feedback_text("a\x00b")
        self.assertTrue(ok)
        self.assertEqual(t, "ab")


if __name__ == "__main__":
    unittest.main()
