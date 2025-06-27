"""Base models for the Siren SDK.

This module contains base models that are used across the SDK.
"""

from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIErrorDetail(BaseModel):
    """Represents the 'error' object in an API response."""

    error_code: str = Field(..., alias="errorCode", description="A unique error code.")
    message: str = Field(..., description="A human-readable error message.")
    details: Optional[Any] = Field(
        None, description="Optional additional error details - can be Dict or List."
    )


class BaseAPIResponse(BaseModel, Generic[T]):
    """Base model for all API responses.

    This model represents the common structure of API responses,
    including data, error, and metadata fields.

    Args:
        T: The type of data expected in the response.
    """

    data: Optional[T] = Field(None, description="Response data")
    error: Optional[APIErrorDetail] = Field(None, description="Error information")
    errors: Optional[list[APIErrorDetail]] = Field(None, description="List of errors")
    meta: Optional[Dict[str, Any]] = Field(
        None, description="Metadata about the response"
    )

    @property
    def error_detail(self) -> Optional[APIErrorDetail]:
        """Get the first available error detail from either error or errors field."""
        if self.error:
            return self.error
        if self.errors:
            return self.errors[0]
        return None


class DeleteResponse(BaseAPIResponse[None]):
    """Common response model for delete operations across the SDK.

    For successful deletions (204), data will be None.
    For errors, error/errors/meta fields will be populated.
    """

    pass
