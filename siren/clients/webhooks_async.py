"""Asynchronous webhook client for the Siren API."""

from __future__ import annotations

from ..models.webhooks import (
    InboundWebhookRequest,
    NotificationsWebhookRequest,
    WebhookConfig,
    WebhookResponse,
)
from .async_base import AsyncBaseClient


class AsyncWebhookClient(AsyncBaseClient):  # noqa: D101 – simple wrapper
    async def configure_notifications(self, url: str) -> WebhookConfig:
        """Configure the notifications webhook (async)."""
        payload = {"webhook_config": {"url": url}}

        response = await self._make_request(
            method="PUT",
            endpoint="/api/v1/public/webhooks",
            request_model=NotificationsWebhookRequest,
            response_model=WebhookResponse,
            data=payload,
        )
        # ``response`` is WebhookData; return nested config.
        return response.webhook_config  # type: ignore[return-value]

    async def configure_inbound(self, url: str) -> WebhookConfig:
        """Configure the inbound message webhook (async)."""
        payload = {"inbound_webhook_config": {"url": url}}

        response = await self._make_request(
            method="PUT",
            endpoint="/api/v1/public/webhooks",
            request_model=InboundWebhookRequest,
            response_model=WebhookResponse,
            data=payload,
        )
        return response.inbound_webhook_config  # type: ignore[return-value]
