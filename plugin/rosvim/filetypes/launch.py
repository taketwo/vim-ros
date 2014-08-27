import os
import re
import vim
import vimp
import rosp
import rospkg
import util.partial_xml_parser as pxp
from vimp.complete import Complete, CompositeComplete


class AttributeValueComplete(Complete):

    PATTERN = r'="(?=[^"]*$)'

    def get_completions(self):
        attr = pxp.get_inner_attr(vim.current.buffer, vimp.buf.cursor)
        if attr:
            if attr[0] == 'pkg':
                return sorted(rosp.Package.list())
            elif attr[0] == 'type':
                tag = pxp.get_inner_tag(vim.current.buffer, vimp.buf.cursor)
                try:
                    pkg = rosp.Package(tag.attr['pkg'])
                    return sorted(pkg.list_executables())
                except KeyError:
                    pass  # there is no "pkg" attribute
                except rospkg.ResourceNotFound:
                    pass  # package does not exist
            elif attr[0] == 'output':
                return ['log', 'screen']
            elif attr[0] == 'launch-prefix':
                # The prefixes are taken from ROS Wiki
                return ['gdb -ex run --args',
                        'nice',
                        'screen -d -m gdb --args',
                        'valgrind',
                        'xterm -e',
                        'xterm -e gdb --args',
                        'xterm -e python -m pdb']
        return []


class SubstitutionArgsComplete(Complete):

    PATTERN = r'\$\((?=\S*$)'

    def get_completions(self):
        return ['env', 'optenv', 'find', 'anon', 'arg']


class EnvironmentVariableComplete(Complete):

    PATTERN = r'(\$\((?:env|optenv) )(?=\S*$)'

    def get_completions(self):
        return os.environ.keys()


class FindPackageComplete(Complete):

    PATTERN = r'(\$\(find )(?=\S*$)'

    def get_completions(self):
        return sorted(rosp.Package.list())


class PackageRelativePathComplete(Complete):

    PATTERN = r'(\$\(find (?P<package>\S*)\)/(?P<path>([^/\0"]+/)*))(?:[^/\0"]+)?$'

    def get_completions(self):
        line = vim.current.line[:vim.current.window.cursor[1]]
        matches = list(re.finditer(self.PATTERN, line))
        groups = matches[-1].groupdict()
        try:
            pkg = rosp.Package(groups['package'])
            return os.listdir(os.path.join(pkg.path, groups['path']))
        except rospkg.ResourceNotFound:
            return []


@vimp.function('ros#launch_complete')
class LaunchComplete(CompositeComplete):

    COMPLETERS = [PackageRelativePathComplete,
                  EnvironmentVariableComplete,
                  FindPackageComplete,
                  SubstitutionArgsComplete,
                  AttributeValueComplete]


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
    vimp.opt['l:omnifunc'] = LaunchComplete
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
        except roslaunch.RLException as e:
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
