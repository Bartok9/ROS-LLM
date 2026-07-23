#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2023 Herman Ye @Auromix
# Licensed under the Apache License, Version 2.0
#
# Helpers to normalize OpenAI message content for ROS std_msgs/String publish.


def normalize_openai_text(content):
    """Return a string safe for std_msgs/msg/String.data.

    OpenAI function-call responses often set content to None. Assigning None
    to String.data raises; publishing empty string is the safe no-op path.
    """
    if content is None:
        return ""
    if isinstance(content, bytes):
        return content.decode("utf-8", errors="replace")
    if isinstance(content, str):
        return content
    return str(content)
