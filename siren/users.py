"""Manages user-related operations for the Siren API client."""

from typing import Any, Dict, List, Optional

import requests


class UsersManager:
    """Manages user-related operations for the Siren API."""

    def __init__(self, api_key: str, base_url: str):
        """
        Initializes the UsersManager.

        Args:
            api_key: The API key for authentication.
            base_url: The base URL for the Siren API.
        """
        self.api_key = api_key
        self.base_url = base_url

    def add_user(  # noqa: C901
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

        Raises:
            requests.exceptions.HTTPError: If the API returns an HTTP error status.
            requests.exceptions.RequestException: For other request-related errors.
        """
        url = f"{self.base_url}/api/v1/public/users"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {"uniqueId": unique_id}

        if first_name is not None:
            payload["firstName"] = first_name
        if last_name is not None:
            payload["lastName"] = last_name
        if reference_id is not None:
            payload["referenceId"] = reference_id
        if whatsapp is not None:
            payload["whatsapp"] = whatsapp
        if active_channels is not None:
            payload["activeChannels"] = active_channels
        if active is not None:
            payload["active"] = active
        if email is not None:
            payload["email"] = email
        if phone is not None:
            payload["phone"] = phone
        if attributes is not None:
            payload["attributes"] = attributes

        final_payload = {
            k: v for k, v in payload.items() if v is not None or k == "uniqueId"
        }

        try:
            response = requests.post(
                url, headers=headers, json=final_payload, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                # Attempt to parse JSON error response from API
                error_json = http_err.response.json()
                return error_json
            except requests.exceptions.JSONDecodeError:
                # If error response is not JSON, re-raise the original HTTPError
                raise http_err
        except requests.exceptions.RequestException as req_err:
            raise req_err
