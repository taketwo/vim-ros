#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import vimp
import rosp
import rospkg

import filetypes as ft

packages = dict()


def package():
    return packages[vimp.var['b:ros_package_name']]


@vimp.function('ros#BufInit')
def buf_init(package_name):
    try:
        p = rosp.Package(package_name)
    except rospkg.common.ResourceNotFound:
        return
    vimp.var['b:ros_package_path'] = p.path
    vimp.var['b:ros_package_name'] = p.name
    if p.name not in packages:
        packages[p.name] = p
    ft.init()


def buf_enter():
    p = vimp.var['b:ros_package_name']
    if p not in packages:
        packages[p] = rosp.Package(p)
    if vimp.var['g:ros_build_system'] == 'catkin':
        _path = packages[p].path
        idx_src = _path.find('/src')
        if idx_src > -1:
            # Remove from the first '/src' to the end
            catkin_ws = _path[:idx_src]
        else:
            catkin_ws = _path
        make_cmd = 'catkin_make -C {0} --pkg '.format(catkin_ws)
    else:
        make_cmd = 'rosmake '
    if vimp.var['g:ros_make'] == 'all':
        vimp.opt['makeprg'] = make_cmd + ' '.join(packages.keys())
    else:
        vimp.opt['makeprg'] = make_cmd + p


# TODO: add 'command' decorator
def alternate():
    mapping = {'.h': ('.cpp', '.cc'), '.cpp': ('.h',), '.cc': ('.h',)}
    if vimp.buf.extension in mapping:
        for altextension in mapping[vimp.buf.extension]:
            altfile = vimp.buf.stem + altextension
            for f in package().locate_files(altfile):
                vimp.edit(f)
                return
            print('No {} alternate found!'.format(altextension))
        else:
            print('Unknown extension!')


@vimp.function('ros#Roscd')
def roscd(package_name):
    try:
        pkg = rosp.Package(package_name)
    except rospkg.ResourceNotFound:
        print('Package {0} not found'.format(package_name))
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
    return '\n'.join(sorted(rosp.Package.list()))


@vimp.function('ros#Rosed')
def rosed(package_name, *file_names):
    try:
        pkg = rosp.Package(package_name)
    except rospkg.ResourceNotFound:
        print('Package {0} not found'.format(package_name))
        return
    for fn in file_names:
        files = list(pkg.locate_files(fn))
        if len(files) == 0:
            print('File {0} not found'.format(fn))
        elif len(files) == 1:
            vimp.edit(files[0])
        else:
            f = vimp.inputlist('You have chosen a non-unique filename, please '
                               'pick one of the following:', files)
            if f is not None:
                vimp.edit(f)


@vimp.function('ros#TabRosed')
def tabrosed(package_name, *file_names):
    try:
        pkg = rosp.Package(package_name)
    except rospkg.ResourceNotFound:
        print('Package {0} not found'.format(package_name))
        return
    for fn in file_names:
        files = list(pkg.locate_files(fn))
        if len(files) == 0:
            print('File {0} not found'.format(fn))
        elif len(files) == 1:
            vimp.tabedit(files[0])
        else:
            f = vimp.inputlist('You have chosen a non-unique filename, please '
                               'pick one of the following:', files)
            if f is not None:
                vimp.tabedit(f)


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
        return '\n'.join(sorted(rosp.Package.list()))
    elif len(args) >= 3:
        # package name already entered
        try:
            pkg = rosp.Package(args[1])
        except rospkg.ResourceNotFound:
            return ''
        pattern = arg_lead + '*'
        return '\n'.join(set(pkg.locate_files(pattern, mode='filename')))
