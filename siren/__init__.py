"""Siren SDK for Python.

Public API:
    SirenClient – synchronous client (blocking HTTP based on *requests*).
    AsyncSirenClient – asynchronous client (non-blocking HTTP based on *httpx*).

Both clients expose the same domain‐specific namespaces (``.message``,
``.template``, etc.). Choose the async variant whenever your application is
already running inside an asyncio event-loop or needs to issue many concurrent
requests.
"""

from .async_client import AsyncSirenClient
from .client import SirenClient

__all__ = ["AsyncSirenClient", "SirenClient"]

__version__ = "0.2.0"
