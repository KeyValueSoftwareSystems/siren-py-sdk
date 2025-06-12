# tests/test_workflows.py
"""Test cases for workflows client."""

import pytest
import requests
from requests_mock import Mocker as RequestsMocker

from siren.client import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError
from siren.models.workflows import (
    BulkWorkflowExecutionData,
    ScheduleData,
    WorkflowExecutionData,
)

API_KEY = "test_api_key_workflows"
MOCK_V2_BASE = "https://api.dev.trysiren.io/api/v2"
MOCK_V1_PUBLIC_BASE = "https://api.dev.trysiren.io/api/v1/public"
WORKFLOW_NAME = "test_otp_workflow"


@pytest.fixture
def client() -> SirenClient:
    """Create a SirenClient instance for testing."""
    return SirenClient(api_key=API_KEY, env="dev")


def test_trigger_workflow_success_with_all_params(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger with all parameters successfully."""
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

    response = client.workflow.trigger(
        workflow_name=WORKFLOW_NAME, data=request_data, notify=request_notify
    )

    # Expect parsed model object
    assert isinstance(response, WorkflowExecutionData)
    assert response.request_id == "a1b2c3d4-e5f6-7890-1234-567890abcdef"
    assert response.workflow_execution_id == "b2c3d4e5-f6a7-8901-2345-67890abcdef0"

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
    """Test trigger with only workflow_name successfully."""
    expected_response = {
        "data": {"requestId": "uuid1", "workflowExecutionId": "uuid2"},
        "error": None,
        "errors": None,
        "meta": None,
    }
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(mock_url, json=expected_response, status_code=200)

    response = client.workflow.trigger(workflow_name=WORKFLOW_NAME)

    # Expect parsed model object
    assert isinstance(response, WorkflowExecutionData)
    assert response.request_id == "uuid1"
    assert response.workflow_execution_id == "uuid2"

    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].json() == {
        "workflowName": WORKFLOW_NAME
    }  # data and notify are optional


def test_trigger_workflow_http_400_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger handles HTTP 400 Bad Request error."""
    error_response = {
        "data": None,
        "error": {"errorCode": "BAD_REQUEST", "message": "Bad request"},
        "errors": [{"errorCode": "BAD_REQUEST", "message": "Bad request"}],
        "meta": None,
    }
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(mock_url, json=error_response, status_code=400)

    with pytest.raises(SirenAPIError) as exc_info:
        client.workflow.trigger(workflow_name=WORKFLOW_NAME)

    assert exc_info.value.status_code == 400
    assert "BAD_REQUEST" in str(exc_info.value)


def test_trigger_workflow_http_401_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger handles HTTP 401 Unauthorized error."""
    error_response = {"detail": "Authentication credentials were not provided."}
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(mock_url, json=error_response, status_code=401)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.trigger(workflow_name=WORKFLOW_NAME)

    assert exc_info.value.status_code == 401


def test_trigger_workflow_http_404_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger handles HTTP 404 Not Found error."""
    error_response = {"detail": "Not found."}
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(mock_url, json=error_response, status_code=404)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.trigger(workflow_name="non_existent_workflow")

    assert exc_info.value.status_code == 404


def test_trigger_workflow_network_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger handles a network error."""
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    requests_mock.post(
        mock_url, exc=requests.exceptions.ConnectionError("Connection failed")
    )

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.trigger(workflow_name=WORKFLOW_NAME)

    assert "Network or connection error" in str(exc_info.value)


def test_trigger_workflow_http_error_non_json_response(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger handles HTTP error with non-JSON response."""
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger"
    non_json_error_text = "Service Unavailable"
    requests_mock.post(mock_url, text=non_json_error_text, status_code=503)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.trigger(workflow_name=WORKFLOW_NAME)

    assert "API response was not valid JSON" in str(exc_info.value)
    assert exc_info.value.status_code == 503


# --- Tests for trigger_bulk_workflow --- #

BULK_WORKFLOW_NAME = "test_bulk_otp_workflow"


def test_trigger_bulk_workflow_success_with_all_params(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk with all parameters successfully."""
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

    response = client.workflow.trigger_bulk(
        workflow_name=BULK_WORKFLOW_NAME,
        notify=request_notify_list,
        data=request_data,
    )

    # Expect parsed model object
    assert isinstance(response, BulkWorkflowExecutionData)
    assert response.request_id == "d4e5f6a7-b8c9-d0e1-f2a3-b4c5d6e7f8a9"
    assert response.workflow_execution_ids == [
        "e5f6a7b8-c9d0-e1f2-a3b4-c5d6e7f8a9b0",
        "f6a7b8c9-d0e1-f2a3-b4c5-d6e7f8a9b0c1",
    ]

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
    """Test trigger_bulk with minimal parameters (workflow_name, notify) successfully."""
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

    response = client.workflow.trigger_bulk(
        workflow_name=BULK_WORKFLOW_NAME, notify=request_notify_list
    )

    # Expect parsed model object
    assert isinstance(response, BulkWorkflowExecutionData)
    assert response.request_id == "uuid_bulk_req"
    assert response.workflow_execution_ids == ["uuid_bulk_exec1"]

    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].json() == {
        "workflowName": BULK_WORKFLOW_NAME,
        "notify": request_notify_list,
    }  # data is optional


def test_trigger_bulk_workflow_http_400_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk_workflow handles HTTP 400 Bad Request error."""
    error_response = {
        "data": None,
        "error": {
            "errorCode": "INVALID_NOTIFICATION_LIST",
            "message": "Invalid notification list",
        },
        "errors": [
            {
                "errorCode": "INVALID_NOTIFICATION_LIST",
                "message": "Invalid notification list",
            }
        ],
        "meta": None,
    }
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    requests_mock.post(mock_url, json=error_response, status_code=400)

    with pytest.raises(SirenAPIError) as exc_info:
        client.workflow.trigger_bulk(
            workflow_name=BULK_WORKFLOW_NAME, notify=[{"invalid": "data"}]
        )

    assert exc_info.value.status_code == 400
    assert "INVALID_NOTIFICATION_LIST" in str(exc_info.value)


def test_trigger_bulk_workflow_http_401_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk handles HTTP 401 Unauthorized error."""
    error_response = {"detail": "Authentication credentials were not provided."}
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    requests_mock.post(mock_url, json=error_response, status_code=401)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.trigger_bulk(
            workflow_name=BULK_WORKFLOW_NAME,
            notify=[{"notificationType": "email", "recipient": "test@test.com"}],
        )

    assert exc_info.value.status_code == 401


def test_trigger_bulk_workflow_http_404_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk handles HTTP 404 Not Found error."""
    error_response = {"detail": "Workflow not found."}
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    requests_mock.post(mock_url, json=error_response, status_code=404)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.trigger_bulk(
            workflow_name="non_existent_bulk_workflow",
            notify=[{"notificationType": "email", "recipient": "test@test.com"}],
        )

    assert exc_info.value.status_code == 404


def test_trigger_bulk_workflow_network_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk handles a network error."""
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    requests_mock.post(
        mock_url, exc=requests.exceptions.ConnectionError("Bulk connection failed")
    )

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.trigger_bulk(
            workflow_name=BULK_WORKFLOW_NAME,
            notify=[{"notificationType": "email", "recipient": "test@test.com"}],
        )

    assert "Network or connection error" in str(exc_info.value)


def test_trigger_bulk_workflow_http_error_non_json_response(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test trigger_bulk handles HTTP error with non-JSON response."""
    mock_url = f"{MOCK_V2_BASE}/workflows/trigger/bulk"
    non_json_error_text = "Service Unavailable"
    requests_mock.post(mock_url, text=non_json_error_text, status_code=503)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.trigger_bulk(
            workflow_name=BULK_WORKFLOW_NAME,
            notify=[{"notificationType": "email", "recipient": "test@test.com"}],
        )

    assert "API response was not valid JSON" in str(exc_info.value)
    assert exc_info.value.status_code == 503


# --- Tests for schedule_workflow --- #

SCHEDULE_NAME = "Test Schedule"
SCHEDULE_TIME = "10:00:00"
TIMEZONE_ID = "Asia/Kolkata"
START_DATE = "2024-01-15"
END_DATE_SPECIFIED = "2024-01-31"
WORKFLOW_TYPE_DAILY = "DAILY"
WORKFLOW_TYPE_ONCE = "ONCE"
SCHEDULE_WORKFLOW_ID = "wf_abc123def456"
INPUT_DATA = {"param1": "value1", "param2": 123}


def test_schedule_workflow_success_all_params(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test schedule with all parameters successfully."""
    expected_api_response = {
        "data": {
            "id": "sch_12345",
            "name": SCHEDULE_NAME,
            "type": WORKFLOW_TYPE_DAILY,
            "startDate": START_DATE,
            "endDate": END_DATE_SPECIFIED,
            "scheduleTime": SCHEDULE_TIME,
            "timezoneId": TIMEZONE_ID,
            "workflowId": SCHEDULE_WORKFLOW_ID,
            "inputData": INPUT_DATA,
            "status": "ACTIVE",
        },
        "error": None,
        "errors": None,
        "meta": None,
    }
    mock_url = f"{MOCK_V1_PUBLIC_BASE}/schedules"
    requests_mock.post(mock_url, json=expected_api_response, status_code=200)

    response = client.workflow.schedule(
        name=SCHEDULE_NAME,
        schedule_time=SCHEDULE_TIME,
        timezone_id=TIMEZONE_ID,
        start_date=START_DATE,
        workflow_type=WORKFLOW_TYPE_DAILY,
        workflow_id=SCHEDULE_WORKFLOW_ID,
        input_data=INPUT_DATA,
        end_date=END_DATE_SPECIFIED,
    )

    # Expect parsed model object
    assert isinstance(response, ScheduleData)
    assert response.id == "sch_12345"
    assert response.name == SCHEDULE_NAME
    assert response.schedule_type == WORKFLOW_TYPE_DAILY
    assert response.start_date == START_DATE
    assert response.end_date == END_DATE_SPECIFIED
    assert response.schedule_time == SCHEDULE_TIME
    assert response.timezone_id == TIMEZONE_ID
    assert response.workflow_id == SCHEDULE_WORKFLOW_ID
    assert response.input_data == INPUT_DATA
    assert response.status == "ACTIVE"

    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].method == "POST"
    assert history[0].url == mock_url
    assert history[0].json() == {
        "name": SCHEDULE_NAME,
        "scheduleTime": SCHEDULE_TIME,
        "timezoneId": TIMEZONE_ID,
        "startDate": START_DATE,
        "type": WORKFLOW_TYPE_DAILY,
        "workflowId": SCHEDULE_WORKFLOW_ID,
        "inputData": INPUT_DATA,
        "endDate": END_DATE_SPECIFIED,
    }
    assert history[0].headers["Authorization"] == f"Bearer {API_KEY}"


def test_schedule_workflow_success_once_no_end_date(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test schedule for ONCE type with no end_date successfully."""
    expected_api_response = {
        "data": {
            "id": "sch_67890",
            "name": SCHEDULE_NAME,
            "type": WORKFLOW_TYPE_ONCE,
            "startDate": START_DATE,
            "endDate": START_DATE,  # API might return startDate as endDate for ONCE
            "scheduleTime": SCHEDULE_TIME,
            "timezoneId": TIMEZONE_ID,
            "workflowId": SCHEDULE_WORKFLOW_ID,
            "inputData": INPUT_DATA,
            "status": "ACTIVE",
        },
        "error": None,
        "errors": None,
        "meta": None,
    }
    mock_url = f"{MOCK_V1_PUBLIC_BASE}/schedules"
    requests_mock.post(mock_url, json=expected_api_response, status_code=200)

    response = client.workflow.schedule(
        name=SCHEDULE_NAME,
        schedule_time=SCHEDULE_TIME,
        timezone_id=TIMEZONE_ID,
        start_date=START_DATE,
        workflow_type=WORKFLOW_TYPE_ONCE,
        workflow_id=SCHEDULE_WORKFLOW_ID,
        input_data=INPUT_DATA,
        end_date=None,  # Explicitly None
    )

    # Expect parsed model object
    assert isinstance(response, ScheduleData)
    assert response.id == "sch_67890"
    assert response.name == SCHEDULE_NAME
    assert response.schedule_type == WORKFLOW_TYPE_ONCE
    assert response.start_date == START_DATE
    assert response.end_date == START_DATE
    assert response.schedule_time == SCHEDULE_TIME
    assert response.timezone_id == TIMEZONE_ID
    assert response.workflow_id == SCHEDULE_WORKFLOW_ID
    assert response.input_data == INPUT_DATA
    assert response.status == "ACTIVE"

    history = requests_mock.request_history
    assert len(history) == 1
    assert history[0].json() == {
        "name": SCHEDULE_NAME,
        "scheduleTime": SCHEDULE_TIME,
        "timezoneId": TIMEZONE_ID,
        "startDate": START_DATE,
        "type": WORKFLOW_TYPE_ONCE,
        "workflowId": SCHEDULE_WORKFLOW_ID,
        "inputData": INPUT_DATA,
        "endDate": "",  # Expected to be an empty string for ONCE type
    }


def test_schedule_workflow_http_400_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test schedule_workflow handles HTTP 400 Bad Request error."""
    error_response = {
        "data": None,
        "error": {"errorCode": "VALIDATION_ERROR", "message": "Invalid input"},
        "errors": [{"field": "scheduleTime", "message": "Invalid time format"}],
        "meta": None,
    }
    mock_url = f"{MOCK_V1_PUBLIC_BASE}/schedules"
    requests_mock.post(mock_url, json=error_response, status_code=400)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.schedule(
            name=SCHEDULE_NAME,
            schedule_time="invalid-time",  # Intentionally invalid
            timezone_id=TIMEZONE_ID,
            start_date=START_DATE,
            workflow_type=WORKFLOW_TYPE_ONCE,
            workflow_id=SCHEDULE_WORKFLOW_ID,
            input_data=INPUT_DATA,
        )

    assert exc_info.value.status_code == 400


def test_schedule_workflow_http_401_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test schedule handles HTTP 401 Unauthorized error."""
    error_response = {"detail": "Authentication credentials were not provided."}
    mock_url = f"{MOCK_V1_PUBLIC_BASE}/schedules"
    requests_mock.post(mock_url, json=error_response, status_code=401)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.schedule(
            name=SCHEDULE_NAME,
            schedule_time=SCHEDULE_TIME,
            timezone_id=TIMEZONE_ID,
            start_date=START_DATE,
            workflow_type=WORKFLOW_TYPE_ONCE,
            workflow_id=SCHEDULE_WORKFLOW_ID,
            input_data=INPUT_DATA,
        )

    assert exc_info.value.status_code == 401


def test_schedule_workflow_http_404_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test schedule handles HTTP 404 Not Found error (e.g., bad workflowId)."""
    error_response = {"detail": "Workflow not found."}
    mock_url = f"{MOCK_V1_PUBLIC_BASE}/schedules"
    requests_mock.post(mock_url, json=error_response, status_code=404)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.schedule(
            name=SCHEDULE_NAME,
            schedule_time=SCHEDULE_TIME,
            timezone_id=TIMEZONE_ID,
            start_date=START_DATE,
            workflow_type=WORKFLOW_TYPE_ONCE,
            workflow_id="wf_non_existent_xyz789",
            input_data=INPUT_DATA,
        )

    assert exc_info.value.status_code == 404


def test_schedule_workflow_network_error(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test schedule handles a network error."""
    mock_url = f"{MOCK_V1_PUBLIC_BASE}/schedules"
    requests_mock.post(
        mock_url, exc=requests.exceptions.ConnectionError("Connection failed")
    )

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.schedule(
            name=SCHEDULE_NAME,
            schedule_time=SCHEDULE_TIME,
            timezone_id=TIMEZONE_ID,
            start_date=START_DATE,
            workflow_type=WORKFLOW_TYPE_ONCE,
            workflow_id=SCHEDULE_WORKFLOW_ID,
            input_data=INPUT_DATA,
        )

    assert "Network or connection error" in str(exc_info.value)


def test_schedule_workflow_http_error_non_json_response(
    client: SirenClient, requests_mock: RequestsMocker
):
    """Test schedule handles HTTP error with non-JSON response."""
    mock_url = f"{MOCK_V1_PUBLIC_BASE}/schedules"
    non_json_error_text = "Gateway Timeout"
    requests_mock.post(mock_url, text=non_json_error_text, status_code=504)

    with pytest.raises(SirenSDKError) as exc_info:
        client.workflow.schedule(
            name=SCHEDULE_NAME,
            schedule_time=SCHEDULE_TIME,
            timezone_id=TIMEZONE_ID,
            start_date=START_DATE,
            workflow_type=WORKFLOW_TYPE_ONCE,
            workflow_id=SCHEDULE_WORKFLOW_ID,
            input_data=INPUT_DATA,
        )

    assert "API response was not valid JSON" in str(exc_info.value)
    assert exc_info.value.status_code == 504
