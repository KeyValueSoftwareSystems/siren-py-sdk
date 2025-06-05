"""Siren API client implementation."""

from typing import Any, Dict, Optional

from .templates import TemplatesManager


class SirenClient:
    """Client for interacting with the Siren API."""

    # TODO: Implement logic to select API URL based on API key type (dev/prod) or environment variable
    BASE_API_URL = "https://api.dev.trysiren.io/api/v1/public"

    def __init__(self, api_key: str):
        """Initialize the SirenClient.

        Args:
            api_key: The API key for authentication.
        """
        self.api_key = api_key
        self._templates = TemplatesManager(
            api_key=self.api_key, base_url=self.BASE_API_URL
        )

    def get_templates(
        self,
        tag_names: Optional[str] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Fetch templates.

        Args:
            tag_names: Filter by tag names.
            search: Search by field.
            sort: Sort by field.
            page: Page number.
            size: Page size.

        Returns:
            A dictionary containing the API response.
        """
        return self._templates.get_templates(
            tag_names=tag_names,
            search=search,
            sort=sort,
            page=page,
            size=size,
        )

    def create_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new template.

        Args:
            template_data: A dictionary containing the template details.

        Returns:
            A dictionary containing the API response.
        """
        return self._templates.create_template(template_data=template_data)

    def update_template(
        self, template_id: str, template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing template.

        Args:
            template_id: The ID of the template to update.
            template_data: A dictionary containing the template details to update.

        Returns:
            A dictionary containing the API response.
        """
        return self._templates.update_template(
            template_id=template_id, template_data=template_data
        )

    def delete_template(self, template_id: str) -> Dict[str, Any]:
        """Delete an existing template.

        Args:
            template_id: The ID of the template to delete.

        Returns:
            A dictionary containing the API response.
        """
        return self._templates.delete_template(template_id=template_id)
