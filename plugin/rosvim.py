#!/usr/bin/env python
# encoding: utf-8

import vim
import vimp
import rosp
import rospkg


packages = dict()


def package():
    return packages[vimp.b['ros_package_name']]


def buf_enter():
    p = vimp.b['ros_package_name']
    if not p in packages:
        packages[p] = rosp.Package(p)
    if vimp.g['ros_make'] == 'all':
        cmd = 'set makeprg=rosmake\ ' + '\ '.join(packages.keys())
    else:
        cmd = 'set makeprg=rosmake\ ' + p
    vim.command(cmd)


def alternate():
    mapping = {'.h': '.cpp', '.cpp': '.h'}
    if vimp.buf.extension in mapping:
        altfile = vimp.buf.stem + mapping[vimp.buf.extension]
        for f in package().locate_files(altfile):
            vimp.edit(f)
            return
        print 'Nothing found!'
    else:
        print 'No alternate for this extension'


@vimp.function
def rosed(package_name, *file_names):
    try:
        pkg = rosp.Package(package_name)
    except rospkg.ResourceNotFound:
        print 'Package {0} not found'.format(package_name)
        return
    for fn in file_names:
        for f in pkg.locate_files(fn):
            vimp.edit(f)


@vimp.function
def rosed_complete(arg_lead, cmd_line, cursor_pos):
    """
    Returns a list of complete suggestions for :Rosed command.

    Arguments
    ---------
    arg_lead:
        The leading portion of the argument currently being completed on.
    cmd_line:
        The entire command line.
    cursor_pos:
        The cursor position in the line (byte index).
    """
    args = cmd_line[0:int(cursor_pos)].split(' ')
    if len(args) == 2:
        # still entering package name
        return '\n'.join(rosp.Package.list())
    elif len(args) >= 3:
        # package name already entered
        try:
            pkg = rosp.Package(args[1])
        except rospkg.ResourceNotFound:
            return ''
        pattern = arg_lead + '*'
        return '\n'.join(list(pkg.locate_files(pattern, mode='filename')))
