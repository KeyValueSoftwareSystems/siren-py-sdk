"""Utility functions for the Siren SDK."""

import requests

from .exceptions import SirenSDKError


def parse_json_response(response: requests.Response) -> dict:
    """
    Parse JSON response and handle parsing errors.

    Args:
        response: The HTTP response to parse.

    Returns:
        dict: The parsed JSON response.

    Raises:
        SirenSDKError: If the response is not valid JSON.
    """
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise SirenSDKError(
            f"API response was not valid JSON. Status: {response.status_code}. Content: {response.text}",
            original_exception=e,
            status_code=response.status_code,
        )
