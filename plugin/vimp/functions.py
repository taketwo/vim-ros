"""
Wrap Python functions so that could be transparently called from Vim.
"""

import vim

PY = 'python'

# Bring vimp and this module into Vim's global scope
vim.command('{0} import vimp, vimp.functions'.format(PY))

# Internal dictionary of registered functions
_functions = dict()


def function(name=None):
    """
    Decorator to wrap a function.

    Arguments
    ---------
    name: str
        How to name the created wrapper VimL function. If this argument is
        omitted then the name of the wrapped function will be used.
    """
    def decorator(f):
        function_name = name or f.func_name
        assert function_name not in _functions
        proto = ('function! {0}(...)\n'
                 ':{1} args = vimp.var["a:000"]\n'
                 ':{1} rv = vimp.functions._functions["{0}"](*args)\n'
                 ':{1} vim.command("return " + vimp.escape(rv))\n'
                 'endfunction')
        vim.command(proto.format(function_name, PY))
        _functions[function_name] = f
        f.viml_name = function_name
        return f
    return decorator
