"""Messaging-related models for the Siren SDK."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .base import BaseAPIResponse


class TemplateInfo(BaseModel):
    """Template information for messaging."""

    name: str


class Recipient(BaseModel):
    """Recipient information for messaging."""

    type: str
    value: str


class SendMessageRequest(BaseModel):
    """Request model for sending messages."""

    # Fix: template_variables was silently becoming None during model creation
    model_config = ConfigDict(populate_by_name=True)

    template: TemplateInfo
    recipient: Recipient
    channel: str
    template_variables: Optional[Dict[str, Any]] = Field(
        alias="templateVariables", default=None
    )


class MessageData(BaseModel):
    """Message response data."""

    message_id: str = Field(alias="notificationId")


class StatusData(BaseModel):
    """Message status data."""

    status: str


class ReplyData(BaseModel):
    """Individual reply data."""

    text: str
    thread_ts: str = Field(alias="threadTs")
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
