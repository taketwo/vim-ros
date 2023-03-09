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

@time_cache(10, maxsize=1)
def list_messages_with_paths():
    """
    List all messages in all packages including paths to files.
    """
    import os
    import rosmsg
    import rospkg
    rospack = rospkg.RosPack()
    pkgs = rospack.list()
    packs = []
    for p in pkgs:
        package_paths = rosmsg._get_package_paths(p, rospack)
        for package_path in package_paths:
            d = os.path.join(package_path, 'msg')
            if os.path.isdir(d):
                packs.append((p, d))
    msgs = []
    for (p, direc) in packs:
        for file in rosmsg._list_types(direc, 'msg', '.msg'):
            msgs.append((f"{p}/{file}", os.path.join(direc, file) + '.msg'))
    return msgs
