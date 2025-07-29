"""
dataguy package
=======

A lightweight toolkit for ingesting, inspecting, and transforming
small‑to‑medium datasets or texts with the help of an LLM.

Import convenience::

    >>> from dataguy import DataGuy, ContextManager, validate_file_path, LLMResponseCache
"""

from .core import DataGuy
from .context_manager import ContextManager
from .utils import validate_file_path, LLMResponseCache

__all__ = ["DataGuy", "ContextManager", "validate_file_path", "LLMResponseCache"]
__version__ = "0.1.5"
