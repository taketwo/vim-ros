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


def call(cmd, arg):
    vim.command('call {0}({1})'.format(cmd, escape(arg)))


def edit(filename):
    vim.command('edit {0}'.format(filename))


def tabedit(filename):
    vim.command('tabedit {0}'.format(filename))


def lcd(path):
    vim.command('lcd {0}'.format(path))


def map(lhs, rhs, mode, buffer=False, silent=False, noremap=True):
    assert mode in 'nvsoic'
    if hasattr(rhs, 'viml_name'):
        # this is a wrapped function, convert to a function call
        rhs = ':call {0}()<CR>'.format(rhs.viml_name)
    proto = '{mode}{remap}map{buffer}{silent} {lhs} {rhs}'
    vim.command(proto.format(mode=mode,
                             remap='nore' if noremap else '',
                             buffer=' <buffer>' if buffer else '',
                             silent=' <silent>' if silent else '',
                             lhs=lhs,
                             rhs=rhs))


def inputlist(prompt, textlist, enumerate=True):
    """
    Wrapper for VimL function 'inputlist' (see :help inputlist).

    Arguments
    ---------
    prompt: str
        Prompt line.
    textlist: list
        List of items for user to choose from.
    enumerate: bool
        If True then an index will be prepended to each item.

    Returns
    -------
    choice: str | None
        The item that the user has chosen or None if the user cancelled input.
    """
    display = [prompt]
    for i, t in zip(range(1, len(textlist) + 1), textlist):
        display.append('{0:2}) {1}'.format(i, t) if enumerate else t)
    choice = vim.eval("inputlist({0})".format(escape(display)))
    if choice is None or choice == '0':
        return None
    choice = int(choice)
    if choice > len(textlist):
        choice = len(textlist)
    return textlist[choice - 1]
