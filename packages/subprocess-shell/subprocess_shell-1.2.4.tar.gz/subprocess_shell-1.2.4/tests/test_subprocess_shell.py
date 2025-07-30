import itertools
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import typing as t

import hypothesis
import hypothesis.strategies as h_strategies
import pytest

import subprocess_shell
from subprocess_shell import *

subprocess_shell._FORCE_ASYNC = None


DATETIME_PATTERN = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d{6})?"


def RETURNED_PATTERN(code: t.Union[str, int] = r"-?\d+"):
    return rf"(returned {code}( after (((\d+h )?\d+m )?\d+s|\d+\.\d+s|\d+ms)| immediately)?)"


STATUS_PATTERN = rf"(running|{RETURNED_PATTERN()})"

_v_ = (
    "import sys\nstdin = sys.stdin.read()\nprint('stdout', stdin)\nprint('stderr',"
    " stdin, file=sys.stderr)"
)
I_ARGUMENTS = [sys.executable, "-c", _v_]

I_STDOUT_PATTERN = lambda datetime_name, stdin_pattern: rf"""
╭─ (?P<_header>(?P<{datetime_name}>{DATETIME_PATTERN}) `{re.escape(subprocess_shell._get_command(I_ARGUMENTS))}`) {STATUS_PATTERN}
│ stdout {stdin_pattern}
╰─ (?P=_header) {RETURNED_PATTERN()}

"""[
    1:-1
]
I_STDERR_PATTERN = lambda datetime_name, stdin_pattern: rf"""
┏━ (?P<_header>(?P<{datetime_name}>{DATETIME_PATTERN}) `{re.escape(subprocess_shell._get_command(I_ARGUMENTS))}`) {STATUS_PATTERN}
┣ stderr {stdin_pattern}
┗━ (?P=_header) {RETURNED_PATTERN()}

"""[
    1:-1
]
ECHO_ARGUMENTS = lambda string: (
    [sys.executable, "-c", f"print({repr(string)})"]
    if os.name == "nt"
    else ["echo", string]
)
CAT_ARGUMENTS = (
    [
        sys.executable,
        "-c",
        "import shutil, sys; shutil.copyfileobj(sys.stdin, sys.stdout)",
    ]
    if os.name == "nt"
    else ["cat", "-"]
)


def test_1_trivial(capsys):
    _v_ = lambda start_kwargs: (
        [sys.executable, "-c", ""] if os.name == "nt" else ["sleep", "0"]
    )
    _test(_v_, "", "", capsys)


def test_1_wait(capsys):
    _v_ = itertools.product([False, True], [False, True], [None, "utf-8", "latin-1"])
    for stdout, stderr, encoding in _v_:

        def assert_(groups):
            assert not (stdout and stderr and groups["d1"] != groups["d2"])

        _test(
            lambda start_kwargs: I_ARGUMENTS,
            I_STDOUT_PATTERN("d1", "") if stdout else "",
            I_STDERR_PATTERN("d2", "") if stderr else "",
            capsys,
            wait=dict(stdout=stdout, stderr=stderr, encoding=encoding),
            assert_=assert_,
        )


def test_1_io(capsys):
    for stdout, stderr, bytes, encoding in itertools.product(
        [False, True], [False, True], [False, True], [None, "utf-8", "latin-1"]
    ):
        stdout_object = f"stdout this{os.linesep}"
        stderr_object = f"stderr this{os.linesep}"

        if bytes:
            _kwargs = dict(encoding=encoding) if encoding is not None else {}
            stdout_object = stdout_object.encode(**_kwargs)
            stderr_object = stderr_object.encode(**_kwargs)

        expected = {
            (False, False): None,
            (True, False): stdout_object,
            (False, True): stderr_object,
            (True, True): (stdout_object, stderr_object),
        }[(stdout, stderr)]

        def assert_(groups):
            assert not (not stdout and not stderr and groups["d1"] != groups["d2"])

        _test(
            lambda start_kwargs: I_ARGUMENTS,
            "" if stdout else I_STDOUT_PATTERN("d1", "this"),
            "" if stderr else I_STDERR_PATTERN("d2", "this"),
            capsys,
            write=write("this", encoding=encoding),
            read=read(stdout=stdout, stderr=stderr, bytes=bytes, encoding=encoding),
            result=expected,
            assert_=assert_,
        )


