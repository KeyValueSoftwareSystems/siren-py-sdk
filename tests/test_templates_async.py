"""Async tests for template client."""

import httpx  # type: ignore
import pytest
import respx  # type: ignore

from siren.async_client import AsyncSirenClient
from siren.models.templates import CreatedTemplate

API_KEY = "test_api_key"
BASE_URL = "https://api.dev.trysiren.io"
TEMPLATE_ID = "tpl_123"
VERSION_ID = "ver_1"


@respx.mock
@pytest.mark.asyncio
async def test_async_create_template_success():
    """create() returns CreatedTemplate object with id."""
    client = AsyncSirenClient(api_key=API_KEY, env="dev")
    expected_json = {
        "data": {
            "templateId": TEMPLATE_ID,
            "templateName": "Welcome_Email_Example",
            "draftVersionId": "draft_1",
            "channelTemplateList": [],
        },
        "error": None,
    }
    route = respx.post(f"{BASE_URL}/api/v1/public/template").mock(
        return_value=httpx.Response(200, json=expected_json)
    )

    created = await client.template.create(name="Welcome_Email_Example")

    assert route.called
    assert isinstance(created, CreatedTemplate)
    assert created.template_id == TEMPLATE_ID

    await client.aclose()
