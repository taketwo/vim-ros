#!/usr/bin/env python
# encoding: utf-8

"""
ROS-related filetypes.
"""

import msg
import srv
import action
import launch
import cfg
import py
import cpp
import manifest
import xacro
modules = [msg, srv, action, launch, cfg, py, cpp, manifest, xacro]


def init():
    for m in modules:
        if m.detect():
            m.init()
            return
