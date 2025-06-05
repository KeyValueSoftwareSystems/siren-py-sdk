"""Siren API client implementation."""

from typing import Any, Dict, Optional

import requests


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
        endpoint = f"{self.BASE_API_URL}/template"
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
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Attempt to return JSON error from response, otherwise re-raise HTTPError
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                raise http_err
        except requests.exceptions.RequestException as req_err:
            # For non-HTTP request issues (e.g., network, timeout)
            raise req_err
