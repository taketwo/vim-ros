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
        p = rosp.Package(str(package_name))
    except rospkg.common.ResourceNotFound:
        return
    vimp.var['b:ros_package_path'] = p.path
    vimp.var['b:ros_package_name'] = p.name
    if p.build_tool is not None:
        vimp.var['b:ros_package_workspace'] = p.build_tool.ws_path
    if p.name not in packages:
        packages[p.name] = p
    ft.init()


def buf_enter():
    p = package()
    if p.build_tool is not None:
        vimp.opt["makeprg"] = p.build_tool.get_make_command(
            catkin_make_options=vimp.var["g:ros_catkin_make_options"],
            targets=vimp.var["g:ros_make"],
        )


# TODO: add 'command' decorator
def alternate():
    mapping = {'.h': ('.cpp', '.cc'), '.cpp': ('.h', '.hpp'), '.cc': ('.h', ),
               '.hpp': ('.cpp', '.impl'), '.impl': ('.hpp', )}
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


def _generic_rosed(vim_func, package_name, *file_names):
    """
    Helper method to edit a file using a specific `vim_func`.

    Arguments
    ---------
    vim_func:
        Reference to a function defined in the `vimp` module.
    """
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
            vim_func(files[0])
        else:
            f = vimp.inputlist('You have chosen a non-unique filename, please '
                               'pick one of the following:', files)
            if f is not None:
                vim_func(f)


@vimp.function('ros#Rosed')
def rosed(package_name, *file_names):
    _generic_rosed(vimp.edit, package_name, *file_names)


@vimp.function('ros#TabRosed')
def tabrosed(package_name, *file_names):
    _generic_rosed(vimp.tabedit, package_name, *file_names)


@vimp.function('ros#SpRosed')
def sprosed(package_name, *file_names):
    _generic_rosed(vimp.split, package_name, *file_names)


@vimp.function('ros#VspRosed')
def vsprosed(package_name, *file_names):
    _generic_rosed(vimp.vsplit, package_name, *file_names)


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
