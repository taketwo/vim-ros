#!/usr/bin/env python
# encoding: utf-8

"""
Python wrapper for Vim.
"""

import vim


def escape(value):
    """
    Creates a vim-friendly string from a group of dicts, lists, strings, and
    bools.
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
        elif obj is None:
            rv = ''
        else:
            rv = str(obj)
        return rv
    return convert(value)


from variables import _Variables
var = _Variables()
del _Variables


from options import _Options
opt = _Options()
del _Options


from registers import _Registers
reg = _Registers()
del _Registers


from buffer import _Buffer
buf = _Buffer()
del _Buffer


from functions import function


def edit(filename):
    vim.command('edit {0}'.format(filename))


def lcd(path):
    vim.command('lcd {0}'.format(path))
