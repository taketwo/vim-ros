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


class function(object):

    """
    Decorator for transparent interfacing of Python functions with Vim.

    At the moment of decoration it declares a VimL function with body that just
    calls the decorated function. The decorated function is automatically fed
    with the list of arguments fetched from Vim's "arguments" variables scope.
    The return value is properly escaped and propagated to Vim's ecosystem.
    """

    def __init__(self, module='', plugin=''):
        """
        Arguments
        ---------
        module: str
            Python module name to which the decorated function belongs. This
            will be prefixed to the function call.
        plugin: str
            Vim plugin name to which the function belongs. If omitted, then the
            wrapper VimL function will be limited to script ('s:') scope.
        """
        self._pyprefix = module + '.' if module else ''
        self._vimprefix = plugin + '#' if plugin else 's:'

    def __call__(self, f):
        proto = 'function! {0}{2}(...)\nexec g:_rpy "{1}{2}()"\nendfunction'
        vim.command(proto.format(self._vimprefix, self._pyprefix, f.func_name))

        def wrapped():
            args = var['a:000']
            result = f(*args)
            vim.command('return ' + escape(result))
        return wrapped


def edit(filename):
    vim.command('edit {0}'.format(filename))


def lcd(path):
    vim.command('lcd {0}'.format(path))
