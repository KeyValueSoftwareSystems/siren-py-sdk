"""Workflow-related data models for the Siren SDK."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseAPIResponse


class TriggerWorkflowRequest(BaseModel):
    """Request model for triggering a workflow."""

    workflow_name: str = Field(..., alias="workflowName")
    data: Optional[Dict[str, Any]] = None
    notify: Optional[Dict[str, Any]] = None

    class Config:
        """Pydantic config."""

        populate_by_name = True


class TriggerBulkWorkflowRequest(BaseModel):
    """Request model for triggering a bulk workflow."""

    workflow_name: str = Field(..., alias="workflowName")
    notify: List[Dict[str, Any]]
    data: Optional[Dict[str, Any]] = None

    class Config:
        """Pydantic config."""

        populate_by_name = True


class ScheduleWorkflowRequest(BaseModel):
    """Request model for scheduling a workflow."""

    name: str
    schedule_time: str = Field(..., alias="scheduleTime")
    timezone_id: str = Field(..., alias="timezoneId")
    start_date: str = Field(..., alias="startDate")
    workflow_type: str = Field(..., alias="type")
    workflow_id: str = Field(..., alias="workflowId")
    input_data: Dict[str, Any] = Field(..., alias="inputData")
    end_date: Optional[str] = Field(None, alias="endDate")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class WorkflowExecutionData(BaseModel):
    """Workflow execution response data."""

    request_id: str = Field(..., alias="requestId")
    workflow_execution_id: str = Field(..., alias="workflowExecutionId")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class BulkWorkflowExecutionData(BaseModel):
    """Bulk workflow execution response data."""

    request_id: str = Field(..., alias="requestId")
    workflow_execution_ids: List[str] = Field(..., alias="workflowExecutionIds")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class ScheduleData(BaseModel):
    """Schedule response data."""

    id: str
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
    deleted_at: Optional[str] = Field(None, alias="deletedAt")
    created_by: Optional[str] = Field(None, alias="createdBy")
    updated_by: Optional[str] = Field(None, alias="updatedBy")
    deleted_by: Optional[str] = Field(None, alias="deletedBy")
    project_environment_id: Optional[str] = Field(None, alias="projectEnvironmentId")
    name: str
    schedule_type: str = Field(..., alias="type")
    input_data: Dict[str, Any] = Field(..., alias="inputData")
    start_date: str = Field(..., alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    schedule_time: str = Field(..., alias="scheduleTime")
    timezone_id: str = Field(..., alias="timezoneId")
    schedule_day: Optional[List[Any]] = Field(None, alias="scheduleDay")
    monthly_schedule_option: Optional[Any] = Field(None, alias="monthlyScheduleOption")
    no_of_occurrences: Optional[int] = Field(None, alias="noOfOccurrences")
    scheduler_pattern: Optional[str] = Field(None, alias="schedulerPattern")
    status: str
    workflow: Optional[Any] = None
    # For backward compatibility with test data
    workflow_id: Optional[str] = Field(None, alias="workflowId")

    class Config:
        """Pydantic config."""

        populate_by_name = True


# Response models
class TriggerWorkflowResponse(BaseAPIResponse[WorkflowExecutionData]):
    """Response model for trigger workflow."""

    pass


class TriggerBulkWorkflowResponse(BaseAPIResponse[BulkWorkflowExecutionData]):
    """Response model for trigger bulk workflow."""

    pass


class ScheduleWorkflowResponse(BaseAPIResponse[ScheduleData]):
    """Response model for schedule workflow."""

    pass
