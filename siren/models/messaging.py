"""Messaging-related models for the Siren SDK."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .base import BaseAPIResponse


class ProviderCode(str, Enum):
    """Available provider codes for messaging."""

    EMAIL_SENDGRID = "EMAIL_SENDGRID"
    SMS_MSG91 = "SMS_MSG91"
    PUSH_FCM = "PUSH_FCM"
    WHATSAPP_META = "WHATSAPP_META"
    WHATSAPP_WATI = "WHATSAPP_WATI"
    IN_APP_SIREN = "IN_APP_SIREN"
    SMS_TWILIO = "SMS_TWILIO"
    SMS_KALEYRA_IO = "SMS_KALEYRA_IO"
    SMS_PLIVO = "SMS_PLIVO"
    EMAIL_MAILCHIMP = "EMAIL_MAILCHIMP"
    EMAIL_GMAIL = "EMAIL_GMAIL"
    EMAIL_POSTMARK = "EMAIL_POSTMARK"
    EMAIL_OUTLOOK = "EMAIL_OUTLOOK"
    EMAIL_SIREN_SAMPLE = "EMAIL_SIREN_SAMPLE"
    SMS_MESSAGEBIRD = "SMS_MESSAGEBIRD"
    PUSH_ONESIGNAL = "PUSH_ONESIGNAL"
    EMAIL_MAILGUN = "EMAIL_MAILGUN"
    EMAIL_SES = "EMAIL_SES"
    SLACK = "SLACK"
    WHATSAPP_TWILIO = "WHATSAPP_TWILIO"
    TEAMS = "TEAMS"
    WHATSAPP_GUPSHUP = "WHATSAPP_GUPSHUP"
    DISCORD = "DISCORD"
    WHATSAPP_MSG91 = "WHATSAPP_MSG91"
    LINE = "LINE"


class TemplateInfo(BaseModel):
    """Template information for messaging."""

    name: str


class Recipient(BaseModel):
    """Recipient information for messaging."""
    # type: str = "direct"  # Default to "direct", can be "user_id" or other values
    slack: str | None = None
    email: str | None = None


class ProviderIntegration(BaseModel):
    """Provider integration information."""
    
    name: str
    code: str


class SendMessageRequest(BaseModel):
    """Request model for sending messages."""

    # Fix: template_variables was silently becoming None during model creation
    model_config = ConfigDict(populate_by_name=True)

    channel: str
    body: Optional[str] = None
    template: Optional[TemplateInfo] = None
    template_variables: Optional[Dict[str, Any]] = Field(
        alias="templateVariables", default=None
    )
    recipient: Recipient
    template_identifier: Optional[str] = Field(alias="templateIdentifier", default=None)
    template_path: Optional[str] = Field(alias="templatePath", default=None)
    provider_integration: Optional[ProviderIntegration] = Field(alias="providerIntegration", default=None)

    @model_validator(mode="after")
    def validate_message_content(self) -> "SendMessageRequest":
        """Validate that either body, template, or template_identifier is provided."""
        if not self.body and not self.template and not self.template_identifier and not self.template_path:
            raise ValueError(
                "Either body, template,template_path or template_identifier must be provided"
            )
        return self

    @model_validator(mode="after")
    def validate_provider_fields(self) -> "SendMessageRequest":
        """Validate that both provider_name and provider_code are provided together."""
        has_provider_name = self.provider_integration is not None and self.provider_integration.name is not None
        has_provider_code = self.provider_integration is not None and self.provider_integration.code is not None

        if has_provider_name != has_provider_code:
            raise ValueError(
                "Both provider_name and provider_code must be provided together"
            )

        return self

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
