import vim
import vimp
import rosp
from .. import fmgr


@fmgr.function('LaunchComplete')
def complete(findstart, base):
    def find_start():
        line = vim.current.line
        col = vim.current.window.cursor[1]
        while col > 0 and line[col - 1] != '"':
            col -= 1
        start = col
        while col > 0 and line[col - 1] != ' ':
            col -= 1
        field = line[col:start - 2]
        return (start, field)
    if findstart == '1':
        return find_start()[0]
    else:
        field = find_start()[1]
        if field == 'pkg':
            packages = sorted(rosp.Package.list())
            return [p for p in packages if p.startswith(base)]
        elif field == 'type':
            executables = ['not implemented']
            return executables
        else:
            return []


def detect():
    return vimp.buf.extension == '.launch'


def init():
    vimp.opt['l:filetype'] = 'roslaunch.xml'
    vimp.opt['l:omnifunc'] = complete
