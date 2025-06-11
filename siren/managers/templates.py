"""New templates manager using BaseManager architecture."""

from typing import List, Optional

from ..models.base import DeleteResponse
from ..models.templates import (
    ChannelTemplate,
    CreateChannelTemplatesRequest,
    CreateChannelTemplatesResponse,
    CreatedTemplate,
    CreateTemplateRequest,
    CreateTemplateResponse,
    GetChannelTemplatesResponse,
    PublishTemplateResponse,
    Template,
    TemplateListResponse,
    UpdateTemplateRequest,
    UpdateTemplateResponse,
)
from .base import BaseManager


class TemplatesManager(BaseManager):
    """Manager for template operations using BaseManager."""

    def get_templates(
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

    def update_template(self, template_id: str, **template_data) -> Template:
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

    def create_template(self, **template_data) -> CreatedTemplate:
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

    def delete_template(self, template_id: str) -> bool:
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

    def publish_template(self, template_id: str) -> Template:
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

    def create_channel_templates(
        self, template_id: str, **channel_templates_data
    ) -> List[ChannelTemplate]:
        """Create or update channel templates for a specific template.

        Args:
            template_id: The ID of the template for which to create channel templates.
            **channel_templates_data: Channel templates configuration where keys are
                                    channel names (e.g., "EMAIL", "SMS") and values
                                    are the channel-specific template objects.

        Returns:
            List[ChannelTemplate]: List of created channel template objects.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        response = self._make_request(
            method="POST",
            endpoint=f"/api/v1/public/template/{template_id}/channel-templates",
            request_model=CreateChannelTemplatesRequest,
            response_model=CreateChannelTemplatesResponse,
            data=channel_templates_data,
        )
        return response

    def get_channel_templates(
        self,
        version_id: str,
        channel: Optional[str] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> List[ChannelTemplate]:
        """Fetch channel templates for a specific template version.

        Args:
            version_id: The ID of the template version for which to fetch channel templates.
            channel: Filter by channel type (e.g., "EMAIL", "SMS").
            search: Search term to filter channel templates.
            sort: Sort by field.
            page: Page number.
            size: Page size.

        Returns:
            List[ChannelTemplate]: List of channel template objects.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        params = {}
        if channel is not None:
            params["channel"] = channel
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
            endpoint=f"/api/v1/public/template/versions/{version_id}/channel-templates",
            response_model=GetChannelTemplatesResponse,
            params=params,
        )
        return response
