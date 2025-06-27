"""Asynchronous User client for Siren SDK."""

from typing import Any

from ..models.base import DeleteResponse
from ..models.user import User, UserAPIResponse, UserRequest
from .async_base import AsyncBaseClient


class AsyncUserClient(AsyncBaseClient):
    """Non-blocking user operations (add, update, delete)."""

    async def add(self, **user_data: Any) -> User:
        """Create a user and return the resulting object."""
        response = await self._make_request(
            method="POST",
            endpoint="/api/v1/public/users",
            request_model=UserRequest,
            response_model=UserAPIResponse,
            data=user_data,
        )
        return response  # type: ignore[return-value]

    async def update(self, unique_id: str, **user_data: Any) -> User:
        """Update user identified by unique_id."""
        user_data["unique_id"] = unique_id
        response = await self._make_request(
            method="PUT",
            endpoint=f"/api/v1/public/users/{unique_id}",
            request_model=UserRequest,
            response_model=UserAPIResponse,
            data=user_data,
        )
        return response  # type: ignore[return-value]

    async def delete(self, unique_id: str) -> bool:
        """Delete user and return True on success."""
        await self._make_request(
            method="DELETE",
            endpoint=f"/api/v1/public/users/{unique_id}",
            response_model=DeleteResponse,
            expected_status=204,
        )
        return True
