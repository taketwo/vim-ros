import vim
import re


class _Options(dict):

    """
    Provides dict-style access to Vim's internal options (see :help options).
    Dictionary keys should be strings of the form '[S:]NNN', where 'S' is the
    name space (global or local, not required) and 'NNN' is the option name.
    """

    def __init__(self):
        super(_Options, self).__init__()

    def __getitem__(self, key):
        return vim.eval('&{0}'.format(key))

    def __setitem__(self, key, value):
        """
        Passing None will reset the option to its default value.
        """
        setcmd = 'set' + (key.replace(':', ' ') if ':' in key else ' ' + key)
        if value is None:
            vim.command('{0}&'.format(setcmd))
        elif isinstance(value, bool):
            vim.command(setcmd if value else setcmd.replace(' ', ' no'))
        elif isinstance(value, str):
            value = re.sub(r'("|\\| |\|)', r'\\\1', value)
            vim.command('{0}={1}'.format(setcmd, value))
        elif isinstance(value, int):
            vim.command('{0}={1}'.format(setcmd, value))
        elif hasattr(value, 'viml_name'):
            vim.command('{0}={1}'.format(setcmd, value.viml_name))
        else:
            pass
