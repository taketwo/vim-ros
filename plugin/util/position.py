class Position(object):

    """
    Represents cursor position in a buffer.

    Adapted from UltiSnips (https://github.com/SirVer/ultisnips)
    """

    def __init__(self, line, col):
        self.line = line
        self.col = col

    def __add__(self, pos):
        if not isinstance(pos, Position):
            raise TypeError('Unsupported operand type(s) for +: '
                            '"Position" and %s' % type(pos))
        return Position(self.line + pos.line, self.col + pos.col)

    def __sub__(self, pos):
        if not isinstance(pos, Position):
            raise TypeError('Unsupported operand type(s) for +: '
                            '"Position" and %s' % type(pos))
        return Position(self.line - pos.line, self.col - pos.col)

    def diff(self, pos):
        if not isinstance(pos, Position):
            raise TypeError('Unsupported operand type(s) for +: '
                            '"Position" and %s' % type(pos))
        if self.line == pos.line:
            return Position(0, self.col - pos.col)
        else:
            if self > pos:
                return Position(self.line - pos.line, self.col)
            else:
                return Position(self.line - pos.line, pos.col)
        return Position(self.line - pos.line, self.col - pos.col)

    def __eq__(self, other):
        return (self.line, self.col) == (other.line, other.col)

    def __ne__(self, other):
        return (self.line, self.col) != (other.line, other.col)

    def __lt__(self, other):
        return (self.line, self.col) < (other.line, other.col)

    def __le__(self, other):
        return (self.line, self.col) <= (other.line, other.col)

    def __repr__(self):
        return "(%i,%i)" % (self.line, self.col)
