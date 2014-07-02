import vimp
import vimp.plugins.ultisnips as ultisnips


def detect():
    return vimp.buf.extension == '.cfg'


def init():
    vimp.opt['l:filetype'] = 'python'
    if ultisnips.is_available():
        ultisnips.add_filetypes(['roscfg', 'python'])