def test_1_file(capsys):
    _v_ = tempfile.NamedTemporaryFile(delete=False)
    with _v_ as stdout_file, tempfile.NamedTemporaryFile(delete=False) as stderr_file:
        try:
            stdout_file.close()
            stderr_file.close()

            _v_ = dict(stdout=stdout_file.name, stderr=stderr_file.name)
            _test(lambda start_kwargs: I_ARGUMENTS, "", "", capsys, start=_v_)

            with open(stdout_file.name, "rb") as file:
                assert file.read() == f"stdout {os.linesep}".encode()

            with open(stderr_file.name, "rb") as file:
                assert file.read() == f"stderr {os.linesep}".encode()

        finally:
            os.unlink(stdout_file.name)
            os.unlink(stderr_file.name)


def test_1_function(capsys):
    stdout_list = [b""]
    stderr_list = [b""]

    def assert_(_):
        nonlocal stdout_list
        nonlocal stderr_list

        for _ in range(10):
            if stdout_list[-1] is None and stderr_list[-1] is None:
                break

            time.sleep(0.01)

        else:
            raise Exception

        assert b"".join(stdout_list[:-1]) == f"stdout {os.linesep}".encode()
        assert b"".join(stderr_list[:-1]) == f"stderr {os.linesep}".encode()

        stdout_list[:] = [b""]
        stderr_list[:] = [b""]

    _v_ = dict(stdout=stdout_list.append, stderr=stderr_list.append)
    _test(lambda start_kwargs: I_ARGUMENTS, "", "", capsys, start=_v_, assert_=assert_)


def test_1_fail(capsys):
    arguments = [sys.executable, "-c", "import sys; sys.exit(1)"]

    _v_ = lambda start_kwargs: arguments
    _test(_v_, "", "", capsys, wait=dict(return_codes=None), result=1)

    _test(
        lambda start_kwargs: arguments,
        "",
        "",
        capsys,
        wait=dict(return_codes=(0,)),
        raises=subprocess_shell.ProcessFailedError,
        raises_pattern=rf"^{DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(arguments))}` {RETURNED_PATTERN(1)}$",
    )

    _v_ = lambda start_kwargs: arguments
    _test(_v_, "", "", capsys, wait=dict(return_codes=(1,)), result=1)


def test_2_trivial(capsys):
    _v_ = rf"""
╭─ (?P<_header>{DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(CAT_ARGUMENTS))}`) {STATUS_PATTERN}
│ this
╰─ (?P=_header) {RETURNED_PATTERN(0)}

"""
    _test(
        lambda start_kwargs: ECHO_ARGUMENTS("this")
        >> start(**start_kwargs) + CAT_ARGUMENTS,
        _v_[1:-1],
        "",
        capsys,
    )


