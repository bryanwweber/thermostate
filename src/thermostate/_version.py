"""The version of thermohw."""
from typing import Tuple

__version_info__ = (0, 5, 4, 'dev0')  # type: Tuple[int, int, int, str]
__version__ = '.'.join([str(v) for v in __version_info__ if str(v)])