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
            print("Received an unexpected response structure for send_message.")

    except Exception as e:
        print(f"An error occurred while sending the message: {e}")


def get_replies_example(client: SirenClient, message_id: str):
    """Demonstrates retrieving replies for a message."""
    print("\nAttempting to get message replies...")
    # IMPORTANT: Replace with an actual message ID that has replies
    message_id_with_replies = "9004b6b0-3e77-4add-9541-56ba28c37f27"

    try:
        print(f"Fetching replies for message ID: {message_id_with_replies}")
        response = client.get_replies(message_id=message_id_with_replies)
        print("Get message replies API response:")
        print(response)

        if response and response.get("data") is not None:  # Check if 'data' key exists
            replies = response["data"]
            if isinstance(replies, list) and replies:
                print(f"Found {len(replies)} replies:")
                for i, reply in enumerate(replies):
                    print(
                        f"  Reply {i+1}: {reply.get('text', 'N/A')} (User: {reply.get('user', 'N/A')}, Timestamp: {reply.get('ts', 'N/A')})"
                    )
            elif isinstance(replies, list) and not replies:
                print("No replies found for this message.")
            else:
                print("Received 'data' but it's not a list of replies as expected.")
        elif response and response.get("error"):
            print(f"Failed to get replies. Error: {response['error']}")
        else:
            print("Received an unexpected response structure for get_message_replies.")

    except Exception as e:
        print(f"An error occurred while getting message replies: {e}")


def get_message_status_example(client: SirenClient, message_id: str):
    """Demonstrates retrieving the status for a message."""
    print("\nAttempting to get message status...")
    # IMPORTANT: Replace with an actual message ID
    # Using an ID from a previous successful run for demonstration
    message_id_to_check_status = message_id

    try:
        print(f"Fetching status for message ID: {message_id_to_check_status}")
        response = client.get_message_status(message_id=message_id_to_check_status)
        print("Get message status API response:")
        print(response)

        if response and response.get("data") and response["data"].get("status"):
            print(f"Message Status: {response['data']['status']}")
        elif response and response.get("error"):
            print(f"Failed to get message status. Error: {response['error']}")
        else:
            print("Received an unexpected response structure for get_message_status.")

    except Exception as e:
        print(f"An error occurred while getting the message status: {e}")


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY not found in environment variables or .env file.")
        print("Please set it to run the example.")
        sys.exit(1)

    siren_client = SirenClient(api_key=api_key)
    # send_message_example(siren_client)
    # get_replies_example(
    #     siren_client, "9004b6b0-3e77-4add-9541-56ba28c37f27"
    # )
    get_message_status_example(siren_client, "c53539ce-2d74-4071-b671-ead6c8465b5b")
