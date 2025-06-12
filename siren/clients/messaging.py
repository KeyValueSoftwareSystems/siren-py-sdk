"""Messaging client for the Siren SDK."""

from typing import Any, Dict, List, Optional

from ..models.messaging import (
    MessageRepliesResponse,
    MessageStatusResponse,
    ReplyData,
    SendMessageRequest,
    SendMessageResponse,
)
from .base import BaseClient


class MessageClient(BaseClient):
    """Client for direct message operations."""

    def send(
        self,
        template_name: str,
        channel: str,
        recipient_type: str,
        recipient_value: str,
        template_variables: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Send a message using a specific template.

        Args:
            template_name: The name of the template to use.
            channel: The channel to send the message through (e.g., "SLACK", "EMAIL").
            recipient_type: The type of recipient (e.g., "direct").
            recipient_value: The identifier for the recipient (e.g., Slack user ID, email address).
            template_variables: A dictionary of variables to populate the template.

        Returns:
            The message ID of the sent message.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        payload = {
            "template": {"name": template_name},
            "recipient": {"type": recipient_type, "value": recipient_value},
            "channel": channel,
        }
        if template_variables is not None:
            payload["template_variables"] = template_variables

        response = self._make_request(
            method="POST",
            endpoint="/api/v1/public/send-messages",
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
