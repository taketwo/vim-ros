import vimp
import vimp.plugins.ultisnips as ultisnips


def detect():
    return vimp.opt['l:filetype'] == 'python'


def init():
    if ultisnips.is_available():
        ultisnips.add_filetypes('rospy')
