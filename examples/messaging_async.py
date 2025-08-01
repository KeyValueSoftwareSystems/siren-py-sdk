"""Asynchronous example: sending a message and fetching status & replies."""

import asyncio

from dotenv import load_dotenv

from siren.async_client import AsyncSirenClient
from siren.exceptions import SirenAPIError, SirenSDKError
from siren.models.messaging import ProviderCode


async def main() -> None:
    """Send message then query its status and replies."""
    load_dotenv()

    # Set environment variables: SIREN_API_KEY & SIREN_ENV (or pass as arguments)
    client = AsyncSirenClient()

    try:
        # Send message
        message_id = await client.message.send(
            template_name="sampleTemplate",
            channel="SLACK",
            recipient_value="U08FK1G6DGE",
            template_variables={"user_name": "John"},
            provider_name="slack-test-py-sdk",  
            provider_code=ProviderCode.SLACK,
        )
        print("Sent message id:", message_id)

        # Fetch status
        status = await client.message.get_status(message_id)
        print("Status:", status)

        # Fetch replies
        replies = await client.message.get_replies(message_id)
        print("Replies count:", len(replies))
    except SirenAPIError as e:
        print(f"API error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK error: {e.message}")

    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
