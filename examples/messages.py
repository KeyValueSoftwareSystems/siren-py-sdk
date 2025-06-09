"""Example script to demonstrate sending messages using the Siren SDK."""

import os
import sys

from dotenv import load_dotenv

# Add the project root to the Python path
# This allows us to import the 'siren' package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from siren import SirenClient  # noqa: E402


def send_message_example(client: SirenClient):
    """Demonstrates sending a message using a template."""
    print("Attempting to send a message...")
    try:
        template_name = "sampleTemplate"
        channel = "SLACK"
        recipient_type = "direct"
        recipient_value = "U01UBCD06BB"

        # Optional: Provide template variables if your template requires them
        template_variables = {
            "user_name": "Jithu",
        }

        response = client.send_message(
            template_name=template_name,
            channel=channel,
            recipient_type=recipient_type,
            recipient_value=recipient_value,
            template_variables=template_variables,
        )
        print("Send message API response:")
        print(response)

        if (
            response
            and response.get("data")
            and response.get("data", {}).get("notificationId")
        ):
            print(
                f"Message sent successfully! Notification ID: {response['data']['notificationId']}"
            )
        elif response and response.get("error"):
            print(f"Failed to send message. Error: {response['error']}")
        else:
            print(
                "Failed to send message. Unknown error or unexpected response format."
            )

    except Exception as e:
        print(f"An error occurred while sending the message: {e}")
    print("-" * 30)


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY not found in environment variables or .env file.")
        print("Please set it to run the example.")
        sys.exit(1)

    siren_client = SirenClient(api_key=api_key)
    send_message_example(siren_client)
