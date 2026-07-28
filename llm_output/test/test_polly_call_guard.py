#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from llm_output.polly_call_guard import (
    clamp_polly_audio_max_bytes,
    safe_read_audio_stream,
)


class _Stream:
    def __init__(self, payload, raise_on_read=False):
        self._payload = payload
        self._raise = raise_on_read

    def read(self, n=-1):
        if self._raise:
            raise OSError("boom")
        if n is None or n < 0:
            return self._payload
        return self._payload[:n]


class TestPollyCallGuard(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(clamp_polly_audio_max_bytes(100), 1000)
        self.assertEqual(clamp_polly_audio_max_bytes(10**12), 20_000_000)
        self.assertEqual(clamp_polly_audio_max_bytes("bad"), 5_000_000)

    def test_read_ok(self):
        ok, data = safe_read_audio_stream(_Stream(b"abc"), max_bytes=1000)
        self.assertTrue(ok)
        self.assertEqual(data, b"abc")

    def test_read_overflow(self):
        ok, err = safe_read_audio_stream(_Stream(b"0123456789"), max_bytes=1000)
        # 10 bytes < 1000 min clamp -> ok
        self.assertTrue(ok)
        ok, err = safe_read_audio_stream(_Stream(b"x" * 2000), max_bytes=1000)
        self.assertFalse(ok)
        self.assertIn("max_bytes", err)

    def test_read_error(self):
        ok, err = safe_read_audio_stream(_Stream(b"x", raise_on_read=True))
        self.assertFalse(ok)
        self.assertIn("failed", err)

    def test_missing(self):
        ok, err = safe_read_audio_stream(None)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
