import vimp
from . import _add_snippets


def detect():
    return vimp.opt['l:filetype'] == 'cpp'


def init():
    _add_snippets('roscpp')
