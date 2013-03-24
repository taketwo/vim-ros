import vim


class _Variables(dict):

    """
    Provides dict-style access to Vim's internal variables. Dictionary keys
    should be strings of the form 'S:NNN', where 'S' is the name space (see
    :help internal-variables) and 'NNN' is the variable name.
    """

    def __init__(self):
        super(_Variables, self).__init__()

    def __contains__(self, key):
        return vim.eval('exists("{0}")'.format(key)) == '1'

    def __getitem__(self, key):
        if not self.__contains__(key):
            raise KeyError()
        else:
            return vim.eval(key)

    def __setitem__(self, key, value):
        if value is not None:
            vim.command('let {0}={1}'.format(key, self._escape(value)))

    def __delitem__(self, key):
        if not self.__contains__(key):
            raise KeyError()
        else:
            vim.command('unlet {0}'.format(key))

    def _escape(value):
        """
        Creates a vim-friendly string from a group of dicts, lists, strings,
        and bools.
        Adapted from Ultisnips (https://github.com/SirVer/ultisnips)
        """
        def convert(obj):
            if isinstance(obj, list):
                rv = '[' + ','.join(convert(o) for o in obj) + ']'
            elif isinstance(obj, dict):
                rv = '{' + ','.join(["{0}:{1}".format(convert(k), convert(v))
                                     for k, v in obj.iteritems()]) + '}'
            elif isinstance(obj, str):
                rv = '"{0}"'.format(obj.replace('"', '\\"'))
            elif isinstance(obj, bool):
                rv = str(int(obj))
            else:
                rv = str(obj)
            return rv
        return convert(value)
