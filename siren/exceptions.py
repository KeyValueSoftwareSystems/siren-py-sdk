"""Custom exceptions for the Siren SDK."""

from typing import Any, Dict, Optional

from .models.base import APIErrorDetail


class SirenSDKError(Exception):
    """Base exception for all SDK-level errors."""

    def __init__(
        self,
        message: str,
        original_exception: Optional[Exception] = None,
        status_code: Optional[int] = None,
        raw_response: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the SDK error."""
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception
        self.status_code = status_code
        self.raw_response = raw_response

    def __str__(self) -> str:
        """Return string representation of the error."""
        return f"{self.__class__.__name__}: {self.message}"


class SirenAPIError(SirenSDKError):
    """Exception for API-level errors."""

    def __init__(
        self,
        error_detail: APIErrorDetail,
        status_code: int,
        raw_response: Dict[str, Any],
    ):
        """Initialize the API error."""
        self.error_detail = error_detail
        self.error_code = error_detail.error_code
        self.api_message = error_detail.message
        self.details = error_detail.details

        message = f"{self.error_code} - {self.api_message}"
        super().__init__(
            message=message,
            status_code=status_code,
            raw_response=raw_response,
        )

    def __str__(self) -> str:
        """Return string representation of the error."""
        return f"{self.__class__.__name__} (Status: {self.status_code}, Code: {self.error_code}): {self.api_message}"
