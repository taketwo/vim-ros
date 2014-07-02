import vim
import vimp
import rosp
import vimp.plugins.ultisnips as ultisnips


@vimp.function('ros#manifest_complete')
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
        if field == 'package':
            packages = sorted(rosp.Package.list())
            return [p for p in packages if p.startswith(base)]
        else:
            return []


def detect():
    return vimp.buf.filename == 'manifest.xml'


def init():
    vimp.opt['l:omnifunc'] = complete
    if ultisnips.is_available():
        ultisnips.add_filetypes('rosmanifest')
