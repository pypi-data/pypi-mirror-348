import os
import subprocess
import re
import textwrap
import time


def _assert_plaintext_match(needle, haystack):
    assert needle in haystack


def _assert_regex_match(needle, haystack):
    assert re.search(needle, haystack) is not None


def assert_run(args, extra_env=None, input=None, verbose=True, use_stderr=False):
    """Runs a command using CommandLauncher, returns stdout (or stderr if
    use_stderr=True) as a string on success, asserts on failure"""
    cm = CommandLauncher(args, extra_env=extra_env)
    cm.run(input=input, verbose=verbose)
    cm.assertSuccess()
    return cm.stderrdata if use_stderr else cm.stdoutdata


class CommandLauncher:
    def __init__(self, args, extra_env=None, cwd=None):
        """
        args: command to run, as an array
        extra_env: if set, must be a dict of environment variables to add to the current environment
        """
        self.proc = None
        self.args = args
        self.extra_env = extra_env
        self.cwd = cwd
        self.duration = None
        self.stdoutdata = ""
        self.stderrdata = ""
        self.returncode = 0

    def run(self, no_pipes=False, input=None, timeout=None, verbose=True):
        """Run the configured command and arguments and save its result code
        and outputs.
        no_pipes: Set to True to avoid blocking start of 'player'. Popen wait for the child to close
        stderr and stdout, but it is not the case with Qt startDetached and forked process.
        input: injected in stdin. Will be encoded to utf-8 if it is str
        timeout: Define a timeout is seconds. After this period, the command will be terminated
        and the outputs will be handled as usual
        """

        def from_utf8(utf8):
            s = str(utf8, "utf-8", errors="replace")
            # On Windows, at least with Android 4.4, adb uses \r\r\n to as
            # new line separator! Fix that.
            return s.replace("\r\r\n", "\r\n")

        # Customize environment
        if self.extra_env:
            env = dict(os.environ)
            env.update(self.extra_env)
        else:
            env = None

        start_time = time.time()
        if verbose:
            print(self._create_message_header(), flush=True)
        try:
            if no_pipes:
                self.proc = subprocess.Popen(self.args, env=env, cwd=self.cwd)
                self.returncode = self.proc.wait(timeout=timeout)
            else:
                self.proc = subprocess.Popen(
                    self.args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    cwd=self.cwd,
                )
                if type(input) is str:
                    input = bytes(input, "utf-8")
                out, err = self.proc.communicate(input=input, timeout=timeout)
        except subprocess.TimeoutExpired:
            print("Process timed out")
            self.abort()
            if not no_pipes:
                # Call communicate() again to read the data we received so far
                out, err = self.proc.communicate()

        if not no_pipes:
            self.stdoutdata = from_utf8(out)
            self.stderrdata = from_utf8(err)
            self.returncode = self.proc.returncode

        self.proc = None
        self.duration = time.time() - start_time
        if verbose:
            print(self._create_message_footer(), flush=True)

    def abort(self):
        assert self.proc is not None, "There is no process to kill"
        self.proc.kill()

    def assertMatch(self, testcase=None, returncode=None, stdout=None, stderr=None, plaintext=False):
        """match result of the command line

        - testcase TestCase instance, use pytest implementation if not provided
        - returncode=X checks return code
        - stdout=['expr1', 'expr2', ...] checks stdout matches all the regexps
        - stderr=['expr1', 'expr2', ...] checks stderr matches all the regexps
        - plaintext=True uses plain text instead of regular expression to match stdout
          and stderr. This is useful to check paths, because Windows paths must be
          escaped to be used in a regular expression.
        """
        if returncode is not None:
            msg = self._create_message(returncode=returncode, stdout=stdout, stderr=stderr)
            assert returncode == self.returncode, msg

        if plaintext:
            match_function = _assert_plaintext_match
        else:
            match_function = _assert_regex_match

        if stdout is not None:
            text = str(self.stdoutdata)
            for regexpr in stdout:
                match_function(regexpr, text)

        if stderr is not None:
            text = str(self.stderrdata)
            for regexpr in stderr:
                match_function(regexpr, text)

    def assertSuccess(self, testcase=None):
        """Checks the return code is 0, fails the testcase if it's not"""
        assert self.returncode == 0, self._create_message(returncode=0)

    def assertFailure(self, returncode, testcase=None):
        assert self.returncode == returncode, self._create_message(returncode=returncode)

    def matches(self, **kwargs):
        """match result of the command line:
        o use returncode=X to check return code
        o use stdout=['expr1', 'expr2', ...] to compare stdout output regarding multiple regexps
        o use stderr=['expr1', 'expr2', ...] to compare stderr output regarding multiple regexps

        When running from a test case, use assertMatch instead.
        """
        if "returncode" in kwargs:
            if kwargs["returncode"] != self.returncode:
                print("return code %s does not match %s" % (self.returncode, kwargs["returncode"]))
                return False

        if "stdout" in kwargs:
            for regexpr in kwargs["stdout"]:
                if not re.search(regexpr, str(self.stdoutdata)):
                    print("stdout does not match regexp %s: %s" % (regexpr, self.stdoutdata))
                    return False

        if "stderr" in kwargs:
            for regexpr in kwargs["stderr"]:
                if not re.search(regexpr, self.stderrdata):
                    print("stderr does not match regexp %s: %s" % (regexpr, self.stderrdata))
                    return False

        return True

    def doesnotmatch(self, **kwargs):
        """make sure results of the command line do not match:
        o returncode=X to check return code
        o stdout=['expr1', 'expr2', ...] to compare stdout output regarding multiple regexps
        o stderr=['expr1', 'expr2', ...] to compare stderr output regarding multiple regexps
        """
        if "returncode" in kwargs:
            if kwargs["returncode"] == self.returncode:
                print("return code %s matches %s" % (self.returncode, kwargs["returncode"]))
                return False

        if "stdout" in kwargs:
            for regexpr in kwargs["stdout"]:
                if re.search(regexpr, self.stdoutdata):
                    print("stdout matches regexp %s: %s" % (regexpr, self.stdoutdata))
                    return False

        if "stderr" in kwargs:
            for regexpr in kwargs["stderr"]:
                if re.search(regexpr, self.stderrdata):
                    print("stderr matches regexp %s: %s" % (regexpr, self.stderrdata))
                    return False

        return True

    def stdout_is_empty(self):
        """check if stdout is empty"""
        # None or ""
        if not self.stdoutdata:
            return True
        print("stdout is not empty: %s" % self.stdoutdata)
        return False

    def stderr_is_empty(self):
        """check if stderr is empty"""
        # None or ""
        if not self.stderrdata:
            return True
        print("stderr is not empty: %s" % self.stderrdata)
        return False

    def _create_message(self, **kwargs):
        """Create a string of the form
        Keyword arguments are here to show expected values and so improve assertion message.

        Command: "<cmd>" "<arg1>" "<arg2>"...
          extra_env:
            <varname>=<value>
            <varname>=<value>
          ret: <command exit code>
          duration: <command duration in seconds>s
          out:
            <command stdout>
          err:
            <command stderr>
          expected
            stdout: ...
            stderr: ...
            returncode: ...
        /Command
        """
        return self._create_message_header() + "\n" + self._create_message_footer(**kwargs)

    def _create_message_header(self):
        cmd_string = " ".join(['"{}"'.format(x) for x in self.args])
        msg = ["Command: {}".format(cmd_string)]

        if self.extra_env:
            msg.append("  extra_env:")
            for key, value in self.extra_env.items():
                msg.append("    {}={}".format(key, value))

        return "\n".join(msg)

    def _create_message_footer(self, **kwargs):
        def format_multiline(title, content):
            if content.strip():
                content = textwrap.indent(content.rstrip(), "    ")
                return "  {title}:\n{content}".format(title=title, content=content)
            else:
                return "  {}:".format(title)

        msg = [
            "  ret: {}".format(self.returncode),
            "  duration: {:.3f}s".format(self.duration),
            format_multiline("out", self.stdoutdata),
            format_multiline("err", self.stderrdata),
        ]

        title_written = False
        for key, value in kwargs.items():
            if value is not None:
                if not title_written:
                    msg.append("  expected:")
                    title_written = True
                msg.append("    {}: {}".format(key, value))

        msg.append("/Command")

        return "\n".join(msg) + "\n"
