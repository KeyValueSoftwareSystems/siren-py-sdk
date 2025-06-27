"""Asynchronous entry point for Siren SDK.

Provides :class:`AsyncSirenClient` which mirrors the synchronous
:class:`siren.client.SirenClient` API but exposes awaitable domain clients for
**all** supported Siren domains (webhooks, messaging, templates, channel
templates, users, workflows). Each synchronous method has an equivalent
asynchronous counterpart with the same name – simply prepend ``await`` when
using the async client.
"""

from __future__ import annotations

import os
from typing import Literal

from .clients.channel_templates_async import AsyncChannelTemplateClient
from .clients.messaging_async import AsyncMessageClient
from .clients.templates_async import AsyncTemplateClient
from .clients.users_async import AsyncUserClient
from .clients.webhooks_async import AsyncWebhookClient
from .clients.workflows_async import AsyncWorkflowClient


class AsyncSirenClient:  # noqa: D101
    API_URLS = {
        "dev": "https://api.dev.trysiren.io",
        "prod": "https://api.trysiren.io",
    }

    def __init__(
        self,
        *,
        api_key: str | None = None,
        env: Literal["dev", "prod"] | None = None,
    ):
        """Create a new *asynchronous* Siren client.

        Args:
            api_key: Siren API key. If ``None``, falls back to the ``SIREN_API_KEY`` env-var.
            env: Deployment environment – ``"dev"`` or ``"prod"``. If ``None``, uses ``SIREN_ENV`` or defaults to ``"prod"``.
        """
        if api_key is None:
            api_key = os.getenv("SIREN_API_KEY")
        if api_key is None:
            raise ValueError(
                "The api_key must be set either by passing api_key to the client or by setting the SIREN_API_KEY environment variable"
            )
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
        self._message_client = AsyncMessageClient(
            api_key=self.api_key, base_url=self.base_url
        )
        self._template_client = AsyncTemplateClient(
            api_key=self.api_key, base_url=self.base_url
        )
        self._channel_template_client = AsyncChannelTemplateClient(
            api_key=self.api_key, base_url=self.base_url
        )
        self._user_client = AsyncUserClient(
            api_key=self.api_key, base_url=self.base_url
        )
        self._workflow_client = AsyncWorkflowClient(
            api_key=self.api_key, base_url=self.base_url
        )

    # ---- Domain accessors ----
    @property
    def webhook(self) -> AsyncWebhookClient:
        """Non-blocking webhook operations."""
        return self._webhook_client

    @property
    def message(self) -> AsyncMessageClient:
        """Non-blocking message operations."""
        return self._message_client

    @property
    def template(self) -> AsyncTemplateClient:
        """Asynchronous template operations."""
        return self._template_client

    @property
    def channel_template(self) -> AsyncChannelTemplateClient:
        """Asynchronous channel-template operations."""
        return self._channel_template_client

    @property
    def user(self) -> AsyncUserClient:
        """Asynchronous user operations."""
        return self._user_client

    @property
    def workflow(self) -> AsyncWorkflowClient:
        """Asynchronous workflow operations."""
        return self._workflow_client

    # ---- Context management ----
    async def aclose(self) -> None:
        """Release underlying HTTP resources."""
        await self._webhook_client.aclose()
        await self._message_client.aclose()
        await self._template_client.aclose()
        await self._channel_template_client.aclose()
        await self._user_client.aclose()
        await self._workflow_client.aclose()

    async def __aenter__(self) -> AsyncSirenClient:
        """Enter async context manager returning *self*."""
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        """Exit async context manager, closing transports."""
        await self.aclose()
