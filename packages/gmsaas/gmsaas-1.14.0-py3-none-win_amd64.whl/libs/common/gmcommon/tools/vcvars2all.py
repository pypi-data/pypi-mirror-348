"""
Load a vcvars script and prints the resulting environment in specified output format.
"""

import argparse
import subprocess
import sys
import json
import os


import re
import shlex
import sys


# These are transient vars which do not need to be modified
IGNORED_VARS = {"PWD", "OLDPWD", "_"}

# These vars contain Unix paths in Git Bash
UNIX_PATH_VARS = {"PATH", "HOME", "TMP", "TEMP"}

DRIVE_RX = re.compile("^([A-Za-z]):")


def unix_path_for_win_path(win_path):
    """
    Turns a Windows path like "C:\Foo\bar" into "/c/Foo/bar"
    """

    def convert_drive(match):
        return "/" + match.group(1)

    return DRIVE_RX.sub(convert_drive, win_path).replace("\\", "/")


def unix_path_list_for_win_path_list(win_path_list):
    """
    Turns a list of Windows Paths like "C:\Foo;C:\Bar" into "/c/Foo:/c/Bar"
    """
    paths = win_path_list.split(";")
    return ":".join(unix_path_for_win_path(x) for x in paths)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)
    parser.add_argument("vcvars_bat", help="The vcvars*.bat script to load")
    parser.add_argument("--output", help="Output target", required=True, choices=["bash", "json"])

    args = parser.parse_args()

    # Filter env to not pass non-ascii variables
    # which are not needed to build.
    ascii_env = os.environ.copy()
    for key in os.environ.keys():
        if not ascii_env[key].isascii():
            del ascii_env[key]

    process = subprocess.Popen(
        '("{}">nul)&&"python3" -c "import os; print(repr(os.environ))"'.format(args.vcvars_bat),
        stdout=subprocess.PIPE,
        shell=True,
        env=ascii_env,
    )
    stdout, _ = process.communicate()
    exitcode = process.wait()

    assert exitcode == 0, "Failed to load vcvars script"

    env = eval(stdout.decode("ascii").strip("environ"))

    if args.output == "json":
        json.dump(env, sys.stdout, indent=4)
    else:
        for key, value in env.items():
            if "(" in key:
                # Some environment variable names contain a "(".  For example
                # COMMONPROGRAMFILES(X86) or PROGRAMFILES(X86).
                # Bash does not like that, so skip them.  Hopefully they aren't
                # required.
                continue
            if key in IGNORED_VARS:
                continue
            if key in UNIX_PATH_VARS:
                value = unix_path_list_for_win_path_list(value)
            value = shlex.quote(value)
            print(f"export {key}={value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
