import vimp
from . import _add_snippets


def detect():
    return vimp.buf.extension == '.cfg'


def init():
    vimp.opt['l:filetype'] = 'python'
    _add_snippets('roscfg.python')
