import asyncio
import asyncio.subprocess as a_subprocess
import collections.abc as c_abc
import contextvars
import datetime
import functools
import io
import itertools
import os
import pathlib
import queue
import re
import selectors
import subprocess
import sys
import threading
import traceback
import types
import typing as t

if t.TYPE_CHECKING:
    import rich.style as r_style


__all__ = ("start", "write", "wait", "read", "run")


class _DefaultType:
    pass


_FORCE_ASYNC = None
_BUFFER_SIZE = int(1e6)
_DEFAULT = _DefaultType()


def _read_streams():
    selector = t.cast(selectors.BaseSelector, _selector)
    try:
        while True:
            for key, _ in selector.select():
                fileobj = t.cast(t.IO, key.fileobj)
                while True:
                    object = fileobj.read(_BUFFER_SIZE)
                    if not object:
                        break

                    key.data(object)

                if object is not None:
                    selector.unregister(key.fileobj)
                    key.data(None)

    except Exception:
        print(
            "CRITICAL: error while reading from stdout/stderr or during callback",
            file=sys.stderr,
        )
        traceback.print_exc()
        raise


_selector = None
_selector_lock = threading.Lock()


def _async(coroutine):
    global _event_loop

    if _event_loop is None:
        with _event_loop_lock:
            if _event_loop is None:
                _event_loop = asyncio.new_event_loop()
                threading.Thread(target=_event_loop.run_forever, daemon=True).start()

    return asyncio.run_coroutine_threadsafe(coroutine, _event_loop)


_event_loop = None
_event_loop_lock = threading.Lock()


class _Defaults:
    _defaults: contextvars.ContextVar

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        cls._defaults = contextvars.ContextVar("_defaults")

    def __enter__(self):
        self._defaults_token = type(self)._defaults.set(self)

    def __exit__(self, exc_type, exc_value, traceback):
        type(self)._defaults.reset(self._defaults_token)


def _with_defaults(init):
    @functools.wraps(init)
    def _init(self, *args, **kwargs):
        defaults = type(self)._defaults.get(None)
        if defaults is not None:
            kwargs = defaults._kwargs | kwargs

        init(self, *args, **kwargs)
        self._kwargs = kwargs

    return _init


class _Start(_Defaults):
    @_with_defaults
    def __init__(
        self,
        stdin: t.Union[None, int, t.IO] = subprocess.PIPE,
        stdout: t.Union[
            None, int, t.IO, str, pathlib.Path, c_abc.Callable[[t.AnyStr], t.Any]
        ] = subprocess.PIPE,
        pass_stdout: bool = False,
        stderr: t.Union[
            None, int, t.IO, str, pathlib.Path, c_abc.Callable[[t.AnyStr], t.Any]
        ] = subprocess.PIPE,
        pass_stderr: bool = False,
        queue_size: int = 0,
        logs: t.Optional[bool] = None,
        return_codes: t.Optional[c_abc.Container[int]] = (0,),
        force_color: bool = True,
        async_: t.Optional[bool] = None,
        **kwargs,
    ):
        """
        `{arguments} >> start(...)` starts a sub process similar to `subprocess.Popen({arguments}, ...)` and returns a process object

        `{process} + {arguments} >> start(...)` passes stdout of the left process to stdin of the right.
        May require `{process} = {arguments} >> start(pass_stdout=True, ...)`.

        `{process} - {arguments} >> start(...)` passes stderr of the left process to stdin of the right.
        May require `{process} = {arguments} >> start(pass_stderr=True, ...)`.

        Parameters
        ----------
        stdin : None | int | IO
            See `subprocess.Popen`
        stdout : None | int | IO | str | pathlib.Path | (str | bytes) -> any
            if      None | int | IO : see `subprocess.Popen`
            if   str | pathlib.Path : write to file at path
            if (str | bytes) -> any : call function for each chunk
                called in a different thread
                **!! must not raise exceptions !!**
        pass_stdout : bool
            Don't touch stdout
        stderr : None | int | IO | str | pathlib.Path | (str | bytes) -> any
            if      None | int | IO : see `subprocess.Popen`
            if   str | pathlib.Path : write to file at path
            if (str | bytes) -> any : call function for each chunk
                called in a different thread
                **!! must not raise exceptions !!**
        pass_stderr : bool
            Don't touch stderr
        queue_size : int
            Limit size of queues
            *! may lead to deadlocks !*
        logs : bool | None
            Analog of `write(logs=logs)` if in a chain
        return_codes : container[int] | None
            Used to validate the return code if in a chain
        force_color : bool
            Set environment variable FORCE_COLOR to 1 if not set
        async_ : bool | None
            Use `asyncio` instead of `selectors`, default: `asyncio`
        **kwargs
            Passed to `subprocess.Popen`
        """

        super().__init__()

        self.stdin = stdin
        self.stdout = stdout
        self.pass_stdout = pass_stdout
        self.stderr = stderr
        self.pass_stderr = pass_stderr
        self.queue_size = queue_size
        self.logs = logs
        self.return_codes = return_codes
        self.force_color = force_color
        self.async_ = async_
        self.kwargs = kwargs

        assert not (pass_stdout and stdout not in (None, subprocess.PIPE))
        assert not (pass_stderr and stderr not in (None, subprocess.PIPE))

    def __rrshift__(self, object: t.Union[c_abc.Iterable, "_Pass"]) -> "_Process":
        return _Process(object, self)

    def __add__(
        self, arguments: c_abc.Iterable
    ) -> "_PassStdout":  # `{arguments} >> start() + {arguments}`
        return _PassStdout(self, arguments)

    def __sub__(
        self, arguments: c_abc.Iterable
    ) -> "_PassStderr":  # `{arguments} >> start() - {arguments}`
        return _PassStderr(self, arguments)


