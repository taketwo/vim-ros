import vimp
from . import msg


def detect():
    return vimp.buf.extension == '.srv'


def init():
    vimp.opt['l:filetype'] = 'rossrv'
    vimp.opt['l:omnifunc'] = msg.MsgComplete
    vimp.map('gd', msg.goto_definition, 'n', buffer=True)
