# -*- coding: utf-8 -*-
import unittest

from llm_robot.duration_sanitize import sanitize_duration, DEFAULT_MAX_DURATION_SEC


class TestDurationSanitize(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(sanitize_duration(0), 0.0)

    def test_clamp_high(self):
        self.assertEqual(sanitize_duration(9999), DEFAULT_MAX_DURATION_SEC)

    def test_normal(self):
        self.assertEqual(sanitize_duration(1.5), 1.5)

    def test_reject_nan(self):
        with self.assertRaises(ValueError):
            sanitize_duration(float("nan"))

    def test_reject_negative(self):
        with self.assertRaises(ValueError):
            sanitize_duration(-1)

    def test_reject_bool(self):
        with self.assertRaises(ValueError):
            sanitize_duration(True)

    def test_string_numeric(self):
        self.assertEqual(sanitize_duration("2"), 2.0)


if __name__ == "__main__":
    unittest.main()
