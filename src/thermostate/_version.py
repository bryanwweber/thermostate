"""The version of ThermoState."""
from __future__ import annotations

__version_info__: tuple[int, int, int, str] = (1, 2, 2, "dev0")
__version__ = ".".join([str(v) for v in __version_info__ if str(v)])
