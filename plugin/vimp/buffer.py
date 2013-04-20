import vim
import os
from util.position import Position


class _Buffer(object):

    def __init__(self):
        pass

    @property
    def name(self):
        if vim.current.buffer.name is not None:
            return vim.current.buffer.name

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
        """
        Extension of the file loaded in the current buffer (including dot).
        """
        if vim.current.buffer.name is not None:
            return os.path.splitext(self.filename)[1]

    @property
    def number(self):
        return vim.current.buffer.number

    @property
    def cursor(self):
        """
        Get cursor position in the current buffer (Note: zero-based index).
        """
        c = vim.current.window.cursor
        return Position(c[0] - 1, c[1])

    @cursor.setter
    def cursor(self, value):
        """
        Set cursor position in the current buffer (Note: zero-based index).
        """
        if isinstance(value, Position):
            c = (value.line + 1, value.col)
        elif isinstance(value, tuple) and len(value) == 2:
            c = (value[0] + 1, value[1])
        else:
            raise TypeError('Unsupported type for cursor: %s' % type(value))
        vim.current.window.cursor = c
