#!/usr/bin/env python
# encoding: utf-8

"""
Python wrapper for Vim.
"""

import vim


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


def function(f):
    """
    Decorator for transparent interfacing of Python functions with Vim.

    Fetches the list of arguments from Vim's "arguments" variables scope and
    passes them to the wrapped function. Stores the value returned by the
    function in the Vim's "local" variables scope.
    """
    def wrapped():
        args = var['a:000']
        var['l:result'] = f(*args)
    return wrapped


def edit(filename):
    vim.command('edit {0}'.format(filename))


def lcd(path):
    vim.command('lcd {0}'.format(path))
