"""Manages messaging-related API interactions for the Siren SDK."""

from typing import Any, Dict, Optional

import requests


class MessagingManager:
    """Manages direct message sending operations."""

    def __init__(self, api_key: str, base_url: str):
        """
        Initialize the MessagingManager.

        Args:
            api_key: The API key for authentication.
            base_url: The base URL of the Siren API.
        """
        self.api_key = api_key
        self.base_url = f"{base_url}/api/v1/public"

    def send_message(
        self,
        template_name: str,
        channel: str,
        recipient_type: str,
        recipient_value: str,
        template_variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Send a message using a specific template.

        Args:
            template_name: The name of the template to use.
            channel: The channel to send the message through (e.g., "SLACK", "EMAIL").
            recipient_type: The type of recipient (e.g., "direct").
            recipient_value: The identifier for the recipient (e.g., Slack user ID, email address).
            template_variables: A dictionary of variables to populate the template.

        Returns:
            A dictionary containing the API response.
        """
        endpoint = f"{self.base_url}/send-messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload: Dict[str, Any] = {
            "template": {"name": template_name},
            "recipient": {"type": recipient_type, "value": recipient_value},
            "channel": channel,
        }
        if template_variables is not None:
            payload["templateVariables"] = template_variables

        try:
            response = requests.post(
                endpoint, headers=headers, json=payload, timeout=10
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Try to return JSON error response from API if available
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                # If response is not JSON, re-raise the original HTTPError
                raise http_err
        except requests.exceptions.RequestException as req_err:
            # For other network errors (timeout, connection error, etc.)
            raise req_err

    def get_replies(self, message_id: str) -> Dict[str, Any]:
        """
        Retrieve replies for a specific message.

        Args:
            message_id: The ID of the message for which to retrieve replies.

        Returns:
            A dictionary containing the API response with replies.
        """
        endpoint = f"{self.base_url}/get-reply/{message_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Try to return JSON error response if available, otherwise re-raise
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                raise http_err
        except requests.exceptions.RequestException as req_err:
            # For network errors or other request issues
            raise req_err
