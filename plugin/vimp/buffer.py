import vim
import os


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
        """
        Extension of the file loaded in the current buffer (including dot).
        """
        if vim.current.buffer.name is not None:
            return os.path.splitext(self.filename)[1]
