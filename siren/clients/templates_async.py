"""Asynchronous template operations for Siren SDK."""

from typing import Any

from ..models.templates import (
    CreatedTemplate,
    CreateTemplateRequest,
    CreateTemplateResponse,
    PublishTemplateResponse,
    Template,
    TemplateListResponse,
    UpdateTemplateRequest,
    UpdateTemplateResponse,
)
from .async_base import AsyncBaseClient


class AsyncTemplateClient(AsyncBaseClient):
    """Non-blocking template operations."""

    async def get(
        self, page: int | None = None, size: int | None = None
    ) -> list[Template]:
        """Return paginated list of templates."""
        params: dict[str, Any] | None = None
        if page is not None or size is not None:
            params = {"page": page or 0, "size": size or 10}
        response = await self._make_request(
            method="GET",
            endpoint="/api/v1/public/template",
            response_model=TemplateListResponse,
            params=params,
        )
        return response  # type: ignore[return-value]

    async def create(
        self,
        name: str,
        description: str | None = None,
        tag_names: list[str] | None = None,
        variables: list[dict[str, Any]] | None = None,
    ) -> CreatedTemplate:
        """Create a new template and return summary data."""
        payload: dict[str, Any] = {"name": name}
        if description is not None:
            payload["description"] = description
        if tag_names is not None:
            payload["tag_names"] = tag_names
        if variables is not None:
            payload["variables"] = variables

        response = await self._make_request(
            method="POST",
            endpoint="/api/v1/public/template",
            request_model=CreateTemplateRequest,
            response_model=CreateTemplateResponse,
            data=payload,
        )
        return response  # type: ignore[return-value]

    async def update(
        self,
        template_id: str,
        **updates: Any,
    ) -> Template:
        """Update a template's metadata fields."""
        response = await self._make_request(
            method="PUT",
            endpoint=f"/api/v1/public/template/{template_id}",
            request_model=UpdateTemplateRequest,
            response_model=UpdateTemplateResponse,
            data=updates,
        )
        return response  # type: ignore[return-value]

    async def delete(self, template_id: str) -> bool:
        """Delete template by ID."""
        await self._make_request(
            method="DELETE",
            endpoint=f"/api/v1/public/template/{template_id}",
            expected_status=204,
        )
        return True

    async def publish(self, template_id: str) -> Template:
        """Publish draft template returning published entity."""
        response = await self._make_request(
            method="PATCH",
            endpoint=f"/api/v1/public/template/{template_id}/publish",
            response_model=PublishTemplateResponse,
        )
        return response  # type: ignore[return-value]
