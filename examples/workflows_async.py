"""Asynchronous example demonstrating workflow trigger APIs."""

import asyncio

from dotenv import load_dotenv

from siren.async_client import AsyncSirenClient
from siren.exceptions import SirenAPIError, SirenSDKError


async def main() -> None:
    """Trigger and bulk-trigger workflows asynchronously."""
    load_dotenv()

    # Set environment variables: SIREN_API_KEY & SIREN_ENV (or pass as arguments)
    client = AsyncSirenClient()

    try:
        # Trigger single workflow execution
        execution = await client.workflow.trigger(
            workflow_name="sampleWorkflow",
            data={"subject": "Welcome"},
            notify={"email": "user@example.com"},
        )
        print("Workflow triggered:", execution.request_id)

        # Trigger bulk workflow
        bulk = await client.workflow.trigger_bulk(
            workflow_name="sampleWorkflow",
            notify=[{"email": "user1@example.com"}, {"email": "user2@example.com"}],
            data={"template": "welcome"},
        )
        print("Bulk workflow triggered:", bulk.request_id)

        # Schedule workflow (commented; requires valid IDs)
        # schedule = await client.workflow.schedule(
        #     name="sampleWorkflow123",
        #     schedule_time="21:31:00",
        #     timezone_id="Asia/Kolkata",
        #     start_date="2024-06-11",
        #     workflow_type="DAILY",
        #     workflow_id="acd59a55-1072-41a7-90d9-5554b21aef1b",
        #     input_data={"type": "daily_summary"},
        # )
        # print("Workflow scheduled:", schedule.id)
    except SirenAPIError as e:
        print(f"API error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK error: {e.message}")

    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
