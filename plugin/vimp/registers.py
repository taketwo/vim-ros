import vim
import string


class _Registers(dict):

    NUMBERED = list(string.digits)   # numbered registers
    NAMED = list(string.letters)     # named registers
    OTHER = ['',                     # unnamed register
             '-',                    # small delete register
             '_',                    # black hole register
             '*',                    # GUI clipboard
             '+',                    # GUI clipboard
             '~',                    # GUI drag'n'drop
             '/']                    # last search pattern register
    READ_ONLY = ['.',                # last inserted text
                 '%',                # name of the current file
                 '#',                # name of the alternate file
                 ':']                # most recent command-line
    READ_WRITE = NUMBERED + NAMED + OTHER
    ALL = READ_WRITE + READ_ONLY

    def __init__(self):
        super(_Registers, self).__init__()

    def __contains__(self, key):
        return key in self.ALL

    def __getitem__(self, key):
        if not self.__contains__(key):
            raise KeyError()
        else:
            return vim.eval('@{0}'.format(key))

    def __setitem__(self, key, value):
        if key not in self.READ_WRITE:
            raise KeyError()
        else:
            vim.command("let @{0}='{1}'".format(key, value.replace("'", "''")))
