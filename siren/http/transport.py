"""HTTP transport abstraction for Siren SDK.

The SDK exposes two transports:
1. ``SyncTransport`` – wraps the blocking ``requests`` API for backwards-compatibility.
2. ``AsyncTransport`` – wraps an ``httpx.AsyncClient`` for non-blocking access.

Both classes expose the same ``request`` signature so domain clients can be
written once and injected with the appropriate transport implementation.
"""

from __future__ import annotations

from typing import Any  # noqa: D401

import httpx  # type: ignore
import requests

__all__ = ["SyncTransport", "AsyncTransport"]


class SyncTransport:  # noqa: D101 – Simple wrapper, docstring at class level
    def __init__(self, timeout: int = 10) -> None:
        """Create a synchronous transport wrapper.

        Args:
            timeout: The request timeout in seconds.
        """
        self._timeout = timeout
        # For now keep compatibility: still use the global ``requests`` API rather
        # than an ``httpx.Client`` so existing unit-tests remain untouched. This
        # branch can later be switched to ``httpx.Client`` once the test mocks
        # are migrated.

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        """Perform a blocking HTTP request using ``requests``."""
        return requests.request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            params=params,
            timeout=self._timeout,
        )


class AsyncTransport:  # noqa: D101 – Simple wrapper, docstring at class level
    def __init__(self, timeout: int = 10) -> None:
        """Instantiate the transport with an internal ``httpx.AsyncClient``."""
        self._client = httpx.AsyncClient(timeout=timeout)

    async def request(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """Make an asynchronous HTTP request using ``httpx.AsyncClient``."""
        response = await self._client.request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            params=params,
        )
        return response

    async def aclose(self) -> None:  # noqa: D401 – simple verb
        """Close the underlying ``httpx`` client."""
        await self._client.aclose()

    # Enable async context-manager usage
    async def __aenter__(self) -> AsyncTransport:
        """Enter async context manager."""
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        """Exit context manager, ensure transport is closed."""
        await self.aclose()
