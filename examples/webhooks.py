"""Examples for configuring webhooks using the Siren SDK."""

from dotenv import load_dotenv

from siren import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError


def configure_notifications_webhook_example(client: SirenClient, webhook_url: str):
    """Example of configuring the notifications webhook."""
    try:
        webhook_config = client.webhook.configure_notifications(url=webhook_url)
        print(
            f"Notifications webhook configured: {webhook_config.url} (key: {webhook_config.verification_key})"
        )
        return webhook_config
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def configure_inbound_message_webhook_example(client: SirenClient, webhook_url: str):
    """Example of configuring the inbound message webhook."""
    try:
        webhook_config = client.webhook.configure_inbound(url=webhook_url)
        print(
            f"Inbound webhook configured: {webhook_config.url} (key: {webhook_config.verification_key})"
        )
        return webhook_config
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


if __name__ == "__main__":
    load_dotenv()
    # Set environment variables: SIREN_API_KEY & SIREN_ENV (or pass as arguments)
    siren_client = SirenClient()

    example_webhook_url = "https://trysiren-test.example.com/siren123"

    configure_notifications_webhook_example(siren_client, example_webhook_url)
    configure_inbound_message_webhook_example(siren_client, example_webhook_url)
