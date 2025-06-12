"""Workflows client using BaseClient architecture."""

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
from .base import BaseClient


class WorkflowClient(BaseClient):
    """Client for workflow operations using BaseClient."""

    def trigger(
        self,
        workflow_name: str,
        data: Optional[Dict[str, Any]] = None,
        notify: Optional[Dict[str, Any]] = None,
    ) -> WorkflowExecutionData:
        """Trigger a workflow with the given name and payload.

        Args:
            workflow_name: The name of the workflow to execute.
            data: Common data for all workflow executions.
            notify: Specific data for this workflow execution.

        Returns:
            WorkflowExecutionData: Workflow execution details.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        # Store original timeout for custom timeout handling
        original_timeout = self.timeout
        self.timeout = 10

        try:
            response = self._make_request(
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
        finally:
            # Restore original timeout
            self.timeout = original_timeout
        return response

    def trigger_bulk(
        self,
        workflow_name: str,
        notify: List[Dict[str, Any]],
        data: Optional[Dict[str, Any]] = None,
    ) -> BulkWorkflowExecutionData:
        """Trigger a workflow in bulk for multiple recipients/notifications.

        Args:
            workflow_name: The name of the workflow to execute.
            notify: A list of notification objects, each representing specific data
                   for a workflow execution. The workflow will be executed for
                   each element in this list.
            data: Common data that will be used across all workflow executions.

        Returns:
            BulkWorkflowExecutionData: Bulk workflow execution details.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        # Store original timeout for custom timeout handling
        original_timeout = self.timeout
        self.timeout = 20  # Increased timeout for bulk

        try:
            response = self._make_request(
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
        finally:
            # Restore original timeout
            self.timeout = original_timeout
        return response

    def schedule(
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
        """Schedule a workflow execution.

        Args:
            name: Name of the schedule.
            schedule_time: Time for the schedule in "HH:MM:SS" format.
            timezone_id: Timezone ID (e.g., "Asia/Kolkata").
            start_date: Start date for the schedule in "YYYY-MM-DD" format.
            workflow_type: Type of schedule (e.g., "ONCE", "DAILY").
            workflow_id: ID of the workflow to schedule.
            input_data: Input data for the workflow.
            end_date: Optional end date for the schedule in "YYYY-MM-DD" format.

        Returns:
            ScheduleData: Schedule details.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        # Handle ONCE type special case for end_date
        if workflow_type == "ONCE" and end_date is None:
            end_date = ""

        response = self._make_request(
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
        return response
