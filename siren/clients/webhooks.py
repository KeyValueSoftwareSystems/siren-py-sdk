"""Webhook client for the Siren API."""

from ..models.webhooks import (
    InboundWebhookRequest,
    NotificationsWebhookRequest,
    WebhookConfig,
    WebhookResponse,
)
from .base import BaseClient


class WebhookClient(BaseClient):
    """Client for webhook configuration operations."""

    def configure_notifications(self, url: str) -> WebhookConfig:
        """Configure the webhook for notifications.

        Args:
            url: The URL to be configured for the notifications webhook.

        Returns:
            The webhook configuration object.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        payload = {"webhook_config": {"url": url}}

        response = self._make_request(
            method="PUT",
            endpoint="/api/v1/public/webhooks",
            request_model=NotificationsWebhookRequest,
            response_model=WebhookResponse,
            data=payload,
        )
        return response.webhook_config

    def configure_inbound(self, url: str) -> WebhookConfig:
        """Configure the webhook for inbound messages.

        Args:
            url: The URL to be configured for the inbound message webhook.

        Returns:
            The webhook configuration object.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        payload = {"inbound_webhook_config": {"url": url}}

        response = self._make_request(
            method="PUT",
            endpoint="/api/v1/public/webhooks",
            request_model=InboundWebhookRequest,
            response_model=WebhookResponse,
            data=payload,
        )
        return response.inbound_webhook_config