def test_2_wait(capsys):
    for stdout, stderr in itertools.product([False, True], [False, True]):

        def assert_(groups):
            _v_ = groups["d0"] != groups.get("d1") and groups["d0"] != groups.get("d2")
            assert _v_ and not (stdout and stderr and groups["d1"] != groups["d2"])

        _v_ = I_STDERR_PATTERN("d0", "") + (
            rf"""
┏━ (?P<_header2>(?P<d2>{DATETIME_PATTERN}) `{re.escape(subprocess_shell._get_command(I_ARGUMENTS))}`) {STATUS_PATTERN}
┣ stderr stdout 
┣ 
┗━ (?P=_header2) {RETURNED_PATTERN(0)}

"""[
                1:-1
            ]
            if stderr
            else ""
        )
        _test(
            lambda start_kwargs: I_ARGUMENTS >> start(**start_kwargs) + I_ARGUMENTS,
            (
                rf"""
╭─ (?P<_header>(?P<d1>{DATETIME_PATTERN}) `{re.escape(subprocess_shell._get_command(I_ARGUMENTS))}`) {STATUS_PATTERN}
│ stdout stdout 
│ 
╰─ (?P=_header) {RETURNED_PATTERN(0)}

"""[
                    1:-1
                ]
                if stdout
                else ""
            ),
            _v_,
            capsys,
            wait=dict(stdout=stdout, stderr=stderr),
            assert_=assert_,
        )

    for stdout, stderr in itertools.product([False, True], [False, True]):

        def assert_(groups):
            _v_ = groups["d0"] != groups.get("d1") and groups["d0"] != groups.get("d2")
            assert _v_ and not (stdout and stderr and groups["d1"] != groups["d2"])

        _v_ = I_STDOUT_PATTERN("d0", "") + (
            rf"""
╭─ (?P<_header2>(?P<d1>{DATETIME_PATTERN}) `{re.escape(subprocess_shell._get_command(I_ARGUMENTS))}`) {STATUS_PATTERN}
│ stdout stderr 
│ 
╰─ (?P=_header2) {RETURNED_PATTERN(0)}

"""[
                1:-1
            ]
            if stdout
            else ""
        )
        _test(
            lambda start_kwargs: I_ARGUMENTS >> start(**start_kwargs) - I_ARGUMENTS,
            _v_,
            (
                rf"""
┏━ (?P<_header>(?P<d2>{DATETIME_PATTERN}) `{re.escape(subprocess_shell._get_command(I_ARGUMENTS))}`) {STATUS_PATTERN}
┣ stderr stderr 
┣ 
┗━ (?P=_header) {RETURNED_PATTERN(0)}

"""[
                    1:-1
                ]
                if stderr
                else ""
            ),
            capsys,
            wait=dict(stdout=stdout, stderr=stderr),
            assert_=assert_,
        )


def test_2_fail():
    source_arguments = ECHO_ARGUMENTS("this")
    target_arguments = CAT_ARGUMENTS
    fail_arguments = [sys.executable, "-c", "import sys; sys.exit(1)"]

    _v_ = (
        rf"^{DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(fail_arguments))}` {RETURNED_PATTERN(1)}"
        rf" \+ {DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(target_arguments))}` {STATUS_PATTERN}$"
    )
    with pytest.raises(subprocess_shell.ProcessFailedError, match=_v_):
        _ = fail_arguments >> start() + target_arguments >> start() >> wait()

    _v_ = (
        rf"^{DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(source_arguments))}` {STATUS_PATTERN}"
        rf" \+ {DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(fail_arguments))}` {RETURNED_PATTERN(1)}$"
    )
    with pytest.raises(subprocess_shell.ProcessFailedError, match=_v_):
        _ = source_arguments >> start() + fail_arguments >> start() >> wait()

    _v_ = (
        rf"^{DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(fail_arguments))}` {RETURNED_PATTERN(1)}"
        rf" \+ {DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(fail_arguments))}` {STATUS_PATTERN}$"
    )
    with pytest.raises(subprocess_shell.ProcessFailedError, match=_v_):
        _ = fail_arguments >> start() + fail_arguments >> start() >> wait()


def test_codec(capsys):
    _v_ = os.name == "nt" or subprocess_shell._FORCE_ASYNC in (None, True)
    for text, bytes, encoding in itertools.product(
        ([False] if _v_ else [False, True]), [False, True], [None, "utf-8", "latin-1"]
    ):
        _string = f"this{os.linesep}"

        _v_ = (
            _string.encode(**dict(encoding=encoding) if encoding is not None else {})
            if bytes
            else _string
        )
        _test(
            lambda start_kwargs: ECHO_ARGUMENTS("this"),
            "",
            "",
            capsys,
            start=dict(text=True, async_=False) if text else dict(text=False),
            read=read(bytes=bytes, encoding=encoding),
            result=_v_,
        )


