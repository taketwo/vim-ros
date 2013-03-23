#!/usr/bin/env python
# encoding: utf-8

"""
Python wrapper for Vim.
"""

import vim


from variables import _Variables
b = _Variables('b')  # local to the current buffer
w = _Variables('w')  # local to the current window
t = _Variables('t')  # local to the current tab page
g = _Variables('g')  # global
l = _Variables('l')  # local to a function
a = _Variables('a')  # function argument (only inside a function)
v = _Variables('v')  # global, predefined by Vim
del _Variables


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
        args = a['000']
        l['result'] = f(*args)
    return wrapped


def edit(filename):
    vim.command('edit {0}'.format(filename))


def lcd(path):
    vim.command('lcd {0}'.format(path))
