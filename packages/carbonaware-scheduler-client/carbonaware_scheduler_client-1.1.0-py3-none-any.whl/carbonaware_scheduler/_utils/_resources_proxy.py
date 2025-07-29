from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `carbonaware_scheduler.resources` module.

    This is used so that we can lazily import `carbonaware_scheduler.resources` only when
    needed *and* so that users can just import `carbonaware_scheduler` and reference `carbonaware_scheduler.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("carbonaware_scheduler.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
