"""Asynchronous example: add, update, delete user."""

import asyncio
import os

from dotenv import load_dotenv

from siren.async_client import AsyncSirenClient
from siren.exceptions import SirenAPIError, SirenSDKError


async def main() -> None:
    """Add, update, delete a user asynchronously."""
    load_dotenv()
    api_key = os.getenv("SIREN_API_KEY")

    client = AsyncSirenClient(api_key=api_key, env=os.getenv("SIREN_ENV", "dev"))

    try:
        # Add user
        user = await client.user.add(
            unique_id="john_doe_008",
            last_name="Doe",
            email="john.doe@company.com",
            active_channels=["EMAIL", "SMS"],
            active=True,
        )
        print("Created user:", user.id)

        # Update user
        updated = await client.user.update(
            "john_doe_008",
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@company.com",
            active_channels=["EMAIL", "SMS", "WHATSAPP"],
        )
        print("Updated user:", updated.id)

        # Delete user
        deleted = await client.user.delete("john_doe_008")
        print("Deleted user:", deleted)
    except SirenAPIError as e:
        print(f"API error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK error: {e.message}")

    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
