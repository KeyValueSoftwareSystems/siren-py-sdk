"""Template management for the Siren SDK."""

from typing import Any, Dict, Optional

import requests


class TemplatesManager:
    """Manages template-related operations for the Siren API."""

    def __init__(self, api_key: str, base_url: str):
        """Initialize the TemplatesManager.

        Args:
            api_key: The API key for authentication.
            base_url: The base URL for the Siren API.
        """
        self.api_key = api_key
        self.base_url = base_url

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
        endpoint = f"{self.base_url}/template"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        params: Dict[str, Any] = {}
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

        try:
            response = requests.get(
                endpoint, headers=headers, params=params, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                raise http_err
        except requests.exceptions.RequestException as req_err:
            raise req_err

    def create_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new template.

        Args:
            template_data: A dictionary containing the template details.

        Returns:
            A dictionary containing the API response.
        """
        endpoint = f"{self.base_url}/template"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                endpoint, headers=headers, json=template_data, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                raise http_err
        except requests.exceptions.RequestException as req_err:
            raise req_err

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
        endpoint = f"{self.base_url}/template/{template_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            response = requests.put(
                endpoint, headers=headers, json=template_data, timeout=10
            )
            response.raise_for_status()  # Raises HTTPError for 4XX/5XX status codes
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Try to return the JSON error response from the API if available
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                # If the error response isn't JSON, re-raise the original HTTPError
                raise http_err
        except requests.exceptions.RequestException as req_err:
            # For other network issues (e.g., connection error)
            raise req_err

    def delete_template(self, template_id: str) -> Dict[str, Any]:
        """Delete an existing template.

        Args:
            template_id: The ID of the template to delete.

        Returns:
            A dictionary containing the API response (e.g., a confirmation message).
        """
        endpoint = f"{self.base_url}/template/{template_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        try:
            response = requests.delete(endpoint, headers=headers, timeout=10)
            response.raise_for_status()  # Raises HTTPError for 4XX/5XX status codes
            if response.status_code == 204:
                return {
                    "status": "success",
                    "message": f"Template {template_id} deleted successfully.",
                }
            # For other successful responses (e.g., 200 OK with a body, though not expected for DELETE here)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                raise http_err
        except requests.exceptions.RequestException as req_err:
            raise req_err

    def publish_template(self, template_id: str) -> Dict[str, Any]:
        """Publish an existing template.

        Args:
            template_id: The ID of the template to publish.

        Returns:
            A dictionary containing the API response.
        """
        endpoint = f"{self.base_url}/template/{template_id}/publish"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        try:
            response = requests.patch(endpoint, headers=headers, timeout=10)
            response.raise_for_status()  # Raises HTTPError for 4XX/5XX status codes
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                raise http_err
        except requests.exceptions.RequestException as req_err:
            raise req_err

    def create_channel_configurations(
        self, template_id: str, configurations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create or update channel configurations for a template.

        Args:
            template_id: The ID of the template.
            configurations: A dictionary containing the channel configurations.

        Example:
                            {
                                "SMS": {"body": "...", "channel": "SMS", ...},
                                "EMAIL": {"subject": "...", "body": "...", ...}
                            }

        Returns:
            A dictionary containing the API response.
        """
        endpoint = f"{self.base_url}/template/{template_id}/channel-templates"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                endpoint, headers=headers, json=configurations, timeout=10
            )
            response.raise_for_status()  # Raises HTTPError for 4XX/5XX status codes
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                raise http_err
        except requests.exceptions.RequestException as req_err:
            raise req_err

    def get_channel_templates(
        self,
        version_id: str,
        channel: Optional[str] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Fetch channel templates for a specific template version.

        Args:
            version_id: The ID of the template version.
            channel: Filter by channel type (e.g., "EMAIL", "SMS").
            search: Search by field.
            sort: Sort by field.
            page: Page number.
            size: Page size.

        Returns:
            A dictionary containing the API response.
        """
        endpoint = f"{self.base_url}/template/versions/{version_id}/channel-templates"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        params: Dict[str, Any] = {}
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

        try:
            response = requests.get(
                endpoint, headers=headers, params=params, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                # If the error response isn't JSON, re-raise the original HTTPError
                raise http_err
        except requests.exceptions.RequestException as req_err:
            # For other network issues (e.g., connection error)
            raise req_err
