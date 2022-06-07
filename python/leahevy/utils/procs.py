import shlex
import subprocess
import sys
import time
import os
import re

from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor

from leahevy.utils.log import print


def _enqueue_output(file, queue, done, idx):
    for line in iter(file.readline, ""):
        queue.put(line)
    file.close()
    done[idx] = True


def _read_popen_pipes(p):
    with ThreadPoolExecutor(2) as pool:
        q_stdout, q_stderr = Queue(), Queue()

        done = {0: False, 1: False}

        pool.submit(_enqueue_output, p.stdout, q_stdout, done, 0)
        pool.submit(_enqueue_output, p.stderr, q_stderr, done, 1)

        while True:
            if p.poll() is not None:
                if all(done.values()) and q_stdout.empty() and q_stderr.empty():
                    break

            out_line = err_line = None

            try:
                out_line = q_stdout.get_nowait()
            except Empty:
                pass

            try:
                err_line = q_stderr.get_nowait()
            except Empty:
                pass

            if not out_line and not err_line:
                continue

            yield (out_line, err_line)


def run(
    cmd: str | list[str],
    communicate: bool = False,
    do_print: bool = True,
    on_out=None,
    on_err=None,
    stdin_data: str | None = None,
    shell: bool = False,
    split_args: bool = True,
) -> tuple[str | None, str | None, int]:
    """
    Runs a shell command and provides a variety of options, such as
    asynchronously getting the stdout and stderr values.

    :param str|list[str] cmd: The command as string or list of strings.
    :param bool communicate: if True: uses p.communicate() instead of
        printing the output asynchronously.
    :param bool do_print: if True and communicate is False:
        print the asynchronous output.
    :param func(process, line) on_out: Function to run on each stdout line.
    :param func(process, line) on_err: Function to run on each stderr line.
    :param str stdin_data: Input string for stdin.
    :param bool shell: Run in shell mode using the bash shell.
    :param bool split_args: Split the cmd string in args (useful when using shell=True).
    :return: The stdout string, stderr string, and the return code
        (or None for the strings).
    :rtype: tuple[str | None, str | None, int]
    """
    if isinstance(cmd, str):
        if split_args:
            cmd = shlex.split(cmd)
        else:
            cmd = [cmd]

    kwargs = {
        "stdin": subprocess.PIPE,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "universal_newlines": True,
        "text": True,
    }

    if shell:
        kwargs["shell"] = True
        kwargs["executable"] = "/bin/bash"

    process = subprocess.Popen(cmd, **kwargs)

    stdoutdata, stderrdata = "", ""

    if not communicate:
        if stdin_data and process.stdin:
            process.stdin.write(stdin_data)
            process.stdin.flush()
        for out_line, err_line in _read_popen_pipes(process):
            if out_line:
                if on_out:
                    on_out(process, re.sub(os.linesep + r"\Z", "", out_line))
                if do_print:
                    print(out_line, end="", file=sys.stdout)
                    sys.stdout.flush()
                stdoutdata += out_line
            if err_line:
                if on_err:
                    on_err(process, re.sub(os.linesep + r"\Z", "", err_line))
                if do_print:
                    print(err_line, end="", file=sys.stderr)
                    sys.stderr.flush()
                stderrdata += err_line
    else:
        stdoutdata, stderrdata = process.communicate(input=stdin_data)

    if not stdoutdata:
        stdoutdata = None
    if not stderrdata:
        stderrdata = None

    while process.poll() is None:
        time.sleep(0.5)

    return stdoutdata, stderrdata, int(process.returncode)


def write_stdin(process, text):
    process.stdin.write(text)
    process.stdin.flush()


__all__ = ["run", "write_stdin"]


if __name__ == "__main__":
    print("#1")
    run("echo test")

    print("#2")
    run(
        'for i in {1..3}; do echo "out $i"; echo "err $i" >&2; done',
        shell=True,
        split_args=False,
    )

    print("#3")
    out, err, ret = run("echo test", communicate=True, shell=True, split_args=False)
    assert out == "test\n"
    assert err is None
    assert ret == 0

    print("#4")
    out, err, ret = run("echo test >&2", communicate=True, shell=True, split_args=False)
    assert out is None
    assert err == "test\n"
    assert ret == 0

    print("#5")
    _, _, ret = run("false", communicate=True)
    assert ret == 1

    print("#6")
    out, err, ret = run(
        "read var1; read var2; echo $var1; echo $var2",
        stdin_data="1\n2\n",
        communicate=True,
        shell=True,
        split_args=False,
    )
    assert out == "1\n2\n"
    assert err is None
    assert ret == 0

    print("#7")
    run(
        "read var1; read var2; echo $var1; echo $var2",
        stdin_data="1\n2\n",
        shell=True,
        split_args=False,
    )

    print("#8")

    def on_out(process, line):
        print(f"OUT:{line}.")

    run(
        "read var1; read var2; echo $var1; echo $var2",
        stdin_data="1\n2\n",
        do_print=False,
        shell=True,
        split_args=False,
        on_out=on_out,
    )

    print("#9")
    _, _, ret = run("git status")
    assert ret == 0

    print("#10")

    def on_out2(process, line):
        if line == "Name:":
            write_stdin(process, "Sam\n")

    run(
        "echo \"Name:\"; read var1; echo \"Your name is: $var1.\"",
        shell=True,
        split_args=False,
        on_out=on_out2,
    )

    print("#11")

    def on_out3(process, line):
        process.kill()

    _, _, ret = run(
        "echo 1; read var1; echo 2",
        shell=True,
        split_args=False,
        on_out=on_out3,
    )
    assert ret == -9

    print("All success")
