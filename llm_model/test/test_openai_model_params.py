#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from llm_model.openai_model_params import (
    clamp_chat_history_max_length,
    safe_chat_history_filename,
    sanitize_openai_model_id,
)


class TestOpenAIModelParams(unittest.TestCase):
    def test_model_ok(self):
        self.assertEqual(
            sanitize_openai_model_id("gpt-4-0613"), "gpt-4-0613"
        )
        self.assertEqual(
            sanitize_openai_model_id("gpt-3.5-turbo-0613"),
            "gpt-3.5-turbo-0613",
        )

    def test_model_reject(self):
        self.assertEqual(
            sanitize_openai_model_id("../x"), "gpt-3.5-turbo-0613"
        )
        self.assertEqual(
            sanitize_openai_model_id("..\\really-outside"), "gpt-3.5-turbo-0613"
        )
        self.assertEqual(
            sanitize_openai_model_id("a/b"), "gpt-3.5-turbo-0613"
        )
        self.assertEqual(sanitize_openai_model_id(""), "gpt-3.5-turbo-0613")
        self.assertEqual(sanitize_openai_model_id(None), "gpt-3.5-turbo-0613")
        self.assertEqual(sanitize_openai_model_id(12), "gpt-3.5-turbo-0613")
        self.assertEqual(
            sanitize_openai_model_id("bad model"), "gpt-3.5-turbo-0613"
        )

    def test_clamp(self):
        self.assertEqual(clamp_chat_history_max_length(100), 100)
        self.assertEqual(clamp_chat_history_max_length(0), 1)
        self.assertEqual(clamp_chat_history_max_length(999999), 16000)
        self.assertEqual(clamp_chat_history_max_length(True), 4000)
        self.assertEqual(clamp_chat_history_max_length("nope"), 4000)
        self.assertEqual(clamp_chat_history_max_length(float("nan")), 4000)

    def test_filename(self):
        self.assertEqual(
            safe_chat_history_filename("2026-07-20-04-10-00"),
            "chat_history_2026-07-20-04-10-00.json",
        )
        self.assertEqual(
            safe_chat_history_filename("../x"), "chat_history_unknown.json"
        )
        self.assertEqual(
            safe_chat_history_filename("a/b"), "chat_history_unknown.json"
        )


if __name__ == "__main__":
    unittest.main()
