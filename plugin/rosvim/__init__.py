#!/usr/bin/env python
# encoding: utf-8

import vimp
import rosp
import rospkg

import filetypes as ft

packages = dict()


def package():
    return packages[vimp.var['b:ros_package_name']]


@vimp.function('ros#BufInit')
def buf_init(package_name):
    p = rosp.Package(package_name)
    vimp.var['b:ros_package_path'] = p.path
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


@vimp.function('ros#Roscd')
def roscd(package_name):
    try:
        pkg = rosp.Package(package_name)
    except rospkg.ResourceNotFound:
        print 'Package {0} not found'.format(package_name)
        return
    vimp.lcd(pkg.path)


@vimp.function('ros#RoscdComplete')
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


@vimp.function('ros#Rosed')
def rosed(package_name, *file_names):
    try:
        pkg = rosp.Package(package_name)
    except rospkg.ResourceNotFound:
        print 'Package {0} not found'.format(package_name)
        return
    for fn in file_names:
        files = list(pkg.locate_files(fn))
        if len(files) == 0:
            print 'File {0} not found'.format(fn)
        elif len(files) == 1:
            vimp.edit(files[0])
        else:
            f = vimp.inputlist('You have chosen a non-unique filename, please '
                               'pick one of the following:', files)
            if f is not None:
                vimp.edit(f)


@vimp.function('ros#RosedComplete')
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
        return '\n'.join(set(pkg.locate_files(pattern, mode='filename')))
