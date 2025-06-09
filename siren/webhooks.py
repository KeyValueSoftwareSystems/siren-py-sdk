"""Manages webhook-related API interactions for the Siren SDK."""

from typing import Any, Dict

import requests


class WebhookManager:
    """Manages webhook configuration operations."""

    def __init__(self, api_key: str, base_url: str):
        """
        Initialize the WebhookManager.

        Args:
            api_key: The API key for authentication.
            base_url: The base URL of the Siren API.
        """
        self.api_key = api_key
        self.base_url = f"{base_url}/api/v1/public"

    def _make_put_request(
        self, endpoint: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Helper function to make PUT requests and handle common logic."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        try:
            response = requests.put(endpoint, headers=headers, json=payload, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                raise http_err
        except requests.exceptions.RequestException as req_err:
            raise req_err

    def configure_notifications_webhook(self, url: str) -> Dict[str, Any]:
        """
        Configure the webhook for notifications.

        Args:
            url: The URL to be configured for the notifications webhook.

        Returns:
            A dictionary containing the API response.
        """
        endpoint = f"{self.base_url}/webhooks"
        payload = {"webhookConfig": {"url": url}}
        return self._make_put_request(endpoint, payload)

    def configure_inbound_message_webhook(self, url: str) -> Dict[str, Any]:
        """
        Configure the webhook for inbound messages.

        Args:
            url: The URL to be configured for the inbound message webhook.

        Returns:
            A dictionary containing the API response.
        """
        endpoint = f"{self.base_url}/webhooks"
        payload = {"inboundWebhookConfig": {"url": url}}
        return self._make_put_request(endpoint, payload)
