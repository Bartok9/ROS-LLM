#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2026 Bartok / contributors
# Licensed under the Apache License, Version 2.0

import unittest

from llm_model.chat_role_sanitize import ALLOWED_CHAT_ROLES, sanitize_chat_role


class TestChatRoleSanitize(unittest.TestCase):
    def test_ok(self):
        for role in sorted(ALLOWED_CHAT_ROLES):
            self.assertEqual(sanitize_chat_role(role), role)
        self.assertEqual(sanitize_chat_role(" User "), "user")
        self.assertEqual(sanitize_chat_role("ASSISTANT"), "assistant")

    def test_reject(self):
        self.assertIsNone(sanitize_chat_role("root"))
        self.assertIsNone(sanitize_chat_role("admin"))
        self.assertIsNone(sanitize_chat_role(""))
        self.assertIsNone(sanitize_chat_role("   "))
        self.assertIsNone(sanitize_chat_role(None))
        self.assertIsNone(sanitize_chat_role(True))
        self.assertIsNone(sanitize_chat_role(12))
        self.assertIsNone(sanitize_chat_role("user;drop"))


if __name__ == "__main__":
    unittest.main()
