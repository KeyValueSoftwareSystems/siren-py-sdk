"""Manages user-related operations for the Siren API client."""

import requests
from pydantic import ValidationError

from .exceptions import SirenAPIError, SirenSDKError
from .models.user import User, UserAPIResponse, UserRequest
from .utils import parse_json_response


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
        # TODO: Make timeout configurable through client initialization
        self.timeout = 10

    def add_user(self, **user_data) -> User:
        """
        Creates a user.

        Args:
            **user_data: User attributes matching the UserRequest model fields.
                       Use snake_case for field names (e.g., first_name, unique_id).

        Returns:
            User: A User model representing the created/updated user.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        url = f"{self.base_url}/api/v1/public/users"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            # Prepare the request with Pydantic validation
            user_request = UserRequest.model_validate(user_data)
            payload = user_request.model_dump(by_alias=True, exclude_none=True)

            # Make API request
            response = requests.post(
                url, headers=headers, json=payload, timeout=self.timeout
            )
            response_json = parse_json_response(response)

            # Parse the response
            parsed_response = UserAPIResponse.model_validate(response_json)

            # Handle success case (200 OK)
            if response.status_code == 200 and parsed_response.data:
                return parsed_response.data

            # Handle API error
            # API error response structure:
            # {
            #     "data": null,
            #     "error": { "errorCode": "...", "message": "..." },
            #     "errors": [{ "errorCode": "...", "message": "..." }],
            #     "meta": null
            # }
            # Status codes:
            # 200 - OK
            # 400 - BAD REQUEST
            # 401 - UNAUTHORISED
            # 404 - NOT FOUND
            if response.status_code in (400, 401, 404):
                error_detail = parsed_response.error_detail
                if error_detail:
                    raise SirenAPIError(
                        error_detail=error_detail,
                        status_code=response.status_code,
                        raw_response=response_json,
                    )

            # Fallback error for unexpected status codes
            raise SirenSDKError(
                message=f"Unexpected API response. Status: {response.status_code}",
                status_code=response.status_code,
                raw_response=response_json,
            )

        except ValidationError as e:
            # Input validation error
            raise SirenSDKError(f"Invalid parameters: {e}", original_exception=e)

        except requests.exceptions.RequestException as e:
            # Network or connection error
            raise SirenSDKError(
                f"Network or connection error: {e}", original_exception=e
            )

    def update_user(self, unique_id: str, **user_data) -> User:
        """
        Updates a user.

        Args:
            unique_id: The unique ID of the user to update.
            **user_data: User attributes matching the UserRequest model fields.

        Returns:
            User: A User model representing the updated user.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        url = f"{self.base_url}/api/v1/public/users/{unique_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            # Add unique_id to the payload
            user_data["unique_id"] = unique_id

            # Prepare the request with Pydantic validation
            user_request = UserRequest.model_validate(user_data)
            payload = user_request.model_dump(by_alias=True, exclude_none=True)

            # Make API request
            response = requests.put(
                url, headers=headers, json=payload, timeout=self.timeout
            )
            response_json = parse_json_response(response)

            # Parse the response
            parsed_response = UserAPIResponse.model_validate(response_json)

            # Handle success case (200 OK)
            if response.status_code == 200 and parsed_response.data:
                return parsed_response.data

            # Handle API error
            if response.status_code in (400, 401, 404):
                error_detail = parsed_response.error_detail
                if error_detail:
                    raise SirenAPIError(
                        error_detail=error_detail,
                        status_code=response.status_code,
                        raw_response=response_json,
                    )

            # Fallback error for unexpected status codes
            raise SirenSDKError(
                message=f"Unexpected API response. Status: {response.status_code}",
                status_code=response.status_code,
                raw_response=response_json,
            )

        except ValidationError as e:
            # Input validation error
            raise SirenSDKError(f"Invalid parameters: {e}", original_exception=e)

        except requests.exceptions.RequestException as e:
            # Network or connection error
            raise SirenSDKError(
                f"Network or connection error: {e}", original_exception=e
            )
