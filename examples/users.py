# examples/users.py
"""Example script demonstrating the usage of the add_user method in the Siren SDK."""

import os
import sys

from siren.client import SirenClient

# It allows the script to be run directly from the examples directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def run_add_user_example(client: SirenClient):
    """Demonstrates adding a new user."""
    print("\n--- Running Add User Example ---")

    user_payload_1 = {
        "unique_id": "example_user_sdk_001",
        "first_name": "Alan",
        "last_name": "Watts",
        "email": "user.one.sdk@example.com",
        "phone": "+9198727",
        "whatsapp": "+9198727",
        "active_channels": ["EMAIL", "SMS", "WHATSAPP"],
        "active": True,
        "reference_id": "ext_ref_001_sdk",
        "attributes": {
            "department": "SDK Examples",
            "preferred_language": "en",
            "tags": ["sdk_test", "new_user"],
        },
    }
    try:
        print(f"\nAttempting to add/update user: {user_payload_1['unique_id']}")
        response = client.add_user(**user_payload_1)
        print("API Response for user 1:")
        print(response)
    except Exception as e:
        print(f"An unexpected error occurred for user 1: {e}")


if __name__ == "__main__":
    api_key = os.environ.get("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY environment variable not set.")
        sys.exit(1)

    siren_client = SirenClient(api_key=api_key)

    run_add_user_example(siren_client)
