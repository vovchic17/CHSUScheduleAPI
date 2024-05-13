"""
Module rewrites all the public methods of the subclasses
of :code:`ABCApi` class of the library so they can run
the loop on their own if it's not already running.
"""

import asyncio
import functools
import inspect

from .api import ABCApi


def async_to_sync(obj: object, name: str) -> None:
    method = getattr(obj, name)

    @functools.wraps(method)
    def sync_wrapper(*args, **kwargs) -> object:
        coro = method(*args, **kwargs)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if loop.is_running():
            return coro
        return loop.run_until_complete(coro)

    setattr(obj, name, sync_wrapper)


def syncify(obj: object) -> None:
    for name in dir(obj):
        if not name.startswith("_") and inspect.iscoroutinefunction(
            getattr(obj, name)
        ):
            async_to_sync(obj, name)


for subclass in ABCApi.__subclasses__():
    syncify(subclass)
