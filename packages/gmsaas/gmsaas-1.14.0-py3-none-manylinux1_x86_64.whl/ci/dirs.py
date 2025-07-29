from os.path import abspath, dirname, join, pardir

import common
from gmcommon.tools.systeminfo import IS_WINDOWS, IS_LINUX

CI_DIR = dirname(__file__)
PROJECT_DIR = abspath(join(CI_DIR, pardir))

if IS_WINDOWS:
    _PREBUILT_DIR = "win32"
elif IS_LINUX:
    _PREBUILT_DIR = "linux64"
else:
    _PREBUILT_DIR = "macx"

PREBUILT_OUT_DIR = join(PROJECT_DIR, "libs", "prebuilt", _PREBUILT_DIR)
PREBUILT_BIN_DIR = join(PREBUILT_OUT_DIR, "bin")
PREBUILT_LIB_DIR = join(PREBUILT_OUT_DIR, "lib")
