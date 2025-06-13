"""Asynchronous example for template & channel template operations."""

import asyncio

from dotenv import load_dotenv

from siren.async_client import AsyncSirenClient
from siren.exceptions import SirenAPIError, SirenSDKError


async def main() -> None:
    """Create and publish a template asynchronously."""
    load_dotenv()

    # Set environment variables: SIREN_API_KEY & SIREN_ENV (or pass as arguments)
    client = AsyncSirenClient()

    try:
        # Get templates list
        templates = await client.template.get(page=0, size=2)
        print("Retrieved", len(templates), "templates")

        # Create template
        created = await client.template.create(
            name="Welcome_Email_Example",
            description="A welcome email template",
            tag_names=["welcome"],
            variables=[{"name": "user_name", "defaultValue": "Guest"}],
        )
        print("Created template:", created.template_id)

        # Update template metadata
        updated = await client.template.update(
            created.template_id,
            name="Updated_Welcome_Template",
            description="Updated welcome email template",
            tag_names=["welcome", "updated"],
        )
        print("Updated template:", updated.name)

        # Create channel templates (EMAIL & SMS)
        channel_templates = await client.channel_template.create(
            template_id=created.template_id,
            EMAIL={
                "subject": "Welcome {{user_name}}!",
                "body": "<h1>Hello {{user_name}}!</h1>",
                "channel": "EMAIL",
                "isRawHTML": True,
            },
            SMS={
                "body": "Hi {{user_name}}! Welcome aboard!",
                "channel": "SMS",
            },
        )
        print("Created", len(channel_templates), "channel templates")

        # Publish template now that channels exist
        published = await client.template.publish(created.template_id)
        print("Published:", published.name)

        if published.published_version:
            # Fetch channel templates list
            channel_templates = await client.channel_template.get(
                version_id=published.published_version.id
            )
            print("Retrieved channel templates count:", len(channel_templates))

        # Delete template (cleanup)
        success = await client.template.delete(created.template_id)
        print("Deleted template:", success)
    except SirenAPIError as e:
        print(f"API error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK error: {e.message}")

    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
