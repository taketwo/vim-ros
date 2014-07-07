"""
Helper classes for implementation of completion finding functions (see
h:complete-functions).
"""

import re
import vim
import vimp.plugins.ycm as ycm


class Complete(object):

    PATTERN = None

    def __call__(self, findstart, base):
        if findstart == '1':
            return self.find_start()
        else:
            completions = self.get_completions()
            # If YouCompleteMe plugin is present we return all possible
            # completions and let it filter them itself using fuzzy matching.
            # Otherwise we return only the complitions starting with base.
            if ycm.is_available():
                return completions
            return sorted([c for c in completions if c.startswith(base)])

    def find_start(self):
        if not self.PATTERN:
            return -3
        line = vim.current.line[:vim.current.window.cursor[1]]
        matches = list(re.finditer(self.PATTERN, line))
        if not matches:
            return -3
        return matches[-1].end()

    def get_completions(self):
        return []


class CompositeComplete(Complete):

    COMPLETERS = []

    def __init__(self):
        self.completers = [c() for c in self.COMPLETERS]

    def find_start(self):
        for c in self.completers:
            start = c.find_start()
            if start >= 0:
                return start
        return -3

    def get_completions(self):
        for c in self.completers:
            if c.find_start() >= 0:
                return c.get_completions()
