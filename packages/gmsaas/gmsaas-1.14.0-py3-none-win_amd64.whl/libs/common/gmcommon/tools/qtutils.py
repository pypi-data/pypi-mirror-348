import os
import json
from subprocess import check_output

from .systeminfo import IS_LINUX, IS_WINDOWS

VCVARS_PATH = r"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
VCVARS2ALL_PATH = os.path.join(os.path.dirname(__file__), "vcvars2all.py")


def _read_required_qt_version(pro_path):
    """Parse pro_path, returns the value of REQUIRED_QT_VERSION"""
    with open(pro_path) as fp:
        for line in fp.readlines():
            try:
                key, value = line.split("=")
            except ValueError:
                continue
            if key.strip() == "REQUIRED_QT_VERSION":
                return value.strip()
    raise Exception("Failed to read REQUIRED_QT_VERSION from {}".format(pro_path))


def _find_qt_install_dir(pro_path):
    qt_version = _read_required_qt_version(pro_path)
    if IS_WINDOWS:
        prefix = os.path.join(r"C:\Qt", "Qt" + qt_version + "-msvc")
    else:
        prefix = os.path.join("~", "Qt" + qt_version)
    install_dir = os.path.join(prefix, qt_version)
    return install_dir


class QtInstall:
    def __init__(self, install_dir):
        # qt_install_dir can be:
        # /opt/Qt5.12.8/5.12.8/ (offline installer)
        # /opt/Qt/5.12.8/ (online installer)
        self.install_dir = install_dir
        self.version = os.path.basename(self.install_dir)
        self.compiler = self._get_qt_compiler()
        self.qt_dir = os.path.join(self.install_dir, self.compiler)
        self.qmake_dir = os.path.join(self.qt_dir, "bin")
        self.lib_dir = os.path.join(self.qt_dir, "lib")
        self.plugins_dir = os.path.join(self.qt_dir, "plugins")
        self.qml_dir = os.path.join(self.qt_dir, "qml")
        self.make_cmd = "jom.exe" if IS_WINDOWS else "make"

    def _get_qt_compiler(self):
        compiler_dirs = [
            x.name
            for x in os.scandir(self.install_dir)
            if x.is_dir() and x.name != "Src" and not x.name.startswith(".")
        ]
        if IS_WINDOWS:
            compiler_dirs = [name for name in compiler_dirs if name.startswith("msvc") and name.endswith("64")]
        assert len(compiler_dirs) == 1, "Multiple compilers found {}: aborting.".format(compiler_dirs)
        return compiler_dirs[0]

    def setup_env(self):
        def _prepend_env(var_name, new_dir):
            try:
                os.environ[var_name] = new_dir + os.path.pathsep + os.environ[var_name]
            except KeyError:
                os.environ[var_name] = new_dir

        _prepend_env("PATH", self.qmake_dir)
        os.environ["MAKE_CMD"] = self.make_cmd

        if IS_LINUX:
            # Define/alter LD_LIBRARY_PATH so that Qt can find its dependencies
            # when linking and when running binaries
            _prepend_env("LD_LIBRARY_PATH", self.lib_dir)
            # Set Qt env vars as aqtinstall's doc suggests
            os.environ["QT_PLUGIN_PATH"] = self.plugins_dir
            os.environ["QML_IMPORT_PATH"] = self.qml_dir
            os.environ["QML2_IMPORT_PATH"] = self.qml_dir
        elif IS_WINDOWS:
            os.environ["QMAKESPEC"] = "win32-clang-msvc"
            # Make sure MSVC env is well loaded
            output = check_output(["python3", VCVARS2ALL_PATH, VCVARS_PATH, "--output", "json"]).decode("utf-8")
            env = json.loads(output)
            # os.environ = env
            os.environ.clear()
            os.environ.update(env)


def get_qt_install(pro_path):
    qt_install_dir = os.environ.get("QT_INSTALL_DIR", _find_qt_install_dir(pro_path))
    qt_install_dir = os.path.expanduser(qt_install_dir)
    return QtInstall(qt_install_dir)