start = _Start


class _Process:
    def __init__(self, object, start):
        super().__init__()

        self.object = object
        self.start = start

        if isinstance(object, _Pass):
            assert start.stdin in (None, subprocess.PIPE)

            self._source_process = object.process

            arguments = object.arguments
            stdin, stdin_is_target = (
                (
                    (object.process._stderr_target, True)
                    if object.process._stderr_target is not None
                    else (object.process._process.stderr, False)
                )
                if object.stderr
                else (
                    (object.process._stdout_target, True)
                    if object.process._stdout_target is not None
                    else (object.process._process.stdout, False)
                )
            )

        else:
            self._source_process = None

            arguments = object
            stdin = start.stdin
            stdin_is_target = False

        _v_ = _FORCE_ASYNC is not None
        _v_ = _FORCE_ASYNC if _v_ else (start.async_ in (None, True) or os.name == "nt")
        self._async = _v_

        self._arguments = list(map(str, arguments))

        _v_ = self._get_argument(start.stdout, start.pass_stdout)
        self._stdout, self._stdout_target = _v_

        _v_ = self._get_argument(start.stderr, start.pass_stderr)
        self._stderr, self._stderr_target = _v_

        kwargs: dict[str, t.Any] = dict(
            stdin=stdin, stdout=self._stdout, stderr=self._stderr, **start.kwargs
        )

        if start.force_color:
            env = kwargs.get("env")
            if env is None:
                env = os.environ

            if "FORCE_COLOR" not in env:
                kwargs["env"] = env | dict(FORCE_COLOR="1")

        if self._async and (_bufsize := kwargs.pop("bufsize", None)) is not None:
            kwargs["limit"] = _bufsize  # TODO correct?

        self._time = None
        self._start_datetime = datetime.datetime.now()
        if self._async:
            _v_ = a_subprocess.create_subprocess_exec(*self._arguments, **kwargs)
            self._process = _async(_v_).result()

            async def _time():
                await t.cast(a_subprocess.Process, self._process).wait()

                _v_ = (datetime.datetime.now() - self._start_datetime).total_seconds()
                self._time = _v_

            _async(_time())

        else:
            self._process = subprocess.Popen(self._arguments, **kwargs)

        self._stdout_queue = (
            self._initialize_stream(self._process.stdout, start.stdout, start)
            if self._process.stdout is not None and not start.pass_stdout
            else None
        )
        self._stderr_queue = (
            self._initialize_stream(self._process.stderr, start.stderr, start)
            if self._process.stderr is not None and not start.pass_stderr
            else None
        )

        _v_ = not stdin_is_target and self._stdout_target is None
        if not (_v_ and self._stderr_target is None):

            async def _close_streams():
                await t.cast(a_subprocess.Process, self._process).wait()

                if stdin_is_target:
                    os.close(stdin)

                if self._stdout_target is not None:
                    os.close(t.cast(int, self._stdout))

                if self._stderr_target is not None:
                    os.close(t.cast(int, self._stderr))

            _async(_close_streams())

    def _get_argument(self, object, pass_):
        # match object:
        # case str() | pathlib.Path():
        if isinstance(object, (str, pathlib.Path)):
            return (open(object, "wb"), None)

        # case c_abc.Callable():
        if isinstance(object, c_abc.Callable):
            return (subprocess.PIPE, None)

        if self._async and pass_:
            target, source = os.pipe()
            return (source, target)

        return (object, None)

    def _initialize_stream(self, stream, start_argument, start):
        global _selector

        if isinstance(start_argument, c_abc.Callable):
            queue_ = None
            function = start_argument

        else:
            queue_ = queue.Queue(maxsize=start.queue_size)
            function = queue_.put

        if self._async:

            async def _read_stream():
                try:
                    while True:
                        object = await stream.read(n=_BUFFER_SIZE)
                        if len(object) == 0:
                            function(None)
                            break

                        function(object)

                except Exception:
                    print(
                        "CRITICAL: error while reading from stdout/stderr or during callback",
                        file=sys.stderr,
                    )
                    traceback.print_exc()
                    raise

            _async(_read_stream())

        else:
            os.set_blocking(stream.fileno(), False)

            if _selector is None:
                with _selector_lock:
                    if _selector is None:
                        _selector = selectors.DefaultSelector()
                        threading.Thread(target=_read_streams, daemon=True).start()

            _selector.register(stream, selectors.EVENT_READ, data=function)

        return queue_

    def get_stdout_lines(
        self, bytes: bool = False, encoding: t.Optional[str] = None
    ) -> c_abc.Generator[t.AnyStr, None, None]:
        """
        Yields lines from stdout as strings or bytes objects similar to `iter(subprocess.Popen(...).stdout)`

        Parameters
        ----------
        bytes : bool
            Yield bytes objects instead of strings
        encoding : str | None
            Encoding to use for encoding strings or decoding bytes objects, default: UTF-8

        Returns
        -------
        generator[str] | generator[bytes]
            Lines as strings or bytes objects
        """
        return self._get_lines(self._stdout_queue, bytes, encoding)

    def get_stderr_lines(
        self, bytes: bool = False, encoding: t.Optional[str] = None
    ) -> c_abc.Generator[t.AnyStr, None, None]:
        """
        Yields lines from stderr as strings or bytes objects similar to `iter(subprocess.Popen(...).stderr)`

        Parameters
        ----------
        bytes : bool
            Yield bytes objects instead of strings
        encoding : str | None
            Encoding to use for encoding strings or decoding bytes objects, default: UTF-8

        Returns
        -------
        generator[str] | generator[bytes]
            Lines as strings or bytes objects
        """
        return self._get_lines(self._stderr_queue, bytes, encoding)

    def _get_lines(self, queue, bytes, encoding):
        line_generator = _LineGenerator(bytes)
        for object in (
            self._get_bytes(queue, encoding)
            if bytes
            else self._get_strings(queue, encoding)
        ):
            yield from line_generator.append(object)

        yield from line_generator.append(None)

    def get_stdout_strings(
        self, encoding: t.Optional[str] = None
    ) -> c_abc.Generator[str, None, None]:
        """
        Yields chunks from stdout as strings

        Parameters
        ----------
        encoding : str | None
            Encoding to use for decoding bytes objects, default: UTF-8

        Returns
        -------
        generator[str]
            Chunks as strings
        """
        return self._get_strings(self._stdout_queue, encoding)

    def get_stderr_strings(
        self, encoding: t.Optional[str] = None
    ) -> c_abc.Generator[str, None, None]:
        """
        Yields chunks from stderr as strings

        Parameters
        ----------
        encoding : str | None
            Encoding to use for decoding bytes objects, default: UTF-8

        Returns
        -------
        generator[str]
            Chunks as strings
        """
        return self._get_strings(self._stderr_queue, encoding)

    def _get_strings(self, queue, encoding):
        if encoding is None:
            encoding = "utf-8"

        objects = iter(self._get_objects(queue))

        object = next(objects, None)
        if object is None:
            return

        if isinstance(object, str):
            yield object
            yield from objects

        else:
            previous_bytes = b""
            for bytes in itertools.chain([object], objects):
                bytes = previous_bytes + bytes
                try:
                    string = bytes.decode(encoding=encoding)

                except UnicodeDecodeError:
                    for index in range(-1, -4, -1):
                        try:
                            string = bytes[:index].decode(encoding=encoding)

                        except UnicodeDecodeError:
                            pass

                        else:
                            break
                    else:
                        if len(bytes) < 4:
                            previous_bytes = bytes
                            continue

                        raise

                    previous_bytes = bytes[index:]

                else:
                    previous_bytes = b""

                yield string

            if previous_bytes != b"":
                yield previous_bytes.decode(encoding=encoding)

    def get_stdout_bytes(
        self, encoding: t.Optional[str] = None
    ) -> c_abc.Generator[bytes, None, None]:
        """
        Yields chunks from stdout as bytes objects

        Parameters
        ----------
        encoding : str | None
            Encoding to use for encoding strings, default: UTF-8

        Returns
        -------
        generator[bytes]
            Chunks as bytes objects
        """
        return self._get_bytes(self._stdout_queue, encoding)

    def get_stderr_bytes(
        self, encoding: t.Optional[str] = None
    ) -> c_abc.Generator[bytes, None, None]:
        """
        Yields chunks from stderr as bytes objects

        Parameters
        ----------
        encoding : str | None
            Encoding to use for encoding strings, default: UTF-8

        Returns
        -------
        generator[bytes]
            Chunks as bytes objects
        """
        return self._get_bytes(self._stderr_queue, encoding)

    def _get_bytes(self, queue, encoding):
        if encoding is None:
            encoding = "utf-8"

        objects = iter(self._get_objects(queue))

        object = next(objects, None)
        if object is None:
            return

        if isinstance(object, str):
            yield object.encode(encoding=encoding)
            yield from (string.encode(encoding=encoding) for string in objects)

        else:
            yield object
            yield from objects

    def get_stdout_objects(self) -> c_abc.Generator[t.AnyStr, None, None]:
        """
        Yields chunks from stdout as strings or bytes objects

        Returns
        -------
        generator[str] | generator[bytes]
            Chunks as strings or bytes objects
        """
        return self._get_objects(self._stdout_queue)

    def get_stderr_objects(self) -> c_abc.Generator[t.AnyStr, None, None]:
        """
        Yields chunks from stderr as strings or bytes objects

        Returns
        -------
        generator[str] | generator[bytes]
            Chunks as strings or bytes objects
        """
        return self._get_objects(self._stderr_queue)

    def _get_objects(self, queue):
        assert queue is not None

        while True:
            object = queue.get()
            if object is None:
                queue.put(None)
                break

            yield object

    def join_stdout_strings(self, encoding: t.Optional[str] = None) -> str:
        """
        Collects chunks from stdout and joins them as string

        Parameters
        ----------
        encoding : str | None
            Encoding to use for decoding bytes objects, default: UTF-8

        Returns
        -------
        str
            Joined string
        """
        _v_ = self._join_objects(self.get_stdout_objects(), False, encoding)
        return t.cast(str, _v_)

    def join_stdout_bytes(self, encoding: t.Optional[str] = None) -> bytes:
        """
        Collects chunks from stdout and joins them as bytes object

        Parameters
        ----------
        encoding : str | None
            Encoding to use for encoding strings, default: UTF-8

        Returns
        -------
        str
            Joined bytes object
        """
        _v_ = self._join_objects(self.get_stdout_objects(), True, encoding)
        return t.cast(bytes, _v_)

    def join_stderr_strings(self, encoding: t.Optional[str] = None) -> str:
        """
        Collects chunks from stderr and joins them as string

        Parameters
        ----------
        encoding : str | None
            Encoding to use for decoding bytes objects, default: UTF-8

        Returns
        -------
        str
            Joined string
        """
        _v_ = self._join_objects(self.get_stderr_objects(), False, encoding)
        return t.cast(str, _v_)

    def join_stderr_bytes(self, encoding: t.Optional[str] = None) -> bytes:
        """
        Collects chunks from stderr and joins them as bytes object

        Parameters
        ----------
        encoding : str | None
            Encoding to use for encoding strings, default: UTF-8

        Returns
        -------
        str
            Joined bytes object
        """
        _v_ = self._join_objects(self.get_stderr_objects(), True, encoding)
        return t.cast(bytes, _v_)

    def _join_objects(self, objects, bytes, encoding):
        if encoding is None:
            encoding = "utf-8"

        objects = iter(objects)
        first_object = next(objects, None)
        if first_object is None:
            return b"" if bytes else ""

        joined = first_object[:0].join(itertools.chain([first_object], objects))
        if isinstance(joined, str) ^ (not bytes):
            joined = (joined.encode if bytes else joined.decode)(encoding=encoding)

        return joined

    def __add__(self, arguments: c_abc.Iterable) -> "_Pass":
        assert self.start.pass_stdout
        return _Pass(self, False, arguments)

    def __sub__(self, arguments: c_abc.Iterable) -> "_Pass":
        assert self.start.pass_stderr
        return _Pass(self, True, arguments)

    def get_subprocess(self) -> t.Union[subprocess.Popen, a_subprocess.Process]:
        """
        Returns the `subprocess.Popen` or `asyncio.subprocess.Process` object

        You shouldn't need to use this unless for complex use cases.
        If you found a common use case that should be covered by *subprocess_shell*, please let me know!

        Returns
        -------
        subprocess.Popen | asyncio.subprocess.Process
            The `subprocess.Popen` or `asyncio.subprocess.Process` object
        """
        return self._process

    def get_source_process(self) -> t.Optional["_Process"]:
        """
        Returns the source process if in a chain

        Returns
        -------
        _Process | None
            The source process
        """
        return self._source_process

    def get_chain_string(self) -> str:
        """
        Returns a readable string representing the process and the source process

        Returns
        -------
        str
            A readable string
        """
        if self._source_process is not None:
            _operator = "-" if self.object.stderr else "+"
            _pass = f"{self._source_process.get_chain_string()} {_operator} "

        else:
            _pass = ""

        return f"{_pass}{str(self)}"

    def _close_stdin(self):
        if self._process.stdin is None:
            return

        t.cast(t.IO, self._process.stdin).close()
        if self._async:
            _async(t.cast(asyncio.StreamWriter, self._process.stdin).wait_closed())

    def _wait(self):
        return (
            _async(self._process.wait()).result()
            if self._async
            else self._process.wait()
        )

    def __str__(self):
        if not self._async:
            t.cast(subprocess.Popen, self._process).poll()

        _v_ = (_returncode := self._process.returncode) is not None
        _status = f"returned {_returncode}{self._get_time()}" if _v_ else "running"

        return f"{self._start_datetime} `{_get_command(self._arguments)}` {_status}"

    def _get_time(self):
        if self._time is None:
            return ""

        if self._time < 0.000_5:
            return " immediately"

        if self._time < 0.999_5:
            return f" after {round(self._time * 1_000)}ms"

        minutes, seconds = divmod(self._time, 60)
        if minutes == 0:
            return f" after {round(seconds, 1):0.1f}s"

        hours, minutes = divmod(int(minutes), 60)
        if hours == 0:
            return f" after {minutes}m {round(seconds)}s"

        return f" after {hours}h {minutes}m {round(seconds)}s"


