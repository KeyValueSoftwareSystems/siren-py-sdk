# examples/users.py
"""Example script demonstrating user management methods in the Siren SDK."""

import os
import sys

from siren.client import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError

# Allow running from examples directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def add_user_example(client: SirenClient) -> None:
    """Example of adding a user."""
    user = {
        "unique_id": "john_doe_008",
        "last_name": "Doe",
        "email": "john.doe@company.com",
        "active_channels": ["EMAIL", "SMS"],
        "active": True,
    }

    try:
        created_user = client.add_user(**user)
        print(f"Created user: {created_user.id}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def update_user_example(client: SirenClient) -> None:
    """Example of updating a user."""
    try:
        updated_user = client.update_user(
            "john_doe_008",
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


def delete_user_example(client: SirenClient) -> None:
    """Example of deleting a user."""
    try:
        deleted = client.delete_user("123")
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

    # add_user_example(client)
    # update_user_example(client)
    delete_user_example(client)
