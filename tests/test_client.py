"""Tests for the Siren API client."""

import os
import sys

# Ensure the 'siren' package in the parent directory can be imported:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# The 'client' fixture is automatically available from conftest.py


def test_siren_client_initialization(client):
    """Test that the SirenClient initializes correctly."""
    assert client.api_key == "test_api_key", "API key should be set on initialization"
    assert hasattr(
        client, "_templates"
    ), "Client should have an internal _templates manager attribute"
    assert hasattr(client, "get_templates"), "Client should have a get_templates method"
    assert hasattr(
        client, "create_template"
    ), "Client should have a create_template method"
    assert (
        client._templates.api_key == "test_api_key"
    ), "Templates manager should have API key"
    assert (
        client._templates.base_url == f"{client.BASE_API_URL}/api/v1/public"
    ), "Templates manager should construct its specific v1 base URL"
