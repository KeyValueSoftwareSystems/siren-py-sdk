"""Unit tests for the messaging client using BaseClient."""

from unittest.mock import Mock, patch

import pytest

from siren.clients.messaging import MessageClient
from siren.exceptions import SirenAPIError, SirenSDKError
from siren.models.messaging import ProviderCode

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"


class TestMessageClient:
    """Tests for MessageClient with BaseClient."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = MessageClient(api_key=API_KEY, base_url=BASE_URL)

    @patch("siren.clients.base.requests.request")
    def test_send_message_success(self, mock_request):
        """Test successful message sending with new BaseClient."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"notificationId": "test_msg_123"},
            "error": None,
        }
        mock_request.return_value = mock_response

        # Call the method
        result = self.client.send(
            template_name="test_template",
            channel="SLACK",
            recipient_value="U123ABC",
            template_variables={"name": "John"},
        )

        # Verify result
        assert result == "test_msg_123"

        # Verify request was made correctly
        mock_request.assert_called_once()
        call_args = mock_request.call_args

        # Check URL and method
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["url"] == f"{BASE_URL}/api/v1/public/send-messages"

        # Check payload has camelCase fields
        payload = call_args[1]["json"]
        assert "templateVariables" in payload
        assert payload["templateVariables"]["name"] == "John"
        assert payload["template"]["name"] == "test_template"

    @patch("siren.clients.base.requests.request")
    def test_get_message_status_success(self, mock_request):
        """Test successful message status retrieval."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"status": "DELIVERED"},
            "error": None,
        }
        mock_request.return_value = mock_response

        # Call the method
        result = self.client.get_status("test_msg_123")

        # Verify result
        assert result == "DELIVERED"

    @patch("siren.clients.base.requests.request")
    def test_get_replies_success(self, mock_request):
        """Test successful replies retrieval."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "text": "Reply 1",
                    "user": "U123",
                    "ts": "12345.6789",
                    "threadTs": "12345.0000",
                },
                {
                    "text": "Reply 2",
                    "user": "U456",
                    "ts": "12346.7890",
                    "threadTs": "12345.0000",
                },
            ],
            "error": None,
        }
        mock_request.return_value = mock_response

        # Call the method
        result = self.client.get_replies("test_msg_123")

        # Verify result
        assert len(result) == 2
        assert result[0].text == "Reply 1"
        assert result[0].user == "U123"
        assert result[1].text == "Reply 2"
        assert result[1].user == "U456"

    @patch("siren.clients.base.requests.request")
    def test_api_error_handling(self, mock_request):
        """Test that API errors are properly handled."""
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "data": None,
            "error": {"errorCode": "NOT_FOUND", "message": "Template not found"},
        }
        mock_request.return_value = mock_response

        # Should raise SirenAPIError
        with pytest.raises(SirenAPIError) as exc_info:
            self.client.send(
                template_name="nonexistent",
                channel="SLACK",
                recipient_value="U123",
            )

        assert exc_info.value.error_code == "NOT_FOUND"
        assert "Template not found" in exc_info.value.api_message

    @patch("siren.clients.base.requests.request")
    def test_send_message_without_template_variables(self, mock_request):
        """Test sending message without template variables."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"notificationId": "test_msg_456"},
            "error": None,
        }
        mock_request.return_value = mock_response

        # Call the method without template_variables
        result = self.client.send(
            template_name="simple_template",
            channel="EMAIL",
            recipient_value="test@example.com",
        )

        # Verify result
        assert result == "test_msg_456"

        # Verify payload excludes templateVariables when None
        payload = mock_request.call_args[1]["json"]
        assert "templateVariables" not in payload

    @patch("siren.clients.base.requests.request")
    def test_get_replies_empty_list(self, mock_request):
        """Test get_replies when no replies exist."""
        # Mock successful API response with empty list
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [], "error": None}
        mock_request.return_value = mock_response

        # Call the method
        result = self.client.get_replies("test_msg_no_replies")

        # Verify result
        assert result == []
        assert len(result) == 0

    @patch("siren.clients.base.requests.request")
    def test_network_error_handling(self, mock_request):
        """Test handling of network errors."""
        # Mock network error
        mock_request.side_effect = Exception("Connection timeout")

        # Should raise SirenSDKError
        with pytest.raises(SirenSDKError) as exc_info:
            self.client.send(
                template_name="test",
                channel="SLACK",
                recipient_value="U123",
            )

        assert "Connection timeout" in str(exc_info.value)

    @patch("siren.clients.base.requests.request")
    def test_send_awesome_template_success(self, mock_request):
        """Test successful awesome template sending."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"notificationId": "awesome_msg_123"},
            "error": None,
        }
        mock_request.return_value = mock_response

        # Call the method
        result = self.client.send_awesome_template(
            recipient_value="U123ABC",
            channel="SLACK",
            template_identifier="awesome-templates/customer-support/escalation_required/official/casual.yaml",
            template_variables={
                "ticket_id": "TICKET-123",
                "customer_name": "John Doe",
                "issue_summary": "Payment failed",
                "ticket_url": "https://support.example.com/tickets/TICKET-123",
                "sender_name": "Support Team"
            },
            provider_name="slack-test-provider",
            provider_code=ProviderCode.SLACK,
        )

        # Verify result
        assert result == "awesome_msg_123"

        # Verify request was made correctly
        mock_request.assert_called_once()
        call_args = mock_request.call_args

        # Check URL and method
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["url"] == f"{BASE_URL}/api/v1/public/send-awesome-messages"

        # Check payload structure
        payload = call_args[1]["json"]
        assert payload["channel"] == "SLACK"
        assert payload["templateIdentifier"] == "awesome-templates/customer-support/escalation_required/official/casual.yaml"
        assert payload["recipient"]["slack"] == "U123ABC"
        assert payload["templateVariables"]["ticket_id"] == "TICKET-123"
        assert payload["templateVariables"]["customer_name"] == "John Doe"
        assert payload["providerIntegration"]["name"] == "slack-test-provider"
        assert payload["providerIntegration"]["code"] == "SLACK"

    @patch("siren.clients.base.requests.request")
    def test_send_awesome_template_without_provider(self, mock_request):
        """Test awesome template sending without provider information."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"notificationId": "awesome_msg_456"},
            "error": None,
        }
        mock_request.return_value = mock_response

        # Call the method without provider info
        result = self.client.send_awesome_template(
            recipient_value="test@example.com",
            channel="EMAIL",
            template_identifier="awesome-templates/welcome/email/official.yaml",
            template_variables={"user_name": "Alice"},
        )

        # Verify result
        assert result == "awesome_msg_456"

        # Verify payload doesn't include providerIntegration
        payload = mock_request.call_args[1]["json"]
        assert "providerIntegration" not in payload

    @patch("siren.clients.base.requests.request")
    def test_send_awesome_template_without_template_variables(self, mock_request):
        """Test awesome template sending without template variables."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"notificationId": "awesome_msg_789"},
            "error": None,
        }
        mock_request.return_value = mock_response

        # Call the method without template variables
        result = self.client.send_awesome_template(
            recipient_value="U456DEF",
            channel="SLACK",
            template_identifier="awesome-templates/simple/notification.yaml",
            provider_name="slack-provider",
            provider_code=ProviderCode.SLACK,
        )

        # Verify result
        assert result == "awesome_msg_789"

        # Verify payload doesn't include templateVariables
        payload = mock_request.call_args[1]["json"]
        assert "templateVariables" not in payload

    @patch("siren.clients.base.requests.request")
    def test_send_awesome_template_api_error(self, mock_request):
        """Test awesome template API error handling."""
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "data": None,
            "error": {
                "errorCode": "VALIDATION_EXCEPTION",
                "message": "Validation failed: Should provide either provider Id or provider name and code."
            },
        }
        mock_request.return_value = mock_response

        # Should raise SirenAPIError
        with pytest.raises(SirenAPIError) as exc_info:
            self.client.send_awesome_template(
                recipient_value="U123",
                channel="SLACK",
                template_identifier="awesome-templates/test.yaml",
                template_variables={"test": "value"},
            )

        assert exc_info.value.error_code == "VALIDATION_EXCEPTION"
        assert "Validation failed" in exc_info.value.api_message

    def test_send_awesome_template_invalid_channel(self):
        """Test awesome template with invalid channel."""
        # Should raise ValueError for unsupported channel
        with pytest.raises(ValueError) as exc_info:
            self.client.send_awesome_template(
                recipient_value="test@example.com",
                channel="INVALID_CHANNEL",
                template_identifier="awesome-templates/test.yaml",
            )

        assert "Unsupported channel" in str(exc_info.value)

    def test_send_awesome_template_provider_validation(self):
        """Test awesome template provider validation."""
        # Should raise ValueError when only one provider field is provided
        with pytest.raises(ValueError) as exc_info:
            self.client.send_awesome_template(
                recipient_value="U123",
                channel="SLACK",
                template_identifier="awesome-templates/test.yaml",
                provider_name="test-provider",
                # Missing provider_code
            )

        assert "Both provider_name and provider_code must be provided together" in str(exc_info.value)

    @patch("siren.clients.base.requests.request")
    def test_send_awesome_template_different_channels(self, mock_request):
        """Test awesome template with different channels."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"notificationId": "awesome_msg_channel_test"},
            "error": None,
        }
        mock_request.return_value = mock_response

        # Test EMAIL channel
        result = self.client.send_awesome_template(
            recipient_value="test@example.com",
            channel="EMAIL",
            template_identifier="awesome-templates/email/welcome.yaml",
            template_variables={"user_name": "Bob"},
            provider_name="email-provider",
            provider_code=ProviderCode.EMAIL_SENDGRID,
        )

        assert result == "awesome_msg_channel_test"

        # Verify recipient structure for EMAIL
        payload = mock_request.call_args[1]["json"]
        assert payload["recipient"]["email"] == "test@example.com"
        assert "slack" not in payload["recipient"]

    @patch("siren.clients.base.requests.request")
    def test_send_awesome_template_network_error(self, mock_request):
        """Test awesome template network error handling."""
        # Mock network error
        mock_request.side_effect = Exception("Network connection failed")

        # Should raise SirenSDKError
        with pytest.raises(SirenSDKError) as exc_info:
            self.client.send_awesome_template(
                recipient_value="U123",
                channel="SLACK",
                template_identifier="awesome-templates/test.yaml",
                template_variables={"test": "value"},
                provider_name="test-provider",
                provider_code=ProviderCode.SLACK,
            )

        assert "Network connection failed" in str(exc_info.value)
