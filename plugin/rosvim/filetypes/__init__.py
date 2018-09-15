#!/usr/bin/env python
# encoding: utf-8

"""
ROS-related filetypes.
"""

from . import msg
from . import srv
from . import action
from . import launch
from . import cfg
from . import py
from . import cpp
from . import manifest
from . import xacro
modules = [msg, srv, action, launch, cfg, py, cpp, manifest, xacro]


def init():
    for m in modules:
        if m.detect():
            m.init()
            return
