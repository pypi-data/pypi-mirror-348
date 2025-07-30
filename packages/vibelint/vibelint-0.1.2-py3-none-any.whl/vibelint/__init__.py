"""
vibelint package initialization module.

vibelint/__init__.py
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("vibelint")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    "__version__",
]
