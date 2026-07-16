#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2026 Bartok9 (Aerial OSS campaign)
# Licensed under the Apache License, Version 2.0

import unittest

from llm_robot.robot_name_sanitize import sanitize_robot_name


class TestRobotNameSanitize(unittest.TestCase):
    def test_empty_default(self):
        ok, n, err = sanitize_robot_name("")
        self.assertTrue(ok)
        self.assertEqual(n, "")
        self.assertEqual(err, "")

    def test_none(self):
        ok, n, err = sanitize_robot_name(None)
        self.assertTrue(ok)
        self.assertEqual(n, "")

    def test_valid(self):
        ok, n, _ = sanitize_robot_name("turtle1")
        self.assertTrue(ok)
        self.assertEqual(n, "turtle1")
        ok, n, _ = sanitize_robot_name("minipupper")
        self.assertTrue(ok)

    def test_invalid(self):
        for bad in ["../x", "a/b", "has space", "rm;id", 12, "x$y", ".hidden"]:
            ok, n, err = sanitize_robot_name(bad)
            self.assertFalse(ok, bad)
            self.assertIsNone(n)
            self.assertIn("invalid", err)


if __name__ == "__main__":
    unittest.main()
