# -*- coding: utf-8 -*-
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from llm_input.transcribe_poll import (  # noqa: E402
    ABS_MAX_WAIT_SEC,
    DEFAULT_MAX_WAIT_SEC,
    MIN_WAIT_SEC,
    clamp_transcribe_wait_sec,
    should_stop_poll,
)


class TestTranscribePoll(unittest.TestCase):
    def test_default_none(self):
        self.assertEqual(clamp_transcribe_wait_sec(None), DEFAULT_MAX_WAIT_SEC)

    def test_clamp_high(self):
        self.assertEqual(clamp_transcribe_wait_sec(9999), ABS_MAX_WAIT_SEC)

    def test_clamp_low(self):
        self.assertEqual(clamp_transcribe_wait_sec(0), MIN_WAIT_SEC)

    def test_bad_value(self):
        self.assertEqual(clamp_transcribe_wait_sec("nope"), DEFAULT_MAX_WAIT_SEC)
        self.assertEqual(clamp_transcribe_wait_sec(float("nan")), DEFAULT_MAX_WAIT_SEC)

    def test_should_stop(self):
        self.assertFalse(should_stop_poll(10, 60))
        self.assertTrue(should_stop_poll(60, 60))
        self.assertTrue(should_stop_poll(61, 60))
        self.assertTrue(should_stop_poll("x", 60))


if __name__ == "__main__":
    unittest.main()
