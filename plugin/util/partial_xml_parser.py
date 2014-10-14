from util.position import Position


def _at(lines, pos):
    try:
        return lines[pos.line][pos.col]
    except IndexError:
        return None


def _between(lines, s, e):
    if s.line == e.line:
        return lines[s.line][s.col:e.col + 1]
    return ''.join([lines[s.line][s.col:]] +
                   [lines[i] for i in range(s.line + 1, e.line - 1)] +
                   [lines[e.line][:e.col + 1]])


def _find(lines, pos, char):
    if _at(lines, pos) == char:
        return pos
    i, j = pos.line, pos.col
    try:
        line = lines[i][j:]
    except IndexError:
        line = ''
    while True:
        try:
            f = line.index(char)
            return Position(i, len(lines[i]) - len(line) + f)
        except ValueError:
            i = i + 1
            if i >= len(lines):
                return None
            line = lines[i]


def _rfind(lines, pos, char):
    if _at(lines, pos) == char:
        return pos
    i, j = pos.line, pos.col
    try:
        line = lines[i][:j]
    except IndexError:
        line = ''
    while True:
        try:
            f = line.rindex(char)
            return Position(i, f)
        except ValueError:
            i = i - 1
            if i < 0:
                return None
            line = lines[i]


class Tag(object):

    def __init__(self, text):
        import re
        self.text = text
        self.attr = dict()
        self.partial = False if re.match(r'<.*>', text) else True
        self.comment = True if re.match(r'<!--.*-->', text) else False
        if self.comment:
            return
        g = re.match(r'<(\w+) *(.*?)[ /]?>?$', text)
        if not g:
            return
        self.name = g.groups()[0]
        self.attr = dict(re.findall(r'(\w+)="([^"]*)" ?', g.groups()[1]))


def get_inner_tag(lines, pos):
    so = _rfind(lines, pos, '<')
    sc = _rfind(lines, pos, '>')
    if sc is not None and sc != pos and sc > so:
        return None
    ec = _find(lines, pos, '>')
    eo = _find(lines, pos, '<')
    if ec is None or (eo is not None and eo != pos and eo < ec):
        return Tag(_between(lines, so, pos))
    return Tag(_between(lines, so, ec))


def get_inner_attr(lines, pos):
    import re
    try:
        begin = lines[pos.line][:pos.col]
        end = lines[pos.line][pos.col:]
    except IndexError:
        return None
    matches = re.findall(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)="(\w?)', begin)
    if not matches:
        return None
    name, value = matches[-1]
    try:
        e = end.index('"')
        return name, value + end[:e]
    except ValueError:
        return name, value
