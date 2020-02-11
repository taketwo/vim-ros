#!/usr/bin/env python
# encoding: utf-8

"""
Utility functions and classes for ROS.
"""

from package import *
from build_tools import *


def list_nodelets():
    """
    List all nodelets in all packages.
    """
    nodelets = []
    for p in rospkg.RosPack().get_depends_on('nodelet', implicit=False):
        nodelets += Package(p).list_nodelets()
    return nodelets
