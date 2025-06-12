"""Unit tests for the webhook client using BaseClient."""

from unittest.mock import Mock, patch

import pytest

from siren.client import SirenClient
from siren.clients.webhooks import WebhookClient
from siren.exceptions import SirenAPIError, SirenSDKError
from siren.models.webhooks import WebhookConfig

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"
WEBHOOK_URL = "https://example.com/webhook"


def mock_response(status_code: int, json_data: dict = None):
    """Helper function to create a mock HTTP response."""
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data if json_data is not None else {}
    return mock_resp


class TestWebhookClient:
    """Tests for the WebhookClient class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = WebhookClient(api_key=API_KEY, base_url=BASE_URL)

    @patch("siren.clients.base.requests.request")
    def test_configure_notifications_webhook_success(self, mock_request):
        """Test successful configuration of notifications webhook."""
        # Mock successful API response
        mock_api_response = {
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
        mock_request.return_value = mock_response(200, mock_api_response)

        # Call the method
        result = self.client.configure_notifications(url=WEBHOOK_URL)

        # Verify result is WebhookConfig object
        assert isinstance(result, WebhookConfig)
        assert result.url == WEBHOOK_URL
        assert result.verification_key == "test_key_123"
        assert result.headers == []

        # Verify request was made correctly with BaseClient
        mock_request.assert_called_once_with(
            method="PUT",
            url=f"{BASE_URL}/api/v1/public/webhooks",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={"webhookConfig": {"url": WEBHOOK_URL}},
            params=None,
            timeout=10,
        )

    @patch("siren.clients.base.requests.request")
    def test_configure_inbound_message_webhook_success(self, mock_request):
        """Test successful configuration of inbound message webhook."""
        # Mock successful API response
        mock_api_response = {
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
        mock_request.return_value = mock_response(200, mock_api_response)

        # Call the method
        result = self.client.configure_inbound(url=WEBHOOK_URL)

        # Verify result is WebhookConfig object
        assert isinstance(result, WebhookConfig)
        assert result.url == WEBHOOK_URL
        assert result.verification_key == "test_key_456"
        assert result.headers == []

        # Verify request was made correctly with BaseClient
        mock_request.assert_called_once_with(
            method="PUT",
            url=f"{BASE_URL}/api/v1/public/webhooks",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={"inboundWebhookConfig": {"url": WEBHOOK_URL}},
            params=None,
            timeout=10,
        )

    @pytest.mark.parametrize(
        "method_name,config_key",
        [
            ("configure_notifications", "webhookConfig"),
            ("configure_inbound", "inboundWebhookConfig"),
        ],
    )
    @patch("siren.clients.base.requests.request")
    def test_webhook_api_error(self, mock_request, method_name: str, config_key: str):
        """Test API error during webhook configuration."""
        # Mock API error response
        mock_api_error = {
            "data": None,
            "error": {
                "errorCode": "INVALID_REQUEST",
                "message": "Invalid webhook URL format",
            },
        }
        mock_request.return_value = mock_response(400, mock_api_error)

        method_to_call = getattr(self.client, method_name)

        with pytest.raises(SirenAPIError) as exc_info:
            method_to_call(url=WEBHOOK_URL)

        assert exc_info.value.error_code == "INVALID_REQUEST"
        assert "Invalid webhook URL format" in exc_info.value.api_message

        # Verify correct payload was sent
        expected_json = {config_key: {"url": WEBHOOK_URL}}
        mock_request.assert_called_once_with(
            method="PUT",
            url=f"{BASE_URL}/api/v1/public/webhooks",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json=expected_json,
            params=None,
            timeout=10,
        )

    @pytest.mark.parametrize(
        "method_name",
        ["configure_notifications", "configure_inbound"],
    )
    @patch("siren.clients.base.requests.request")
    def test_webhook_network_error(self, mock_request, method_name: str):
        """Test network error during webhook configuration."""
        from requests.exceptions import ConnectionError

        # Mock network error
        mock_request.side_effect = ConnectionError("Connection failed")

        method_to_call = getattr(self.client, method_name)

        with pytest.raises(SirenSDKError) as exc_info:
            method_to_call(url=WEBHOOK_URL)

        assert "Connection failed" in exc_info.value.message


def test_siren_client_configure_notifications_webhook():
    """Test SirenClient.webhook.configure_notifications calls WebhookClient correctly."""
    client = SirenClient(api_key=API_KEY, env="dev")

    with patch.object(client._webhook_client, "configure_notifications") as mock_method:
        # Create WebhookConfig using model_validate to handle aliases properly
        mock_config = WebhookConfig.model_validate(
            {"url": WEBHOOK_URL, "headers": [], "verificationKey": "test_key_123"}
        )
        mock_method.return_value = mock_config

        result = client.webhook.configure_notifications(url=WEBHOOK_URL)

        mock_method.assert_called_once_with(url=WEBHOOK_URL)
        assert result == mock_config


def test_siren_client_configure_inbound_message_webhook():
    """Test SirenClient.webhook.configure_inbound calls WebhookClient correctly."""
    client = SirenClient(api_key=API_KEY, env="dev")

    with patch.object(client._webhook_client, "configure_inbound") as mock_method:
        # Create WebhookConfig using model_validate to handle aliases properly
        mock_config = WebhookConfig.model_validate(
            {"url": WEBHOOK_URL, "headers": [], "verificationKey": "test_key_456"}
        )
        mock_method.return_value = mock_config

        result = client.webhook.configure_inbound(url=WEBHOOK_URL)

        mock_method.assert_called_once_with(url=WEBHOOK_URL)
        assert result == mock_config
