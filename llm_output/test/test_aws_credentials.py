#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from llm_output.aws_credentials import aws_credentials_ok


class TestAwsCredentials(unittest.TestCase):
    def test_ok(self):
        self.assertTrue(aws_credentials_ok("AKIA", "secret"))

    def test_empty(self):
        self.assertFalse(aws_credentials_ok("", "secret"))
        self.assertFalse(aws_credentials_ok("AKIA", ""))
        self.assertFalse(aws_credentials_ok("  ", "secret"))
        self.assertFalse(aws_credentials_ok("AKIA", "   "))

    def test_none_and_types(self):
        self.assertFalse(aws_credentials_ok(None, "secret"))
        self.assertFalse(aws_credentials_ok("AKIA", None))
        self.assertFalse(aws_credentials_ok(123, "secret"))


if __name__ == "__main__":
    unittest.main()
