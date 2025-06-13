"""Messaging-related models for the Siren SDK."""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .base import BaseAPIResponse


class TemplateInfo(BaseModel):
    """Template information for messaging."""

    name: str


class Recipient(BaseModel):
    """Recipient information for messaging."""

    type: Literal["user_id", "direct"]
    value: str


class SendMessageRequest(BaseModel):
    """Request model for sending messages."""

    # Fix: template_variables was silently becoming None during model creation
    model_config = ConfigDict(populate_by_name=True)

    recipient: Recipient
    channel: str
    body: Optional[str] = None
    template: Optional[TemplateInfo] = None
    template_variables: Optional[Dict[str, Any]] = Field(
        alias="templateVariables", default=None
    )

    @field_validator("body")
    @classmethod
    def validate_body(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        """Validate that either body or template is provided."""
        if not v and not values.get("template"):
            raise ValueError("Either body or template must be provided")
        return v


class MessageData(BaseModel):
    """Message response data."""

    message_id: str = Field(alias="notificationId")


class StatusData(BaseModel):
    """Message status data."""

    status: str


class ReplyData(BaseModel):
    """Individual reply data."""

    text: str
    thread_ts: Optional[str] = Field(None, alias="threadTs")
    user: str
    ts: str


class SendMessageResponse(BaseAPIResponse[MessageData]):
    """API response for send message operations."""

    pass


class MessageStatusResponse(BaseAPIResponse[StatusData]):
    """API response for message status operations."""

    pass


class MessageRepliesResponse(BaseAPIResponse[List[ReplyData]]):
    """API response for message replies operations."""

    pass
