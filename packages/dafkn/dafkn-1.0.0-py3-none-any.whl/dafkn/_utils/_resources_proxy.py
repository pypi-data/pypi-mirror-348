from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `dafkn.resources` module.

    This is used so that we can lazily import `dafkn.resources` only when
    needed *and* so that users can just import `dafkn` and reference `dafkn.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("dafkn.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
