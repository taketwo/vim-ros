import vimp
from . import _add_snippets


def detect():
    return vimp.opt['l:filetype'] == 'python'


def init():
    _add_snippets('rospy')
