# -*- coding: utf-8 -*-
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.normpath(os.path.join(_HERE, "..", "llm_model"))
if _PKG not in sys.path:
    sys.path.insert(0, _PKG)

from service_response_text import normalize_function_call_response_text  # noqa: E402


class _Resp:
    def __init__(self, response_text):
        self.response_text = response_text


class TestServiceResponseText(unittest.TestCase):
    def test_success_passthrough(self):
        self.assertEqual(
            normalize_function_call_response_text(_Resp("moved 1m")),
            "moved 1m",
        )

    def test_dict_response(self):
        self.assertEqual(
            normalize_function_call_response_text({"response_text": "ok"}),
            "ok",
        )

    def test_empty_and_none(self):
        self.assertEqual(normalize_function_call_response_text(None), "null")
        self.assertEqual(normalize_function_call_response_text(_Resp("")), "null")
        self.assertEqual(normalize_function_call_response_text(_Resp(None)), "null")

    def test_error_path(self):
        out = normalize_function_call_response_text(error=RuntimeError("boom"))
        self.assertTrue(out.startswith("error: "))
        self.assertIn("boom", out)

    def test_bounds(self):
        long = "x" * 5000
        out = normalize_function_call_response_text(_Resp(long))
        self.assertEqual(len(out), 4000)


if __name__ == "__main__":
    unittest.main()
