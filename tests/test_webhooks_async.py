"""Asynchronous tests for Siren webhook client."""

import httpx  # type: ignore
import pytest
import respx  # type: ignore

from siren.async_client import AsyncSirenClient
from siren.models.webhooks import WebhookConfig

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"
WEBHOOK_URL = "https://example.com/webhook"


@respx.mock
@pytest.mark.asyncio
async def test_async_configure_notifications_success():
    """Async configure_notifications returns expected WebhookConfig."""
    async with AsyncSirenClient(api_key=API_KEY, env="dev") as client:
        expected_json = {
            "data": {
                "id": "wh_123",
                "webhookConfig": {
                    "url": WEBHOOK_URL,
                    "headers": [],
                    "verificationKey": "test_key_123",
                },
            },
            "error": None,
        }
        route = respx.put(f"{BASE_URL}/api/v1/public/webhooks").mock(
            return_value=httpx.Response(200, json=expected_json)
        )

        response: WebhookConfig = await client.webhook.configure_notifications(
            url=WEBHOOK_URL
        )

        assert route.called
        assert isinstance(response, WebhookConfig)
        assert response.url == WEBHOOK_URL
        assert response.verification_key == "test_key_123"


@respx.mock
@pytest.mark.asyncio
async def test_async_configure_inbound_success():
    """Async configure_inbound returns expected WebhookConfig."""
    async with AsyncSirenClient(api_key=API_KEY, env="dev") as client:
        expected_json = {
            "data": {
                "id": "wh_456",
                "inboundWebhookConfig": {
                    "url": WEBHOOK_URL,
                    "headers": [],
                    "verificationKey": "test_key_456",
                },
            },
            "error": None,
        }
        route = respx.put(f"{BASE_URL}/api/v1/public/webhooks").mock(
            return_value=httpx.Response(200, json=expected_json)
        )

        response = await client.webhook.configure_inbound(url=WEBHOOK_URL)

        assert route.called
        assert isinstance(response, WebhookConfig)
        assert response.url == WEBHOOK_URL
        assert response.verification_key == "test_key_456"
