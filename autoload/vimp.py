#!/usr/bin/env python
# encoding: utf-8

"""
Python wrapper for Vim.
"""

import vim
import os


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


class _Registers(dict):

    import string

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


class _Buffer(object):

    def __init__(self):
        pass

    @property
    def path(self):
        if vim.current.buffer.name is not None:
            return os.path.split(vim.current.buffer.name)[0]

    @property
    def filename(self):
        if vim.current.buffer.name is not None:
            return os.path.split(vim.current.buffer.name)[1]

    @property
    def stem(self):
        if vim.current.buffer.name is not None:
            return os.path.splitext(self.filename)[0]

    @property
    def extension(self):
        if vim.current.buffer.name is not None:
            return os.path.splitext(self.filename)[1]


def edit(filename):
    vim.command('edit {0}'.format(filename))


b = _Variables('b')  # local to the current buffer
w = _Variables('w')  # local to the current window
t = _Variables('t')  # local to the current tab page
g = _Variables('g')  # global
v = _Variables('v')  # global, predefined by Vim

reg = _Registers()

buf = _Buffer()
