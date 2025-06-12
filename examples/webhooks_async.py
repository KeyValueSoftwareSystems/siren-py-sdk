"""Asynchronous usage example: configuring webhooks with Siren SDK."""

import asyncio
import os

from dotenv import load_dotenv

from siren.async_client import AsyncSirenClient
from siren.exceptions import SirenAPIError, SirenSDKError


async def main() -> None:
    """Run a simple webhook configuration flow."""
    load_dotenv()

    api_key = os.getenv("SIREN_API_KEY")

    client = AsyncSirenClient(api_key=api_key, env=os.getenv("SIREN_ENV", "dev"))

    try:
        # Configure notifications webhook
        config = await client.webhook.configure_notifications(
            url="https://example.com/async_notify"
        )
        print("Notifications webhook set:", config.url)

        # Configure inbound-message webhook
        inbound_config = await client.webhook.configure_inbound(
            url="https://example.com/async_inbound"
        )
        print("Inbound webhook set:", inbound_config.url)
    except SirenAPIError as e:
        print(f"API error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK error: {e.message}")

    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
