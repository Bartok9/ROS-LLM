#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2023 Herman Ye @Auromix
# Licensed under the Apache License, Version 2.0
#
# Normalize and ensure the chat history directory used by ChatGPTNode.

import os


def normalize_chat_history_dir(path):
    """Return an absolute directory path for chat history JSON files.

    Empty/None input falls back to the user home directory.
    """
    if path is None:
        raw = ""
    else:
        raw = str(path).strip()
    if not raw:
        raw = "~"
    return os.path.abspath(os.path.expanduser(raw))


def ensure_chat_history_dir(path):
    """Normalize ``path`` and create the directory if needed. Return abs path."""
    directory = normalize_chat_history_dir(path)
    os.makedirs(directory, exist_ok=True)
    return directory
