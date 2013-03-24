import vim


def _escape(value):
    """
    Creates a vim-friendly string from a group of dicts, lists, strings, and
    bools.
    Adapted from Ultisnips (https://github.com/SirVer/ultisnips)
    """
    def convert(obj):
        if isinstance(obj, list):
            rv = '[' + ','.join(convert(o) for o in obj) + ']'
        elif isinstance(obj, dict):
            rv = '{' + ','.join(["{0}:{1}".format(convert(key), convert(value))
                                 for key, value in obj.iteritems()]) + '}'
        elif isinstance(obj, str):
            rv = '"{0}"'.format(obj.replace('"', '\\"'))
        elif isinstance(obj, bool):
            rv = str(int(obj))
        else:
            rv = str(obj)
        return rv
    return convert(value)


class _Variables(dict):

    def __init__(self, scope):
        super(_Variables, self).__init__()
        self._scope = scope

    def __contains__(self, key):
        return vim.eval('exists("{0}")'.format(self._name(key))) == '1'

    def __getitem__(self, key):
        if not self.__contains__(key):
            raise KeyError()
        else:
            return vim.eval(self._name(key))

    def __setitem__(self, key, value):
        if value is not None:
            vim.command('let {0}={1}'.format(self._name(key), _escape(value)))

    def __delitem__(self, key):
        if not self.__contains__(key):
            raise KeyError()
        else:
            vim.command('unlet {0}'.format(self._name(key)))

    def _name(self, key):
        return '{0}:{1}'.format(self._scope, key)
