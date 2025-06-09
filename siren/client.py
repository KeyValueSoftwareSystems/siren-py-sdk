"""Siren API client implementation."""

from typing import Any, Dict, List, Optional

from .templates import TemplatesManager
from .workflows import WorkflowsManager


class SirenClient:
    """Client for interacting with the Siren API."""

    # TODO: Implement logic to select API URL based on API key type (dev/prod) or environment variable
    BASE_API_URL = "https://api.dev.trysiren.io"  # General base URL

    def __init__(self, api_key: str):
        """Initialize the SirenClient.

        Args:
            api_key: The API key for authentication.
        """
        self.api_key = api_key
        self._templates = TemplatesManager(
            api_key=self.api_key, base_url=self.BASE_API_URL
        )
        self._workflows = WorkflowsManager(
            api_key=self.api_key,
            base_url=self.BASE_API_URL,  # Note: WorkflowsManager uses /api/v2 internally
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

    def publish_template(self, template_id: str) -> Dict[str, Any]:
        """Publish an existing template.

        Args:
            template_id: The ID of the template to publish.

        Returns:
            A dictionary containing the API response.
        """
        return self._templates.publish_template(template_id=template_id)

    def create_channel_templates(
        self,
        template_id: str,
        channel_templates: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create or update channel templates for a specific template.

        Args:
            template_id: The ID of the template for which to create channel templates.
            channel_templates: A dictionary where keys are channel names (e.g., "EMAIL", "SMS")
                             and values are the channel-specific template objects.

        Returns:
            A dictionary containing the API response.
        """
        return self._templates.create_channel_templates(
            template_id=template_id, channel_templates=channel_templates
        )

    def get_channel_templates(
        self,
        version_id: str,
        channel: Optional[str] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get channel templates for a specific template version.

        Args:
            version_id: The ID of the template version for which to fetch channel templates.
            channel: Filter by channel type (e.g., "EMAIL", "SMS").
            search: Search by field.
            sort: Sort by field.
            page: Page number.
            size: Page size.

        Returns:
            A dictionary containing the API response.
        """
        return self._templates.get_channel_templates(
            version_id=version_id,
            channel=channel,
            search=search,
            sort=sort,
            page=page,
            size=size,
        )

    def trigger_workflow(
        self,
        workflow_name: str,
        data: Optional[Dict[str, Any]] = None,
        notify: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Triggers a workflow with the given name and payload.

        Args:
            workflow_name: The name of the workflow to execute.
            data: Common data for all workflow executions.
            notify: Specific data for this workflow execution.

        Returns:
            A dictionary containing the API response.
        """
        return self._workflows.trigger_workflow(
            workflow_name=workflow_name, data=data, notify=notify
        )

    def trigger_bulk_workflow(
        self,
        workflow_name: str,
        notify: List[Dict[str, Any]],
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Triggers a workflow in bulk for multiple recipients/notifications.

        Args:
            workflow_name: The name of the workflow to execute.
            notify: A list of notification objects, each representing specific data
                    for a workflow execution.
            data: Common data that will be used across all workflow executions.

        Returns:
            A dictionary containing the API response.
        """
        return self._workflows.trigger_bulk_workflow(
            workflow_name=workflow_name, notify=notify, data=data
        )
