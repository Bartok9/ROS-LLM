#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from llm_input.aws_credentials import aws_credentials_ok


class TestAwsCredentialsInput(unittest.TestCase):
    def test_ok(self):
        self.assertTrue(aws_credentials_ok("AKIAEXAMPLE", "secret"))

    def test_empty(self):
        self.assertFalse(aws_credentials_ok("", "secret"))
        self.assertFalse(aws_credentials_ok("AKIAEXAMPLE", ""))
        self.assertFalse(aws_credentials_ok("  ", "secret"))
        self.assertFalse(aws_credentials_ok("AKIAEXAMPLE", "   "))

    def test_none_and_types(self):
        self.assertFalse(aws_credentials_ok(None, "secret"))
        self.assertFalse(aws_credentials_ok("AKIAEXAMPLE", None))
        self.assertFalse(aws_credentials_ok(123, "secret"))
        self.assertFalse(aws_credentials_ok("AKIAEXAMPLE", True))


if __name__ == "__main__":
    unittest.main()
