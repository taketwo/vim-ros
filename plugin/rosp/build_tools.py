import os
import os.path


class BuildTool(object):
    def __init__(self, package_path, ws_path):
        self._package_path = package_path
        self._package_name = os.path.split(package_path)[1]
        self._ws_path = ws_path

    @property
    def ws_path(self):
        return self._ws_path


class CatkinBuild(BuildTool):
    def __init__(self, package_path, ws_path):
        super(CatkinBuild, self).__init__(package_path, ws_path)

    def get_make_command(self, catkin_make_options="", targets="workspace"):
        make_cmd = "catkin build --workspace {0}".format(self._ws_path)
        if targets == "this":
            targets = [self._package_name]
        elif targets == "workspace":
            targets = []
        make_cmd += " " + " ".join(targets)
        return make_cmd

    @classmethod
    def find_enclosing_workspace(cls, path):
        try:
            from catkin_tools.metadata import find_enclosing_workspace
            return find_enclosing_workspace(path)
        except:
            return None


class CatkinMake(BuildTool):
    def __init__(self, package_path, ws_path):
        super(CatkinMake, self).__init__(package_path, ws_path)

    def get_make_command(self, catkin_make_options="", targets="workspace"):
        make_cmd = "catkin_make -C {0} {1}".format(self._ws_path, catkin_make_options)
        if targets == "this":
            make_cmd += " --pkg " + self._package_name
        elif targets != "workspace":
            make_cmd += " --pkg " + " ".join(targets)
        return make_cmd

    @classmethod
    def find_enclosing_workspace(cls, path):
        p = path
        while p != "/":
            tag = os.path.join(p, ".catkin_workspace")
            if os.path.isfile(tag):
                return p
            p = os.path.dirname(p)
        return None


def create_build_tool(package_path):
    for builder_cls in (CatkinBuild, CatkinMake):
        ws_path = builder_cls.find_enclosing_workspace(package_path)
        if ws_path is not None:
            return builder_cls(package_path, ws_path)
    return None
