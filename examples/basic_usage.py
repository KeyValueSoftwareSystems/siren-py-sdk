"""Basic usage examples for the Siren SDK."""

# For local development, you might need to adjust sys.path:
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from siren.client import SirenClient

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    api_key = os.getenv("SIREN_API_KEY")

    if not api_key:
        print("Error: SIREN_API_KEY not found in .env file or environment variables.")
        print(
            "Please create a .env file in the project root with SIREN_API_KEY='your_key'"
        )
        sys.exit(1)

    client = SirenClient(api_key=api_key)

    try:
        templates_response = client.get_templates(
            page=0, size=5
        )  # Get first 5 templates
        print("Successfully fetched templates:")
        import json  # For pretty printing

        print(json.dumps(templates_response, indent=2))
    except Exception as e:
        print(f"Error fetching templates: {e}")

    print("\nBasic usage example finished.")
