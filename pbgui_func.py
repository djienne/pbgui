"""
Compatibility shim exposing the legacy ``pbgui_func`` module path.

Historically, modules imported helpers as ``from pbgui_func import ...``.
The actual implementation now lives under ``pbgui.pbgui_func``; this file
re-exports those symbols so existing imports continue to work.
"""

from pbgui import pbgui_func as _impl
from pbgui.pbgui_func import *  # noqa: F401,F403

try:
    __all__ = _impl.__all__  # type: ignore[attr-defined]
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]

del _impl