def _get_command(arguments):
    return re.sub(r"\r?\n", r"\\n", subprocess.list2cmdline(arguments))


class _Pass:
    def __init__(self, process, stderr, arguments):
        super().__init__()

        self.process = process
        self.stderr = stderr
        self.arguments = arguments


class _Write(_Defaults):
    @_with_defaults
    def __init__(
        self, object: t.AnyStr, close: bool = False, encoding: t.Optional[str] = None
    ):
        """
        `{process} >> write(...)` writes to, flushes and optionally closes stdin and returns the process object

        similar to
        ```python
        stdin = subprocess.Popen(...).stdin
        stdin.write(object)
        stdin.flush()
        if close:
            stdin.close()
        ```

        Parameters
        ----------
        object : str | bytes
            String or bytes object to write
        close : bool
            Close stdin after write
        encoding : str | None
            Encoding to use for encoding the string, default: UTF-8
        """

        super().__init__()

        self.object = object
        self.close = close
        self.encoding = encoding

    def __rrshift__(self, process: _Process) -> _Process:
        stdin = t.cast(t.IO, process.get_subprocess().stdin)
        assert stdin is not None

        encoding = self.encoding if self.encoding is not None else "utf-8"
        if isinstance(stdin, io.TextIOBase):
            _v_ = isinstance(self.object, str)
            stdin.write(self.object if _v_ else self.object.decode(encoding=encoding))

        else:
            _v_ = isinstance(self.object, str)
            stdin.write(self.object.encode(encoding=encoding) if _v_ else self.object)

        (
            _async(t.cast(asyncio.StreamWriter, stdin).drain()).result()
            if process._async
            else stdin.flush()
        )

        if self.close:
            process._close_stdin()

        return process

    def __add__(
        self, arguments: c_abc.Iterable
    ) -> "_PassStdout":  # `{process} >> write({string or bytes}) + {arguments}`
        return _PassStdout(self, arguments)

    def __sub__(
        self, arguments: c_abc.Iterable
    ) -> "_PassStderr":  # `{process} >> write({string or bytes}) - {arguments}`
        return _PassStderr(self, arguments)


