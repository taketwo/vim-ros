"""
Wrap Python functions/classes so that they could be transparently called from Vim.
"""

import vim
import inspect

# Bring vimp and this module into Vim's global scope
vim.command("exec g:_rpy 'import vimp, vimp.functions'")

# Internal dictionary of registered functions
_functions = dict()


def function(name=None):
    """
    Decorator to wrap a function or a class.

    Creates a proxy VimL function, which forwards its arguments to the wrapped
    function and returns the output.

    When the decorator is applied to a class, an instance of the class is
    created and stored in the function register. The object should be callable.

    Arguments
    ---------
    name: str
        How to name the created wrapper VimL function. If this argument is
        omitted then the name of the wrapped function or class will be used.
    """

    def decorator(f):
        assert callable(f)
        is_function = not inspect.isclass(f)
        function_name = name or f.__name__
        assert function_name not in _functions
        proto = """
function! {0}(...)
  exec g:_rpy "args = vimp.var['a:000']"
  exec g:_rpy "rv = vimp.functions._functions['{0}'](*args)"
  exec g:_rpy "vim.command('return ' + vimp.escape(rv))"
endfunction
"""
        vim.command(proto.format(function_name))
        _functions[function_name] = f if is_function else f()
        f.viml_name = function_name
        return f

    return decorator
