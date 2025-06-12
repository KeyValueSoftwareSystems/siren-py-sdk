"""Asynchronous entry point for Siren SDK.

Provides :class:`AsyncSirenClient` which mirrors the synchronous
:class:`siren.client.SirenClient` API but exposes awaitable domain clients.
Currently only the *webhook* domain is implemented; other domains will follow
incrementally.
"""

from __future__ import annotations

import os
from typing import Literal

from .clients.webhooks_async import AsyncWebhookClient


class AsyncSirenClient:  # noqa: D101
    API_URLS = {
        "dev": "https://api.dev.trysiren.io",
        "prod": "https://api.trysiren.io",
    }

    def __init__(self, api_key: str, env: Literal["dev", "prod"] | None = None):
        """Create a new *asynchronous* Siren client.

        Args:
            api_key: Bearer token obtained from the Siren dashboard.
            env: Target environment – ``"dev"`` (default when ``SIREN_ENV=dev``)
                or ``"prod"`` (default).
        """
        self.api_key = api_key

        if env is None:
            env = os.getenv("SIREN_ENV", "prod")

        if env not in self.API_URLS:
            raise ValueError(
                f"Invalid environment '{env}'. Must be one of: {list(self.API_URLS.keys())}"
            )

        self.env: Literal["dev", "prod"] = env  # concrete
        self.base_url = self.API_URLS[env]

        # Domain clients
        self._webhook_client = AsyncWebhookClient(
            api_key=self.api_key, base_url=self.base_url
        )

    # ---- Domain accessors ----
    @property
    def webhook(self) -> AsyncWebhookClient:
        """Non-blocking webhook operations."""
        return self._webhook_client

    # ---- Context management ----
    async def aclose(self) -> None:
        """Release underlying HTTP resources."""
        await self._webhook_client.aclose()

    async def __aenter__(self) -> AsyncSirenClient:
        """Enter async context manager returning *self*."""
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        """Exit async context manager, closing transports."""
        await self.aclose()
