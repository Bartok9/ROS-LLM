# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm_model.openai_call_guard import (  # noqa: E402
    completion_or_empty,
    empty_chat_completion,
    is_usable_chat_completion,
)


class TestOpenAICallGuard(unittest.TestCase):
    def test_empty_shape(self):
        e = empty_chat_completion()
        self.assertTrue(is_usable_chat_completion(e))
        self.assertIsNone(e["choices"][0]["message"]["content"])

    def test_reject_bad(self):
        self.assertFalse(is_usable_chat_completion(None))
        self.assertFalse(is_usable_chat_completion({}))
        self.assertFalse(is_usable_chat_completion({"choices": []}))
        self.assertFalse(is_usable_chat_completion({"choices": [{"message": "x"}]}))

    def test_accept_good(self):
        good = {"choices": [{"message": {"role": "assistant", "content": "hi"}}]}
        self.assertTrue(is_usable_chat_completion(good))
        self.assertEqual(completion_or_empty(good)["choices"][0]["message"]["content"], "hi")

    def test_error_path(self):
        out = completion_or_empty({"choices": []}, error=RuntimeError("boom"))
        self.assertTrue(is_usable_chat_completion(out))
        self.assertIsNone(out["choices"][0]["message"].get("function_call"))


if __name__ == "__main__":
    unittest.main()
