import os
import time
import ctypes

from contextlib import contextmanager


class TimeoutError(Exception):
    pass


def wait_for(condition_function, max_timeout=30, poll_interval=1, err_msg=None):
    start = time.time()
    while not condition_function():
        time.sleep(poll_interval)
        duration = time.time() - start
        if duration > max_timeout:
            message = "waited for too long ({:.3f} seconds).".format(duration)
            if err_msg:
                message = message + " " + err_msg
            raise TimeoutError(message)


@contextmanager
def environ_saver():
    """
    Saves os.environ so that any changes to it are reverted, even if an
    exception is raised.

    Usage:

        with environ_saver():
            os.environ['FOO'] = 'bar'
            # $FOO equals 'bar' here

        # $FOO is back to its older value (or undefined) here
    """
    old_environ = dict(os.environ)
    try:
        yield
    finally:
        # We do not do `os.environ = old_environ` because os.environ is not a
        # dict: it is a special object with a dict-like API. Assigning to it
        # would replace it with a plain dict. To avoid that, update it in
        # place.
        os.environ.clear()
        os.environ.update(old_environ)


def is_admin():
    try:
        admin = os.getuid() == 0
    except AttributeError:
        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return admin
