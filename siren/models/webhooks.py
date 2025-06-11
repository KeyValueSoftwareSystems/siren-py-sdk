"""Webhook-related models for the Siren SDK."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .base import BaseAPIResponse


class WebhookConfig(BaseModel):
    """Webhook configuration with URL, headers, and verification key."""

    url: str
    headers: List[Dict[str, Any]] = []
    verification_key: str = Field(alias="verificationKey")


class WebhookData(BaseModel):
    """Webhook response data containing both webhook configurations."""

    id: str
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")
    deleted_at: Optional[str] = Field(None, alias="deletedAt")
    created_by: Optional[str] = Field(None, alias="createdBy")
    updated_by: Optional[str] = Field(None, alias="updatedBy")
    deleted_by: Optional[str] = Field(None, alias="deletedBy")
    environment: Optional[str] = None
    webhook_config: Optional[WebhookConfig] = Field(None, alias="webhookConfig")
    inbound_webhook_config: Optional[WebhookConfig] = Field(
        None, alias="inboundWebhookConfig"
    )


class NotificationsWebhookRequest(BaseModel):
    """Request model for notifications webhook configuration."""

    model_config = ConfigDict(validate_by_name=True)

    webhook_config: "WebhookConfigRequest" = Field(alias="webhookConfig")


class InboundWebhookRequest(BaseModel):
    """Request model for inbound webhook configuration."""

    model_config = ConfigDict(validate_by_name=True)

    inbound_webhook_config: "WebhookConfigRequest" = Field(alias="inboundWebhookConfig")


class WebhookConfigRequest(BaseModel):
    """Webhook configuration for requests."""

    url: str


class WebhookResponse(BaseAPIResponse[WebhookData]):
    """API response for webhook operations."""

    pass
