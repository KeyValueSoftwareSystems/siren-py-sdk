# tests/test_workflows.py
"""Tests for Siren SDK Workflow operations."""

import pytest
import requests
from requests_mock import Mocker as RequestsMocker

from siren import SirenClient

# Constants for testing
API_KEY = "test_api_key_workflow"  # Use a distinct key for clarity if needed
WORKFLOW_NAME = "test_otp_workflow"
# Access BASE_API_URL as a class attribute of SirenClient
MOCK_V2_BASE = f"{SirenClient.BASE_API_URL}/api/v2"  # Construct the v2 base for mocking


@pytest.fixture
def client() -> SirenClient:
    """Provides a SirenClient instance for testing."""
    return SirenClient(api_key=API_KEY)


def test_trigger_workflow_success_with_all_params(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_workflow with all parameters successfully."""
    request_data = {"subject": "otp verification"}
    request_notify = {"notificationType": "email", "recipient": "example@example.com"}
    expected_response = {
        "data": {
            "requestId": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "workflowExecutionId": "b2c3d4e5-f6a7-8901-2345-67890abcdef0",
        },
        "error": None,
        "errors": None,
        "meta": None,
    }
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"

    requests_mock.post(mock_url, json=expected_response, status_code=200)

    response = client.trigger_workflow(
        workflow_name=WORKFLOW_NAME, data=request_data, notify=request_notify
    )

    assert response == expected_response
    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].method == "POST"
    assert history[0].url == mock_url
    assert history[0].json() == {
        "workflowName": WORKFLOW_NAME,
        "data": request_data,
        "notify": request_notify,
    }
    assert history[0].headers["Authorization"] == f"Bearer {API_KEY}"


def test_trigger_workflow_success_minimal_params(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_workflow with only workflow_name successfully."""
    expected_response = {
        "data": {"requestId": "uuid1", "workflowExecutionId": "uuid2"},
        "error": None,
        "errors": None,
        "meta": None,
    }
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(mock_url, json=expected_response, status_code=200)

    response = client.trigger_workflow(workflow_name=WORKFLOW_NAME)

    assert response == expected_response
    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].json() == {
        "workflowName": WORKFLOW_NAME
    }  # data and notify are optional


# Error handling tests (similar to test_templates.py)


def test_trigger_workflow_http_400_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_workflow handles HTTP 400 Bad Request error."""
    error_response = {
        "data": None,
        "error": {"errorCode": "BAD_REQUEST", "message": "Bad request"},
        "errors": [{"errorCode": "BAD_REQUEST", "message": "Bad request"}],
        "meta": None,
    }
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(mock_url, json=error_response, status_code=400)

    response = client.trigger_workflow(workflow_name=WORKFLOW_NAME)
    assert response == error_response


def test_trigger_workflow_http_401_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_workflow handles HTTP 401 Unauthorized error."""
    error_response = {"detail": "Authentication credentials were not provided."}
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(mock_url, json=error_response, status_code=401)

    response = client.trigger_workflow(workflow_name=WORKFLOW_NAME)
    assert response == error_response


def test_trigger_workflow_http_404_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_workflow handles HTTP 404 Not Found error."""
    error_response = {"detail": "Not found."}
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(mock_url, json=error_response, status_code=404)

    response = client.trigger_workflow(workflow_name="non_existent_workflow")
    assert response == error_response


def test_trigger_workflow_network_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_workflow handles a network error."""
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(
        mock_url, exc=requests.exceptions.ConnectionError("Connection failed")
    )

    with pytest.raises(
        requests.exceptions.RequestException
    ):  # More general than ConnectionError
        client.trigger_workflow(workflow_name=WORKFLOW_NAME)


def test_trigger_workflow_http_error_non_json_response(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_workflow handles HTTP error with non-JSON response."""
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    non_json_error_text = "Service Unavailable"
    requests_mock.post(mock_url, text=non_json_error_text, status_code=503)

    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        client.trigger_workflow(workflow_name=WORKFLOW_NAME)

    # Check if the original error text is part of the raised exception's message
    assert non_json_error_text in str(excinfo.value)
    assert excinfo.value.response is not None
    assert excinfo.value.response.status_code == 503
