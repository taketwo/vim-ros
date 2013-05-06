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

    def __getitem__(self, pos):
        """
        Get the character at the specified position in the buffer (supports
        slicing).

        Arguments
        ---------
        pos: Position | slice
            If 'pos' is of type Position, then a single character is returned.
            If 'pos' is a slice, then a string containing all the characters in
            between the start and the stop positions of the slice are returned.
            Note that lines are joined with '\n'.
        """
        if isinstance(pos, Position):
            return vim.current.buffer[pos.line][pos.col]
        if isinstance(pos, slice):
            if pos.start is not None and not isinstance(pos.start, Position):
                raise TypeError('Unsupported type for pos.start: '
                                '{0}'.format(type(pos.start)))
            s = pos.start or Position(0, 0)
            if pos.stop is not None and not isinstance(pos.stop, Position):
                raise TypeError('Unsupported type for pos.stop: '
                                '{0}'.format(type(pos.stop)))
            e = pos.stop or self._get_last_position()
            if s.line == e.line:
                return vim.current.buffer[s.line][s.col:e.col + 1]
            else:
                return '\n'.join([vim.current.buffer[s.line][s.col:]] +
                                 [vim.current.buffer[i]
                                  for i in range(s.line + 1, e.line - 1)] +
                                 [vim.current.buffer[e.line][:e.col + 1]])
        raise TypeError('Unsupported type for pos: {0}'.format(type(pos)))

    def items(self, start=None, stop=None, reversed=False):
        """
        An iterator over (position, character) items in the current buffer.

        Arguments
        ---------
        start: Position
            Position of the character where the iterator has to start. If
            omitted then (0, 0) position is used.
        stop: Position
            Position of the character at which the iterator should terminate
            (the character at this position will *NOT* be returned). If omitted
            then the position after the last character in the buffer is used.
        reversed: bool
            If set to True then 'start' should be greater than 'stop' and the
            items are returned in reverse order.
        """
        if not reversed:
            start = start or Position(0, 0)
            line, col = start.line, start.col
            while line < len(vim.current.buffer):
                while col < len(vim.current.buffer[line]):
                    p = Position(line, col)
                    if stop is not None and p >= stop:
                        return
                    yield (p, vim.current.buffer[line][col])
                    col += 1
                line += 1
                col = 0
        else:
            start = start or self._get_last_position()
            line, col = start.line, start.col
            while line >= 0:
                while col >= 0:
                    p = Position(line, col)
                    if stop is not None and p <= stop:
                        return
                    yield (p, vim.current.buffer[line][col])
                    col -= 1
                line -= 1
                col = len(vim.current.buffer[line]) - 1

    def _get_last_position(self):
        """
        Get the position of the last character in the buffer.
        """
        return Position(len(vim.current.buffer) - 1,
                        len(vim.current.buffer[-1]) - 1)
