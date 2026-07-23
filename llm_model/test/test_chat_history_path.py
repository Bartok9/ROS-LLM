#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import tempfile
import unittest
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1] / "llm_model"
sys.path.insert(0, str(PKG))

from chat_history_path import (  # noqa: E402
    ensure_chat_history_dir,
    normalize_chat_history_dir,
)


class TestChatHistoryPath(unittest.TestCase):
    def test_empty_falls_back_home(self):
        got = normalize_chat_history_dir("")
        self.assertTrue(os.path.isabs(got))
        self.assertEqual(got, os.path.abspath(os.path.expanduser("~")))

    def test_none_falls_back_home(self):
        got = normalize_chat_history_dir(None)
        self.assertEqual(got, os.path.abspath(os.path.expanduser("~")))

    def test_expanduser(self):
        got = normalize_chat_history_dir("~/llm_chat_hist_test_norm")
        self.assertTrue(got.endswith("llm_chat_hist_test_norm"))
        self.assertTrue(os.path.isabs(got))

    def test_ensure_makedirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "nested", "hist")
            out = ensure_chat_history_dir(target)
            self.assertTrue(os.path.isdir(out))
            self.assertEqual(out, os.path.abspath(target))


if __name__ == "__main__":
    unittest.main()
