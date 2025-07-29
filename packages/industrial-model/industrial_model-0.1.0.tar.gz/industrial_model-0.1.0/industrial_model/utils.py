from collections.abc import Callable, Generator
from datetime import datetime
from typing import (
    Any,
    ParamSpec,
    TypeVar,
)

from anyio import to_thread

TAny = TypeVar("TAny")
T_Retval = TypeVar("T_Retval")
P = ParamSpec("P")


def datetime_to_ms_iso_timestamp(dt: datetime) -> str:
    if not isinstance(dt, datetime):
        raise ValueError(f"Expected datetime object, got {type(dt)}")
    if dt.tzinfo is None:
        dt = dt.astimezone()
    return dt.isoformat(timespec="milliseconds")


def chunk_list(
    entries: list[TAny], chunk_size: int
) -> Generator[list[TAny], Any, None]:
    for i in range(0, len(entries), chunk_size):
        start = i
        end = i + chunk_size
        yield entries[start:end]


async def run_async(
    func: Callable[..., T_Retval],
    *args: object,
    cancellable: bool = False,
) -> T_Retval:
    return await to_thread.run_sync(func, *args, cancellable=cancellable)
