# -*- coding: utf-8 -*-
import unittest

from llm_robot.function_call_guard import resolve_function, ALLOWED_FUNCTIONS


class TestFunctionCallGuard(unittest.TestCase):
    def test_allow_known(self):
        ok, name = resolve_function("turtle", "publish_cmd_vel")
        self.assertTrue(ok)
        self.assertEqual(name, "publish_cmd_vel")

    def test_reject_destroy_node(self):
        ok, err = resolve_function("turtle", "destroy_node")
        self.assertFalse(ok)
        self.assertIn("allowlist", err)

    def test_reject_dunder(self):
        ok, err = resolve_function("multi", "__class__")
        self.assertFalse(ok)

    def test_reject_path(self):
        ok, err = resolve_function("multi", "publish_cmd_vel;rm")
        self.assertFalse(ok)

    def test_strip_whitespace_ok_name(self):
        ok, name = resolve_function("arm", "  publish_target_pose  ")
        self.assertTrue(ok)
        self.assertEqual(name, "publish_target_pose")

    def test_kinds_cover_demo_robots(self):
        self.assertIn("multi", ALLOWED_FUNCTIONS)
        self.assertIn("turtle", ALLOWED_FUNCTIONS)
        self.assertIn("arm", ALLOWED_FUNCTIONS)


if __name__ == "__main__":
    unittest.main()
