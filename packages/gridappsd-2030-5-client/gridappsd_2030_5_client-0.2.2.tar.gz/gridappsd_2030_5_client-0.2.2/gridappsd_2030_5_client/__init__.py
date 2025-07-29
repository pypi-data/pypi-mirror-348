"""
GridAppSD IEEE 2030.5 Client

A Python client library for IEEE 2030.5 (Smart Energy Profile 2.0) servers.
"""

__version__ = "0.1.0"

from .client import IEEE2030Client, IEEE2030EventHandler, ContentType
from .exceptions import (
    IEEE2030Error,
    AuthenticationError,
    ConnectionError,
    ResourceError,
    ParseError,
)

# Make important classes available at package level
__all__ = [
    "IEEE2030Client",
    "IEEE2030EventHandler",
    "ContentType",
    "IEEE2030Error",
    "AuthenticationError",
    "ConnectionError",
    "ResourceError",
    "ParseError",
]
