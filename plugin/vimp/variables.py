import vim
from . import escape


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
            vim.command('let {0}={1}'.format(key, escape(value)))

    def __delitem__(self, key):
        if not self.__contains__(key):
            raise KeyError()
        else:
            vim.command('unlet {0}'.format(key))
