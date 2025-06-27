"""Asynchronous Workflow client for Siren SDK."""

from typing import Any, Dict, List, Optional

from ..models.workflows import (
    BulkWorkflowExecutionData,
    ScheduleData,
    ScheduleWorkflowRequest,
    ScheduleWorkflowResponse,
    TriggerBulkWorkflowRequest,
    TriggerBulkWorkflowResponse,
    TriggerWorkflowRequest,
    TriggerWorkflowResponse,
    WorkflowExecutionData,
)
from .async_base import AsyncBaseClient


class AsyncWorkflowClient(AsyncBaseClient):
    """Non-blocking operations for triggering and scheduling workflows."""

    async def trigger(
        self,
        workflow_name: str,
        data: Optional[Dict[str, Any]] = None,
        notify: Optional[Dict[str, Any]] = None,
    ) -> WorkflowExecutionData:
        """Trigger a workflow execution and return execution data."""
        response = await self._make_request(
            method="POST",
            endpoint="/api/v2/workflows/trigger",
            request_model=TriggerWorkflowRequest,
            response_model=TriggerWorkflowResponse,
            data={
                "workflow_name": workflow_name,
                "data": data,
                "notify": notify,
            },
        )
        return response  # type: ignore[return-value]

    async def trigger_bulk(
        self,
        workflow_name: str,
        notify: List[Dict[str, Any]],
        data: Optional[Dict[str, Any]] = None,
    ) -> BulkWorkflowExecutionData:
        """Trigger workflow for multiple recipients in bulk."""
        response = await self._make_request(
            method="POST",
            endpoint="/api/v2/workflows/trigger/bulk",
            request_model=TriggerBulkWorkflowRequest,
            response_model=TriggerBulkWorkflowResponse,
            data={
                "workflow_name": workflow_name,
                "notify": notify,
                "data": data,
            },
        )
        return response  # type: ignore[return-value]

    async def schedule(
        self,
        name: str,
        schedule_time: str,
        timezone_id: str,
        start_date: str,
        workflow_type: str,
        workflow_id: str,
        input_data: Dict[str, Any],
        end_date: Optional[str] = None,
    ) -> ScheduleData:
        """Schedule a workflow as per provided recurrence params."""
        if workflow_type == "ONCE" and end_date is None:
            end_date = ""
        response = await self._make_request(
            method="POST",
            endpoint="/api/v1/public/schedules",
            request_model=ScheduleWorkflowRequest,
            response_model=ScheduleWorkflowResponse,
            data={
                "name": name,
                "schedule_time": schedule_time,
                "timezone_id": timezone_id,
                "start_date": start_date,
                "workflow_type": workflow_type,
                "workflow_id": workflow_id,
                "input_data": input_data,
                "end_date": end_date,
            },
        )
        return response  # type: ignore[return-value]
