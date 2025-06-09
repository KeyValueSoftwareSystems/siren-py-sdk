# tests/test_users.py
"""Unit tests for the user management features of the Siren SDK."""

from typing import Optional
from unittest.mock import MagicMock, patch

import pytest
import requests

from siren.client import SirenClient
from siren.users import UsersManager

# Mock API responses
MOCK_API_KEY = "test_api_key"
MOCK_BASE_URL = "https://api.siren.com"
MOCK_USER_ID = "user_123"


@pytest.fixture
def users_manager():
    """Fixture to create a UsersManager instance."""
    return UsersManager(api_key=MOCK_API_KEY, base_url=MOCK_BASE_URL)


@pytest.fixture
def siren_client():
    """Fixture to create a SirenClient instance."""
    return SirenClient(api_key=MOCK_API_KEY)


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


class TestUsersManager:
    """Tests for the UsersManager class."""

    @patch("siren.users.requests.post")
    def test_add_user_success(self, mock_post, users_manager: UsersManager):
        """Test successful user creation/update."""
        expected_response = {
            "status": "success",
            "data": {"id": MOCK_USER_ID, "uniqueId": MOCK_USER_ID},
        }
        mock_post.return_value = mock_response(200, expected_response)

        payload = {
            "unique_id": MOCK_USER_ID,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "active_channels": ["EMAIL"],
            "attributes": {"custom_field": "value1"},
        }
        response = users_manager.add_user(**payload)

        expected_headers = {
            "Authorization": f"Bearer {MOCK_API_KEY}",
            "Content-Type": "application/json",
        }
        mock_post.assert_called_once_with(
            f"{MOCK_BASE_URL}/api/v1/public/users",
            json={
                "uniqueId": MOCK_USER_ID,
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "activeChannels": ["EMAIL"],
                "attributes": {"custom_field": "value1"},
            },
            headers=expected_headers,
            timeout=10,
        )
        assert response == expected_response

    @patch("siren.users.requests.post")
    def test_add_user_minimal_payload_success(
        self, mock_post, users_manager: UsersManager
    ):
        """Test successful user creation/update with minimal payload."""
        expected_response = {
            "status": "success",
            "data": {"id": MOCK_USER_ID, "uniqueId": MOCK_USER_ID},
        }
        mock_post.return_value = mock_response(200, expected_response)

        response = users_manager.add_user(unique_id=MOCK_USER_ID)

        expected_headers = {
            "Authorization": f"Bearer {MOCK_API_KEY}",
            "Content-Type": "application/json",
        }
        mock_post.assert_called_once_with(
            f"{MOCK_BASE_URL}/api/v1/public/users",
            json={"uniqueId": MOCK_USER_ID},
            headers=expected_headers,
            timeout=10,
        )
        assert response == expected_response

    @patch("siren.users.requests.post")
    def test_add_user_api_error_returns_json(
        self, mock_post, users_manager: UsersManager
    ):
        """Test API error (e.g., 400, 422) that returns a JSON body."""
        error_response_json = {
            "error": "Validation failed",
            "details": {"uniqueId": "is required"},
        }

        # Create a mock response object that will be associated with the HTTPError
        err_response_obj = mock_response(422, error_response_json)
        http_error = requests.exceptions.HTTPError(response=err_response_obj)
        err_response_obj.raise_for_status.side_effect = (
            http_error  # Configure raise_for_status to raise the error
        )

        mock_post.return_value = (
            err_response_obj  # The session.post call returns this response object
        )

        response = users_manager.add_user(unique_id=MOCK_USER_ID)

        assert response == error_response_json

    @patch("siren.users.requests.post")
    def test_add_user_http_error_no_json(self, mock_post, users_manager: UsersManager):
        """Test API error (e.g., 500) that does not return a JSON body."""
        # Mock response that raises HTTPError but .json() call on response raises JSONDecodeError
        err_response_obj = mock_response(500, text_data="Internal Server Error")
        http_error = requests.exceptions.HTTPError(response=err_response_obj)
        err_response_obj.raise_for_status.side_effect = http_error
        err_response_obj.json.side_effect = requests.exceptions.JSONDecodeError(
            "Expecting value", "doc", 0
        )

        mock_post.return_value = err_response_obj

        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            users_manager.add_user(unique_id=MOCK_USER_ID)

        assert excinfo.value.response.status_code == 500
        assert excinfo.value.response.text == "Internal Server Error"

    @patch("siren.users.requests.post")
    def test_add_user_request_exception(self, mock_post, users_manager: UsersManager):
        """Test handling of requests.exceptions.RequestException."""
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")

        with pytest.raises(requests.exceptions.RequestException):
            users_manager.add_user(unique_id=MOCK_USER_ID)


class TestSirenClientUsers:
    """Tests for user management methods exposed on SirenClient."""

    @patch.object(UsersManager, "add_user")
    def test_client_add_user_delegates_to_manager(
        self, mock_manager_add_user, siren_client: SirenClient
    ):
        """Test that SirenClient.add_user correctly delegates to UsersManager.add_user."""
        payload = {
            "unique_id": "client_user_001",
            "first_name": "Client",
            "last_name": "User",
            "email": "client.user@example.com",
            "attributes": {"source": "client_test"},
        }
        expected_return_value = {"id": "client_user_001", "status": "delegated"}
        mock_manager_add_user.return_value = expected_return_value

        # This is the payload passed to the client method
        payload_to_client = payload.copy()

        # This is the expected payload for the manager method, including defaults
        expected_payload_for_manager = {
            "unique_id": "client_user_001",
            "first_name": "Client",
            "last_name": "User",
            "reference_id": None,
            "whatsapp": None,
            "active_channels": None,
            "active": None,
            "email": "client.user@example.com",
            "phone": None,
            "attributes": {"source": "client_test"},
        }

        response = siren_client.add_user(**payload_to_client)

        mock_manager_add_user.assert_called_once_with(**expected_payload_for_manager)
        assert response == expected_return_value
