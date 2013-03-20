#!/usr/bin/env python
# encoding: utf-8

import os
import vim
import fnmatch

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
