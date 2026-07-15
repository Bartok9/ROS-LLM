#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline tests for cmd_vel sanitization (no rclpy required)."""

import math
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from llm_robot.cmd_vel_sanitize import sanitize_cmd_vel_float, sanitize_duration


class TestCmdVelSanitize(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(sanitize_cmd_vel_float(1.0, "linear_x"), 1.0)
        self.assertEqual(sanitize_cmd_vel_float("-0.5", "angular_z"), -0.5)

    def test_nan_inf(self):
        with self.assertRaises(ValueError):
            sanitize_cmd_vel_float(float("nan"), "linear_x")
        with self.assertRaises(ValueError):
            sanitize_cmd_vel_float(float("inf"), "angular_z")
        with self.assertRaises(ValueError):
            sanitize_cmd_vel_float(-math.inf, "linear_y")

    def test_clamp(self):
        self.assertEqual(sanitize_cmd_vel_float(10.0, "linear_x", max_abs=2.0), 2.0)
        self.assertEqual(sanitize_cmd_vel_float(-9.0, "angular_z", max_abs=2.0), -2.0)

    def test_bad_type(self):
        with self.assertRaises(ValueError):
            sanitize_cmd_vel_float("nope", "linear_x")

    def test_duration(self):
        self.assertEqual(sanitize_duration(1.5), 1.5)
        self.assertEqual(sanitize_duration(-1), 0.0)
        self.assertEqual(sanitize_duration(float("nan")), 0.0)
        self.assertEqual(sanitize_duration(float("inf")), 0.0)
        self.assertEqual(sanitize_duration(999, max_sec=30.0), 30.0)
        self.assertEqual(sanitize_duration("unicode"), 0.0)


if __name__ == "__main__":
    unittest.main()
