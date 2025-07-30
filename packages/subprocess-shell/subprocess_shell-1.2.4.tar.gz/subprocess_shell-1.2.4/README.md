# _subprocess_shell_

is a Python package providing an alternative interface to sub processes. The aim is simplicity comparable to shell scripting and transparency for more complex use cases.

[[_TOC_]]

![`videos/aperitif.mp4`](videos/aperitif.mp4)

**Update:** the showcase presents an earlier version which didn't provide `run()`, `wait(logs=...)` and context managers for default arguments

## Features

- Simple
  - e.g. 5 functions (`start`, `write`, `wait`, `read`, `run`) and 3 operators (`>>`, `+`, `-`)
- Transparent
  - usability layer for [_subprocess_](https://docs.python.org/3/library/subprocess.html) except streams
- Separates streams
  - no interleaving of stdout and stderr and from different processes of a chain
- Avoids deadlocks due to OS pipe buffer limits by using queues
- Uses [_Rich_](https://github.com/Textualize/rich) if available
- Supports Windows[^r4]

[^r4]: Insofar as tests succeed most of the time. On my system, tests freeze up sometimes for no apparent reason. If you experience the same and can reproduce it consistently, please open an issue!

<details>
  <summary>

`images/rich_output.png`

</summary>

![](images/rich_output.png)

</details>

## Examples

<table>
<thead>
  <tr>
    <th></th>
    <th>

`bash -e`

</th>
    <th>

_subprocess_shell_

</th>
    <th>

_subprocess_

</th>
    <th>

[_Plumbum_](https://github.com/tomerfiliba/plumbum)[^r1]

</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>initialization</td>
    <td></td>
    <td>

```python
from subprocess_shell import *
```

</td>
    <td>

```python
import subprocess
```

</td>
    <td>

```python
from plumbum import local
```

</td>
  </tr>
  <tr>
    <td>run command</td>
    <td>

```bash
echo this
```

</td>
    <td>

```python
["echo", "this"] >> run()
```

</td>
    <td>

```python
assert subprocess.Popen(["echo", "this"]).wait() == 0
```

</td>
    <td>

```python
local["echo"]["this"].run_fg()
```

</td>
  </tr>
  <tr>
    <td>redirect stream</td>
    <td>

```bash
echo this > /path/to/file
```

</td>
    <td>

```python
["echo", "this"] >> run(start(stdout="/path/to/file"))
```

</td>
    <td>

```python
with open("/path/to/file", "wb") as stdout:
    assert subprocess.Popen(["echo", "this"], stdout=stdout).wait() == 0
```

</td>
    <td>

```python
(local["echo"]["this"] > "/path/to/file").run_fg()
```

</td>
  </tr>
  <tr>
    <td>read stream</td>
    <td>

```bash
a=$(echo this)
```

</td>
    <td>

```python
a = ["echo", "this"] >> run()
```

</td>
    <td>

```python
process = subprocess.Popen(["echo", "this"], stdout=subprocess.PIPE)
a, _ = process.communicate()
assert process.wait() == 0
```

</td>
    <td>

```python
a = local["echo"]("this")
```

</td>
  </tr>
  <tr>
    <td>write stream</td>
    <td>

```bash
cat - <<EOF
this
EOF
```

</td>
    <td>

```python
["cat", "-"] >> run(write("this"))
```

</td>
    <td>

```python
process = subprocess.Popen(["cat", "-"], stdin=subprocess.PIPE)
process.communicate(b"this")
assert process.wait() == 0
```

</td>
    <td>

```python
(local["cat"]["-"] << "this").run_fg()
```

</td>
  </tr>
  <tr>
    <td>chain commands</td>
    <td>

```bash
echo this | cat -
```

</td>
    <td>

```python
["echo", "this"] >> start() + ["cat", "-"] >> run()
```

</td>
    <td>

```python
process = subprocess.Popen(["echo", "this"], stdout=subprocess.PIPE)
assert subprocess.Popen(["cat", "-"], stdin=process.stdout).wait() == 0
assert process.wait() == 0
```

</td>
    <td>

```python
(local["echo"]["this"] | local["cat"]["-"]).run_fg()
```

</td>
  </tr>
  <tr>
    <td>branch out</td>
    <td>?</td>
    <td>

```python
import sys

_v_ = "import sys; print('stdout'); print('stderr', file=sys.stderr)"
arguments = [sys.executable, "-c", _v_]

process = arguments >> start(pass_stdout=True, pass_stderr=True)
process + ["cat", "-"] >> run()
process - ["cat", "-"] >> run()
```

</td>
    <td>

```python
import sys

_v_ = "import sys; print('stdout'); print('stderr', file=sys.stderr)"
arguments = [sys.executable, "-c", _v_]

process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert subprocess.Popen(["cat", "-"], stdin=process.stdout).wait() == 0
assert subprocess.Popen(["cat", "-"], stdin=process.stderr).wait() == 0
assert process.wait() == 0
```

</td>
    <td>

not supported[^r2]

</td>
  </tr>
  <tr>
    <td>errors in chains</td>
    <td>?</td>
    <td>

```python
_v_ = ["echo", "this"] >> start(return_codes=(0, 1)) - ["cat", "-"]
_v_ >> run(wait(return_codes=(0, 2)))
```

</td>
    <td>

```python
first_process = subprocess.Popen(["echo", "this"], stderr=subprocess.PIPE)
second_process = subprocess.Popen(["cat", "-"], stdin=first_process.stderr)
assert first_process.wait() in (0, 1) and second_process.wait() in (0, 2)
```

</td>
    <td>

not supported[^r2]

</td>
  </tr>
  <tr>
    <td>callbacks</td>
    <td></td>
    <td>

```python
["echo", "this"] >> run(start(stdout=print))
```

</td>
    <td>

```python
process = subprocess.Popen(["echo", "this"], stdout=subprocess.PIPE)

for bytes in process.stdout:
    print(bytes)

assert process.wait() == 0
```

!![^r3]

</td>
    <td></td>
  </tr>
</tbody>
</table>

[^r1]: Mostly adapted versions from https://www.reddit.com/r/Python/comments/16byt8j/comment/jzhh21f/?utm_source=share&utm_medium=web2x&context=3

[^r2]: Has been requested years ago

[^r3]: This is very limited and has several issues with potential for deadlocks. An exact equivalent would be too long for this table.

**Notes**

- `bash -e` because errors can have serious consequences
  - e.g.

```bash
a=$(failing command)
sudo chown -R root:root "$a/"
```

- `assert process.wait() == 0` is the shortest (readable) code waiting for a process to stop and asserting the return code
- complexity of code for _Plumbum_ can be misleading because it has a much wider scope (e.g. remote execution and files)

## Quickstart

- Prepare virtual environment (optional but recommended)
  - e.g. [_Pipenv_](https://github.com/pypa/pipenv): `python -m pip install -U pipenv`
- Install _subprocess_shell_
  - e.g. `python -m pipenv run pip install subprocess_shell`
- Import and use it
  - e.g. `from subprocess_shell import *` and `python -m pipenv run python ...`
- Prepare tests
  - e.g. `python -m pipenv run pip install subprocess_shell[test]`
- Run tests
  - e.g. `python -m pipenv run pytest ./tests`

## Documentation

```python
from subprocess_shell import *
```

### Start process

```python
process = arguments >> start(
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    pass_stdout=False,
    stderr=subprocess.PIPE,
    pass_stderr=False,
    queue_size=0,
    logs=None,
    return_codes=(0,),
    force_color=True,
    async_=None,
    **{},
)

# change defaults temporarily, e.g. cwd and env
with start(...):
    ...
```

<table>
  <tbody>
    <tr>
      <td>

`arguments`

</td>
      <td>

iterable

</td>
      <td>

arguments are converted to string using `str(...)` and passed to `subprocess.Popen(...)`

</td>
    </tr>
    <tr>
      <td>

`stdin`

</td>
      <td>

`subprocess.PIPE`

</td>
      <td>provide stdin</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

same as `subprocess.Popen(..., stdin=object)`

</td>
    </tr>
    <tr>
      <td>

`stdout`

</td>
      <td>

`subprocess.PIPE`

</td>
      <td>provide stdout</td>
    </tr>
    <tr>
      <td></td>
      <td>

string or `pathlib.Path`

</td>
      <td>

redirect stdout to file

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`function(chunk: bytes | str) -> typing.Any`

</td>
      <td>call function for each chunk from stdout</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

same as `subprocess.Popen(..., stdout=object)`

</td>
    </tr>
    <tr>
      <td>

`pass_stdout`

</td>
      <td>

`False`

</td>
      <td>

if `stdout=subprocess.PIPE`: queue chunks from stdout

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>don't use stdout</td>
    </tr>
    <tr>
      <td>

`stderr`

</td>
      <td>

`subprocess.PIPE`

</td>
      <td>provide stderr</td>
    </tr>
    <tr>
      <td></td>
      <td>

string or `pathlib.Path`

</td>
      <td>

redirect stderr to file

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`function(chunk: bytes | str) -> typing.Any`

</td>
      <td>call function for each chunk from stderr</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

same as `subprocess.Popen(..., stderr=object)`

</td>
    </tr>
    <tr>
      <td>

`pass_stderr`

</td>
      <td>

`False`

</td>
      <td>

if `stderr=subprocess.PIPE`: queue chunks from stderr

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>don't use stderr</td>
    </tr>
    <tr>
      <td>

`queue_size`

</td>
      <td>

`0`

</td>
      <td>no limit on size of queues</td>
    </tr>
    <tr>
      <td></td>
      <td>

`int > 0`

</td>
      <td>

wait for other threads to process queues if full; **!! can lead to deadlocks !!**

</td>
    </tr>
    <tr>
      <td>

`logs`

</td>
      <td>

`None`

</td>
      <td>

if in a chain: analog of `wait(logs=None)`

</td>
    </tr>
    <tr>
      <td></td>
      <td>boolean</td>
      <td>

if in a chain: analog of `wait(logs=False)` or `wait(logs=True)`

</td>
    </tr>
    <tr>
      <td>

`return_codes`

</td>
      <td>

`(0,)`

</td>
      <td>

if in a chain: analog of `wait(return_codes=(0,))`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

collection `object` or `None`

</td>
      <td>

if in a chain: analog of `wait(return_codes=object)` or `wait(return_codes=None)`

</td>
    </tr>
    <tr>
      <td>

`force_color`

</td>
      <td>

`False`

</td>
      <td>

don't touch environment variable `FORCE_COLOR`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>

if environment variable `FORCE_COLOR` is not set: set to `1`

</td>
    </tr>
    <tr>
      <td>

`async_`

</td>
      <td>

`None` or `True`

</td>
      <td>

use `asyncio`; cannot be mixed and matched in a chain

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`False`

</td>
      <td>

if Windows: use `asyncio`; else: use `selectors`

</td>
    </tr>
    <tr>
      <td>

`**`

</td>
      <td>

`{}`

</td>
      <td>

passed to `subprocess.Popen(...)`

</td>
    </tr>
  </tbody>
</table>

### Write to stdin

```python
process = process >> write(object, close=False, encoding=None)

# change defaults temporarily
with write("", encoding=...):  # "" will be ignored
    ...
```

<table>
  <tbody>
    <tr>
      <td>

`object`

</td>
      <td>

string or `bytes`

</td>
      <td>en/decoded if necessary, written to stdin and flushed</td>
    </tr>
    <tr>
      <td>

`close`

</td>
      <td>

`False`

</td>
      <td>keep stdin open</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>close stdin after flush</td>
    </tr>
    <tr>
      <td>

`encoding`

</td>
      <td>

`None`

</td>
      <td>use the default encoding (UTF-8) for encoding the string</td>
    </tr>
    <tr>
      <td></td>
      <td>

`str`

</td>
      <td>use a different encoding</td>
    </tr>
  </tbody>
</table>

**requires** `start(stdin=subprocess.PIPE)`

### Wait for process

```python
return_code = process >> wait(
    stdout=True,
    stderr=True,
    logs=None,
    return_codes=(0,),
    rich=True,
    stdout_style="green",
    log_style="dark_orange3",
    error_style="red",
    ascii=False,
    encoding=None,
)

# change defaults temporarily, e.g. logs
with wait(...):
    ...
```

<table>
  <tbody>
    <tr>
      <td>

`stdout`

</td>
      <td>

`True`

</td>
      <td>

if stdout is queued: collect stdout, format and print to stdout

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`False`

</td>
      <td>don't use stdout</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

if stdout is queued: collect stdout, format and print with `print(..., file=object)`

</td>
    </tr>
    <tr>
      <td>

`stderr`

</td>
      <td>

`True`

</td>
      <td>

if stderr is queued: collect stderr, format and print to stderr

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`False`

</td>
      <td>don't use stderr</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

if stderr is queued: collect stderr, format and print with `print(..., file=object)`

</td>
    </tr>
    <tr>
      <td>

`logs`

</td>
      <td>

`None`

</td>
      <td>

write stdout first and use `log_style` for stderr if the return code assert succeeds or `error_style` otherwise

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`False`

</td>
      <td>

write stdout first and use `error_style` for stderr

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>

write stderr first and use `log_style`

</td>
    </tr>
    <tr>
      <td>

`return_codes`

</td>
      <td>

`(0,)`

</td>
      <td>assert that the return code is 0</td>
    </tr>
    <tr>
      <td></td>
      <td>

collection `object`

</td>
      <td>

assert that the return code is in `object`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`None`

</td>
      <td>don't assert the return code</td>
    </tr>
    <tr>
      <td>

`rich`

</td>
      <td>

`True`

</td>
      <td>

use _Rich_ if available

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`False`

</td>
      <td>

don't use _Rich_

</td>
    </tr>
    <tr>
      <td>

`stdout_style`

</td>
      <td>

`"green"`

</td>
      <td>use color "green" for stdout frame</td>
    </tr>
    <tr>
      <td></td>
      <td>style object or string</td>
      <td>

use style for stdout frame, see [Styles](https://rich.readthedocs.io/en/stable/style.html)

</td>
    </tr>
    <tr>
      <td>

`log_style`

</td>
      <td>

`"dark_orange3"`

</td>
      <td>

use color "dark_orange3" for stderr frame, see argument `logs`

</td>
    </tr>
    <tr>
      <td></td>
      <td>style object or string</td>
      <td>

use style for stderr frame, see argument `logs` and [Styles](https://rich.readthedocs.io/en/stable/style.html)

</td>
    </tr>
    <tr>
      <td>

`error_style`

</td>
      <td>

`"red"`

</td>
      <td>

use color "red" for stderr frame, see argument `logs`

</td>
    </tr>
    <tr>
      <td></td>
      <td>style object or string</td>
      <td>

use style for stderr frame, see argument `logs` and [Styles](https://rich.readthedocs.io/en/stable/style.html)

</td>
    </tr>
    <tr>
      <td>

`ascii`

</td>
      <td>

`False`

</td>
      <td>use Unicode</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>use ASCII</td>
    </tr>
    <tr>
      <td>

`encoding`

</td>
      <td>

`None`

</td>
      <td>

use the default encoding (UTF-8) for encoding strings or decoding `bytes` objects

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`str`

</td>
      <td>use a different encoding</td>
    </tr>
  </tbody>
</table>

### Read from stdout/stderr

```python
string = process >> read(
    stdout=True,
    stderr=False,
    bytes=False,
    encoding=None,
    logs=_DEFAULT,
    return_codes=_DEFAULT,
    wait=None,
)
# (obsolete) optionally one of
.cast_str     # shortcut for `typing.cast(str, ...)`
.cast_bytes   #          for `typing.cast(bytes, ...)`
.cast_strs    #          for `typing.cast(tuple[str, str], ...)`
.cast_bytess  #          for `typing.cast(tuple[bytes, bytes], ...)`

# change defaults temporarily, e.g. bytes
with read(...):
    ...
```

<table>
  <tbody>
    <tr>
      <td>

`stdout`

</td>
      <td>

`True`

</td>
      <td>

execute `process >> wait(..., stdout=False)`, collect stdout, join and return; **requires** queued stdout

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`False`

</td>
      <td>

execute `process >> wait(..., stdout=True)`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

execute `process >> wait(..., stdout=object)`

</td>
    </tr>
    <tr>
      <td>

`stderr`

</td>
      <td>

`False`

</td>
      <td>

execute `process >> wait(..., stderr=True)`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>

execute `process >> wait(..., stderr=False)`, collect stderr, join and return; **requires** queued stderr

</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

execute `process >> wait(..., stderr=object)`

</td>
    </tr>
    <tr>
      <td>

`bytes`

</td>
      <td>

`False`

</td>
      <td>return a string or tuple of strings</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>

return `bytes` or tuple of `bytes`

</td>
    </tr>
    <tr>
      <td>

`encoding`

</td>
      <td>

`None`

</td>
      <td>

use the default encoding (UTF-8) for encoding strings or decoding `bytes` objects

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`str`

</td>
      <td>use a different encoding</td>
    </tr>
    <tr>
      <td>

`logs`

</td>
      <td>

`_DEFAULT`

</td>
      <td>

use `logs` from argument `wait`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`bool` or `None`

</td>
      <td>

replace `logs` from argument `wait`

</td>
    </tr>
    <tr>
      <td>

`return_codes`

</td>
      <td>

`_DEFAULT`

</td>
      <td>

use `return_codes` from argument `wait`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

replace `return_codes` from argument `wait`

</td>
    </tr>
    <tr>
      <td>

`wait`

</td>
      <td>

`None`

</td>
      <td>

use `wait()` for waiting

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`wait(...)`

</td>
      <td>use a different wait object</td>
    </tr>
  </tbody>
</table>

```python
process.get_stdout_lines(bytes=False, encoding=None)  # generator[str | bytes]
process.get_stderr_lines(bytes=False, encoding=None)  # generator[str | bytes]
process.join_stdout_strings(encoding=None)  # str
process.join_stderr_strings(encoding=None)  # str
process.get_stdout_strings(encoding=None)  # generator[str]
process.get_stderr_strings(encoding=None)  # generator[str]
process.join_stdout_bytes(encoding=None)  # bytes
process.join_stderr_bytes(encoding=None)  # bytes
process.get_stdout_bytes(encoding=None)  # generator[bytes]
process.get_stderr_bytes(encoding=None)  # generator[bytes]
process.get_stdout_objects()  # generator[str | bytes]
process.get_stderr_objects()  # generator[str | bytes]
```

<table>
  <tbody>
    <tr>
      <td>

`bytes`

</td>
      <td>

`False`

</td>
      <td>return iterable of strings</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>

return iterable of `bytes`

</td>
    </tr>
    <tr>
      <td>

`encoding`

</td>
      <td>

`None`

</td>
      <td>

use the default encoding (UTF-8) for encoding strings or decoding `bytes` objects

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`str`

</td>
      <td>use a different encoding</td>
    </tr>
  </tbody>
</table>

**requires** queued stdout/stderr

### Chain processes / pass streams

```python
process = source_arguments >> start(...) + arguments >> start(...)
# or
source_process = source_arguments >> start(..., pass_stdout=True)
process = source_process + arguments >> start(...)
```

```python
process = source_arguments >> start(...) - arguments >> start(...)
# or
source_process = source_arguments >> start(..., pass_stderr=True)
process = source_process - arguments >> start(...)
```

```python
source_process = process.get_source_process()
```

- `process >> wait(...)` waits for the processes from left/source to right/target

### Shortcut

```python
object = object >> run(*args)
# optionally one of
.cast_int     # shortcut for `typing.cast(int, ...)`
.cast_str     #          for `typing.cast(str, ...)`
.cast_bytes   #          for `typing.cast(bytes, ...)`
.cast_strs    #          for `typing.cast(tuple[str, str], ...)`
.cast_bytess  #          for `typing.cast(tuple[bytes, bytes], ...)`
```

<table>
  <tbody>
    <tr>
      <td>

`*args`

</td>
      <td>none</td>
      <td>

short for `>> start() >> wait()`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

sequence of objects returned by `start(...)`, `write(...)`, `wait(...)` and `read(...)`

</td>
      <td>

short for `>> start(...) {* >> write(...) *} >> {wait(...) | read(...)}`

</td>
    <tr>
  </tbody>
</table>

### Other

#### LineStream

If you want to use `wait` and process the streams line by line at the same time, you can use `LineStream`.

Example:

```python
import subprocess_shell
import sys

def function(line_string):
    pass

process >> wait(stdout=subprocess_shell.LineStream(function, sys.stdout))
```

## Motivation

Shell scripting is great for simple tasks.
When tasks become more complex, e.g. hard to chain or require non-trivial processing, I always switch to Python.
The interface provided by _subprocess_ is rather verbose and parts that would look trivial in a shell script end up a repetitive mess.
After refactoring up the mess once too often, it was time for a change.

## See also

- [_Plumbum_](https://github.com/tomerfiliba/plumbum)
- [_sh_](https://github.com/amoffat/sh)

## Why the name subprocess_shell

Simply because I like the picture of _subprocess_ with a sturdy layer that is easy and safe to handle.
Also, while writing `import subprocess` it is easy to remember to add `_shell`.

Before subprocess_shell I chose to call it shell.
This was a bad name for several reasons, but most notably because the term shell is commonly used for applications providing an interface to the operating system.

---
