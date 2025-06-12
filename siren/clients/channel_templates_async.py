"""Asynchronous channel-template operations for Siren SDK."""

from typing import Any

from ..models.templates import (
    ChannelTemplate,
    CreateChannelTemplatesRequest,
    CreateChannelTemplatesResponse,
    GetChannelTemplatesResponse,
)
from .async_base import AsyncBaseClient


class AsyncChannelTemplateClient(AsyncBaseClient):
    """Non-blocking channel-template actions."""

    async def create(
        self, template_id: str, **channel_payloads: Any
    ) -> list[ChannelTemplate]:
        """Create channel templates for the given template ID."""
        payload: dict[str, Any] = {k: v for k, v in channel_payloads.items() if v}
        response = await self._make_request(
            method="POST",
            endpoint=f"/api/v1/public/template/{template_id}/channel-templates",
            request_model=CreateChannelTemplatesRequest,
            response_model=CreateChannelTemplatesResponse,
            data=payload,
        )
        return response  # type: ignore[return-value]

    async def get(self, version_id: str, **params: Any) -> list[ChannelTemplate]:
        """Get channel templates for a specific template version."""
        response = await self._make_request(
            method="GET",
            endpoint=f"/api/v1/public/template/versions/{version_id}/channel-templates",
            response_model=GetChannelTemplatesResponse,
            params=params or None,
        )
        return response  # type: ignore[return-value]
