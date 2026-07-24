#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.normpath(os.path.join(_HERE, "..", "llm_robot"))
if _PKG not in sys.path:
    sys.path.insert(0, _PKG)

from function_call_json import parse_function_call_request  # noqa: E402


class TestFunctionCallJson(unittest.TestCase):
    def test_ok(self):
        payload = json.dumps(
            {"name": "publish_cmd_vel", "arguments": '{"linear_x": 0.1}'}
        )
        ok, name, args, err = parse_function_call_request(payload)
        self.assertTrue(ok)
        self.assertEqual(name, "publish_cmd_vel")
        self.assertEqual(args, {"linear_x": 0.1})
        self.assertIsNone(err)

    def test_dict_args(self):
        payload = json.dumps(
            {"name": "call_service", "arguments": {"service_name": "/a"}}
        )
        ok, name, args, err = parse_function_call_request(payload)
        self.assertTrue(ok)
        self.assertEqual(args["service_name"], "/a")

    def test_bad_json(self):
        ok, name, args, err = parse_function_call_request("{")
        self.assertFalse(ok)
        self.assertIn("invalid JSON", err)

    def test_missing_name(self):
        ok, _, _, err = parse_function_call_request('{"arguments": "{}"}')
        self.assertFalse(ok)
        self.assertIn("name", err)

    def test_args_not_object(self):
        ok, _, _, err = parse_function_call_request(
            json.dumps({"name": "x", "arguments": "[1,2]"})
        )
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
