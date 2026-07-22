#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline tests for AWS region + S3 bucket sanitizers in user_config."""
import unittest
import sys
import os
import types
import importlib.util

_PKG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_LLM_CFG = os.path.join(_PKG_DIR, "llm_config")

# Build fake package so relative import works
pkg = types.ModuleType("llm_config")
pkg.__path__ = [_LLM_CFG]
sys.modules["llm_config"] = pkg

rb_mod = types.ModuleType("llm_config.robot_behavior")

class RobotBehavior:  # noqa: N801
    robot_functions_list = []

rb_mod.RobotBehavior = RobotBehavior
sys.modules["llm_config.robot_behavior"] = rb_mod

spec = importlib.util.spec_from_file_location(
    "llm_config.user_config",
    os.path.join(_LLM_CFG, "user_config.py"),
    submodule_search_locations=[_LLM_CFG],
)
uc = importlib.util.module_from_spec(spec)
sys.modules["llm_config.user_config"] = uc
spec.loader.exec_module(uc)

sanitize_aws_region = uc.sanitize_aws_region
sanitize_s3_bucket = uc.sanitize_s3_bucket


class TestAwsRegionBucket(unittest.TestCase):
    def test_region_ok(self):
        self.assertEqual(sanitize_aws_region("us-east-1"), "us-east-1")
        self.assertEqual(sanitize_aws_region("AP-SOUTHEAST-1"), "ap-southeast-1")

    def test_region_bad_falls_back(self):
        self.assertEqual(sanitize_aws_region("not-a-region"), "ap-southeast-1")
        self.assertEqual(sanitize_aws_region(""), "ap-southeast-1")
        self.assertEqual(sanitize_aws_region(None), "ap-southeast-1")
        self.assertEqual(sanitize_aws_region("../../etc"), "ap-southeast-1")

    def test_bucket_ok(self):
        self.assertEqual(sanitize_s3_bucket("auromixbucket"), "auromixbucket")
        self.assertEqual(sanitize_s3_bucket("my-bucket.example"), "my-bucket.example")
        self.assertEqual(sanitize_s3_bucket("MyBucket"), "mybucket")

    def test_bucket_bad(self):
        with self.assertRaises(ValueError):
            sanitize_s3_bucket("ab")
        with self.assertRaises(ValueError):
            sanitize_s3_bucket("-bad")
        with self.assertRaises(ValueError):
            sanitize_s3_bucket("has_underscore")
        with self.assertRaises(ValueError):
            sanitize_s3_bucket("bad..dots")
        with self.assertRaises(ValueError):
            sanitize_s3_bucket("space name")


if __name__ == "__main__":
    unittest.main()
