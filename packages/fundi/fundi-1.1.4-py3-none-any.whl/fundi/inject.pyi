import typing
from typing import overload
from contextlib import ExitStack as SyncExitStack, AsyncExitStack

from fundi.types import CallableInfo

R = typing.TypeVar("R")

ExitStack = AsyncExitStack | SyncExitStack

@overload
def inject(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[typing.Generator[R, None, None]],
    stack: ExitStack,
    cache: typing.Mapping[typing.Callable, typing.Any] | None = None,
    override: typing.Mapping[typing.Callable, typing.Any] | None = None,
) -> R: ...
@overload
def inject(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[R],
    stack: ExitStack,
    cache: typing.Mapping[typing.Callable, typing.Any] | None = None,
    override: typing.Mapping[typing.Callable, typing.Any] | None = None,
) -> R: ...
@overload
async def ainject(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[typing.Generator[R, None, None]],
    stack: AsyncExitStack,
    cache: typing.Mapping[typing.Callable, typing.Any] | None = None,
    override: typing.Mapping[typing.Callable, typing.Any] | None = None,
) -> R: ...
@overload
async def ainject(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[typing.AsyncGenerator[R, None]],
    stack: AsyncExitStack,
    cache: typing.Mapping[typing.Callable, typing.Any] | None = None,
    override: typing.Mapping[typing.Callable, typing.Any] | None = None,
) -> R: ...
@overload
async def ainject(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[typing.Awaitable[R]],
    stack: AsyncExitStack,
    cache: typing.Mapping[typing.Callable, typing.Any] | None = None,
    override: typing.Mapping[typing.Callable, typing.Any] | None = None,
) -> R: ...
@overload
async def ainject(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[R],
    stack: AsyncExitStack,
    cache: typing.Mapping[typing.Callable, typing.Any] | None = None,
    override: typing.Mapping[typing.Callable, typing.Any] | None = None,
) -> R: ...
