# examples/users.py
"""Example script demonstrating user management methods in the Siren SDK."""

import os
import sys

from siren.client import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError

# Allow running from examples directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def add_user_example(client: SirenClient) -> str:
    """Example of adding a user."""
    user = {
        "unique_id": "john_doe_008",
        "last_name": "Doe",
        "email": "john.doe@company.com",
        "active_channels": ["EMAIL", "SMS"],
        "active": True,
    }

    try:
        created_user = client.user.add(**user)
        print(f"Created user: {created_user.id}")
        return created_user.unique_id
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def update_user_example(client: SirenClient, unique_id: str) -> None:
    """Example of updating a user."""
    try:
        updated_user = client.user.update(
            unique_id,
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@company.com",
            active_channels=["EMAIL", "SMS", "WHATSAPP"],
        )
        print(f"Updated user: {updated_user.id}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def delete_user_example(client: SirenClient, unique_id: str) -> None:
    """Example of deleting a user."""
    try:
        deleted = client.user.delete(unique_id)
        print(f"Deleted user: {deleted}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


if __name__ == "__main__":
    api_key = os.environ.get("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY environment variable not set.")
        sys.exit(1)

    client = SirenClient(api_key=api_key)

    unique_id = add_user_example(client)
    if unique_id:
        update_user_example(client, unique_id)
        # Uncomment to delete the user after testing
        delete_user_example(client, unique_id)
