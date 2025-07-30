import sys
from collections.abc import Callable, Coroutine, Generator, Iterable, Mapping
from concurrent.futures import Future
from functools import wraps
from typing import Any, ParamSpec, TypeVar

import anyio.from_thread

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from exceptiongroup import ExceptionGroup
    from typing_extensions import Self

_P = ParamSpec('_P')
_T = TypeVar('_T')
_K = TypeVar('_K')
_V = TypeVar('_V')


def async_to_sync(
    func: Callable[_P, Coroutine[Any, Any, _T]],
) -> Callable[_P, _T]:
    @wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        return anyio.from_thread.run(lambda: func(*args, **kwargs))

    return wrapper


async def wrap_concurrent_future(future: Future[_T]) -> _T:
    if future.done() or future.exception():
        return future.result()
    event = anyio.Event()
    future.add_done_callback(lambda _: event.set())
    await event.wait()
    return future.result()


class FuturesDict(dict[_K, Coroutine[Any, Any, _V]]):
    """
    A dictionary which values are awaitable objects.
    It can be awaited to get a dictionary of results.

    .. code-block:: python

       async def foo(x: int) -> int:
           return x ** 2

       data = FuturesDict({1: foo(1), 2: foo(2)})
       assert await data == {1: 1, 2: 4}
    """

    def __await__(self) -> Generator[Any, Any, dict[_K, _V]]:
        return self.__await().__await__()

    async def __await(self) -> dict[_K, _V]:
        result: dict[_K, _V] = {}
        exceptions: list[Exception] = []
        for key, coro in self.items():
            try:
                result[key] = await coro
            except Exception as exc:
                exceptions.append(exc)
        if exceptions:
            raise ExceptionGroup('Multiple exceptions occurred', exceptions)
        return result

    @classmethod
    def from_concurrent_futures(cls, futures: Mapping[_K, Future[_V]]) -> Self:
        return cls({key: wrap_concurrent_future(value) for key, value in futures.items()})


def to_list(obj: Iterable[_T]) -> list[_T]:
    if isinstance(obj, list):
        return obj
    return list(obj)


def to_dict(obj: Mapping[_K, _V]) -> dict[_K, _V]:
    if isinstance(obj, dict):
        return obj
    return dict(obj)


def to_set(obj: Iterable[_T]) -> set[_T]:
    if isinstance(obj, set):
        return obj
    return set(obj)


def make_kwargs(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}
