import vimp
import vimp.plugins.ultisnips as ultisnips


def detect():
    return vimp.opt['l:filetype'] == 'cpp'


def init():
    if ultisnips.is_available():
        ultisnips.add_filetypes('roscpp')
