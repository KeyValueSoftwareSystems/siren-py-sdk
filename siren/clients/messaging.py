"""Messaging client for the Siren SDK."""

from typing import Any, Dict, List, Optional

from ..models.messaging import (
    MessageRepliesResponse,
    MessageStatusResponse,
    ProviderCode,
    Recipient,
    ReplyData,
    SendMessageRequest,
    SendMessageResponse,
)
from .base import BaseClient


class MessageClient(BaseClient):
    """Client for direct message operations."""

    def send(
        self,
        recipient_value: str,
        channel: str,
        *,
        body: Optional[str] = None,
        template_name: Optional[str] = None,
        template_variables: Optional[Dict[str, Any]] = None,
        provider_name: Optional[str] = None,
        provider_code: Optional[ProviderCode] = None,
    ) -> str:
        """Send a message either using a template or directly.

        Args:
            recipient_value: The identifier for the recipient (e.g., Slack user ID, email address)
            channel: The channel to send the message through (e.g., "SLACK", "EMAIL")
            body: Optional message body text (required if no template)
            template_name: Optional template name (required if no body)
            template_variables: Optional template variables for template-based messages
            provider_name: Optional provider name (must be provided with provider_code)
            provider_code: Optional provider code from ProviderCode enum (must be provided with provider_name)

        Returns:
            The message ID of the sent message.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
            ValueError: If neither body nor template_name is provided
        """
        # Validate that both provider arguments are provided together
        if (provider_name is not None) != (provider_code is not None):
            raise ValueError(
                "Both provider_name and provider_code must be provided together"
            )

        recipient = Recipient(value=recipient_value)
        payload = {
            "recipient": recipient.model_dump(),
            "channel": channel,
        }

        if body is not None:
            payload["body"] = body
        elif template_name is not None:
            payload["template"] = {"name": template_name}
            if template_variables is not None:
                payload["template_variables"] = template_variables

        if provider_name is not None and provider_code is not None:
            payload["provider_name"] = provider_name
            payload["provider_code"] = provider_code.value

        response = self._make_request(
            method="POST",
            endpoint="/api/v1/public/send-messages",
            request_model=SendMessageRequest,
            response_model=SendMessageResponse,
            data=payload,
        )
        return response.message_id

    def send_awesome_template(
        self,
        recipient_value: str,
        channel: str,
        template_identifier: str,
        *,
        template_variables: Optional[Dict[str, Any]] = None,
        provider_name: Optional[str] = None,
        provider_code: Optional[ProviderCode] = None,
    ) -> str:
        """Send a message using a template path.

        Args:
            recipient_value: The identifier for the recipient (e.g., Slack user ID, email address)
            channel: The channel to send the message through (e.g., "SLACK", "EMAIL")
            template_identifier: The template identifier path (e.g., "awesome-templates/support/escalation/official/friendly")
            template_variables: Optional template variables for template-based messages
            provider_name: Optional provider name (must be provided with provider_code)
            provider_code: Optional provider code from ProviderCode enum (must be provided with provider_name)

        Returns:
            The message ID of the sent message.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
            ValueError: If provider_name and provider_code are not both provided together
        """
        # Validate that both provider arguments are provided together
        if (provider_name is not None) != (provider_code is not None):
            raise ValueError(
                "Both provider_name and provider_code must be provided together"
            )

        recipient = Recipient(value=recipient_value)
        payload = {
            "recipient": recipient.model_dump(),
            "channel": channel,
            "template_identifier": template_identifier,
        }

        if template_variables is not None:
            payload["template_variables"] = template_variables

        if provider_name is not None and provider_code is not None:
            payload["provider_name"] = provider_name
            payload["provider_code"] = provider_code.value

        response = self._make_request(
            method="POST",
            endpoint="/api/v1/public/send-awesome-messages",
            request_model=SendMessageRequest,
            response_model=SendMessageResponse,
            data=payload,
        )
        return response.message_id

    def get_status(self, message_id: str) -> str:
        """Retrieve the status of a specific message.

        Args:
            message_id: The ID of the message for which to retrieve the status.

        Returns:
            The status of the message (e.g., "DELIVERED", "PENDING").

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        response = self._make_request(
            method="GET",
            endpoint=f"/api/v1/public/message-status/{message_id}",
            response_model=MessageStatusResponse,
        )
        return response.status

    def get_replies(self, message_id: str) -> List[ReplyData]:
        """Retrieve replies for a specific message.

        Args:
            message_id: The ID of the message for which to retrieve replies.

        Returns:
            A list of reply objects containing message details.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        response = self._make_request(
            method="GET",
            endpoint=f"/api/v1/public/get-reply/{message_id}",
            response_model=MessageRepliesResponse,
        )
        return response
