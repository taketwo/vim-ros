import vim
import vimp


def get_syntax_group(position=None):
    """
    Get the name of the syntax group of the character at the specified position
    in the current buffer.

    Arguments
    ---------
    position: Position
        Position of the character in question (line and column indices are
        zero-based). If omitted then the current cursor position is used.
    """
    line = position.line + 1 if position else 'line(".")'
    col = position.col + 1 if position else 'col(".")'
    return vim.eval('synIDattr(synID({0},{1},1),"name")'.format(line, col))


def get_entire_syntax_region(position=None):
    """
    Get the entire syntax region to which the characted at the specified
    position in the current buffer belongs.

    Arguments
    ---------
    position: Position
        Position of the character in question (line and column indices are
        zero-based). If omitted then the current cursor position is used.

    Returns
    -------
    tuple(region, group, start, end)
        region: str
            The text of the entire region.
        group: str
            Syntax group name.
        start: Position
            Position where the region starts.
        end: Position
            Position immediately following the character where the region ends.
    """
    seed = position or vimp.buf.cursor
    group = get_syntax_group(seed)
    start, end = seed, seed
    for p, c in vimp.buf.items(start=seed, reversed=False):
        if not group == get_syntax_group(p):
            break
        end = p
    for p, c in vimp.buf.items(start=seed, reversed=True):
        if not group == get_syntax_group(p):
            break
        start = p
    return (vimp.buf[start:end], group, start, end)
