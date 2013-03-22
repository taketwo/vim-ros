#!/usr/bin/env python
# encoding: utf-8

import os
import vim
import fnmatch
import subprocess

import vimp

packages = dict()


class Package(object):

    def __init__(self, path):
        self._path = path
        self._name = os.path.split(path)[1]

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    def locate_files(self, pattern, mode='absolute'):
        """
        Locate all files matching supplied filename pattern in and below
        package root directory.
        Recipe from: http://bit.ly/bOlAHw

        Arguments
        ---------
        mode: 'absolute' | 'filename'
            Controls how the function outputs found files, whether absolute
            paths or just filenames.
        """
        exclude = ['.git', '.hg', '.svn', 'bin', 'build', 'lib']
        for path, dirs, files in os.walk(os.path.abspath(self._path)):
            for d in exclude:
                if d in dirs:
                    dirs.remove(d)
            for filename in fnmatch.filter(files, pattern):
                if mode == 'absolute':
                    yield os.path.join(path, filename)
                else:
                    yield filename

    def has_file(self, filename):
        return len([self.locate_files(filename)]) > 0


def package():
    return packages[vimp.b['ros_package_name']]


def buf_enter():
    p = vimp.b['ros_package_name']
    if not p in packages:
        packages[p] = Package(vimp.b['ros_package_root'])
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


def list_packages():
    cmd = 'rospack list-names'
    return subprocess.check_output(cmd.split()).strip().split('\n')


def find_package(package_name):
    cmd = 'rospack find {0}'.format(package_name)
    return subprocess.check_output(cmd.split()).strip()


def vim_function(f):
    def wrapped():
        args = vimp.a['000']
        vimp.l['result'] = f(*args)
    return wrapped


@vim_function
def rosed(package_name, *file_names):
    path = find_package(package_name)
    for fn in file_names:
        for f in Package(path).locate_files(fn):
            vimp.edit(f)


@vim_function
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
        return '\n'.join(list_packages())
    elif len(args) >= 3:
        # package name already entered
        path = find_package(args[1])
        pattern = arg_lead + '*'
        files = list(Package(path).locate_files(pattern, mode='filename'))
        return '\n'.join(files)