_v_ = h_strategies.sampled_from(["\n", None])
_v_ = h_strategies.one_of(h_strategies.text(max_size=5), _v_)


@hypothesis.settings(
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
    print_blob=True,
)
@hypothesis.given(
    objects=h_strategies.lists(_v_, max_size=5),
    bufsize=h_strategies.sampled_from(
        [2, 3, 4, 5]
        if os.name == "nt" or subprocess_shell._FORCE_ASYNC in (None, True)
        else [0, 2, 3, 4, 5]
    ),
)
def test_lines(objects, bufsize, capsys):
    capsys.readouterr()

    _v_ = "".join(filter(lambda object: isinstance(object, str), objects))
    expected_lines = re.split(r"(?<=\n)", _v_)

    if expected_lines[-1] == "":
        expected_lines.pop()

    if os.name == "nt":
        expected_lines = [string.replace("\n", "\r\n") for string in expected_lines]

    _v_ = os.environ | dict(PYTHONIOENCODING="utf-8") if os.name == "nt" else None
    _v_ = [sys.executable] >> start(bufsize=bufsize, env=_v_)
    process = _v_ >> write(
        f"""
import sys

for object in {repr(objects)}:
    if isinstance(object, str):
        sys.stdout.write(object)

    elif object is None:
        sys.stdout.flush()

    else:
        raise Exception
""".strip(),
        close=True,
    )

    assert list(process.get_stdout_lines()) == expected_lines
    assert process >> wait() == 0
    _assert_std("", "", capsys)


def test_rich(capsys):
    pytest.importorskip("rich")

    arguments = ECHO_ARGUMENTS("[red]this[/red]")

    _v_ = rf"""
╭─ (?P<_header>{DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(arguments))}`) {STATUS_PATTERN}
│ \[red\]this\[/red\]
╰─ (?P=_header) {RETURNED_PATTERN(0)}

"""
    _test(lambda start_kwargs: arguments, _v_[1:-1], "", capsys)


def test_ascii(capsys):
    _v_ = sys.executable
    _v_ = [_v_, "-c", "import sys; print('stdout'); print('stderr', file=sys.stderr)"]
    arguments = _v_

    _v_ = rf"""
\+\- (?P<_header>{DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(arguments))}`) {STATUS_PATTERN}
\| stdout
\| 
\+\- (?P=_header) {RETURNED_PATTERN(0)}

"""
    _test(
        lambda start_kwargs: arguments,
        _v_[1:-1],
        rf"""
EE (?P<_header>{DATETIME_PATTERN} `{re.escape(subprocess_shell._get_command(arguments))}`) {STATUS_PATTERN}
E stderr
E 
EE (?P=_header) {RETURNED_PATTERN(0)}

"""[
            1:-1
        ],
        capsys,
        wait=dict(ascii=True),
    )


@h_strategies.composite
def _text(draw):
    encoding = draw(h_strategies.sampled_from([None, "utf-8", "latin-1"]))

    _v_ = draw(h_strategies.text(alphabet=h_strategies.characters(codec=encoding)))
    return (encoding, _v_)


_v_ = os.name == "nt" or subprocess_shell._FORCE_ASYNC in (None, True)
_v_ = h_strategies.sampled_from([2, 3, 4, 5] if _v_ else [0, 2, 3, 4, 5])


