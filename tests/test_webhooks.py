"""Unit tests for the webhook module of the Siren SDK."""

import pytest
import requests
from requests_mock import Mocker as RequestsMocker

from siren.client import SirenClient
from siren.webhooks import WebhookManager

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"
WEBHOOK_URL = "https://example.com/webhook"


class TestWebhookManager:
    """Tests for the WebhookManager class."""

    def test_configure_notifications_webhook_success(
        self, requests_mock: RequestsMocker
    ):
        """Test successful configuration of notifications webhook."""
        manager = WebhookManager(api_key=API_KEY, base_url=BASE_URL)
        expected_response = {
            "data": {"id": "wh_123", "webhookConfig": {"url": WEBHOOK_URL}}
        }
        requests_mock.put(
            f"{BASE_URL}/api/v1/public/webhooks",
            json=expected_response,
            status_code=200,
        )
        response = manager.configure_notifications_webhook(url=WEBHOOK_URL)
        assert response == expected_response
        assert requests_mock.last_request is not None
        assert requests_mock.last_request.json() == {
            "webhookConfig": {"url": WEBHOOK_URL}
        }

    def test_configure_inbound_message_webhook_success(
        self, requests_mock: RequestsMocker
    ):
        """Test successful configuration of inbound message webhook."""
        manager = WebhookManager(api_key=API_KEY, base_url=BASE_URL)
        expected_response = {
            "data": {"id": "wh_456", "inboundWebhookConfig": {"url": WEBHOOK_URL}}
        }
        requests_mock.put(
            f"{BASE_URL}/api/v1/public/webhooks",
            json=expected_response,
            status_code=200,
        )
        response = manager.configure_inbound_message_webhook(url=WEBHOOK_URL)
        assert response == expected_response
        assert requests_mock.last_request is not None
        assert requests_mock.last_request.json() == {
            "inboundWebhookConfig": {"url": WEBHOOK_URL}
        }

    @pytest.mark.parametrize(
        "method_name",
        ["configure_notifications_webhook", "configure_inbound_message_webhook"],
    )
    def test_webhook_http_error_json_response(
        self, requests_mock: RequestsMocker, method_name: str
    ):
        """Test HTTP error with JSON response during webhook configuration."""
        manager = WebhookManager(api_key=API_KEY, base_url=BASE_URL)
        error_response = {"error": "Bad Request", "message": "Invalid URL"}
        requests_mock.put(
            f"{BASE_URL}/api/v1/public/webhooks",
            json=error_response,
            status_code=400,
        )
        method_to_call = getattr(manager, method_name)
        response = method_to_call(url=WEBHOOK_URL)
        assert response == error_response

    @pytest.mark.parametrize(
        "method_name",
        ["configure_notifications_webhook", "configure_inbound_message_webhook"],
    )
    def test_webhook_http_error_no_json_response(
        self, requests_mock: RequestsMocker, method_name: str
    ):
        """Test HTTP error without JSON response during webhook configuration."""
        manager = WebhookManager(api_key=API_KEY, base_url=BASE_URL)
        requests_mock.put(
            f"{BASE_URL}/api/v1/public/webhooks",
            text="Server Error",
            status_code=500,
        )
        method_to_call = getattr(manager, method_name)
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            method_to_call(url=WEBHOOK_URL)
        assert excinfo.value.response.status_code == 500
        assert excinfo.value.response.text == "Server Error"

    @pytest.mark.parametrize(
        "method_name",
        ["configure_notifications_webhook", "configure_inbound_message_webhook"],
    )
    def test_webhook_request_exception(
        self, requests_mock: RequestsMocker, method_name: str
    ):
        """Test requests.exceptions.RequestException during webhook configuration."""
        manager = WebhookManager(api_key=API_KEY, base_url=BASE_URL)
        requests_mock.put(
            f"{BASE_URL}/api/v1/public/webhooks",
            exc=requests.exceptions.Timeout("Connection timed out"),
        )
        method_to_call = getattr(manager, method_name)
        with pytest.raises(requests.exceptions.RequestException):
            method_to_call(url=WEBHOOK_URL)


def test_siren_client_configure_notifications_webhook(mocker):
    """Test SirenClient.configure_notifications_webhook calls WebhookManager correctly."""
    client = SirenClient(api_key=API_KEY)
    mock_webhook_manager_method = mocker.patch.object(
        client._webhooks, "configure_notifications_webhook"
    )
    expected_response = {"data": "success"}
    mock_webhook_manager_method.return_value = expected_response

    response = client.configure_notifications_webhook(url=WEBHOOK_URL)

    mock_webhook_manager_method.assert_called_once_with(url=WEBHOOK_URL)
    assert response == expected_response


def test_siren_client_configure_inbound_message_webhook(mocker):
    """Test SirenClient.configure_inbound_message_webhook calls WebhookManager correctly."""
    client = SirenClient(api_key=API_KEY)
    mock_webhook_manager_method = mocker.patch.object(
        client._webhooks, "configure_inbound_message_webhook"
    )
    expected_response = {"data": "success_inbound"}
    mock_webhook_manager_method.return_value = expected_response

    response = client.configure_inbound_message_webhook(url=WEBHOOK_URL)

    mock_webhook_manager_method.assert_called_once_with(url=WEBHOOK_URL)
    assert response == expected_response
