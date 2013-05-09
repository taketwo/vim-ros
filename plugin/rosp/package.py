import os
import fnmatch
import rospkg


class Package(object):

    _rospack = rospkg.RosPack()

    def __init__(self, name):
        """
        Arguments
        ---------
        name: str
            Could be either name, or absolute path to the package. In the case
            if package with this name or under this path does not exist
            'rospkg.ResourceNotFound' exception will be raised.
        """
        if os.path.isabs(name):
            self._path = os.path.normpath(name)
            self._name = os.path.split(self._path)[1]
            found_path = self._rospack.get_path(self._name)
            if found_path != self._path:
                raise rospkg.ResourceNotFound
        else:
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
        return len(list(self.locate_files(filename))) > 0

    @classmethod
    def list(cls):
        return cls._rospack.list()
