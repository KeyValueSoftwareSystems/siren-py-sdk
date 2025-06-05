"""Examples for template-related operations using the Siren SDK."""

import json
import os
import sys

from dotenv import load_dotenv

# Ensure the 'siren' package in the parent directory can be imported:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from siren import SirenClient


def run_get_templates_example(client: SirenClient):
    """Runs the example for fetching templates."""
    print("--- Fetching Templates ---")
    try:
        templates_response = client.get_templates(
            page=0,
            size=2,  # Get first 2 templates for brevity
        )
        if templates_response and templates_response.get("error") is None:
            print("Successfully fetched templates:")
        print(json.dumps(templates_response, indent=2))
    except Exception as e:
        print(f"Error fetching templates: {e}")


def run_create_template_example(client: SirenClient):
    """Runs the example for creating a template."""
    print("\n--- Creating a Template ---")
    new_template_payload = {
        "name": "Sample5",
        "description": "A simple template created via the examples/templates.py script.",
        "tagNames": ["sdk-example", "template-ops"],
        "variables": [{"name": "user_name", "defaultValue": "Guest"}],
        "configurations": {
            "EMAIL": {
                "subject": "SDK Test Email for {{user_name}} from templates.py",
                "channel": "EMAIL",
                "body": "<p>Hello {{user_name}}, this is a test from examples/templates.py!</p>",
                "isRawHTML": True,
                "isPlainText": False,
            }
        },
    }
    try:
        created_template_response = client.create_template(new_template_payload)
        if created_template_response and created_template_response.get("error") is None:
            print("Successfully created template:")
        print(json.dumps(created_template_response, indent=2))
    except Exception as e:
        print(f"Error creating template: {e}")


def run_update_template_example(client: SirenClient):
    """Runs the example for updating a template."""
    print("\n--- Updating a Template ---")
    template_id_to_update = "dc58f20d-bad1-4ffd-8f92-34682397100f"
    update_payload = {
        "name": "Updated_SDK_Example_Template",
        "description": "This template was updated by the examples/templates.py script.",
        "tagNames": ["sdk-example", "update-op"],
        "variables": [{"name": "customer_name", "defaultValue": "Valued Customer"}],
        "configurations": {
            "EMAIL": {
                "subject": "Updated Subject for {{customer_name}}",
                "body": "<p>Hello {{customer_name}}, your template has been updated!</p>",
            }
        },
    }

    try:
        updated_template_response = client.update_template(
            template_id_to_update, update_payload
        )
        if updated_template_response and updated_template_response.get("error") is None:
            print(f"Successfully updated template '{template_id_to_update}':")
        print(json.dumps(updated_template_response, indent=2))
    except Exception as e:
        print(f"Error updating template '{template_id_to_update}': {e}")


def run_delete_template_example(client: SirenClient):
    """Runs the example for deleting a template."""
    print("\n--- Deleting a Template ---")
    template_id_to_delete = "b5d4cdf8-a46a-4867-aa02-c7551d3fe747"

    try:
        delete_response = client.delete_template(template_id_to_delete)
        if delete_response and delete_response.get("status") == "success":
            print(f"Successfully deleted template '{template_id_to_delete}':")
        print(json.dumps(delete_response, indent=2))
    except Exception as e:
        print(f"Error deleting template '{template_id_to_delete}': {e}")


def run_publish_template_example(client: SirenClient):
    """Runs the example for publishing a template."""
    print("\n--- Publishing a Template ---")
    template_id_to_publish = "11921404-4517-48b7-82ee-fcdcf8f9c03b"

    try:
        publish_response = client.publish_template(template_id_to_publish)
        if publish_response and publish_response.get("error") is None:
            print(f"Successfully published template '{template_id_to_publish}':")
        print(json.dumps(publish_response, indent=2))
    except Exception as e:
        print(f"Error publishing template '{template_id_to_publish}': {e}")


if __name__ == "__main__":
    load_dotenv()

    api_key = os.getenv("SIREN_API_KEY")

    if not api_key:
        print(
            "Error: SIREN_API_KEY is not set. Please check your .env file or environment variables."
        )
        sys.exit(1)

    siren_client = SirenClient(api_key=api_key)

    # run_get_templates_example(siren_client)
    # run_create_template_example(siren_client)
    # run_update_template_example(siren_client)
    # run_delete_template_example(siren_client)
    # run_publish_template_example(siren_client)