write = _Write


class _PassStdout:
    def __init__(self, right_object, target_arguments):
        super().__init__()

        self.right_object = right_object
        self.target_arguments = target_arguments

        if isinstance(right_object, _Start):
            assert right_object.stdout in (None, subprocess.PIPE)
            right_object.pass_stdout = True

        elif isinstance(right_object, _Process):
            assert right_object.start.pass_stdout

        else:
            raise Exception

    def __rrshift__(self, left_object: t.Union[c_abc.Iterable, _Process]) -> _Pass:
        # `{arguments} >> start() + {arguments}`
        # `{process} >> write() + {arguments}`
        return (left_object >> self.right_object) + self.target_arguments


class _PassStderr:
    def __init__(self, right_object, target_arguments):
        super().__init__()

        self.right_object = right_object
        self.target_arguments = target_arguments

        if isinstance(right_object, _Start):
            assert right_object.stderr in (None, subprocess.PIPE)
            right_object.pass_stderr = True

        elif isinstance(right_object, _Process):
            assert right_object.start.pass_stderr

        else:
            raise Exception

    def __rrshift__(self, left_object: t.Union[c_abc.Iterable, _Process]) -> _Pass:
        # `{arguments} >> start() - {arguments}`
        # `{process} >> write() + {arguments}`
        return (left_object >> self.right_object) - self.target_arguments


