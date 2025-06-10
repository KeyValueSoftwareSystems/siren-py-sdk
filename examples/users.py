# examples/users.py
"""Example script demonstrating the usage of the add_user method in the Siren SDK."""

import os
import sys

from siren.client import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError

# Allow running from examples directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def add_user_example(client: SirenClient) -> None:
    """Example of adding a user using the Siren SDK."""
    # Example user payload
    user = {
        "unique_id": "john_doe_003",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@company.com",
        "phone": "+919876543210",
        "whatsapp": "+919876543210",
        "active_channels": ["EMAIL", "SMS", "WHATSAPP"],
        "active": True,
        "reference_id": "EMP_001",
        "attributes": {
            "department": "Engineering",
            "role": "Senior Developer",
            "location": "Bangalore",
            "preferred_language": "en",
        },
    }

    try:
        # Call the SDK method
        created_user = client.add_user(**user)
        print(f"User ID: {created_user.id}")

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
    add_user_example(client)
