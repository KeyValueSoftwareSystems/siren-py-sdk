"""Example script demonstrating template and channel template operations."""

import os
import sys

from siren.client import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError

# Allow running from examples directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def create_template_example(client: SirenClient) -> str:
    """Example of creating a template."""
    try:
        created = client.template.create(
            name="Welcome_Email_Example",
            description="A welcome email template",
            tag_names=["welcome"],
            variables=[{"name": "user_name", "defaultValue": "Guest"}],
        )
        print(f"Created template: {created.template_id}")
        return created.template_id
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def create_channel_templates_example(client: SirenClient, template_id: str):
    """Example of creating channel templates."""
    try:
        channel_templates = client.channel_template.create(
            template_id=template_id,
            EMAIL={
                "subject": "Welcome {{user_name}}!",
                "body": "<h1>Hello {{user_name}}!</h1>",
                "channel": "EMAIL",
                "isRawHTML": True,
            },
            SMS={"body": "Hi {{user_name}}! Welcome aboard!", "channel": "SMS"},
        )
        print(f"Created {len(channel_templates)} channel templates")
        return channel_templates[0].template_version_id if channel_templates else None
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def update_template_example(client: SirenClient, template_id: str):
    """Example of updating a template."""
    try:
        updated = client.template.update(
            template_id,
            name="Updated_Welcome_Template",
            description="Updated welcome email template",
            tag_names=["welcome", "updated"],
        )
        print(f"Updated template: {updated.name}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def get_templates_example(client: SirenClient):
    """Example of getting templates."""
    try:
        templates = client.template.get(page=0, size=2)
        print(f"Retrieved {len(templates)} templates")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def get_channel_templates_example(client: SirenClient, version_id: str):
    """Example of getting channel templates."""
    try:
        channel_templates = client.channel_template.get(version_id=version_id)
        print(f"Retrieved {len(channel_templates)} channel templates")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def publish_template_example(client: SirenClient, template_id: str):
    """Example of publishing a template."""
    try:
        published = client.template.publish(template_id)
        print(f"Published template: {published.name}")
        return published
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def delete_template_example(client: SirenClient, template_id: str):
    """Example of deleting a template."""
    try:
        success = client.template.delete(template_id)
        print(f"Deleted template: {success}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


if __name__ == "__main__":
    # Set environment variables: SIREN_API_KEY & SIREN_ENV (or pass as arguments)
    client = SirenClient()

    get_templates_example(client)
    template_id = create_template_example(client)
    if template_id:
        update_template_example(client, template_id)
        version_id = create_channel_templates_example(client, template_id)
        published = publish_template_example(client, template_id)
        if published and published.published_version:
            get_channel_templates_example(client, published.published_version.id)
        delete_template_example(client, template_id)
