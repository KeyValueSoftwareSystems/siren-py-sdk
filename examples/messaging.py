"""Example script demonstrating messaging methods in the Siren SDK."""

import os
import sys

from siren.client import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError

# Allow running from examples directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def send_message_example(client: SirenClient) -> str:
    """Example of sending a message."""
    try:
        message_id = client.message.send(
            template_name="sampleTemplate",
            channel="SLACK",
            recipient_type="direct",
            recipient_value="U01UBCD06BB",
            template_variables={"user_name": "John"},
        )
        print(f"Message sent: {message_id}")
        return message_id
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def get_message_status_example(client: SirenClient, message_id: str) -> None:
    """Example of getting message status."""
    try:
        status = client.message.get_status(message_id=message_id)
        print(f"Message status: {status}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def get_replies_example(client: SirenClient, message_id: str) -> None:
    """Example of getting message replies."""
    try:
        replies = client.message.get_replies(message_id=message_id)
        print(f"Found {len(replies)} replies:")
        for i, reply in enumerate(replies):
            print(f"  Reply {i + 1}: {reply.text} (User: {reply.user})")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


if __name__ == "__main__":
    # Set environment variables: SIREN_API_KEY & SIREN_ENV (or pass as arguments)
    client = SirenClient()

    message_id = send_message_example(client)
    if message_id:
        get_message_status_example(client, message_id)
        get_replies_example(client, message_id)
