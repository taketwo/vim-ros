import vimp
import subprocess


@vimp.function('ros#msg_complete')
def complete(findstart, base):
    if findstart == '1':
        return 0
    else:
        msgs = subprocess.check_output(['rosmsg', 'list']).strip().split('\n')
        builtin = ['bool', 'int8', 'uint8', 'int16', 'uint16', 'int32',
                   'uint32', 'int64', 'uint64', 'float32', 'float64', 'string',
                   'time', 'duration', 'Header']
        return [m for m in builtin + msgs if m.startswith(base)]


def detect():
    return vimp.buf.extension == '.msg'


def init():
    vimp.opt['l:filetype'] = 'rosmsg'
    vimp.opt['l:omnifunc'] = complete
