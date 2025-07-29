import contextlib
import os
import shlex
import subprocess


@contextlib.contextmanager
def chdir(dest_dir):
    """Wraps a change of the current dir"""
    current_dir = os.getcwd()
    try:
        os.chdir(dest_dir)
        yield
    finally:
        os.chdir(current_dir)


def run(*cmd, **kwargs):
    """Run a command after expanding variables in it and log it.
    Raise CalledProcessError on failure
    """
    cmd = [os.path.expandvars(x) for x in cmd]
    cmd_str = " ".join([shlex.quote(x) for x in cmd])
    printf("## Running command '{}'".format(cmd_str))
    result = subprocess.run(cmd, **kwargs)
    result.check_returncode()


def printf(*args, **kwargs):
    """A print command which always flushes at the end

    This is useful in a build script whose output is redirected to a log file
    to ensure line order in the output is correct. Without flushing, this:

        print("hello")
        subprocess.call("ls")

    can print the output of `ls` before printing `hello`.
    """
    kwargs["flush"] = True
    print(*args, **kwargs)
