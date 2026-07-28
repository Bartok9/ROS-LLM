#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import unittest

from llm_input.transcript_http import (
    clamp_transcript_http_max_bytes,
    clamp_transcript_http_timeout,
    extract_transcript_text,
    parse_transcript_http_body,
)


class TestTranscriptHttp(unittest.TestCase):
    def test_clamp_timeout(self):
        self.assertEqual(clamp_transcript_http_timeout(0), 1.0)
        self.assertEqual(clamp_transcript_http_timeout(9999), 120.0)
        self.assertEqual(clamp_transcript_http_timeout("x"), 15.0)

    def test_clamp_bytes(self):
        self.assertEqual(clamp_transcript_http_max_bytes(10), 1024)
        self.assertEqual(clamp_transcript_http_max_bytes(10**12), 10_000_000)

    def test_extract(self):
        ok, t = extract_transcript_text(
            {"results": {"transcripts": [{"transcript": "hello"}]}}
        )
        self.assertTrue(ok)
        self.assertEqual(t, "hello")
        ok, err = extract_transcript_text({})
        self.assertFalse(ok)

    def test_parse_body(self):
        body = json.dumps(
            {"results": {"transcripts": [{"transcript": "hi robot"}]}}
        ).encode()
        ok, t = parse_transcript_http_body(body)
        self.assertTrue(ok)
        self.assertEqual(t, "hi robot")
        ok, err = parse_transcript_http_body(b"x" * 2000, max_bytes=1024)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
