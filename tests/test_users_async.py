"""Async tests for user client."""

import httpx  # type: ignore
import pytest
import respx  # type: ignore

from siren.async_client import AsyncSirenClient
from siren.models.user import User

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"
UNIQUE_ID = "user_123"


@respx.mock
@pytest.mark.asyncio
async def test_async_add_user_success():
    """add() returns created User object."""
    client = AsyncSirenClient(api_key=API_KEY, env="dev")
    expected_json = {
        "data": {
            "id": "u1",
            "uniqueId": UNIQUE_ID,
        },
        "error": None,
    }
    route = respx.post(f"{BASE_URL}/api/v1/public/users").mock(
        return_value=httpx.Response(200, json=expected_json)
    )

    user = await client.user.add(unique_id=UNIQUE_ID)

    assert route.called
    assert isinstance(user, User)
    assert user.unique_id == UNIQUE_ID

    await client.aclose()
