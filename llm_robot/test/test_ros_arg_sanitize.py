#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2026 Bartok9 (Aerial OSS campaign)
# Licensed under the Apache License, Version 2.0

import unittest

from llm_robot.ros_arg_sanitize import (
    is_valid_ros_name,
    is_valid_ros_type,
    sanitize_service_call_args,
)


class TestRosArgSanitize(unittest.TestCase):
    def test_valid_names(self):
        self.assertTrue(is_valid_ros_name("/reset"))
        self.assertTrue(is_valid_ros_name("turtle1/reset"))
        self.assertTrue(is_valid_ros_name("/foo/bar_baz"))

    def test_invalid_names(self):
        self.assertFalse(is_valid_ros_name(""))
        self.assertFalse(is_valid_ros_name("a;rm -rf /"))
        self.assertFalse(is_valid_ros_name("../etc"))
        self.assertFalse(is_valid_ros_name("has space"))
        self.assertFalse(is_valid_ros_name(None))

    def test_valid_types(self):
        self.assertTrue(is_valid_ros_type("std_srvs/Empty"))
        self.assertTrue(is_valid_ros_type("std_srvs/srv/Empty"))

    def test_invalid_types(self):
        self.assertFalse(is_valid_ros_type(""))
        self.assertFalse(is_valid_ros_type("Empty"))  # needs package/
        self.assertFalse(is_valid_ros_type("std_srvs/Empty;id"))

    def test_sanitize_ok(self):
        ok, n, t = sanitize_service_call_args("/reset", "std_srvs/srv/Empty")
        self.assertTrue(ok)
        self.assertEqual(n, "/reset")
        self.assertEqual(t, "std_srvs/srv/Empty")

    def test_sanitize_bad(self):
        ok, err, _ = sanitize_service_call_args("bad name", "std_srvs/Empty")
        self.assertFalse(ok)
        self.assertIn("invalid", err)


if __name__ == "__main__":
    unittest.main()
