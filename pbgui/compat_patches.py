"""Runtime patches to keep legacy imports and UI hooks working."""

from importlib import import_module
from typing import Any


def _patch_bot_ui():
    bot_module = import_module("pbgui.configs.v7.bot")
    bot_ui = import_module("pbgui.ui.bot_ui")
    bot_class = getattr(bot_module, "Bot")

    if not hasattr(bot_class, "edit"):
        setattr(bot_class, "edit", lambda self: bot_ui.edit(self))
    if not hasattr(bot_class, "edit_cf"):
        setattr(bot_class, "edit_cf", lambda self: bot_ui.edit_cf(self))
    if not hasattr(bot_class, "edit_co"):
        setattr(bot_class, "edit_co", lambda self: bot_ui.edit_co(self))


def _patch_config_ui():
    config_module = import_module("pbgui.configs.v7.config")
    config_v7_class = getattr(config_module, "ConfigV7")
    config_v6_module = import_module("pbgui.configs.v6.config")
    config_v6_class = getattr(config_v6_module, "Config")

    config_v7_ui = import_module("pbgui.ui.config_v7_ui")
    config_v6_ui = import_module("pbgui.ui.config_v6_ui")

    if not hasattr(config_v7_class, "view_coin_overrides"):
        setattr(
            config_v7_class,
            "view_coin_overrides",
            lambda self: config_v7_ui.view_coin_overrides(self),
        )
    if not hasattr(config_v7_class, "edit_coin_override"):
        setattr(
            config_v7_class,
            "edit_coin_override",
            lambda self, symbol: config_v7_ui.edit_coin_override(self, symbol),
        )
    if not hasattr(config_v7_class, "clean_co_session_state"):
        setattr(
            config_v7_class,
            "clean_co_session_state",
            lambda self: config_v7_ui.clean_co_session_state(self),
        )

    if not hasattr(config_v6_class, "edit_config"):
        setattr(config_v6_class, "edit_config", lambda self: config_v6_ui.edit_config(self))


def _patch_bounds():
    bounds_module = import_module("pbgui.configs.v7.bounds")
    bounds_class = getattr(bounds_module, "Bounds")

    if getattr(bounds_class, "__pb_bounds_patch__", False):
        return

    def _bounds_getattr(self, name: str) -> Any:
        internal = f"_{name}"
        dct = object.__getattribute__(self, "__dict__")
        if internal in dct:
            return object.__getattribute__(self, internal)
        raise AttributeError(name)

    def _bounds_setattr(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return

        if name.startswith(("long_", "short_")) and name.endswith(("_0", "_1")):
            internal = f"_{name}"
            dct = object.__getattribute__(self, "__dict__")
            if internal in dct:
                object.__setattr__(self, internal, value)

            key = name[:-2]
            idx = 0 if name.endswith("_0") else 1
            try:
                bounds = object.__getattribute__(self, "_bounds")
                if key in bounds:
                    bounds[key][idx] = value
            except AttributeError:
                pass
            return

        object.__setattr__(self, name, value)

    bounds_class.__getattr__ = _bounds_getattr  # type: ignore[attr-defined]
    bounds_class.__setattr__ = _bounds_setattr  # type: ignore[attr-defined]
    bounds_class.__pb_bounds_patch__ = True


def apply_runtime_patches():
    """Ensure UI helper methods are attached even if modules were imported earlier."""
    _patch_bot_ui()
    _patch_config_ui()
    _patch_bounds()
