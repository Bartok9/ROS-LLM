# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "llm_input"))

from tmp_audio_path import DEFAULT_TMP_AUDIO, resolve_tmp_audio_path, safe_unlink  # noqa: E402


class TestTmpAudioPath(unittest.TestCase):
    def test_default(self):
        self.assertEqual(resolve_tmp_audio_path(None), os.path.realpath(DEFAULT_TMP_AUDIO))
        self.assertEqual(resolve_tmp_audio_path(""), os.path.realpath(DEFAULT_TMP_AUDIO))

    def test_reject_outside_tmp(self):
        self.assertEqual(
            resolve_tmp_audio_path("/etc/passwd.flac"),
            os.path.realpath(DEFAULT_TMP_AUDIO),
        )
        self.assertEqual(
            resolve_tmp_audio_path("/var/tmp/x.flac"),
            os.path.realpath(DEFAULT_TMP_AUDIO),
        )

    def test_reject_bad_suffix(self):
        self.assertEqual(
            resolve_tmp_audio_path("/tmp/evil.sh"),
            os.path.realpath(DEFAULT_TMP_AUDIO),
        )

    def test_ok_under_tmp(self):
        p = "/tmp/user_audio_input.wav"
        self.assertEqual(resolve_tmp_audio_path(p), os.path.realpath(p))

    def test_safe_unlink_missing_ok(self):
        self.assertTrue(safe_unlink("/tmp/definitely-missing-ros-llm-test.flac"))

    def test_safe_unlink_creates_and_removes(self):
        path = "/tmp/ros_llm_test_unlink.flac"
        with open(path, "wb") as f:
            f.write(b"x")
        self.assertTrue(safe_unlink(path))
        self.assertFalse(os.path.exists(path))

    def test_safe_unlink_rejects_outside(self):
        # should not throw; should not unlink /etc if somehow passed
        self.assertFalse(safe_unlink("/etc/hosts"))


if __name__ == "__main__":
    unittest.main()
