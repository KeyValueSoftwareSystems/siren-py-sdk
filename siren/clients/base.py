"""Base client class for all Siren API clients."""

from typing import Any, Dict, Optional, Type, Union

import requests
from pydantic import BaseModel, ValidationError

from ..exceptions import SirenAPIError, SirenSDKError


class BaseClient:
    """Base class for all API clients with common HTTP handling."""

    def __init__(self, api_key: str, base_url: str, timeout: int = 10):
        """Initialize the BaseClient.

        Args:
            api_key: The API key for authentication.
            base_url: The base URL for the Siren API.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

    def _parse_json_response(self, response: requests.Response) -> dict:
        """Parse JSON response and handle parsing errors.

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

    def _make_request(  # noqa: C901
        self,
        method: str,
        endpoint: str,
        request_model: Optional[Type[BaseModel]] = None,
        response_model: Optional[Type[BaseModel]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        expected_status: int = 200,
    ) -> Union[BaseModel, bool]:
        """Make HTTP request with complete error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            endpoint: API endpoint (e.g., "/api/v1/public/users").
            request_model: Pydantic model for request validation.
            response_model: Pydantic model for response parsing.
            data: Raw data to validate and send.
            params: Query parameters for GET requests.
            expected_status: Expected HTTP status code.

        Returns:
            Parsed response data or True for successful operations.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        # Validate request data first (outside main try block)
        json_data = None
        if data and request_model:
            try:
                validated_request = request_model.model_validate(data)
                json_data = validated_request.model_dump(
                    by_alias=True, exclude_none=True
                )
            except ValidationError as e:
                raise SirenSDKError(f"Invalid parameters: {e}", original_exception=e)

        try:
            # Prepare headers
            if json_data:
                headers["Content-Type"] = "application/json"

            # Make HTTP request
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                params=params,
                timeout=self.timeout,
            )

            # Handle success cases
            if response.status_code == expected_status:
                if expected_status == 204:  # No Content
                    return True

                if response_model:
                    response_json = self._parse_json_response(response)
                    parsed_response = response_model.model_validate(response_json)
                    if (
                        hasattr(parsed_response, "data")
                        and parsed_response.data is not None
                    ):
                        return parsed_response.data

            # Handle error cases
            response_json = self._parse_json_response(response)
            # Try to parse as structured error response
            if response_model:
                try:
                    parsed_response = response_model.model_validate(response_json)
                    if (
                        hasattr(parsed_response, "error_detail")
                        and parsed_response.error_detail
                    ):
                        raise SirenAPIError(
                            error_detail=parsed_response.error_detail,
                            status_code=response.status_code,
                            raw_response=response_json,
                        )
                except ValidationError:
                    pass  # Fall through to generic error

            # Generic error for unexpected responses
            raise SirenSDKError(
                message=f"Unexpected API response. Status: {response.status_code}",
                status_code=response.status_code,
                raw_response=response_json,
            )

        except requests.exceptions.RequestException as e:
            raise SirenSDKError(
                f"Network or connection error: {e}", original_exception=e
            )
        except (SirenAPIError, SirenSDKError):
            # Let our custom exceptions bubble up unchanged
            raise
        except Exception as e:
            # Catch any other exceptions (e.g., JSON parsing errors)
            raise SirenSDKError(f"Unexpected error: {e}", original_exception=e)
