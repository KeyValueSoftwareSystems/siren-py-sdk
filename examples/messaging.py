"""Examples for using the messaging client."""

from dotenv import load_dotenv

from siren import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError
from siren.models.messaging import ProviderCode


def send_direct_message_example(client: SirenClient) -> str:
    """Example of sending a direct message to a Slack user."""
    try:
        message_id = client.message.send(
            recipient_type="direct",
            recipient_value="U01UBCD06BB",
            channel="SLACK",
            body="Hello! This is a direct message without template.",
            provider_name="slack",  # Optional, if not provided, the default provider will be used
            provider_code=ProviderCode.SLACK,  # Optional, if not provided, the default provider will be used
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


def send_template_message_example(client: SirenClient) -> str:
    """Example of sending a message using a template."""
    try:
        message_id = client.message.send(
            recipient_type="direct",
            recipient_value="U01UBCD06BB",
            channel="SLACK",
            template_name="sampleTemplate",
            template_variables={"user_name": "Alan"},
            provider_name="slack",  # Optional, if not provided, the default provider will be used
            provider_code=ProviderCode.SLACK,  # Optional, if not provided, the default provider will be used
        )
        print(f"Message sent: {message_id}")
        return message_id
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
    load_dotenv()
    # Set environment variables: SIREN_API_KEY & SIREN_ENV (or pass as arguments)
    client = SirenClient()

    # Send direct message and check status
    message_id = send_direct_message_example(client)
    if message_id:
        get_message_status_example(client, message_id)

    # Send template message and get replies
    message_id = send_template_message_example(client)
    if message_id:
        get_replies_example(client, message_id)