class _Wait(_Defaults):
    @_with_defaults
    def __init__(
        self,
        stdout: t.Union[bool, t.TextIO] = True,
        stderr: t.Union[bool, t.TextIO] = True,
        logs: t.Optional[bool] = None,
        return_codes: t.Optional[c_abc.Container[int]] = (0,),
        rich: bool = True,
        stdout_style: t.Union["r_style.Style", str] = "green",
        log_style: t.Union["r_style.Style", str] = "dark_orange3",
        error_style: t.Union["r_style.Style", str] = "red",
        ascii: bool = False,
        encoding: t.Optional[str] = None,
    ):
        """
        `{process} >> wait(...)` "waits for" the source process, writes stdout and stderr as separate frames and validates and returns the return code

        Parameters
        ----------
        stdout : bool | TextIO
            if   bool : optionally write stdout to `sys.stdout`
            if TextIO : write stdout to writable object
        stderr : bool | TextIO
            if   bool : optionally write stderr to `sys.stderr`
            if TextIO : write stderr to writable object
        logs : bool | None
            if False : write stdout first and use `error_style` for stderr
                True : write stderr first and use `log_style`
                None : write stdout first and use `log_style` for stderr if return code assert succeeds or `error_style` otherwise
        return_codes : container[int]
            Used to validate the return code
        rich : bool
            Use *Rich* if available
        stdout_style : rich.style.Style | str
            Used for stdout frame
        log_style : rich.style.Style | str
            Used for stderr frame, see `logs`
        error_style : rich.style.Style | str
            Used for stderr frame, see `logs`
        ascii : bool
            Use ASCII instead of Unicode
        encoding : str | None
            Encoding to use for encoding strings or decoding bytes objects, default: UTF-8
        """

        super().__init__()

        self.stdout = stdout
        self.stderr = stderr
        self.logs = logs
        self.return_codes = return_codes
        self.rich = rich
        self.stdout_style = stdout_style
        self.log_style = log_style
        self.error_style = error_style
        self.ascii = ascii
        self.encoding = encoding

        self._r_console = None
        self._r_highlighter = None
        self._r_theme = None
        if rich:
            try:
                import rich.console as r_console
                import rich.highlighter as r_highlighter
                import rich.theme as r_theme

            except ModuleNotFoundError:
                pass

            else:
                self._r_console = r_console
                self._r_highlighter = r_highlighter
                self._r_theme = r_theme

    def __rrshift__(self, process: _Process) -> int:
        if (_source_process := process.get_source_process()) is not None:
            _start = _source_process.start
            _wait = self._with_changes(
                stdout=self.stdout if not isinstance(self.stdout, bool) else True,
                stderr=self.stderr if not isinstance(self.stderr, bool) else True,
                logs=_start.logs,
                return_codes=_start.return_codes,
            )
            try:
                _ = _source_process >> _wait

            except ProcessFailedError:
                raise ProcessFailedError(process)

        process._close_stdin()

        def _print_stdout():
            _v_ = process._stdout_queue is None or process.start.pass_stdout
            if not (_v_ or self.stdout is False):
                self._print_stream(
                    process.get_stdout_strings(encoding=self.encoding),
                    sys.stdout if self.stdout is True else self.stdout,
                    False,
                    False,
                    process,
                )

        def _print_stderr(log):
            _v_ = process._stderr_queue is None or process.start.pass_stderr
            if not (_v_ or self.stderr is False):
                self._print_stream(
                    process.get_stderr_strings(encoding=self.encoding),
                    sys.stderr if self.stderr is True else self.stderr,
                    True,
                    log,
                    process,
                )

        if self.logs is True:
            _print_stderr(True)
            _print_stdout()
            return_code = process._wait()

        else:
            _print_stdout()
            return_code = process._wait()

            _v_ = self.logs is None and not (
                self.return_codes is not None and return_code not in self.return_codes
            )
            _print_stderr(_v_)

        if isinstance(process.start.stdout, (str, pathlib.Path)):
            t.cast(t.IO, process._stdout).close()

        if isinstance(process.start.stderr, (str, pathlib.Path)):
            t.cast(t.IO, process._stderr).close()

        if self.return_codes is not None and return_code not in self.return_codes:
            raise ProcessFailedError(process)

        return t.cast(int, return_code)

    def _print_stream(self, strings, file, is_stderr, log, process):
        strings = iter(strings)

        string = next(strings, None)
        if string is None:
            return

        newline_str = (
            ("\nE " if self.ascii else "\n┣ ")
            if is_stderr
            else ("\n| " if self.ascii else "\n│ ")
        )
        newline = False

        if self._r_console is not None:
            _v_ = t.cast(types.ModuleType, self._r_highlighter).RegexHighlighter

            class _Highlighter(_v_):
                base_style = "m."
                highlights = [
                    r"^(?P<p1>[^`]+`).*?((?P<p2>` running)|(?P<p3>` returned )-?\d+((?P<p4> after )(((\d+h )?\d+m )?\d+s|\d+\.\d+s|\d+ms)|(?P<p5> immediately))?)",
                    f"(?P<p1>{re.escape(newline_str)})",
                ]

            _style = (
                (self.log_style if log else self.error_style)
                if is_stderr
                else self.stdout_style
            )

            _v_ = {f"m.p{index + 1}": _style for index in range(5)}
            _v_ = t.cast(types.ModuleType, self._r_theme).Theme(_v_)
            console = t.cast(types.ModuleType, self._r_console).Console(
                file=file, soft_wrap=True, highlighter=_Highlighter(), theme=_v_
            )

            def _print(*args, **kwargs):
                console.out(*args, **kwargs)
                file.flush()

        else:

            def _print(*args, **kwargs):
                print(*args, file=file, flush=True, **kwargs)

        _corner = (
            ("EE" if self.ascii else "┏━")
            if is_stderr
            else ("+-" if self.ascii else "╭─")
        )
        _print(f"{_corner} {process}{newline_str}", end="")

        if string.endswith("\n") and not self.ascii:
            string = string[:-1]
            newline = True

        _print(string.replace("\n", newline_str), end="")

        for string in strings:
            if newline:
                _print(newline_str, end="")
                newline = False

            if string.endswith("\n") and not self.ascii:
                string = string[:-1]
                newline = True

            _print(string.replace("\n", newline_str), end="")

        _print("␄" if not newline and not self.ascii else "")

        process._wait()

        _corner = (
            (f"EE" if self.ascii else "┗━")
            if is_stderr
            else ("+-" if self.ascii else "╰─")
        )
        _print(f"{_corner} {process}")

    def _with_changes(self, **kwargs):
        _v_ = [
            "stdout",
            "stderr",
            "logs",
            "return_codes",
            "rich",
            "stdout_style",
            "log_style",
            "error_style",
            "ascii",
            "encoding",
        ]
        _kwargs = {name: getattr(self, name) for name in _v_}

        _kwargs.update(kwargs)
        return _Wait(**_kwargs)


