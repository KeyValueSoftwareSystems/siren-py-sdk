"""Example script demonstrating workflow methods using SirenClient."""

import os
import sys

from siren.client import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError

# Allow running from examples directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def trigger_workflow_example(client: SirenClient) -> None:
    """Example of triggering a workflow."""
    try:
        execution = client.workflow.trigger(
            workflow_name="sampleWorkflow",
            data={"subject": "Welcome"},
            notify={"email": "user@example.com"},
        )
        print(f"Workflow triggered: {execution.request_id}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def trigger_bulk_workflow_example(client: SirenClient) -> None:
    """Example of triggering a bulk workflow."""
    try:
        bulk_execution = client.workflow.trigger_bulk(
            workflow_name="sampleWorkflow",
            notify=[{"email": "user1@example.com"}, {"email": "user2@example.com"}],
            data={"template": "welcome"},
        )
        print(f"Bulk workflow triggered: {bulk_execution.request_id}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def schedule_workflow_example(client: SirenClient) -> None:
    """Example of scheduling a workflow."""
    try:
        schedule = client.workflow.schedule(
            name="sampleWorkflow123",
            schedule_time="21:31:00",
            timezone_id="Asia/Kolkata",
            start_date="2024-06-11",
            workflow_type="DAILY",
            workflow_id="acd59a55-1072-41a7-90d9-5554b21aef1b",
            input_data={"type": "daily_summary"},
        )
        print(f"Workflow scheduled: {schedule.id}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


if __name__ == "__main__":
    api_key = os.environ.get("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY environment variable not set.")
        sys.exit(1)

    client = SirenClient(api_key=api_key)

    # trigger_workflow_example(client)
    # trigger_bulk_workflow_example(client)
    # schedule_workflow_example(client)
