"""Asynchronous example: sending a message and fetching status & replies."""

import asyncio
import os

from dotenv import load_dotenv

from siren.async_client import AsyncSirenClient
from siren.exceptions import SirenAPIError, SirenSDKError


async def main() -> None:
    """Send message then query its status and replies."""
    load_dotenv()
    api_key = os.getenv("SIREN_API_KEY")

    client = AsyncSirenClient(api_key=api_key, env=os.getenv("SIREN_ENV", "dev"))

    try:
        # Send message
        message_id = await client.message.send(
            template_name="sampleTemplate",
            channel="SLACK",
            recipient_type="direct",
            recipient_value="U01UBCD06BB",
            template_variables={"user_name": "John"},
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
