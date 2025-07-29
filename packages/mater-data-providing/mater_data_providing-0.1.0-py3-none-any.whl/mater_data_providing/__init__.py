import logging
from importlib.metadata import PackageNotFoundError, version

from .core import metadata_definition, provider_definition, replace_equivalence, to_json

# Version
try:
    __version__ = version("mater-data-providing")
except PackageNotFoundError:
    __version__ = "unknown"

# Wildcard imports
__all__ = [
    "metadata_definition",
    "provider_definition",
    "to_json",
    "replace_equivalence",
]

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
