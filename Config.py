"""
Compatibility alias for the legacy ``Config`` module path.

Historically, consumers imported ``Config``, ``ConfigV7``, ``BalanceCalculator``,
and ``Logging`` from the project root. The real implementations now live under
the ``pbgui`` package, so we re-export them here to avoid touching every caller.
"""

from pbgui.configs.v6.config import Config as _Config
from pbgui.configs.v7.config import ConfigV7
from pbgui.balance_calculator import BalanceCalculator
from pbgui.configs.v7.logging import Logging
from pbgui.configs.v7.bounds import Bounds

Config = _Config

__all__ = ["Config", "ConfigV7", "BalanceCalculator", "Logging", "Bounds"]
