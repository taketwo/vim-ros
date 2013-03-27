import vimp
from . import msg


def detect():
    return vimp.buf.extension == '.action'


def init():
    vimp.opt['l:filetype'] = 'rosaction'
    vimp.opt['l:omnifunc'] = msg.complete
