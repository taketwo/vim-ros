import vim
from . import escape, var


class FunctionManager(object):

    def __init__(self, name, plugin):
        self._name = name
        self._plugin = plugin
        self._py = ':python'
        self._functions = dict()

    def function(self, name=None, local=False):
        def decorator(f):
            function_name = name or f.func_name
            assert function_name not in self._functions
            self._functions[function_name] = f
            f.viml_name = self._define_viml_function(function_name, local)
            return f
        return decorator

    def invoke(self, function_name):
        assert function_name in self._functions
        args = var['a:000']
        result = self._functions[function_name](*args)
        vim.command('return ' + escape(result))

    def _define_viml_function(self, function_name, local):
        prefix = 's:' if local else self._plugin + '#'
        proto = 'function! {0}{1}(...)\n{2} {3}.invoke("{1}")\nendfunction'
        vim.command(proto.format(prefix, function_name, self._py, self._name))
        return prefix + function_name
