#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from llm_input.aws_transcribe_params import (
    ALLOWED_AWS_TRANSCRIBE_LANG,
    sanitize_aws_transcribe_language,
)


class TestAwsTranscribeParams(unittest.TestCase):
    def test_default_en_us(self):
        self.assertEqual(sanitize_aws_transcribe_language(None), "en-US")
        self.assertEqual(sanitize_aws_transcribe_language(""), "en-US")
        self.assertEqual(sanitize_aws_transcribe_language("   "), "en-US")

    def test_allowed(self):
        self.assertEqual(sanitize_aws_transcribe_language("zh-CN"), "zh-CN")
        self.assertEqual(sanitize_aws_transcribe_language("en-US"), "en-US")
        self.assertIn("ja-JP", ALLOWED_AWS_TRANSCRIBE_LANG)

    def test_reject_path_and_unknown(self):
        self.assertEqual(sanitize_aws_transcribe_language("../evil"), "en-US")
        self.assertEqual(sanitize_aws_transcribe_language("en-US/../../x"), "en-US")
        self.assertEqual(sanitize_aws_transcribe_language("not-a-lang"), "en-US")
        self.assertEqual(sanitize_aws_transcribe_language("EN-US"), "en-US")  # case
        self.assertEqual(sanitize_aws_transcribe_language(123), "en-US")
        self.assertEqual(sanitize_aws_transcribe_language("zh-CN\n"), "zh-CN")

    def test_custom_default(self):
        self.assertEqual(
            sanitize_aws_transcribe_language("nope", default="zh-CN"), "zh-CN"
        )


if __name__ == "__main__":
    unittest.main()
