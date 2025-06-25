"""Asynchronous MessagingClient implementation."""

from __future__ import annotations

from typing import Any

from ..models.messaging import (
    MessageRepliesResponse,
    MessageStatusResponse,
    Recipient,
    ReplyData,
    SendMessageRequest,
    SendMessageResponse,
)
from .async_base import AsyncBaseClient


class AsyncMessageClient(AsyncBaseClient):
    """Non-blocking client for message operations."""

    async def send(
        self,
        template_name: str,
        channel: str,
        recipient_value: str,
        template_variables: dict[str, Any] | None = None,
        provider_name: str | None = None,
        provider_code: str | None = None,
    ) -> str:
        """Send a message and return the notification ID.

        Args:
            template_name: The name of the template to use.
            channel: The channel to send the message to.
            recipient_value: The value of the recipient.
            template_variables: The variables to use in the template.
            provider_name: The name of the provider to use.
            provider_code: The code of the provider to use.
        """
        recipient = self._create_recipient(channel, recipient_value)
        
        payload: dict[str, Any] = {
            "template": {"name": template_name},
            "recipient": recipient.model_dump(),
            "channel": channel,
        }
        if template_variables is not None:
            payload["templateVariables"] = template_variables
        if provider_name is not None and provider_code is not None:
            payload["providerIntegration"] = {
                "name": provider_name,
                "code": provider_code.value,
            }

        response = await self._make_request(
            method="POST",
            endpoint="/api/v1/public/send-messages",
            request_model=SendMessageRequest,
            response_model=SendMessageResponse,
            data=payload,
        )
        return response.message_id  # type: ignore[return-value]

    async def get_status(self, message_id: str) -> str:
        """Return delivery status for a given message ID."""
        response = await self._make_request(
            method="GET",
            endpoint=f"/api/v1/public/message-status/{message_id}",
            response_model=MessageStatusResponse,
        )
        return response.status  # type: ignore[return-value]

    async def get_replies(self, message_id: str) -> list[ReplyData]:
        """Return list of replies for a given message ID."""
        response = await self._make_request(
            method="GET",
            endpoint=f"/api/v1/public/get-reply/{message_id}",
            response_model=MessageRepliesResponse,
        )
        return response  # type: ignore[return-value]

    def _create_recipient(self, channel: str, recipient_value: str) -> Recipient:
            """Create a Recipient object based on the channel and recipient value.
            
            Args:
                channel: The channel to send the message through (e.g., "SLACK", "EMAIL")
                recipient_value: The identifier for the recipient (e.g., Slack user ID, email address)
                
            Returns:
                A Recipient object configured for the specified channel
                
            Raises:
                ValueError: If the channel is not supported
            """
            channel_to_recipient_key = {
                "EMAIL": "email",
                "SMS": "sms", 
                "WHATSAPP": "whatsapp",
                "SLACK": "slack",
                "TEAMS": "teams",
                "DISCORD": "discord",
                "LINE": "line",
                "IN_APP": "inApp",
                "PUSH": "pushToken",
            }
            
            recipient_key = channel_to_recipient_key.get(channel.upper())
            if recipient_key is None:
                raise ValueError(f"Unsupported channel: {channel}")
            
            return Recipient(**{recipient_key: recipient_value})