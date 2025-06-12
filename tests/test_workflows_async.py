"""Async tests for workflow client."""

import httpx  # type: ignore
import pytest
import respx  # type: ignore

from siren.async_client import AsyncSirenClient
from siren.models.workflows import BulkWorkflowExecutionData, WorkflowExecutionData

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"


@respx.mock
@pytest.mark.asyncio
async def test_async_trigger_workflow_success():
    """trigger() returns execution data."""
    client = AsyncSirenClient(api_key=API_KEY, env="dev")
    expected_json = {
        "data": {
            "requestId": "req1",
            "workflowExecutionId": "exec1",
        },
        "error": None,
    }
    route = respx.post(f"{BASE_URL}/api/v2/workflows/trigger").mock(
        return_value=httpx.Response(200, json=expected_json)
    )

    exec_data = await client.workflow.trigger(workflow_name="sampleWorkflow")

    assert route.called
    assert isinstance(exec_data, WorkflowExecutionData)
    assert exec_data.request_id == "req1"

    await client.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_async_trigger_bulk_workflow_success():
    """trigger_bulk() returns bulk execution data."""
    client = AsyncSirenClient(api_key=API_KEY, env="dev")
    expected_json = {
        "data": {
            "requestId": "req_bulk",
            "workflowExecutionIds": ["e1", "e2"],
        },
        "error": None,
    }
    route = respx.post(f"{BASE_URL}/api/v2/workflows/trigger/bulk").mock(
        return_value=httpx.Response(200, json=expected_json)
    )

    bulk_data = await client.workflow.trigger_bulk(
        workflow_name="sampleWorkflow",
        notify=[{"email": "u1"}],
    )

    assert route.called
    assert isinstance(bulk_data, BulkWorkflowExecutionData)
    assert bulk_data.request_id == "req_bulk"

    await client.aclose()
