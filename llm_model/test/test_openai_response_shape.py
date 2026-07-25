#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2026 Bartok9 (Aerial OSS campaign)
# Licensed under the Apache License, Version 2.0

import unittest

from llm_model.openai_response_shape import extract_choice_message


class TestOpenaiResponseShape(unittest.TestCase):
    def test_none_response(self):
        m, c, fc, flag = extract_choice_message(None)
        self.assertEqual(m, {})
        self.assertIsNone(c)
        self.assertIsNone(fc)
        self.assertEqual(flag, 0)

    def test_empty_choices(self):
        m, c, fc, flag = extract_choice_message({"choices": []})
        self.assertEqual(m, {})
        self.assertEqual(flag, 0)

    def test_missing_message(self):
        m, c, fc, flag = extract_choice_message({"choices": [{}]})
        self.assertEqual(m, {})
        self.assertEqual(flag, 0)

    def test_text_path(self):
        m, c, fc, flag = extract_choice_message(
            {"choices": [{"message": {"content": "hello", "role": "assistant"}}]}
        )
        self.assertEqual(c, "hello")
        self.assertIsNone(fc)
        self.assertEqual(flag, 0)
        self.assertEqual(m.get("role"), "assistant")

    def test_function_call_path(self):
        fc_in = {"name": "publish_cmd_vel", "arguments": "{}"}
        m, c, fc, flag = extract_choice_message(
            {"choices": [{"message": {"content": None, "function_call": fc_in}}]}
        )
        self.assertIsNone(c)
        self.assertEqual(fc, fc_in)
        self.assertEqual(flag, 1)

    def test_null_content_without_function_call(self):
        m, c, fc, flag = extract_choice_message(
            {"choices": [{"message": {"content": None}}]}
        )
        self.assertIsNone(c)
        self.assertIsNone(fc)
        self.assertEqual(flag, 0)


if __name__ == "__main__":
    unittest.main()
