# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "llm_input"))

from transcribe_job_cleanup import (  # noqa: E402
    sanitize_transcribe_job_name,
    should_attempt_job_delete,
)


class TestTranscribeJobCleanup(unittest.TestCase):
    def test_sanitize_ok(self):
        name = "my-transcribe-job-2026-07-29-04-10-00"
        self.assertEqual(sanitize_transcribe_job_name(name), name)

    def test_sanitize_reject(self):
        self.assertIsNone(sanitize_transcribe_job_name(""))
        self.assertIsNone(sanitize_transcribe_job_name(None))
        self.assertIsNone(sanitize_transcribe_job_name("../evil"))
        self.assertIsNone(sanitize_transcribe_job_name("a/b"))
        self.assertIsNone(sanitize_transcribe_job_name("has space"))
        self.assertIsNone(sanitize_transcribe_job_name("x" * 201))

    def test_should_delete(self):
        self.assertTrue(should_attempt_job_delete("COMPLETED"))
        self.assertTrue(should_attempt_job_delete("FAILED"))
        self.assertTrue(should_attempt_job_delete(" completed "))
        self.assertFalse(should_attempt_job_delete("IN_PROGRESS"))
        self.assertFalse(should_attempt_job_delete(None))
        self.assertFalse(should_attempt_job_delete(""))


if __name__ == "__main__":
    unittest.main()
