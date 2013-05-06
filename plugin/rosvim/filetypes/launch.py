import vim
import vimp
import rosp
import util.partial_xml_parser as pxp


@vimp.function('ros#launch_complete')
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


@vimp.function('ros#launch_goto_file')
def goto_file():
    tag = pxp.get_inner_tag(vim.current.buffer, vimp.buf.cursor)
    if 'file' in tag.attr:
        import roslaunch.substitution_args
        f = roslaunch.substitution_args.resolve_args(tag.attr['file'])
        vimp.edit(f)


def detect():
    return vimp.buf.extension == '.launch'


def init():
    vimp.opt['l:filetype'] = 'roslaunch.xml'
    vimp.opt['l:omnifunc'] = complete
    vimp.var['b:syntastic_checkers'] = ['rosvim']
    vimp.map('gf', goto_file, 'n', buffer=True)


###############################################################################
#                            Syntastic integration                            #
###############################################################################
if vimp.var['g:ros_syntastic_integration'] == '1':

    import vimp.plugins.syntastic as syntastic

    def syntastic_checker():
        import re
        import roslaunch
        import roslaunch.loader
        conf = roslaunch.ROSLaunchConfig()
        loader = roslaunch.XmlLoader()
        try:
            loader.load(vimp.buf.name, conf, verbose=False)
        except roslaunch.XmlParseException as e:
            rx = re.compile('(?:while processing (?P<filename>.*):\n)*'
                            '(?P<text>.*)'
                            '(?:: line (?P<lnum>\d+), column (?P<col>\d+))?')
            g = rx.match(e.message)
            if g is not None:
                return [syntastic.Error(**g.groupdict())]
            else:
                return [syntastic.Error(text='UPDATE RE TO HANDLE THIS TYPE OF'
                                        'ERROR MESSAGE!' + str(e.message))]
        except roslaunch.loader.LoadException as e:
            return [syntastic.Error(text=str(e.message))]
        # no parsing errors, but there could be warnigns
        warn = list()
        for e in conf.config_errors:
            g = re.match(r'\[(.*)\] (.*)', e)
            if g is not None:
                fn, text = g.groups()
                warn.append(syntastic.Error(filename=fn, text=text, type='W'))
                continue
            g = re.match(r'WARN: (.*)', e)
            if g is not None:
                warn.append(syntastic.Error(text=g.groups()[0], type='W'))
                continue
            warn.append(syntastic.Error(text='vim-ros does not know how to '
                                             'parse this warning: "%s"' % e,
                                             type='W'))
        return warn

    if syntastic.is_available():
        syntastic.add_syntax_checker('roslaunch', 'rosvim', syntastic_checker)
