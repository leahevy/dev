import os
import tempfile

from contextlib import contextmanager, ExitStack


from pathlib import Path
from typing import Generator


tmpdir = tempfile.TemporaryDirectory
tmpfile = tempfile.NamedTemporaryFile


@contextmanager
def cd(path: str | Path) -> Generator[Path, None, None]:
    if isinstance(path, str):
        path = Path(path)
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(origin)


class cdtmpdir:
    """
    >>> a = os.getcwd()
    >>> b = None
    >>> with cdtmpdir() as p:
    ...     b = os.path.realpath((os.getcwd()))
    ...     p == b
    True

    >>> c = os.getcwd()
    >>> a != b
    True

    >>> b != c
    True

    >>> a == c
    True

    >>> with cdtmpdir() as p:
    ...     b = os.getcwd()
    ...     raise ValueError("some error")
    Traceback (most recent call last):
        ...
    ValueError: some error

    >>> c = os.getcwd()
    >>> a != b
    True

    >>> a == c
    True
    """

    def __init__(self):
        self._tmp = tmpdir()

    def __enter__(self):
        tmppath = None
        with ExitStack() as stack:
            tmppath = os.path.realpath(stack.enter_context(self._tmp))
            stack.enter_context(cd(tmppath))
            self._stack = stack.pop_all()
        return tmppath

    def __exit__(self, exc_type, exc, traceback):
        self._stack.__exit__(exc_type, exc, traceback)


__all__ = ["cd", "tmpdir", "tmpfile", "cdtmpdir"]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
