"""Channel template client for the Siren API."""

from typing import List, Optional

from ..models.templates import (
    ChannelTemplate,
    CreateChannelTemplatesRequest,
    CreateChannelTemplatesResponse,
    GetChannelTemplatesResponse,
)
from .base import BaseClient


class ChannelTemplateClient(BaseClient):
    """Client for channel template operations."""

    def create(
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

    def get(
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
