# -*- coding: utf-8 -*-
# flake8: noqa

import json
import os
import sys
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from llm_model.function_call_payload import sanitize_function_call  # noqa: E402


class TestSanitizeFunctionCall(unittest.TestCase):
    def test_ok_dict_string_args(self):
        ok, out = sanitize_function_call(
            {"name": "publish_cmd_vel", "arguments": '{"linear_x": 0.1}'}
        )
        self.assertTrue(ok)
        self.assertEqual(out["name"], "publish_cmd_vel")
        self.assertEqual(json.loads(out["arguments"])["linear_x"], 0.1)

    def test_ok_dict_object_args(self):
        ok, out = sanitize_function_call(
            {"name": "call_service", "arguments": {"service_name": "/reset"}}
        )
        self.assertTrue(ok)
        self.assertEqual(json.loads(out["arguments"])["service_name"], "/reset")

    def test_ok_none_args_default_empty_object(self):
        ok, out = sanitize_function_call({"name": "publish_cmd_vel"})
        self.assertTrue(ok)
        self.assertEqual(out["arguments"], "{}")

    def test_reject_empty_name(self):
        ok, err = sanitize_function_call({"name": "  ", "arguments": "{}"})
        self.assertFalse(ok)
        self.assertIn("empty", err)

    def test_reject_path_like_name(self):
        ok, err = sanitize_function_call({"name": "os.system", "arguments": "{}"})
        self.assertFalse(ok)

    def test_reject_dunder_name(self):
        ok, err = sanitize_function_call({"name": "__init__", "arguments": "{}"})
        self.assertFalse(ok)

    def test_reject_non_object_json_args(self):
        ok, err = sanitize_function_call(
            {"name": "publish_cmd_vel", "arguments": "[1,2]"}
        )
        self.assertFalse(ok)

    def test_reject_invalid_json_string(self):
        ok, err = sanitize_function_call(
            {"name": "publish_cmd_vel", "arguments": "{not-json"}
        )
        self.assertFalse(ok)

    def test_attr_style_object(self):
        class FC:
            def __init__(self):
                self.name = "publish_cmd_vel"
                self.arguments = "{}"

        ok, out = sanitize_function_call(FC())
        self.assertTrue(ok)
        self.assertEqual(out["name"], "publish_cmd_vel")


if __name__ == "__main__":
    unittest.main()