class ProcessFailedError(Exception):
    def __init__(self, process: _Process):
        super().__init__(process)

        self.process = process

    def __str__(self):
        return self.process.get_chain_string()


wait = _Wait


class _Read(_Defaults):
    @_with_defaults
    def __init__(
        self,
        stdout: t.Union[bool, t.TextIO] = True,
        stderr: t.Union[bool, t.TextIO] = False,
        bytes: bool = False,
        encoding: t.Optional[str] = None,
        logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
        return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
        wait: t.Optional[_Wait] = None,
    ):
        """
        `{process} >> read(...)` "waits for" the process, concatenates the chunks from stdout and optionally stderr and returns the result

        `{process} >> read(stdout=True, stderr=True, ...)` returns the tuple (result from stdout, result from stderr).

        Parameters
        ----------
        stdout : bool | TextIO
            if  False : don't touch stdout
            if   True : concatenate and return stdout
            if TextIO : passed to `wait`
        stderr : bool | TextIO
            if  False : don't touch stderr
            if   True : concatenate and return stderr
            if TextIO : passed to `wait`
        bytes : bool
            Return bytes objects instead of strings
        encoding : str | None
            Encoding to use for encoding strings or decoding bytes objects, default: UTF-8
        logs : bool | None
            Passed to `wait`
        return_codes : collection[int] | None
            Passed to `wait`
        wait : _Wait | None
            Wait object to use as reference
        """

        super().__init__()

        self.stdout = stdout
        self.stderr = stderr
        self.bytes = bytes
        self.encoding = encoding
        self.logs = logs
        self.return_codes = return_codes
        self.wait = wait

    def __rrshift__(
        self, process: _Process
    ) -> t.Union[str, bytes, tuple[t.AnyStr, t.AnyStr], None]:
        stdout = self.stdout is True
        stderr = self.stderr is True

        _ = process >> (self.wait if self.wait is not None else _Wait())._with_changes(
            stdout=(not self.stdout) if isinstance(self.stdout, bool) else self.stdout,
            stderr=(not self.stderr) if isinstance(self.stderr, bool) else self.stderr,
            **{
                name: _object
                for name in ["logs", "return_codes"]
                if (_object := getattr(self, name)) is not _DEFAULT
            },
        )

        _get_stderr = lambda: (
            (process.join_stderr_bytes if self.bytes else process.join_stderr_strings)(
                encoding=self.encoding
            )
        )
        if stdout:
            _stdout = (
                process.join_stdout_bytes if self.bytes else process.join_stdout_strings
            )(encoding=self.encoding)
            return (
                t.cast(tuple[t.AnyStr, t.AnyStr], (_stdout, _get_stderr()))
                if stderr
                else _stdout
            )

        if stderr:
            return _get_stderr()

    @property
    def cast_str(self) -> "_ReadStr":
        return t.cast(_ReadStr, self)

    @property
    def cast_bytes(self) -> "_ReadBytes":
        return t.cast(_ReadBytes, self)

    @property
    def cast_strs(self) -> "_ReadStrs":
        return t.cast(_ReadStrs, self)

    @property
    def cast_bytess(self) -> "_ReadBytess":
        return t.cast(_ReadBytess, self)


