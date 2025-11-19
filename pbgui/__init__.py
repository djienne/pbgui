"""Package initializer exposing helpers without eager imports.

Legacy modules sometimes do ``from pbgui import pbgui_func``. Importing the
Streamlit-heavy modules eagerly would trigger circular imports, so we load them
on demand via ``__getattr__``.
"""

from importlib import import_module
from types import ModuleType
from typing import List

__all__: List[str] = ["pbgui_func", "pbgui_purefunc"]


def __getattr__(name: str) -> ModuleType:
    if name in __all__:
        module = import_module(f"pbgui.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module 'pbgui' has no attribute '{name}'")
