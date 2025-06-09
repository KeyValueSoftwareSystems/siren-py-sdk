"""Unit tests for the messaging module of the Siren SDK."""

import pytest
import requests
from requests_mock import Mocker as RequestsMocker

from siren.client import SirenClient
from siren.messaging import MessagingManager

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"


class TestMessagingManager:
    """Tests for the MessagingManager class."""

    def test_send_message_success(self, requests_mock: RequestsMocker):
        """Test successful message sending."""
        manager = MessagingManager(api_key=API_KEY, base_url=BASE_URL)
        template_name = "test_template"
        channel = "SLACK"
        recipient_type = "direct"
        recipient_value = "U123ABC"
        template_variables = {"name": "John Doe"}

        expected_payload = {
            "template": {"name": template_name},
            "recipient": {"type": recipient_type, "value": recipient_value},
            "channel": channel,
            "templateVariables": template_variables,
        }
        mock_response_data = {"data": {"notificationId": "notif_123"}, "error": None}

        requests_mock.post(
            f"{BASE_URL}/send-messages",
            json=mock_response_data,
            status_code=200,
        )

        response = manager.send_message(
            template_name=template_name,
            channel=channel,
            recipient_type=recipient_type,
            recipient_value=recipient_value,
            template_variables=template_variables,
        )

        assert response == mock_response_data
        assert requests_mock.called_once
        last_request = requests_mock.last_request
        assert last_request is not None
        assert last_request.json() == expected_payload
        assert last_request.headers["Authorization"] == f"Bearer {API_KEY}"
        assert last_request.headers["Content-Type"] == "application/json"
        assert last_request.headers["Accept"] == "application/json"

    def test_send_message_success_no_variables(self, requests_mock: RequestsMocker):
        """Test successful message sending without template variables."""
        manager = MessagingManager(api_key=API_KEY, base_url=BASE_URL)
        template_name = "test_template_no_vars"
        channel = "EMAIL"
        recipient_type = "direct"
        recipient_value = "test@example.com"

        expected_payload = {
            "template": {"name": template_name},
            "recipient": {"type": recipient_type, "value": recipient_value},
            "channel": channel,
        }
        mock_response_data = {"data": {"notificationId": "notif_456"}, "error": None}

        requests_mock.post(
            f"{BASE_URL}/send-messages",
            json=mock_response_data,
            status_code=200,
        )

        response = manager.send_message(
            template_name=template_name,
            channel=channel,
            recipient_type=recipient_type,
            recipient_value=recipient_value,
        )

        assert response == mock_response_data
        assert requests_mock.called_once
        last_request = requests_mock.last_request
        assert last_request is not None
        assert last_request.json() == expected_payload

    def test_send_message_http_error_with_json_response(
        self, requests_mock: RequestsMocker
    ):
        """Test HTTP error with JSON response during message sending."""
        manager = MessagingManager(api_key=API_KEY, base_url=BASE_URL)
        error_response = {"error": "Bad Request", "message": "Invalid template name"}
        requests_mock.post(
            f"{BASE_URL}/send-messages",
            json=error_response,
            status_code=400,
        )

        response = manager.send_message(
            template_name="invalid_template",
            channel="SLACK",
            recipient_type="direct",
            recipient_value="U123",
        )
        assert response == error_response

    def test_send_message_http_error_no_json_response(
        self, requests_mock: RequestsMocker
    ):
        """Test HTTP error without JSON response during message sending."""
        manager = MessagingManager(api_key=API_KEY, base_url=BASE_URL)
        requests_mock.post(
            f"{BASE_URL}/send-messages",
            text="Internal Server Error",
            status_code=500,
        )

        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            manager.send_message(
                template_name="any_template",
                channel="SLACK",
                recipient_type="direct",
                recipient_value="U123",
            )
        assert excinfo.value.response.status_code == 500
        assert excinfo.value.response.text == "Internal Server Error"

    def test_send_message_request_exception(self, requests_mock: RequestsMocker):
        """Test requests.exceptions.RequestException during message sending."""
        manager = MessagingManager(api_key=API_KEY, base_url=BASE_URL)
        requests_mock.post(
            f"{BASE_URL}/send-messages",
            exc=requests.exceptions.ConnectTimeout,
        )

        with pytest.raises(requests.exceptions.RequestException):
            manager.send_message(
                template_name="any_template",
                channel="SLACK",
                recipient_type="direct",
                recipient_value="U123",
            )


def test_siren_client_send_message(mocker):
    """Test SirenClient.send_message calls MessagingManager correctly."""
    client = SirenClient(api_key=API_KEY)
    mock_messaging_manager_send = mocker.patch.object(client._messaging, "send_message")
    mock_response = {"data": "success"}
    mock_messaging_manager_send.return_value = mock_response

    template_name = "client_test_template"
    channel = "EMAIL"
    recipient_type = "direct_client"
    recipient_value = "client@example.com"
    template_variables = {"client_var": "client_val"}

    response = client.send_message(
        template_name=template_name,
        channel=channel,
        recipient_type=recipient_type,
        recipient_value=recipient_value,
        template_variables=template_variables,
    )

    assert response == mock_response
    mock_messaging_manager_send.assert_called_once_with(
        template_name=template_name,
        channel=channel,
        recipient_type=recipient_type,
        recipient_value=recipient_value,
        template_variables=template_variables,
    )
