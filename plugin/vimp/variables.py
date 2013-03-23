import vim


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
            if isinstance(value, str):
                value = '"{0}"'.format(value)
            elif isinstance(value, bool):
                value = int(value)
            vim.command('let {0}={1}'.format(self._name(key), value))

    def __delitem__(self, key):
        if not self.__contains__(key):
            raise KeyError()
        else:
            vim.command('unlet {0}'.format(self._name(key)))

    def _name(self, key):
        return '{0}:{1}'.format(self._scope, key)
