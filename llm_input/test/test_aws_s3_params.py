#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from llm_input.aws_s3_params import sanitize_aws_region, sanitize_s3_bucket_name


class TestAwsS3Params(unittest.TestCase):
    def test_region_ok(self):
        self.assertEqual(sanitize_aws_region("ap-southeast-1"), "ap-southeast-1")
        self.assertEqual(sanitize_aws_region("us-east-1"), "us-east-1")
        self.assertEqual(sanitize_aws_region("eu-west-1"), "eu-west-1")
        self.assertEqual(sanitize_aws_region("  us-west-2  "), "us-west-2")

    def test_region_reject(self):
        self.assertIsNone(sanitize_aws_region(None))
        self.assertIsNone(sanitize_aws_region(True))
        self.assertIsNone(sanitize_aws_region(12))
        self.assertIsNone(sanitize_aws_region(""))
        self.assertIsNone(sanitize_aws_region("   "))
        self.assertIsNone(sanitize_aws_region("../x"))
        self.assertIsNone(sanitize_aws_region("s3://evil"))
        self.assertIsNone(sanitize_aws_region("US-EAST-1"))
        self.assertIsNone(sanitize_aws_region("us east 1"))
        self.assertIsNone(sanitize_aws_region("not-a-region"))
        self.assertIsNone(sanitize_aws_region("us"))

    def test_bucket_ok(self):
        self.assertEqual(sanitize_s3_bucket_name("auromixbucket"), "auromixbucket")
        self.assertEqual(sanitize_s3_bucket_name("my.bucket-name"), "my.bucket-name")
        self.assertEqual(sanitize_s3_bucket_name("  abc  "), "abc")

    def test_bucket_reject(self):
        self.assertIsNone(sanitize_s3_bucket_name(None))
        self.assertIsNone(sanitize_s3_bucket_name(True))
        self.assertIsNone(sanitize_s3_bucket_name(""))
        self.assertIsNone(sanitize_s3_bucket_name("ab"))  # too short
        self.assertIsNone(sanitize_s3_bucket_name("My_Bucket"))
        self.assertIsNone(sanitize_s3_bucket_name("a..b"))
        self.assertIsNone(sanitize_s3_bucket_name("../x"))
        self.assertIsNone(sanitize_s3_bucket_name("bad_name_underscore"))
        self.assertIsNone(sanitize_s3_bucket_name("bucket.-bad"))
        self.assertIsNone(sanitize_s3_bucket_name("192.168.1.1"))
        self.assertIsNone(sanitize_s3_bucket_name("-leading"))
        self.assertIsNone(sanitize_s3_bucket_name("trailing-"))


if __name__ == "__main__":
    unittest.main()
