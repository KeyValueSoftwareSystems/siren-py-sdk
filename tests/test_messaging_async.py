"""Async tests for messaging client using respx."""

import httpx  # type: ignore
import pytest
import respx  # type: ignore

from siren.async_client import AsyncSirenClient
from siren.models.messaging import ReplyData

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"
MESSAGE_ID = "msg_123"


@respx.mock
@pytest.mark.asyncio
async def test_async_send_message_success():
    """send() returns message_id and correct payload."""
    client = AsyncSirenClient(api_key=API_KEY, env="dev")

    expected_json = {
        "data": {"notificationId": MESSAGE_ID},
        "error": None,
    }
    route = respx.post(f"{BASE_URL}/api/v1/public/send-messages").mock(
        return_value=httpx.Response(200, json=expected_json)
    )

    msg_id = await client.message.send(
        template_name="ai_summary",
        channel="EMAIL",
        recipient_value="user@example.com",
    )

    assert route.called
    assert msg_id == MESSAGE_ID

    await client.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_async_get_status_success():
    """get_status() retrieves delivered status."""
    client = AsyncSirenClient(api_key=API_KEY, env="dev")

    expected_json = {"data": {"status": "DELIVERED"}, "error": None}
    route = respx.get(f"{BASE_URL}/api/v1/public/message-status/{MESSAGE_ID}").mock(
        return_value=httpx.Response(200, json=expected_json)
    )

    status = await client.message.get_status(MESSAGE_ID)

    assert route.called
    assert status == "DELIVERED"

    await client.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_async_get_replies_success():
    """get_replies() returns parsed ReplyData list."""
    client = AsyncSirenClient(api_key=API_KEY, env="dev")

    expected_json = {
        "data": [
            {
                "text": "Thanks!",
                "threadTs": "111",
                "user": "U1",
                "ts": "111.1",
            }
        ],
        "error": None,
    }
    route = respx.get(f"{BASE_URL}/api/v1/public/get-reply/{MESSAGE_ID}").mock(
        return_value=httpx.Response(200, json=expected_json)
    )

    replies = await client.message.get_replies(MESSAGE_ID)

    assert route.called
    assert isinstance(replies, list)
    assert isinstance(replies[0], ReplyData)

    await client.aclose()