@hypothesis.settings(
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
    print_blob=True,
)
@hypothesis.given(
    text=_text(), length=h_strategies.integers(min_value=1, max_value=4), bufsize=_v_
)
def test_unicode(text, length, bufsize, capsys):
    encoding, string = text
    bytes = string.encode(**dict(encoding=encoding) if encoding is not None else {})

    _v_ = (
        os.environ
        | dict(PYTHONIOENCODING=encoding if encoding is not None else "utf-8")
        if os.name == "nt"
        else None
    )
    _v_ = [sys.executable] >> start(bufsize=bufsize, env=_v_)
    process = _v_ >> write(
        f"""
import sys

bytes = {repr(bytes)}

index = 0
while True:
    part_bytes = bytes[index : index + {repr(length)}]
    if part_bytes == b"":
        break

    sys.stdout.buffer.write(part_bytes)
    sys.stdout.flush()

    index += {repr(length)}
""".strip(),
        close=True,
    )

    assert process.join_stdout_strings(encoding=encoding) == string
    assert process >> wait() == 0
    _assert_std("", "", capsys)


def _test(
    function,
    stdout_pattern,
    stderr_pattern,
    capsys,
    start=None,
    write=None,
    wait=None,
    read=None,
    result: t.Any = 0,
    raises=None,
    raises_pattern=None,
    assert_=None,
    _start=start,
    _wait=wait,
):
    assert not (wait is not None and read is not None)

    _v_ = itertools.product([None, False, True], [False, True], [False, True])
    for async_, _run, logs in _v_:
        start_kwargs = {}
        if async_ is not None:
            start_kwargs["async_"] = async_

        if start is not None:
            start_kwargs.update(start)

        wait_kwargs = {}
        if logs:
            wait_kwargs["logs"] = True

        if wait is not None:
            wait_kwargs.update(wait)

        if _run:
            _v_ = read is not None or len(wait_kwargs) == 0
            _v_ = [
                None if len(start_kwargs) == 0 else _start(**start_kwargs),
                write,
                None if _v_ else _wait(**wait_kwargs),
                read,
            ]
            run_arguments = filter(None, _v_)

            if raises is None:
                assert function(start_kwargs) >> run(*run_arguments) == result

            else:
                with pytest.raises(raises, match=raises_pattern):
                    _ = function(start_kwargs) >> run(*run_arguments)
        else:
            process = function(start_kwargs) >> _start(**start_kwargs)
            if write is not None:
                process = process >> write

            right_object = read if read is not None else _wait(**wait_kwargs)
            if raises is None:
                assert process >> right_object == result

            else:
                with pytest.raises(raises, match=raises_pattern):
                    _ = process >> right_object

        groups = _assert_std(stdout_pattern, stderr_pattern, capsys)
        if assert_ is not None:
            assert_(groups)


def _assert_std(stdout_pattern, stderr_pattern, capsys):
    capture_result = capsys.readouterr()

    stdout_match = re.search(rf"\A{stdout_pattern}\Z", capture_result.out, re.MULTILINE)
    if stdout_match is None:
        raise Exception(f"\n{capture_result.out}")

    stderr_match = re.search(rf"\A{stderr_pattern}\Z", capture_result.err, re.MULTILINE)
    if stderr_match is None:
        raise Exception(f"\n{capture_result.err}")

    return stdout_match.groupdict() | stderr_match.groupdict()


def test_defaults():
    with start():
        assert start().stdin == subprocess.PIPE

    with start(stdin=None):
        assert start().stdin is None
        assert start(stdin=subprocess.PIPE).stdin == subprocess.PIPE

    _path = pathlib.Path()
    with start(cwd=_path):
        assert start().kwargs["cwd"] is _path
        assert start(cwd=None).kwargs["cwd"] is None

    with write(""):
        _bytes = b"test"
        _write = write(_bytes)
        assert _write.object is _bytes
        assert _write.close is False

    with write("", close=True):
        assert write("").close is True
        assert write("", close=False).close is False

    with wait():
        assert wait().stdout is True

    with wait(stdout=False):
        assert wait().stdout is False
        assert wait(stdout=True).stdout is True

    with read():
        assert read().stdout is True

    with read(stdout=False):
        assert read().stdout is False
        assert read(stdout=True).stdout is True

    with start(cwd=None):
        wait()  # regression
