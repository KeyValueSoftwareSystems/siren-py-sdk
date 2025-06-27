"""Asynchronous BaseClient for Siren SDK.

Mirrors the synchronous ``BaseClient`` behaviour but utilises
:class:`siren.http.transport.AsyncTransport` for non-blocking HTTP calls.
"""

from __future__ import annotations

from typing import Any

import httpx  # type: ignore
from pydantic import BaseModel, ValidationError

from ..exceptions import SirenAPIError, SirenSDKError
from ..http.transport import AsyncTransport


class AsyncBaseClient:  # noqa: D101 – docstring provided at module level
    def __init__(self, api_key: str, base_url: str, timeout: int = 10):
        """Construct the asynchronous base client.

        Args:
            api_key: Bearer token for Siren API.
            base_url: Fully-qualified API root (e.g. ``https://api.trysiren.io``).
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key
        self.base_url = base_url
        self._transport = AsyncTransport(timeout=timeout)

    async def _parse_json_response(self, response: httpx.Response) -> dict:  # noqa: D401
        try:
            return response.json()
        except ValueError as e:
            # httpx raises ValueError for invalid JSON
            raise SirenSDKError(
                f"API response was not valid JSON. Status: {response.status_code}. Content: {response.text}",
                original_exception=e,
                status_code=response.status_code,
            )

    async def _make_request(  # noqa: C901
        self,
        method: str,
        endpoint: str,
        request_model: type[BaseModel] | None = None,
        response_model: type[BaseModel] | None = None,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        expected_status: int = 200,
    ) -> BaseModel | bool:
        url = f"{self.base_url}{endpoint}"
        headers: dict[str, str] = {"Authorization": f"Bearer {self.api_key}"}

        json_data = None
        if data and request_model:
            try:
                validated_request = request_model.model_validate(data)
                json_data = validated_request.model_dump(
                    by_alias=True, exclude_none=True
                )
            except ValidationError as e:
                raise SirenSDKError(f"Invalid parameters: {e}", original_exception=e)

        if json_data is not None:
            headers["Content-Type"] = "application/json"

        try:
            response = await self._transport.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                params=params,
            )

            # Success
            if response.status_code == expected_status:
                if expected_status == 204:
                    return True

                if response_model is not None:
                    response_json = await self._parse_json_response(response)
                    parsed = response_model.model_validate(response_json)
                    if hasattr(parsed, "data") and parsed.data is not None:
                        return parsed.data

            # Error handling
            response_json = await self._parse_json_response(response)
            if response_model is not None:
                try:
                    parsed = response_model.model_validate(response_json)
                    if getattr(parsed, "error_detail", None):
                        raise SirenAPIError(
                            error_detail=parsed.error_detail,
                            status_code=response.status_code,
                            raw_response=response_json,
                        )
                except ValidationError:
                    pass

            raise SirenSDKError(
                message=f"Unexpected API response. Status: {response.status_code}",
                status_code=response.status_code,
                raw_response=response_json,
            )

        except httpx.RequestError as e:
            raise SirenSDKError(
                f"Network or connection error: {e}", original_exception=e
            )
        except (SirenAPIError, SirenSDKError):
            raise
        except Exception as e:  # noqa: BLE001
            raise SirenSDKError(f"Unexpected error: {e}", original_exception=e)

    async def aclose(self) -> None:
        """Close underlying transport."""
        await self._transport.aclose()

    async def __aenter__(self) -> AsyncBaseClient:
        """Enter async context manager and return *self*."""
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        """Exit context manager, closing the underlying transport."""
        await self.aclose()
