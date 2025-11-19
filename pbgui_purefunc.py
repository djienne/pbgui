"""
Compatibility shim exposing the legacy ``pbgui_purefunc`` module path.

Helper functions were moved into ``pbgui.pbgui_purefunc`` but many modules
still import them from the old top-level module. Re-export everything here
so those imports keep working without modifying every call site at once.
"""

from pbgui import pbgui_purefunc as _impl
from pbgui.pbgui_purefunc import *  # noqa: F401,F403

try:
    __all__ = _impl.__all__  # type: ignore[attr-defined]
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]

del _impl
