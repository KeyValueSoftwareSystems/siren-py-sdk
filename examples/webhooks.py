"""Examples for configuring webhooks using the Siren SDK."""

import os
import sys

from dotenv import load_dotenv

from siren import SirenClient


def configure_notifications_webhook_example(client: SirenClient, webhook_url: str):
    """Demonstrates configuring the notifications webhook."""
    print("\nAttempting to configure notifications webhook...")
    try:
        print(f"Configuring notifications webhook URL to: {webhook_url}")
        response = client.configure_notifications_webhook(url=webhook_url)
        print("Configure notifications webhook API response:")
        print(response)

        if response and response.get("data") and response["data"].get("id"):
            print(
                f"Successfully configured notifications webhook. ID: {response['data']['id']}"
            )
            if response["data"].get("webhookConfig"):
                print(f"Configured URL: {response['data']['webhookConfig'].get('url')}")
                print(
                    f"Verification Key: {response['data']['webhookConfig'].get('verificationKey')}"
                )
        elif response and response.get("error"):
            print(
                f"Failed to configure notifications webhook. Error: {response['error']}"
            )
        else:
            print("Received an unexpected response structure.")

    except Exception as e:
        print(f"An error occurred: {e}")


def configure_inbound_message_webhook_example(client: SirenClient, webhook_url: str):
    """Demonstrates configuring the inbound message webhook."""
    print("\nAttempting to configure inbound message webhook...")
    try:
        print(f"Configuring inbound message webhook URL to: {webhook_url}")
        response = client.configure_inbound_message_webhook(url=webhook_url)
        print("Configure inbound message webhook API response:")
        print(response)

        if response and response.get("data") and response["data"].get("id"):
            print(
                f"Successfully configured inbound message webhook. ID: {response['data']['id']}"
            )
            if response["data"].get("inboundWebhookConfig"):
                print(
                    f"Configured URL: {response['data']['inboundWebhookConfig'].get('url')}"
                )
                print(
                    f"Verification Key: {response['data']['inboundWebhookConfig'].get('verificationKey')}"
                )
        elif response and response.get("error"):
            print(
                f"Failed to configure inbound message webhook. Error: {response['error']}"
            )
        else:
            print("Received an unexpected response structure.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY not found in environment variables or .env file.")
        print("Please set it to run the example.")
        sys.exit(1)

    siren_client = SirenClient(api_key=api_key)

    # IMPORTANT: Replace with your desired webhook URL
    example_webhook_url = "https://siren-ai-test.example.com/siren"

    configure_notifications_webhook_example(siren_client, example_webhook_url)
    configure_inbound_message_webhook_example(siren_client, example_webhook_url)
