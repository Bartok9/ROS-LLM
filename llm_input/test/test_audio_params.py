# -*- coding: utf-8 -*-
# flake8: noqa

import os
import sys
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from llm_input.audio_params import sanitize_recording_params  # noqa: E402


class TestSanitizeRecordingParams(unittest.TestCase):
    def test_ok_defaults(self):
        ok, d, sr, g, err = sanitize_recording_params(5, 16000, 1)
        self.assertTrue(ok)
        self.assertEqual(d, 5.0)
        self.assertEqual(sr, 16000)
        self.assertEqual(g, 1.0)
        self.assertEqual(err, "")

    def test_reject_zero_duration(self):
        ok, *_rest = sanitize_recording_params(0, 16000, 1)
        self.assertFalse(ok)

    def test_reject_huge_duration(self):
        ok, *_rest = sanitize_recording_params(3600, 16000, 1)
        self.assertFalse(ok)

    def test_reject_nan_duration(self):
        ok, *_rest = sanitize_recording_params(float("nan"), 16000, 1)
        self.assertFalse(ok)

    def test_reject_low_sample_rate(self):
        ok, *_rest = sanitize_recording_params(5, 100, 1)
        self.assertFalse(ok)

    def test_reject_bool_sample_rate(self):
        ok, *_rest = sanitize_recording_params(5, True, 1)
        self.assertFalse(ok)

    def test_reject_gain_zero(self):
        ok, *_rest = sanitize_recording_params(5, 16000, 0)
        self.assertFalse(ok)

    def test_reject_gain_high(self):
        ok, *_rest = sanitize_recording_params(5, 16000, 50)
        self.assertFalse(ok)

    def test_ok_upper_bounds(self):
        ok, d, sr, g, err = sanitize_recording_params(60, 48000, 10)
        self.assertTrue(ok)
        self.assertEqual((d, sr, g), (60.0, 48000, 10.0))


if __name__ == "__main__":
    unittest.main()
