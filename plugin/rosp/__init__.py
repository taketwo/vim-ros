#!/usr/bin/env python
# encoding: utf-8

"""
Utility functions and classes for ROS.
"""

import subprocess

from .package import Package
from util import time_cache


def list_nodelets():
    """
    List all nodelets in all packages.
    """
    nodelets = []
    for p in rospkg.RosPack().get_depends_on("nodelet", implicit=False):
        nodelets += Package(p).list_nodelets()
    return nodelets


@time_cache(10, maxsize=1)
def list_messages():
    """
    List all messages in all packages.
    """
    return (
        subprocess.check_output(["rosmsg", "list"], encoding="utf-8")
        .strip()
        .split("\n")
    )
