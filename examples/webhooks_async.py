"""Asynchronous usage example: configuring webhooks with Siren SDK."""

import asyncio

from siren.async_client import AsyncSirenClient

API_KEY = "sk_example_key"


async def main() -> None:
    """Run a simple webhook configuration flow."""
    client = AsyncSirenClient(api_key=API_KEY, env="dev")

    # Configure notifications webhook
    config = await client.webhook.configure_notifications(
        url="https://example.com/notify"
    )
    print("Notifications webhook set:", config)

    # Configure inbound-message webhook
    inbound_config = await client.webhook.configure_inbound(
        url="https://example.com/inbound"
    )
    print("Inbound webhook set:", inbound_config)

    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
