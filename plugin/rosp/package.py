import os
import fnmatch
import rospkg
from subprocess import check_output, Popen, PIPE


class Package(object):

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
            found_path = rospkg.RosPack().get_path(self._name)
            if found_path != self._path:
                raise rospkg.ResourceNotFound
        else:
            self._path = rospkg.RosPack().get_path(name)
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

    def list_executables(self):
        """
        List executable files in the package.
        """
        cmd = 'catkin_find --without-underlays --libexec {0}'
        libexec_dir = check_output(cmd.format(self.name).split(' ')).strip()
        paths = ' '.join([p for p in [libexec_dir, self.path] if p])
        # The sequence of commands below is ported from functions
        # _roscomplete_exe and _roscomplete_find in rosbash suite.
        # Though the same result can be achived with native Python functions,
        # we (hopefully) simplify maintenance using this approach.
        regex1 = '! -regex ".*/[.].*"'
        regex2 = '! -regex ".*{0}/build/.*"'.format(self.path)
        find = 'find -L {0} -type f -perm /111 {1} {2}'.format(paths,
                                                               regex1,
                                                               regex2)
        sed = ['sed', '-e', r's/.*\/\(.*\)/\1/g']
        find_process = Popen(find.split(' '), stdout=PIPE)
        result = check_output(sed, stdin=find_process.stdout).strip()
        find_process.wait()
        return result.split('\n')

    def has_file(self, filename):
        return len(list(self.locate_files(filename))) > 0

    @classmethod
    def list(cls):
        return rospkg.RosPack().list()
