"""
Compatibility layer for the legacy ``pbgui_help`` import path.

All helper text has been moved into ``pbgui.pbgui_help`` but many modules
still import it from the repository root. Re-export everything here so the
old imports continue to resolve without touching every consumer.
"""

from pbgui import pbgui_help as _impl
from pbgui.pbgui_help import *  # noqa: F401,F403

try:
    __all__ = _impl.__all__  # type: ignore[attr-defined]
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]

del _impl
