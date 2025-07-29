from .shelve import open
from . import serialer

__all__ = ["open", serialer]
try:
    from setuptools_scm import get_version
    __version__ = get_version()
except ImportError:
    __version__ = "0.0.0"