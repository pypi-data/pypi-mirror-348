"""Solving the Traveling Salesman Problem"""

from importlib.metadata import metadata

from .tsp import distance, tsp

_package_metadata = metadata(str(__package__))
__version__ = _package_metadata["Version"]
__author__ = _package_metadata.get("Author-email", "")

__all__ = ["__author__", "__version__", "distance", "tsp"]
