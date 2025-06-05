"""Tests for the Siren API client."""

import os

# For local development, you might need to adjust sys.path:
import sys

import pytest
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from siren.client import SirenClient


@pytest.fixture
def client():
    """Provides a SirenClient instance for testing."""
    return SirenClient(api_key="test_api_key")


def test_siren_client_initialization(client):
    """Test that the SirenClient initializes correctly."""
    assert client.api_key == "test_api_key", "API key should be set on initialization"


def test_get_templates_success(client, requests_mock):
    """Test successful retrieval of templates."""
    mock_response_data = {
        "data": {
            "content": [
                {"id": "tpl_1", "name": "Test Template 1"},
                {"id": "tpl_2", "name": "Test Template 2"},
            ],
            "totalElements": 2,
        }
    }
    requests_mock.get(
        f"{client.BASE_API_URL}/template",
        json=mock_response_data,
        status_code=200,
    )

    response = client.get_templates(page=0, size=10)
    assert response == mock_response_data
    assert len(response["data"]["content"]) == 2
    assert response["data"]["content"][0]["name"] == "Test Template 1"


def test_get_templates_http_error(client, requests_mock):
    """Test handling of HTTP error when getting templates."""
    error_response_data = {
        "error": {"errorCode": "UNAUTHORISED", "message": "Invalid API Key"}
    }
    requests_mock.get(
        f"{client.BASE_API_URL}/template",
        json=error_response_data,
        status_code=401,
    )

    response = client.get_templates()
    assert response == error_response_data


def test_get_templates_network_error(client, requests_mock):
    """Test handling of a network error when getting templates."""
    requests_mock.get(
        f"{client.BASE_API_URL}/template", exc=requests.exceptions.ConnectTimeout
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.get_templates()
