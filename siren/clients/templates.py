"""New templates client using BaseClient architecture."""

from typing import List, Optional

from ..models.base import DeleteResponse
from ..models.templates import (
    ChannelTemplate,
    CreatedTemplate,
    CreateTemplateRequest,
    CreateTemplateResponse,
    PublishTemplateResponse,
    Template,
    TemplateListResponse,
    UpdateTemplateRequest,
    UpdateTemplateResponse,
)
from .base import BaseClient
from .channel_templates import ChannelTemplateClient


class TemplateClient(BaseClient):
    """Client for template operations."""

    def __init__(self, api_key: str, base_url: str, timeout: int = 10):
        """Initialize TemplateClient with an internal ChannelTemplateClient.

        Args:
            api_key: Bearer token for Siren API.
            base_url: API root.
            timeout: Request timeout in seconds.
        """
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout)
        # Re-use specialised client instead of duplicating logic
        self._channel_template_client = ChannelTemplateClient(
            api_key=api_key, base_url=base_url, timeout=timeout
        )

    def get(
        self,
        tag_names: Optional[str] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> List[Template]:
        """Fetch templates.

        Args:
            tag_names: Filter by tag names.
            search: Search by field.
            sort: Sort by field.
            page: Page number.
            size: Page size.

        Returns:
            List[Template]: A list of Template models.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        params = {}
        if tag_names is not None:
            params["tagNames"] = tag_names
        if search is not None:
            params["search"] = search
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size

        response = self._make_request(
            method="GET",
            endpoint="/api/v1/public/template",
            response_model=TemplateListResponse,
            params=params,
        )
        return response

    def create(self, **template_data) -> CreatedTemplate:
        """Create a new template.

        Args:
            **template_data: Template attributes matching the CreateTemplateRequest model fields.

        Returns:
            CreatedTemplate: A CreatedTemplate model representing the created template.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        response = self._make_request(
            method="POST",
            endpoint="/api/v1/public/template",
            request_model=CreateTemplateRequest,
            response_model=CreateTemplateResponse,
            data=template_data,
        )
        return response

    def update(self, template_id: str, **template_data) -> Template:
        """Update an existing template.

        Args:
            template_id: The ID of the template to update.
            **template_data: Template attributes matching the UpdateTemplateRequest model fields.

        Returns:
            Template: A Template model representing the updated template.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        response = self._make_request(
            method="PUT",
            endpoint=f"/api/v1/public/template/{template_id}",
            request_model=UpdateTemplateRequest,
            response_model=UpdateTemplateResponse,
            data=template_data,
        )
        return response

    def delete(self, template_id: str) -> bool:
        """Delete a template.

        Args:
            template_id: The ID of the template to delete.

        Returns:
            bool: True if deletion was successful.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        return self._make_request(
            method="DELETE",
            endpoint=f"/api/v1/public/template/{template_id}",
            response_model=DeleteResponse,
            expected_status=204,
        )

    def publish(self, template_id: str) -> Template:
        """Publish a template.

        Args:
            template_id: The ID of the template to publish.

        Returns:
            Template: A Template model representing the published template.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        response = self._make_request(
            method="PATCH",
            endpoint=f"/api/v1/public/template/{template_id}/publish",
            response_model=PublishTemplateResponse,
        )
        return response

    # ---------------------------------------------------------------------
    # Channel-template helpers (deprecated wrappers)
    # ---------------------------------------------------------------------

    def create_channel_templates(
        self, template_id: str, **channel_templates_data
    ) -> list[ChannelTemplate]:
        """DEPRECATED – use :pyattr:`siren.SirenClient.channel_template.create`.

        This thin wrapper delegates to an internal ``ChannelTemplateClient`` to
        preserve backwards-compatibility while avoiding code duplication.
        """
        return self._channel_template_client.create(
            template_id, **channel_templates_data
        )

    def get_channel_templates(
        self,
        version_id: str,
        channel: str | None = None,
        search: str | None = None,
        sort: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> list[ChannelTemplate]:
        """DEPRECATED – use ``ChannelTemplateClient.get`` instead."""
        return self._channel_template_client.get(
            version_id,
            channel=channel,
            search=search,
            sort=sort,
            page=page,
            size=size,
        )
