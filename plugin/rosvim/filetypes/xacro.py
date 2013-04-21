import vim
import vimp
import util.partial_xml_parser as pxp


@vimp.function('ros#xacro_goto_file')
def goto_file():
    tag = pxp.get_inner_tag(vim.current.buffer, vimp.buf.cursor)
    if 'filename' in tag.attr and tag.name != 'mesh':
        import roslaunch.substitution_args
        f = roslaunch.substitution_args.resolve_args(tag.attr['filename'])
        vimp.edit(f)


def detect():
    return vimp.buf.extension == '.xacro'


def init():
    vimp.opt['l:filetype'] = 'xacro.xml'
    vimp.map('gf', goto_file, 'n', buffer=True)
