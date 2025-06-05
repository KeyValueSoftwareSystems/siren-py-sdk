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


if __name__ == "__main__":
    api_key = os.environ.get("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY environment variable not set.")
        print("Please set it before running the example.")
        sys.exit(1)

    siren_client = SirenClient(api_key=api_key)
    run_trigger_workflow_example(siren_client)
