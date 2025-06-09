"""Siren API client implementation."""

from typing import Any, Dict, List, Optional

from .messaging import MessagingManager
from .templates import TemplatesManager
from .users import UsersManager
from .webhooks import WebhookManager
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
        self._webhooks = WebhookManager(
            api_key=self.api_key, base_url=self.BASE_API_URL
        )
        self._messaging = MessagingManager(
            api_key=self.api_key, base_url=self.BASE_API_URL
        )
        self._users = UsersManager(api_key=self.api_key, base_url=self.BASE_API_URL)

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

    def schedule_workflow(
        self,
        name: str,
        schedule_time: str,
        timezone_id: str,
        start_date: str,
        workflow_type: str,
        workflow_id: str,
        input_data: Dict[str, Any],
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Schedules a workflow execution.

        Args:
            name: Name of the schedule.
            schedule_time: Time for the schedule in "HH:MM:SS" format.
            timezone_id: Timezone ID (e.g., "Asia/Kolkata").
            start_date: Start date for the schedule in "YYYY-MM-DD" format.
            workflow_type: Type of schedule (e.g., "ONCE", "DAILY").
            workflow_id: ID of the workflow to schedule.
            input_data: Input data for the workflow.
            end_date: Optional end date for the schedule in "YYYY-MM-DD" format.
        """
        return self._workflows.schedule_workflow(
            name=name,
            schedule_time=schedule_time,
            timezone_id=timezone_id,
            start_date=start_date,
            workflow_type=workflow_type,
            workflow_id=workflow_id,
            input_data=input_data,
            end_date=end_date,
        )

    def add_user(
        self,
        unique_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        reference_id: Optional[str] = None,
        whatsapp: Optional[str] = None,
        active_channels: Optional[List[str]] = None,
        active: Optional[bool] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Creates or updates a user.

        Args:
            unique_id: The unique identifier for the user.
            first_name: The user's first name.
            last_name: The user's last name.
            reference_id: An external reference ID for the user.
            whatsapp: The user's WhatsApp number.
            active_channels: A list of channels the user is active on (e.g., ["SLACK", "EMAIL"]).
            active: Boolean indicating if the user is active.
            email: The user's email address.
            phone: The user's phone number.
            attributes: A dictionary of additional custom attributes for the user.

        Returns:
            A dictionary containing the API response.
        """
        return self._users.add_user(
            unique_id=unique_id,
            first_name=first_name,
            last_name=last_name,
            reference_id=reference_id,
            whatsapp=whatsapp,
            active_channels=active_channels,
            active=active,
            email=email,
            phone=phone,
            attributes=attributes,
        )

    def send_message(
        self,
        template_name: str,
        channel: str,
        recipient_type: str,
        recipient_value: str,
        template_variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Send a message using a specific template.

        Args:
            template_name: The name of the template to use.
            channel: The channel to send the message through (e.g., "SLACK", "EMAIL").
            recipient_type: The type of recipient (e.g., "direct").
            recipient_value: The identifier for the recipient (e.g., Slack user ID, email address).
            template_variables: A dictionary of variables to populate the template.

        Returns:
            A dictionary containing the API response.
        """
        return self._messaging.send_message(
            template_name=template_name,
            channel=channel,
            recipient_type=recipient_type,
            recipient_value=recipient_value,
            template_variables=template_variables,
        )

    def get_replies(self, message_id: str) -> Dict[str, Any]:
        """
        Retrieve replies for a specific message ID.

        Args:
            message_id: The ID of the message for which to retrieve replies.

        Returns:
            A dictionary containing the API response with replies.
        """
        return self._messaging.get_replies(message_id=message_id)

    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """
        Retrieve the status of a specific message.

        Args:
            message_id: The ID of the message for which to retrieve the status.

        Returns:
            A dictionary containing the API response with the message status.
        """
        return self._messaging.get_message_status(message_id=message_id)

    # Webhook Management

    def configure_notifications_webhook(self, url: str) -> Dict[str, Any]:
        """
        Configure the webhook for outgoing notifications.

        Args:
            url: The URL to be configured for the notifications webhook.

        Returns:
            A dictionary containing the API response.
        """
        return self._webhooks.configure_notifications_webhook(url=url)

    def configure_inbound_message_webhook(self, url: str) -> Dict[str, Any]:
        """
        Configure the webhook for inbound messages.

        Args:
            url: The URL to be configured for the inbound message webhook.

        Returns:
            A dictionary containing the API response.
        """
        return self._webhooks.configure_inbound_message_webhook(url=url)
