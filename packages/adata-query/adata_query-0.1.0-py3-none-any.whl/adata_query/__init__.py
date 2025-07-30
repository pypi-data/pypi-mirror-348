# -- configure logging: -------------------------------------------------------
from ._logging import configure_logging

logger = configure_logging()

# -- fetch version: -----------------------------------------------------------
from .__version__ import __version__

# -- functional imports: ------------------------------------------------------
from . import _core
from ._core import format_data, fetch, locate

# -- export: ------------------------------------------------------------------
__all__ = ["format_data", "fetch", "locate", "_core", "__version__", "logger"]
