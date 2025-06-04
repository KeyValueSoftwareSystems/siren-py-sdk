# tests/test_client.py

import pytest
# from siren.client import SirenClient # Adjust import based on package structure

# For local development, you might need to adjust sys.path:
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from siren.client import SirenClient


@pytest.fixture
def client():
    """Provides a SirenClient instance for testing."""
    return SirenClient(api_key="test_api_key")


def test_siren_client_initialization(client):
    """Test that the SirenClient initializes correctly."""
    assert client.api_key == "test_api_key", "API key should be set on initialization"
    print("SirenClient initialized successfully for testing.")

# We will add more tests here as we implement features.
# For example:
# def test_send_message_success(client, mocker):
#     mocker.patch('requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {"id": "msg_123", "status": "sent"}))
#     response = client.send_message({"to": "test@example.com", "message": "Hello"})
#     assert response["id"] == "msg_123"

