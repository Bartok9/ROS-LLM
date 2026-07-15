#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline tests for arx5 target pose sanitization (no rclpy)."""

import math
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from llm_robot.target_pose_sanitize import sanitize_pose_component, sanitize_target_pose


class TestTargetPoseSanitize(unittest.TestCase):
    def test_defaults(self):
        pose = sanitize_target_pose({})
        self.assertEqual(len(pose), 6)
        self.assertTrue(all(math.isfinite(v) for v in pose))

    def test_nan_falls_to_default(self):
        pose = sanitize_target_pose({"x": float("nan"), "y": 0.1})
        self.assertEqual(pose[0], 0.2)  # default then finite
        self.assertEqual(pose[1], 0.1)

    def test_clamp_xyz_rpy(self):
        pose = sanitize_target_pose(
            {"x": 50.0, "roll": 10.0}, max_abs_xyz=2.0, max_abs_rpy=math.pi
        )
        self.assertEqual(pose[0], 2.0)
        self.assertLessEqual(pose[3], math.pi + 1e-9)

    def test_component_bad_type(self):
        self.assertEqual(
            sanitize_pose_component("x", "x", default=0.2, max_abs=2.0), 0.2
        )


if __name__ == "__main__":
    unittest.main()
