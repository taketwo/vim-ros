"""
Integration with Syntastic plugin (https://github.com/scrooloose/syntastic).
"""

import vimp


def is_available():
    """
    Test whether Syntastic plugin is available (was loaded).
    """
    return 'g:loaded_syntastic_plugin' in vimp.var


def add_syntax_checker(filetype,
                       name,
                       get_loc_list_cb,
                       is_available_cb=None,
                       get_highlight_regex_cb=None):
    """
    Register a new syntax checker for the specified filetype in Syntastic
    framework. This creates VimL wrapper functions as needed.

    See: https://github.com/scrooloose/syntastic/wiki/Syntax-Checker-Guide

    Arguments
    ---------
    filetype: str
        Target filetype.
    name: str
        Syntax checker name.
    get_loc_list_cb: function
        Function that will be called to perform syntax check.
    is_available_cb: function
        Function that will be called to determine whether the syntax checker
        is available. If omitted then a lambda returning True is assumed.
    get_highlight_regex_cb: function
        Function that will be called to determinew which parts of the file are
        erroneous and should be highlighted. This is optional.
    """
    cmd = 'g:SyntasticRegistry.CreateAndRegisterChecker'
    arg = {'filetype': filetype, 'name': name}
    prefix = 'SyntaxCheckers_{0}_{1}_'.format(filetype, name)
    is_available_cb = is_available_cb or (lambda: True)
    vimp.function(prefix + 'GetLocList')(get_loc_list_cb)
    vimp.function(prefix + 'IsAvailable')(is_available_cb)
    if get_highlight_regex_cb is not None:
        vimp.function(prefix + 'GetHighlightRegex')(get_highlight_regex_cb)
    vimp.call(cmd, arg)


class Error(dict):
    """
    A helper ditionary class to simplify filling location list.
    """
    def __init__(self, **kwargs):
        super(Error, self).__init__()
        self['text'] = ''
        self['lnum'] = 0
        self['col'] = 0
        self['vcol'] = 1
        self['type'] = 'E'
        self['valid'] = 1
        self['bufnr'] = vimp.buf.number
        for key, value in kwargs.iteritems():
            if value is not None:
                self[key] = str(value)
        if 'filename' in self:
            self['bufnr'] = 0
