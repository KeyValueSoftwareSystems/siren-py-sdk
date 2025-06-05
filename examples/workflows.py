# examples/workflows.py
"""Example script for demonstrating Siren SDK workflow operations."""

import os
import sys

from siren import SirenClient

# This allows running the script directly from the examples directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def run_trigger_workflow_example(client: SirenClient):
    """Demonstrates triggering a workflow using the Siren SDK."""
    print("Attempting to trigger a workflow with data and notify parameters...")
    workflow_name = "sampleWorkflow"
    try:
        data_payload = {"subject": "SDK Test OTP", "user_id": "12345"}
        notify_payload = {
            "notificationType": "email",
            "recipient": "test_user@example.com",
            "name": "Test User",
        }

        response = client.trigger_workflow(
            workflow_name=workflow_name, data=data_payload, notify=notify_payload
        )
        print("Trigger Workflow Response (with data/notify):")
        print(response)

    except Exception as e:
        print(f"An error occurred while triggering workflow '{workflow_name}': {e}")

    print("\nAttempting to trigger a workflow with only the workflow name...")
    minimal_workflow_name = "another_workflow_name"
    try:
        response_minimal = client.trigger_workflow(workflow_name=minimal_workflow_name)
        print(f"Trigger Workflow Response (minimal for '{minimal_workflow_name}'):")
        print(response_minimal)

    except Exception as e:
        print(
            f"An error occurred while triggering workflow '{minimal_workflow_name}': {e}"
        )


def run_trigger_bulk_workflow_example(client: SirenClient):
    """Demonstrates triggering workflows in bulk using the Siren SDK."""
    print("\n--- Running Bulk Trigger Workflow Example ---")

    # Example 1: Bulk trigger with common data and multiple notify objects
    print(
        "\nAttempting to trigger a bulk workflow with common data and multiple notifications..."
    )
    bulk_workflow_name_1 = "sampleWorkflow"
    common_data_payload = {"campaign_id": "summer_promo_2024"}
    notify_list_1 = [
        {
            "notificationType": "email",
            "recipient": "user1@example.com",
            "name": "User One",
            "discount_code": "SUMMER10",
        },
        {
            "notificationType": "sms",
            "recipient": "+15551234567",
            "product_name": "New Gadget",
            "tracking_link": "http://example.com/track/xyz123",
        },
    ]

    try:
        response_1 = client.trigger_bulk_workflow(
            workflow_name=bulk_workflow_name_1,
            notify=notify_list_1,
            data=common_data_payload,
        )
        print(
            f"Bulk Trigger Workflow Response (with data for '{bulk_workflow_name_1}'):"
        )
        print(response_1)
    except Exception as e:
        print(
            f"An error occurred while triggering bulk workflow '{bulk_workflow_name_1}': {e}"
        )


if __name__ == "__main__":
    api_key = os.environ.get("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY environment variable not set.")
        print("Please set it before running the example.")
        sys.exit(1)

    siren_client = SirenClient(api_key=api_key)
    # run_trigger_workflow_example(siren_client)
    run_trigger_bulk_workflow_example(siren_client)
