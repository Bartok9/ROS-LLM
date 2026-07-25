#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2026 Bartok9 (Aerial OSS campaign)
# Licensed under the Apache License, Version 2.0

import subprocess
import unittest
from unittest import mock

from llm_robot.service_call_timeout import (
    DEFAULT_TIMEOUT_SEC,
    MAX_TIMEOUT_SEC,
    MIN_TIMEOUT_SEC,
    clamp_timeout,
    run_ros2_service_call,
)


class TestServiceCallTimeout(unittest.TestCase):
    def test_clamp_default(self):
        self.assertEqual(clamp_timeout(None), DEFAULT_TIMEOUT_SEC)
        self.assertEqual(clamp_timeout("bad"), DEFAULT_TIMEOUT_SEC)

    def test_clamp_bounds(self):
        self.assertEqual(clamp_timeout(0.1), MIN_TIMEOUT_SEC)
        self.assertEqual(clamp_timeout(999), MAX_TIMEOUT_SEC)
        self.assertEqual(clamp_timeout(12), 12.0)

    def test_timeout_message(self):
        with mock.patch(
            "llm_robot.service_call_timeout.subprocess.check_output",
            side_effect=subprocess.TimeoutExpired(cmd="x", timeout=15),
        ):
            msg = run_ros2_service_call(["ros2", "service", "call", "/a", "pkg/srv/T"], 15)
        self.assertIn("timed out", msg)
        self.assertIn("15", msg)

    def test_success_decode(self):
        with mock.patch(
            "llm_robot.service_call_timeout.subprocess.check_output",
            return_value=b"ok-result",
        ):
            msg = run_ros2_service_call(["ros2", "service", "call", "/a", "pkg/srv/T"])
        self.assertEqual(msg, "ok-result")


if __name__ == "__main__":
    unittest.main()
