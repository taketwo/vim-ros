import os
import fnmatch
import subprocess


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


def list_packages():
    cmd = 'rospack list-names'
    return subprocess.check_output(cmd.split()).strip().split('\n')


def find_package(package_name):
    cmd = 'rospack find {0}'.format(package_name)
    return subprocess.check_output(cmd.split()).strip()
