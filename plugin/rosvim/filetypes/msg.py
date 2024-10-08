from __future__ import print_function

import vim
import rosp
import vimp
import vimp.syntax
import subprocess
from vimp.complete import Complete


@vimp.function('ros#msg_complete')
class MsgComplete(Complete):

    PATTERN = r'^(?=\S*)'

    def get_completions(self):
        BUILTIN = ['bool', 'int8', 'uint8', 'int16', 'uint16', 'int32',
                   'uint32', 'int64', 'uint64', 'float32', 'float64', 'string',
                   'time', 'duration', 'Header']
        line = vim.current.line[:vim.current.window.cursor[1]]
        t = line.split('/')
        if len(t) > 2:
            # Does not make sense
            return []
        elif len(t) == 2:
            return [
                msg.split("/")[1]
                for msg in rosp.list_messages()
                if msg.split("/")[0] == t[0]
            ]
        else:
            return BUILTIN + rosp.list_messages()


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
        # The type name may fully-qualified or relative to the package
        if '/' in text:
            package_name, msg_type = text.split('/')
        else:
            package_name, msg_type = vimp.var['b:ros_package_name'], text
        for f in rosp.Package(package_name).locate_files(msg_type + '.msg'):
            vimp.edit(f)
    elif group == 'rosmsgBuiltInType':
        print('"{0}" is a built-in type and has no definition'.format(text))
    else:
        print('Not a message type')


def detect():
    return vimp.buf.extension == '.msg'


def init():
    vimp.opt['l:filetype'] = 'rosmsg'
    vimp.opt['l:omnifunc'] = MsgComplete
    vimp.opt['l:commentstring'] = '# %s'
    vimp.map('gd', goto_definition, 'n', buffer=True)
