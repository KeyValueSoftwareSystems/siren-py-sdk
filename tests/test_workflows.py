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


# --- Tests for trigger_bulk_workflow --- #

BULK_WORKFLOW_NAME = "test_bulk_otp_workflow"


def test_trigger_bulk_workflow_success_with_all_params(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk_workflow with all parameters successfully."""
    request_notify_list = [
        {"notificationType": "email", "recipient": "bulk1@example.com"},
        {"notificationType": "sms", "recipient": "+12345678901"},
    ]
    request_data = {"common_field": "common_value"}
    expected_response = {
        "data": {
            "requestId": "d4e5f6a7-b8c9-d0e1-f2a3-b4c5d6e7f8a9",
            "workflowExecutionIds": [
                "e5f6a7b8-c9d0-e1f2-a3b4-c5d6e7f8a9b0",
                "f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1",
            ],
        },
        "error": None,
        "errors": None,
        "meta": None,
    }
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"

    requests_mock.post(mock_url, json=expected_response, status_code=200)

    response = client.trigger_bulk_workflow(
        workflow_name=BULK_WORKFLOW_NAME,
        notify=request_notify_list,
        data=request_data,
    )

    assert response == expected_response
    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].method == "POST"
    assert history[0].url == mock_url
    assert history[0].json() == {
        "workflowName": BULK_WORKFLOW_NAME,
        "notify": request_notify_list,
        "data": request_data,
    }
    assert history[0].headers["Authorization"] == f"Bearer {API_KEY}"


def test_trigger_bulk_workflow_success_minimal_params(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk_workflow with minimal parameters (workflow_name, notify) successfully."""
    request_notify_list = [
        {"notificationType": "email", "recipient": "minimal_bulk@example.com"}
    ]
    expected_response = {
        "data": {
            "requestId": "uuid_bulk_req",
            "workflowExecutionIds": ["uuid_bulk_exec1"],
        },
        "error": None,
        "errors": None,
        "meta": None,
    }
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    requests_mock.post(mock_url, json=expected_response, status_code=200)

    response = client.trigger_bulk_workflow(
        workflow_name=BULK_WORKFLOW_NAME, notify=request_notify_list
    )

    assert response == expected_response
    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].json() == {
        "workflowName": BULK_WORKFLOW_NAME,
        "notify": request_notify_list,
    }


def test_trigger_bulk_workflow_http_400_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk_workflow handles HTTP 400 Bad Request error."""
    error_response = {
        "data": None,
        "error": {"errorCode": "BAD_REQUEST", "message": "Invalid notify payload"},
        "errors": [{"errorCode": "BAD_REQUEST", "message": "Invalid notify payload"}],
        "meta": None,
    }
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    requests_mock.post(mock_url, json=error_response, status_code=400)

    response = client.trigger_bulk_workflow(
        workflow_name=BULK_WORKFLOW_NAME,
        notify=[{}],  # Example invalid notify
    )
    assert response == error_response


def test_trigger_bulk_workflow_http_401_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk_workflow handles HTTP 401 Unauthorized error."""
    error_response = {"detail": "Authentication credentials were not provided."}
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    requests_mock.post(mock_url, json=error_response, status_code=401)

    response = client.trigger_bulk_workflow(
        workflow_name=BULK_WORKFLOW_NAME, notify=[{"recipient": "test@example.com"}]
    )
    assert response == error_response


def test_trigger_bulk_workflow_http_404_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk_workflow handles HTTP 404 Not Found error for the workflow."""
    error_response = {"detail": "Workflow not found."}
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    requests_mock.post(mock_url, json=error_response, status_code=404)

    response = client.trigger_bulk_workflow(
        workflow_name="non_existent_bulk_workflow",
        notify=[{"recipient": "test@example.com"}],
    )
    assert response == error_response


def test_trigger_bulk_workflow_network_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk_workflow handles a network error."""
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    requests_mock.post(
        mock_url, exc=requests.exceptions.ConnectionError("Bulk connection failed")
    )

    with pytest.raises(requests.exceptions.RequestException):
        client.trigger_bulk_workflow(
            workflow_name=BULK_WORKFLOW_NAME,
            notify=[{"recipient": "test@example.com"}],
        )


def test_trigger_bulk_workflow_http_error_non_json_response(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk_workflow handles HTTP error with non-JSON response."""
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    non_json_error_text = "Bulk Service Unavailable"
    requests_mock.post(mock_url, text=non_json_error_text, status_code=503)

    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        client.trigger_bulk_workflow(
            workflow_name=BULK_WORKFLOW_NAME,
            notify=[{"recipient": "test@example.com"}],
        )

    assert non_json_error_text in str(excinfo.value)
    assert excinfo.value.response is not None
    assert excinfo.value.response.status_code == 503
