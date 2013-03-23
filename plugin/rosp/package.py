import os
import fnmatch
import rospkg


class Package(object):

    _rospack = rospkg.RosPack()

    def __init__(self, name):
        # will raise rospkg.ResourceNotFound if the package could not be found
        self._path = self._rospack.get_path(name)
        self._name = name

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

    @classmethod
    def list(cls):
        return cls._rospack.list()
