# tests/test_users.py
"""Unit tests for the user management features of the Siren SDK."""

from typing import Optional
from unittest.mock import MagicMock, patch

import pytest
import requests

from siren.client import SirenClient
from siren.clients.users import UserClient
from siren.exceptions import SirenAPIError, SirenSDKError
from siren.models.user import User

# Test constants
MOCK_API_KEY = "test_api_key"
MOCK_BASE_URL = "https://api.siren.com"
MOCK_USER_ID = "user_123"


@pytest.fixture
def user_client():
    """Fixture to create a UserClient instance."""
    return UserClient(api_key=MOCK_API_KEY, base_url=MOCK_BASE_URL)


@pytest.fixture
def siren_client():
    """Fixture to create a SirenClient instance."""
    return SirenClient(api_key=MOCK_API_KEY, env="dev")


def mock_response(
    status_code: int,
    json_data: Optional[dict] = None,
    text_data: str = "",
    raise_for_status_exception=None,
):
    """Helper function to create a mock HTTP response."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data if json_data is not None else {}
    mock_resp.text = text_data
    if raise_for_status_exception:
        mock_resp.raise_for_status.side_effect = raise_for_status_exception
    return mock_resp


class TestUserClient:
    """Tests for the UserClient class."""

    @patch("siren.clients.base.requests.request")
    def test_add_user_success(self, mock_request, user_client: UserClient):
        """Test successful user creation/update returns a User model instance."""
        # Mock API response with all possible user fields
        mock_api_json_response = {
            "data": {
                "id": "user_api_generated_id_001",
                "uniqueId": MOCK_USER_ID,
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "activeChannels": ["EMAIL"],
                "attributes": {"custom_field": "value1"},
                "referenceId": None,
                "whatsapp": None,
                "active": True,
                "phone": None,
                "createdAt": "2023-01-01T12:00:00Z",
                "updatedAt": "2023-01-01T12:00:00Z",
                "avatarUrl": None,
            },
            "error": None,
        }
        mock_request.return_value = mock_response(200, json_data=mock_api_json_response)

        # Test payload with snake_case keys (SDK input)
        payload = {
            "unique_id": MOCK_USER_ID,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "active_channels": ["EMAIL"],
            "attributes": {"custom_field": "value1"},
        }
        response = user_client.add(**payload)

        # Expected API request with camelCase keys
        expected_headers = {
            "Authorization": f"Bearer {MOCK_API_KEY}",
            "Content-Type": "application/json",
        }
        expected_json_payload = {
            "uniqueId": MOCK_USER_ID,
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "activeChannels": ["EMAIL"],
            "attributes": {"custom_field": "value1"},
        }
        mock_request.assert_called_once_with(
            method="POST",
            url=f"{MOCK_BASE_URL}/api/v1/public/users",
            headers=expected_headers,
            json=expected_json_payload,
            params=None,
            timeout=10,
        )

        # Verify all User model fields
        assert isinstance(response, User)
        assert response.id == "user_api_generated_id_001"
        assert response.unique_id == MOCK_USER_ID
        assert response.first_name == "John"
        assert response.last_name == "Doe"
        assert response.email == "john.doe@example.com"
        assert response.active_channels == ["EMAIL"]
        assert response.attributes == {"custom_field": "value1"}
        assert response.created_at == "2023-01-01T12:00:00Z"
        assert response.updated_at == "2023-01-01T12:00:00Z"
        assert response.active is True
        assert response.reference_id is None
        assert response.whatsapp is None
        assert response.phone is None
        assert response.avatar_url is None

    @patch("siren.clients.base.requests.request")
    def test_add_user_api_error_returns_json(
        self, mock_request, user_client: UserClient
    ):
        """Test API error (400, 401, 404) with JSON body raises SirenAPIError."""
        # Mock API error response with validation details
        mock_api_error_payload = {
            "error": {
                "errorCode": "VALIDATION_ERROR",
                "message": "Validation failed on one or more fields.",
                "details": [
                    {
                        "field": "uniqueId",
                        "message": "This field is required and cannot be empty.",
                    },
                    {"field": "email", "message": "Not a valid email address."},
                ],
            }
        }
        status_code = 400

        err_response_obj = mock_response(status_code, json_data=mock_api_error_payload)
        mock_request.return_value = err_response_obj

        with pytest.raises(SirenAPIError) as excinfo:
            user_client.add(unique_id=MOCK_USER_ID)

        # Verify error details
        assert excinfo.value.status_code == status_code
        assert excinfo.value.api_message == mock_api_error_payload["error"]["message"]
        assert excinfo.value.error_code == mock_api_error_payload["error"]["errorCode"]
        assert (
            excinfo.value.error_detail.details
            == mock_api_error_payload["error"]["details"]
        )

    @patch("siren.clients.base.requests.request")
    def test_add_user_http_error_no_json(self, mock_request, user_client: UserClient):
        """Test API error (500) without JSON body raises SirenSDKError."""
        # Mock non-JSON error response
        status_code = 500
        error_text = "Internal Server Error - Not JSON"
        err_response_obj = mock_response(status_code, text_data=error_text)
        err_response_obj.json.side_effect = requests.exceptions.JSONDecodeError(
            "Expecting value", "doc", 0
        )

        mock_request.return_value = err_response_obj

        with pytest.raises(SirenSDKError) as excinfo:
            user_client.add(unique_id=MOCK_USER_ID)

        assert isinstance(
            excinfo.value.original_exception, requests.exceptions.JSONDecodeError
        )
        assert "API response was not valid JSON" in excinfo.value.message
        assert error_text in excinfo.value.message

    @patch("siren.clients.base.requests.request")
    def test_add_user_request_exception(self, mock_request, user_client: UserClient):
        """Test handling of requests.exceptions.RequestException (e.g., network error) raises SirenSDKError."""
        # Mock network error
        original_exception = requests.exceptions.ConnectionError(
            "Simulated connection failed"
        )
        mock_request.side_effect = original_exception

        with pytest.raises(SirenSDKError) as excinfo:
            user_client.add(unique_id=MOCK_USER_ID)

        assert excinfo.value.original_exception == original_exception
        assert isinstance(
            excinfo.value.original_exception, requests.exceptions.ConnectionError
        )
        assert "Network or connection error" in excinfo.value.message

    @patch("siren.clients.base.requests.request")
    def test_update_user_success(self, mock_request, user_client: UserClient):
        """Test successful user update returns a User model instance."""
        # Mock API response
        mock_api_json_response = {
            "data": {
                "id": "user_api_generated_id_001",
                "uniqueId": MOCK_USER_ID,
                "firstName": "Jane",
                "lastName": "Smith",
                "email": "jane.smith@example.com",
                "activeChannels": ["SLACK"],
                "attributes": {"updated_field": "value2"},
                "referenceId": "020",
                "whatsapp": "+919632323154",
                "active": True,
                "phone": None,
                "createdAt": "2023-01-01T12:00:00Z",
                "updatedAt": "2023-01-02T12:00:00Z",
                "avatarUrl": None,
            },
            "error": None,
        }
        mock_request.return_value = mock_response(200, json_data=mock_api_json_response)

        # Test payload with snake_case keys (SDK input)
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "active_channels": ["SLACK"],
            "attributes": {"updated_field": "value2"},
            "reference_id": "020",
            "whatsapp": "+919632323154",
        }
        response = user_client.update(MOCK_USER_ID, **payload)

        # Expected API request with camelCase keys
        expected_headers = {
            "Authorization": f"Bearer {MOCK_API_KEY}",
            "Content-Type": "application/json",
        }
        expected_json_payload = {
            "uniqueId": MOCK_USER_ID,
            "firstName": "Jane",
            "lastName": "Smith",
            "email": "jane.smith@example.com",
            "activeChannels": ["SLACK"],
            "attributes": {"updated_field": "value2"},
            "referenceId": "020",
            "whatsapp": "+919632323154",
        }
        mock_request.assert_called_once_with(
            method="PUT",
            url=f"{MOCK_BASE_URL}/api/v1/public/users/{MOCK_USER_ID}",
            headers=expected_headers,
            json=expected_json_payload,
            params=None,
            timeout=10,
        )

        # Verify User model fields
        assert isinstance(response, User)
        assert response.id == "user_api_generated_id_001"
        assert response.unique_id == MOCK_USER_ID
        assert response.first_name == "Jane"
        assert response.last_name == "Smith"
        assert response.email == "jane.smith@example.com"
        assert response.active_channels == ["SLACK"]
        assert response.reference_id == "020"
        assert response.whatsapp == "+919632323154"
        assert response.updated_at == "2023-01-02T12:00:00Z"

    @patch("siren.clients.base.requests.request")
    def test_update_user_api_error_returns_json(
        self, mock_request, user_client: UserClient
    ):
        """Test API error (400, 401, 404) with JSON body raises SirenAPIError."""
        # Mock API error response
        mock_api_error_payload = {
            "error": {
                "errorCode": "USER_NOT_FOUND",
                "message": "User with the specified unique ID does not exist.",
            }
        }
        status_code = 404

        err_response_obj = mock_response(status_code, json_data=mock_api_error_payload)
        mock_request.return_value = err_response_obj

        with pytest.raises(SirenAPIError) as excinfo:
            user_client.update(MOCK_USER_ID, first_name="Jane")

        # Verify error details
        assert excinfo.value.status_code == status_code
        assert excinfo.value.api_message == mock_api_error_payload["error"]["message"]
        assert excinfo.value.error_code == mock_api_error_payload["error"]["errorCode"]

    @patch("siren.clients.base.requests.request")
    def test_update_user_validation_error(self, mock_request, user_client: UserClient):
        """Test invalid parameters raise SirenSDKError."""
        with pytest.raises(SirenSDKError) as excinfo:
            user_client.update(MOCK_USER_ID, email="invalid-email")

        assert "Invalid parameters" in excinfo.value.message
        mock_request.assert_not_called()

    @patch("siren.clients.base.requests.request")
    def test_update_user_request_exception(self, mock_request, user_client: UserClient):
        """Test handling of requests.exceptions.RequestException raises SirenSDKError."""
        # Mock network error
        original_exception = requests.exceptions.ConnectionError(
            "Simulated connection failed"
        )
        mock_request.side_effect = original_exception

        with pytest.raises(SirenSDKError) as excinfo:
            user_client.update(MOCK_USER_ID, first_name="Jane")

        assert excinfo.value.original_exception == original_exception
        assert "Network or connection error" in excinfo.value.message

    @patch("siren.clients.base.requests.request")
    def test_delete_user_success(self, mock_request, user_client: UserClient):
        """Test successful user deletion returns True."""
        # Mock API response for 204 No Content
        mock_request.return_value = mock_response(204)

        response = user_client.delete(MOCK_USER_ID)

        # Expected API request
        expected_headers = {
            "Authorization": f"Bearer {MOCK_API_KEY}",
        }
        mock_request.assert_called_once_with(
            method="DELETE",
            url=f"{MOCK_BASE_URL}/api/v1/public/users/{MOCK_USER_ID}",
            headers=expected_headers,
            json=None,
            params=None,
            timeout=10,
        )

        # Verify response
        assert response is True

    @patch("siren.clients.base.requests.request")
    def test_delete_user_not_found(self, mock_request, user_client: UserClient):
        """Test API error (404) raises SirenAPIError."""
        # Mock API error response
        mock_api_error_payload = {
            "error": {
                "errorCode": "USER_NOT_FOUND",
                "message": "User with the specified unique ID does not exist.",
            }
        }
        status_code = 404

        err_response_obj = mock_response(status_code, json_data=mock_api_error_payload)
        mock_request.return_value = err_response_obj

        with pytest.raises(SirenAPIError) as excinfo:
            user_client.delete(MOCK_USER_ID)

        # Verify error details
        assert excinfo.value.status_code == status_code
        assert excinfo.value.api_message == mock_api_error_payload["error"]["message"]
        assert excinfo.value.error_code == mock_api_error_payload["error"]["errorCode"]

    @patch("siren.clients.base.requests.request")
    def test_delete_user_request_exception(self, mock_request, user_client: UserClient):
        """Test handling of requests.exceptions.RequestException raises SirenSDKError."""
        # Mock network error
        original_exception = requests.exceptions.ConnectionError(
            "Simulated connection failed"
        )
        mock_request.side_effect = original_exception

        with pytest.raises(SirenSDKError) as excinfo:
            user_client.delete(MOCK_USER_ID)

        assert excinfo.value.original_exception == original_exception
        assert "Network or connection error" in excinfo.value.message


class TestSirenClientUsers:
    """Tests for user management methods exposed on SirenClient."""

    @patch("siren.client.UserClient.add")
    def test_client_add_user_delegates_to_client(
        self, mock_client_add_user, siren_client: SirenClient
    ):
        """Test that SirenClient.user.add correctly delegates to UserClient.add."""
        # Test data
        payload = {
            "unique_id": "client_user_001",
            "first_name": "Client",
            "last_name": "User",
            "email": "client.user@example.com",
            "attributes": {"source": "client_test"},
        }

        # Mock response
        mock_user_instance = User(
            id="user_api_id_123",
            uniqueId="client_user_001",
            createdAt="2023-01-01T10:00:00Z",
            updatedAt="2023-01-01T10:00:00Z",
            firstName="Client",
            lastName="User",
            email="client.user@example.com",
            attributes={"source": "client_test"},
            referenceId=None,
            whatsapp=None,
            activeChannels=None,
            active=None,
            phone=None,
            avatarUrl=None,
            pushToken=None,
            inApp=None,
            slack=None,
            discord=None,
            teams=None,
            line=None,
            customData=None,
        )
        mock_client_add_user.return_value = mock_user_instance

        response = siren_client.user.add(**payload)

        # Verify delegation
        mock_client_add_user.assert_called_once()
        call_args = mock_client_add_user.call_args[1]
        assert call_args["unique_id"] == payload["unique_id"]
        assert call_args["first_name"] == payload["first_name"]
        assert call_args["last_name"] == payload["last_name"]
        assert call_args["email"] == payload["email"]
        assert call_args["attributes"] == payload["attributes"]
        assert response == mock_user_instance

    @patch("siren.client.UserClient.update")
    def test_client_update_user_delegates_to_client(
        self, mock_client_update_user, siren_client: SirenClient
    ):
        """Test that SirenClient.user.update correctly delegates to UserClient.update."""
        # Test data
        unique_id = "client_user_001"
        payload = {
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated.user@example.com",
            "attributes": {"source": "update_test"},
            "push_token": "push_token_123",
            "in_app": True,
            "slack": "slack_user_id_123",
            "discord": "discord_user_id_123",
            "teams": "teams_user_id_123",
            "line": "line_user_id_123",
            "custom_data": {"custom_field": "custom_value"},
        }

        # Mock response
        mock_user_instance = User(
            id="user_api_id_123",
            uniqueId=unique_id,
            createdAt="2023-01-01T10:00:00Z",
            updatedAt="2023-01-02T15:00:00Z",
            firstName="Updated",
            lastName="User",
            email="updated.user@example.com",
            attributes={"source": "update_test"},
            referenceId=None,
            whatsapp=None,
            activeChannels=None,
            active=None,
            phone=None,
            avatarUrl=None,
            pushToken="push_token_123",
            inApp=True,
            slack="slack_user_id_123",
            discord="discord_user_id_123",
            teams="teams_user_id_123",
            line="line_user_id_123",
            customData={"custom_field": "custom_value"},
        )
        mock_client_update_user.return_value = mock_user_instance

        response = siren_client.user.update(unique_id, **payload)

        # Verify delegation
        mock_client_update_user.assert_called_once()
        call_args = mock_client_update_user.call_args
        # Check positional args
        args = call_args[0]
        call_kwargs = call_args[1]
        assert args[0] == unique_id  # unique_id is first positional argument
        assert call_kwargs["first_name"] == payload["first_name"]
        assert call_kwargs["last_name"] == payload["last_name"]
        assert call_kwargs["email"] == payload["email"]
        assert call_kwargs["attributes"] == payload["attributes"]
        assert response == mock_user_instance

    @patch("siren.client.UserClient.delete")
    def test_client_delete_user_delegates_to_client(
        self, mock_client_delete_user, siren_client: SirenClient
    ):
        """Test that SirenClient.user.delete correctly delegates to UserClient.delete."""
        # Test data
        unique_id = "client_user_001"

        # Mock response
        mock_client_delete_user.return_value = True

        response = siren_client.user.delete(unique_id)

        # Verify delegation
        mock_client_delete_user.assert_called_once_with(unique_id)
        assert response is True
