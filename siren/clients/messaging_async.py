"""Asynchronous MessagingClient implementation."""

from __future__ import annotations

from typing import Any

from ..models.messaging import (
    MessageRepliesResponse,
    MessageStatusResponse,
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
        recipient_type: str,
        recipient_value: str,
        template_variables: dict[str, Any] | None = None,
    ) -> str:
        """Send a message and return the notification ID."""
        payload: dict[str, Any] = {
            "template": {"name": template_name},
            "recipient": {"type": recipient_type, "value": recipient_value},
            "channel": channel,
        }
        if template_variables is not None:
            payload["template_variables"] = template_variables

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
