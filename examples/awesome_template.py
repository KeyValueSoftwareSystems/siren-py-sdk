"""Awesome template example: sending a message using awesome templayes and fetching status & replies."""

import asyncio

from dotenv import load_dotenv

from siren import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError
from siren.models.messaging import ProviderCode

def main() -> None:
    """Send message then query its status and replies."""
    load_dotenv()

    # Set environment variables: SIREN_API_KEY & SIREN_ENV (or pass as arguments)
    client = SirenClient()

    try:
        # Send message using awesome template -- slack
        message_id = client.message.send_awesome_template(
            recipient_value="U08FK1G6DGE",
            channel="SLACK",
            template_identifier="awesome-templates/customer-support/escalation_required/official/casual.yaml",
            template_variables={
                "ticket_id": "123456",
                "customer_name": "John", 
                "issue_summary": "Issue summary",
                "ticket_url": "https://siren.ai",
                "sender_name": "Siren"
            },
            provider_name="slack-test-py-sdk",
            provider_code=ProviderCode.SLACK,
        )

        # Send message using awesome template -- email
        # message_id = client.message.send_awesome_template(
        #     recipient_value="kv@keyvalue.systems",
        #     channel="EMAIL",
        #     template_identifier="awesome-templates/customer-support/escalation_required/official/casual.yaml",
        #     template_variables={
        #         "ticket_id": "123456",
        #         "customer_name": "John", 
        #         "issue_summary": "Issue summary",
        #         "ticket_url": "https://siren.ai",
        #         "sender_name": "Siren"
        #     },
        #     provider_name="py-sdk-test-mailgun",
        #     provider_code=ProviderCode.EMAIL_MAILGUN,
        # )

        print("Sent message id:", message_id)

        # Get message status
        status = client.message.get_status(message_id)
        print("Message status:", status)

        # Get message replies
        replies = client.message.get_replies(message_id)
        print("Message replies:", replies)  
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")

if __name__ == "__main__":
    main()     
