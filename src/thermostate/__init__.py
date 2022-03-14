from .thermostate import units, Q_, State, set_default_units  # noqa
from .abbreviations import EnglishEngineering, SystemInternational  # noqa

try:
    import importlib.metadata as implib
except ImportError:
    import importlib_metadata as implib

__version__ = implib.version("thermostate")
