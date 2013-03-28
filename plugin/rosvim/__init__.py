#!/usr/bin/env python
# encoding: utf-8

import vimp
import rosp
import rospkg

fmgr = vimp.FunctionManager(name='rosvim.fmgr', plugin='ros')

import filetypes as ft

packages = dict()


def package():
    return packages[vimp.var['b:ros_package_name']]


@fmgr.function('BufInit')
def buf_init(package_name):
    p = rosp.Package(package_name)
    vimp.var['b:ros_package_root'] = p.path
    vimp.var['b:ros_package_name'] = p.name
    if not p.name in packages:
        packages[p.name] = p
    ft.init()


def buf_enter():
    p = vimp.var['b:ros_package_name']
    if not p in packages:
        packages[p] = rosp.Package(p)
    if vimp.var['g:ros_make'] == 'all':
        vimp.opt['makeprg'] = 'rosmake ' + ' '.join(packages.keys())
    else:
        vimp.opt['makeprg'] = 'rosmake ' + p


# TODO: add 'command' decorator
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


@fmgr.function('Roscd')
def roscd(package_name):
    try:
        pkg = rosp.Package(package_name)
    except rospkg.ResourceNotFound:
        print 'Package {0} not found'.format(package_name)
        return
    vimp.lcd(pkg.path)


@fmgr.function('RoscdComplete')
def roscd_complete(arg_lead, cmd_line, cursor_pos):
    """
    Returns a list of complete suggestions for :Roscd command.

    Arguments
    ---------
    arg_lead:
        The leading portion of the argument currently being completed on.
    cmd_line:
        The entire command line.
    cursor_pos:
        The cursor position in the line (byte index).
    """
    return '\n'.join(rosp.Package.list())


@fmgr.function('Rosed')
def rosed(package_name, *file_names):
    try:
        pkg = rosp.Package(package_name)
    except rospkg.ResourceNotFound:
        print 'Package {0} not found'.format(package_name)
        return
    for fn in file_names:
        for f in pkg.locate_files(fn):
            vimp.edit(f)


@fmgr.function('RosedComplete')
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
