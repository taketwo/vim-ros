import rosp
import vimp
import vimp.syntax
import subprocess


@vimp.function('ros#msg_complete')
def complete(findstart, base):
    if findstart == '1':
        return 0
    else:
        msgs = subprocess.check_output(['rosmsg', 'list']).strip().split('\n')
        builtin = ['bool', 'int8', 'uint8', 'int16', 'uint16', 'int32',
                   'uint32', 'int64', 'uint64', 'float32', 'float64', 'string',
                   'time', 'duration', 'Header']
        return [m for m in builtin + msgs if m.startswith(base)]


@vimp.function('ros#msg_goto_definition')
def goto_definition():
    text, group, start, end = vimp.syntax.get_entire_syntax_region()
    # We can go to the definition of only "complex" user-defined message types,
    # because build-in types have no definition. The only exception is the
    # "Header" type, which despite being a built-in is actually a "complex"
    # message type with a definition.
    if group == 'rosmsgBuiltInType' and text == 'Header':
        group, text = 'rosmsgType', 'std_msgs/Header'
    if group == 'rosmsgType':
        package_name, msg_type = text.split('/')
        for f in rosp.Package(package_name).locate_files(msg_type + '.msg'):
            vimp.edit(f)
    elif group == 'rosmsgBuiltInType':
        print '"{0}" is a built-in type and has no definition'.format(text)
    else:
        print 'Not a message type'


def detect():
    return vimp.buf.extension == '.msg'


def init():
    vimp.opt['l:filetype'] = 'rosmsg'
    vimp.opt['l:omnifunc'] = complete
    vimp.map('gd', goto_definition, 'n', buffer=True)
