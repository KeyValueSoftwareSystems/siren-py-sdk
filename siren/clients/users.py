"""User client for the Siren API."""

from ..models.base import DeleteResponse
from ..models.user import User, UserAPIResponse, UserRequest
from .base import BaseClient


class UserClient(BaseClient):
    """Client for user-related operations."""

    def add(self, **user_data) -> User:
        """Create a user.

        Args:
            **user_data: User attributes matching the UserRequest model fields.

        Returns:
            User: A User model representing the created user.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        return self._make_request(
            method="POST",
            endpoint="/api/v1/public/users",
            request_model=UserRequest,
            response_model=UserAPIResponse,
            data=user_data,
        )

    def update(self, unique_id: str, **user_data) -> User:
        """Update a user.

        Args:
            unique_id: The unique ID of the user to update.
            **user_data: User attributes matching the UserRequest model fields.

        Returns:
            User: A User model representing the updated user.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        user_data["unique_id"] = unique_id
        return self._make_request(
            method="PUT",
            endpoint=f"/api/v1/public/users/{unique_id}",
            request_model=UserRequest,
            response_model=UserAPIResponse,
            data=user_data,
        )

    def delete(self, unique_id: str) -> bool:
        """Delete a user.

        Args:
            unique_id: The unique ID of the user to delete.

        Returns:
            bool: True if the user was successfully deleted.

        Raises:
            SirenAPIError: If the API returns an error response.
            SirenSDKError: If there's an SDK-level issue (network, parsing, etc).
        """
        return self._make_request(
            method="DELETE",
            endpoint=f"/api/v1/public/users/{unique_id}",
            response_model=DeleteResponse,
            expected_status=204,
        )