class _ReadStr(_Read):
    def __rrshift__(self, process: _Process) -> str: ...


class _ReadBytes(_Read):
    def __rrshift__(self, process: _Process) -> bytes: ...


class _ReadStrs(_Read):
    def __rrshift__(self, process: _Process) -> tuple[str, str]: ...


class _ReadBytess(_Read):
    def __rrshift__(self, process: _Process) -> tuple[bytes, bytes]: ...


# generated from definitions below
@t.overload
def read(
    stdout: t.Literal[True] = True,
    stderr: t.Literal[False] = False,
    bytes: t.Literal[False] = False,
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _ReadStr: ...
@t.overload
def read(
    stdout: t.Literal[False],
    stderr: t.Literal[True],
    bytes: t.Literal[False] = False,
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _ReadStr: ...
@t.overload
def read(
    stdout: t.Literal[True] = True,
    *,
    stderr: t.Literal[True],
    bytes: t.Literal[False] = False,
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _ReadStrs: ...
@t.overload
def read(
    stdout: t.Literal[True],
    stderr: t.Literal[True],
    /,
    bytes: t.Literal[False] = False,
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _ReadStrs: ...
@t.overload
def read(
    stdout: t.Literal[True] = True,
    stderr: t.Literal[False] = False,
    *,
    bytes: t.Literal[True],
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _ReadBytes: ...
@t.overload
def read(
    stdout: t.Literal[True],
    stderr: t.Literal[False],
    bytes: t.Literal[True],
    /,
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _ReadBytes: ...
@t.overload
def read(
    stdout: t.Literal[False],
    stderr: t.Literal[True],
    bytes: t.Literal[True],
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _ReadBytes: ...
@t.overload
def read(
    stdout: t.Literal[True] = True,
    *,
    stderr: t.Literal[True],
    bytes: t.Literal[True],
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _ReadBytess: ...
@t.overload
def read(
    stdout: t.Literal[True],
    stderr: t.Literal[True],
    /,
    bytes: t.Literal[True],
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _ReadBytess: ...


# @t.overload
# read(stdout: t.Literal[True] = True  , stderr: t.Literal[False] = False, bytes: t.Literal[False] = False) -> _ReadStr
# read(stdout: t.Literal[False] = False, stderr: t.Literal[True] = True  , bytes: t.Literal[False] = False) -> _ReadStr
# read(stdout: t.Literal[True] = True  , stderr: t.Literal[True] = True  , bytes: t.Literal[False] = False) -> _ReadStrs
# read(stdout: t.Literal[True] = True  , stderr: t.Literal[False] = False, bytes: t.Literal[True] = True) -> _ReadBytes
# read(stdout: t.Literal[False] = False, stderr: t.Literal[True] = True  , bytes: t.Literal[True] = True) -> _ReadBytes
# read(stdout: t.Literal[True] = True  , stderr: t.Literal[True] = True  , bytes: t.Literal[True] = True) -> _ReadBytess
def read(
    stdout: t.Union[bool, t.TextIO] = True,
    stderr: t.Union[bool, t.TextIO] = False,
    bytes: bool = False,
    encoding: t.Optional[str] = None,
    logs: t.Union[bool, None, _DefaultType] = _DEFAULT,
    return_codes: t.Union[t.Collection[int], None, _DefaultType] = _DEFAULT,
    wait: t.Optional[_Wait] = None,
) -> _Read:
    return _Read()


read = _Read


class _Run:
    def __init__(self, *args):
        """
        `{arguments} >> run(...)` is a shortcut for `{arguments} >> start(...) {* >> write(...) *} >> {wait(...) | read(...)}`

        `{arguments} >> run()` is equivalent to `{arguments} >> start() >> wait()`.

        Parameters
        ----------
        *args
            A sequence of objects returned by `start(...)`, `write(...)`, `wait(...)` and `read(...)`
        """

        super().__init__()

        self.args = args

        self._start = None
        self._writes = []
        self._wait = None
        self._read = None

        for object in args:
            if isinstance(object, _Start):
                assert self._start is None
                self._start = object

            elif isinstance(object, _Write):
                self._writes.append(object)

            elif isinstance(object, _Wait):
                assert self._wait is None
                self._wait = object

            elif isinstance(object, _Read):
                assert self._read is None
                self._read = object

        assert not (self._wait is not None and self._read is not None)

    def __rrshift__(
        self, object: t.Union[c_abc.Iterable, "_Pass"]
    ) -> t.Union[int, str, bytes, tuple[t.AnyStr, t.AnyStr], None]:
        process = object >> (self._start if self._start is not None else _Start())
        for write in self._writes:
            process = process >> write

        if self._read is not None:
            return process >> self._read

        return process >> (self._wait if self._wait is not None else _Wait())

    @property
    def cast_int(self) -> "_RunInt":
        return t.cast(_RunInt, self)

    @property
    def cast_str(self) -> "_RunStr":
        return t.cast(_RunStr, self)

    @property
    def cast_bytes(self) -> "_RunBytes":
        return t.cast(_RunBytes, self)

    @property
    def cast_strs(self) -> "_RunStrs":
        return t.cast(_RunStrs, self)

    @property
    def cast_bytess(self) -> "_RunBytess":
        return t.cast(_RunBytess, self)


class _RunInt(_Run):
    def __rrshift__(self, object: t.Union[c_abc.Iterable, "_Pass"]) -> int: ...


class _RunStr(_Run):
    def __rrshift__(self, object: t.Union[c_abc.Iterable, "_Pass"]) -> str: ...


class _RunBytes(_Run):
    def __rrshift__(self, object: t.Union[c_abc.Iterable, "_Pass"]) -> bytes: ...


class _RunStrs(_Run):
    def __rrshift__(
        self, object: t.Union[c_abc.Iterable, "_Pass"]
    ) -> tuple[str, str]: ...


class _RunBytess(_Run):
    def __rrshift__(
        self, object: t.Union[c_abc.Iterable, "_Pass"]
    ) -> tuple[bytes, bytes]: ...


run = _Run


class LineStream(io.IOBase):
    def __init__(
        self,
        function: c_abc.Callable[[t.AnyStr], t.Any],
        stream: t.IO,
        bytes: bool = False,
    ):
        """
        A writable stream which passes objects on to another stream and calls a function for each line

        The motivating use case:
        ```python
        matches = False

        def function(string):
            global matches
            matches = matches or re.search(pattern, string) is not None

        process >> wait(stdout=LineStream(function, sys.stdout))
        ```

        Use `{process}.get_stdout_lines(...)` and `{process}.get_stderr_lines(...)` for more complex use cases.

        Parameters
        ----------
        function : (str) -> any | (bytes) -> any
            The function to call
        stream : IO
            A writable stream
        """

        super().__init__()

        self.function = function
        self.stream = stream
        self.bytes = bytes

        self._line_generator = _LineGenerator(bytes)

    def write(self, object):
        self.stream.write(object)

        for line_object in self._line_generator.append(object):
            self.function(line_object)

    def flush(self):
        return self.stream.flush()


class _LineGenerator:
    def __init__(self, bytes):
        super().__init__()

        self.bytes = bytes

        self._idle = True
        self._empty_object, self._newline_object = (b"", b"\n") if bytes else ("", "\n")
        self._parts = []

    def append(self, object) -> c_abc.Generator[t.AnyStr, None, None]:
        assert self._idle
        self._idle = False

        if object is None:
            object = self._empty_object.join(self._parts)
            if object != self._empty_object:
                yield t.cast(t.AnyStr, object)
                self._parts.clear()

            self._idle = True
            return

        start_index = 0
        while True:
            end_index = object.find(self._newline_object, start_index)
            if end_index == -1:
                self._parts.append(object[start_index:])
                break

            self._parts.append(object[start_index : end_index + 1])
            yield t.cast(t.AnyStr, self._empty_object.join(self._parts))
            self._parts.clear()

            start_index = end_index + 1

        self._idle = True
