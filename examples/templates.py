"""Example script demonstrating template methods using SirenClient."""

import os
import sys

from siren.client import SirenClient
from siren.exceptions import SirenAPIError, SirenSDKError

# Allow running from examples directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def get_templates_example(client: SirenClient) -> None:
    """Example of getting templates."""
    try:
        templates = client.get_templates(page=0, size=2)
        print(f"Retrieved {len(templates)} templates")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def create_template_example(client: SirenClient) -> str:
    """Example of creating a template."""
    import time

    timestamp = int(time.time())

    try:
        created = client.create_template(
            name=f"SDK_Example_Template_{timestamp}",
            description="Test template from SDK",
            tag_names=["sdk-test", "example"],
            variables=[{"name": "user_name", "defaultValue": "Guest"}],
            configurations={
                "EMAIL": {
                    "subject": "Hello {{user_name}}!",
                    "channel": "EMAIL",
                    "body": "<p>Welcome {{user_name}}!</p>",
                    "isRawHTML": True,
                    "isPlainText": False,
                }
            },
        )
        print(f"Created template: {created.template_id}")
        return created.template_id
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
        return None
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")
        return None


def update_template_example(client: SirenClient, template_id: str) -> None:
    """Example of updating a template."""
    try:
        updated = client.update_template(
            template_id,
            name="Updated_SDK_Example",
            description="Updated description from SDK",
            tag_names=["updated", "sdk-test"],
        )
        print(f"Updated template: {updated.id}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def publish_template_example(client: SirenClient, template_id: str):
    """Example of publishing a template."""
    try:
        published = client.publish_template(template_id)
        print(f"Published template: {published.id}")
        return published
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
        return None
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")
        return None


def create_channel_templates_example(client: SirenClient, template_id: str) -> None:
    """Example of creating channel templates for a template."""
    try:
        result = client.create_channel_templates(
            template_id,
            SMS={
                "body": "Hello {{user_name}}! This is from SDK.",
                "channel": "SMS",
                "isFlash": False,
                "isUnicode": False,
            },
            EMAIL={
                "subject": "Welcome {{user_name}}!",
                "channel": "EMAIL",
                "body": "<p>Hello {{user_name}}, welcome from SDK!</p>",
                "isRawHTML": True,
                "isPlainText": False,
            },
        )
        print(f"Created {len(result)} channel templates")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def get_channel_templates_example(client: SirenClient, version_id: str) -> None:
    """Example of getting channel templates for a template version."""
    try:
        result = client.get_channel_templates(version_id, page=0, size=5)
        print(f"Retrieved {len(result)} channel templates")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


def delete_template_example(client: SirenClient, template_id: str) -> None:
    """Example of deleting a template."""
    try:
        result = client.delete_template(template_id)
        if result:
            print(f"Successfully deleted template: {template_id}")
        else:
            print(f"Failed to delete template: {template_id}")
    except SirenAPIError as e:
        print(f"API Error: {e.error_code} - {e.api_message}")
    except SirenSDKError as e:
        print(f"SDK Error: {e.message}")


if __name__ == "__main__":
    api_key = os.environ.get("SIREN_API_KEY")
    if not api_key:
        print("Error: SIREN_API_KEY environment variable not set.")
        sys.exit(1)

    client = SirenClient(api_key)

    get_templates_example(client)
    template_id = create_template_example(client)
    if template_id:
        update_template_example(client, template_id)
        create_channel_templates_example(client, template_id)
        published = publish_template_example(client, template_id)
        if published and published.published_version:
            get_channel_templates_example(client, published.published_version.id)
        delete_template_example(client, template_id)
