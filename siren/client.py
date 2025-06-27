"""Siren API client implementation."""

import os
from typing import Literal, Optional

from .clients.channel_templates import ChannelTemplateClient
from .clients.messaging import MessageClient
from .clients.templates import TemplateClient
from .clients.users import UserClient
from .clients.webhooks import WebhookClient
from .clients.workflows import WorkflowClient


class SirenClient:
    """Client for interacting with the Siren API."""

    # Environment-specific API URLs
    API_URLS = {
        "dev": "https://api.dev.trysiren.io",
        "prod": "https://api.trysiren.io",
    }

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        env: Optional[Literal["dev", "prod"]] = None,
    ):
        """Initialize the SirenClient.

        Args:
            api_key: The API key for authentication. If not provided, will be read from SIREN_API_KEY environment variable.
            env: Environment to use ('dev' or 'prod'). If not provided, defaults to 'prod' or uses SIREN_ENV environment variable.
        """
        # Get API key from environment if not provided
        if api_key is None:
            api_key = os.getenv("SIREN_API_KEY")
        if api_key is None:
            raise ValueError(
                "The api_key must be set either by passing api_key to the client or by setting the SIREN_API_KEY environment variable"
            )
        self.api_key = api_key

        # Determine environment and base URL
        if env is None:
            env = os.getenv("SIREN_ENV", "prod")

        if env not in self.API_URLS:
            raise ValueError(
                f"Invalid environment '{env}'. Must be one of: {list(self.API_URLS.keys())}"
            )

        self.env = env
        self.base_url = self.API_URLS[env]

        # Initialize API clients
        self._template_client = TemplateClient(
            api_key=self.api_key, base_url=self.base_url
        )
        self._channel_template_client = ChannelTemplateClient(
            api_key=self.api_key, base_url=self.base_url
        )
        self._workflow_client = WorkflowClient(
            api_key=self.api_key, base_url=self.base_url
        )
        self._message_client = MessageClient(
            api_key=self.api_key, base_url=self.base_url
        )
        self._user_client = UserClient(api_key=self.api_key, base_url=self.base_url)
        self._webhook_client = WebhookClient(
            api_key=self.api_key, base_url=self.base_url
        )

    @property
    def template(self) -> TemplateClient:
        """Access to template operations."""
        return self._template_client

    @property
    def channel_template(self) -> ChannelTemplateClient:
        """Access to channel template operations."""
        return self._channel_template_client

    @property
    def workflow(self) -> WorkflowClient:
        """Access to workflow operations."""
        return self._workflow_client

    @property
    def message(self) -> MessageClient:
        """Access to message operations."""
        return self._message_client

    @property
    def user(self) -> UserClient:
        """Access to user operations."""
        return self._user_client

    @property
    def webhook(self) -> WebhookClient:
        """Access to webhook operations."""
        return self._webhook_client
