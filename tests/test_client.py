"""Tests for the Siren API client."""

import os
import sys

# Ensure the 'siren' package in the parent directory can be imported:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from siren.client import SirenClient

# The 'client' fixture is automatically available from conftest.py


def test_siren_client_initialization(client):
    """Test that the SirenClient initializes correctly."""
    assert client.api_key == "test_api_key", "API key should be set on initialization"
    assert hasattr(client, "template"), "Client should have a template property"
    assert hasattr(client.template, "get"), "Template client should have a get method"
    assert hasattr(
        client.template, "create"
    ), "Template client should have a create method"
    assert (
        client.template.api_key == "test_api_key"
    ), "Template client should have API key"
    assert (
        client.template.base_url == client.base_url
    ), "Template client should use the base URL from client"

    # Test workflow property
    assert hasattr(client, "workflow"), "Client should have a workflow property"
    assert hasattr(
        client.workflow, "trigger"
    ), "Workflow client should have a trigger method"
    assert hasattr(
        client.workflow, "trigger_bulk"
    ), "Workflow client should have a trigger_bulk method"
    assert hasattr(
        client.workflow, "schedule"
    ), "Workflow client should have a schedule method"
    assert (
        client.workflow.api_key == "test_api_key"
    ), "Workflow client should have API key"
    assert (
        client.workflow.base_url == client.base_url
    ), "Workflow client should use the base URL from client"

    # Test message property
    assert hasattr(client, "message"), "Client should have a message property"
    assert hasattr(client.message, "send"), "Message client should have a send method"
    assert hasattr(
        client.message, "get_replies"
    ), "Message client should have a get_replies method"
    assert hasattr(
        client.message, "get_status"
    ), "Message client should have a get_status method"
    assert (
        client.message.api_key == "test_api_key"
    ), "Message client should have API key"
    assert (
        client.message.base_url == client.base_url
    ), "Message client should use the base URL from client"

    # Test user property
    assert hasattr(client, "user"), "Client should have a user property"
    assert hasattr(client.user, "add"), "User client should have an add method"
    assert hasattr(client.user, "update"), "User client should have an update method"
    assert hasattr(client.user, "delete"), "User client should have a delete method"
    assert client.user.api_key == "test_api_key", "User client should have API key"
    assert (
        client.user.base_url == client.base_url
    ), "User client should use the base URL from client"

    # Test webhook property
    assert hasattr(client, "webhook"), "Client should have a webhook property"
    assert hasattr(
        client.webhook, "configure_notifications"
    ), "Webhook client should have a configure_notifications method"
    assert hasattr(
        client.webhook, "configure_inbound"
    ), "Webhook client should have a configure_inbound method"
    assert (
        client.webhook.api_key == "test_api_key"
    ), "Webhook client should have API key"
    assert (
        client.webhook.base_url == client.base_url
    ), "Webhook client should use the base URL from client"


def test_siren_client_default_environment():
    """Test that SirenClient defaults to 'prod' environment."""
    # Ensure SIREN_ENV is not set for this test
    original_env = os.environ.get("SIREN_ENV")
    if "SIREN_ENV" in os.environ:
        del os.environ["SIREN_ENV"]

    try:
        client = SirenClient(api_key="test_key")
        assert client.env == "prod"
        assert client.base_url == "https://api.trysiren.io"
    finally:
        # Restore original environment variable if it existed
        if original_env is not None:
            os.environ["SIREN_ENV"] = original_env


def test_siren_client_explicit_environment():
    """Test that SirenClient uses explicit environment parameter."""
    # Test dev environment
    client_dev = SirenClient(api_key="test_key", env="dev")
    assert client_dev.env == "dev"
    assert client_dev.base_url == "https://api.dev.trysiren.io"

    # Test prod environment
    client_prod = SirenClient(api_key="test_key", env="prod")
    assert client_prod.env == "prod"
    assert client_prod.base_url == "https://api.trysiren.io"


def test_siren_client_environment_variable():
    """Test that SirenClient uses SIREN_ENV environment variable."""
    # Set environment variable
    os.environ["SIREN_ENV"] = "dev"

    try:
        client = SirenClient(api_key="test_key")
        assert client.env == "dev"
        assert client.base_url == "https://api.dev.trysiren.io"
    finally:
        # Clean up
        del os.environ["SIREN_ENV"]


def test_siren_client_explicit_env_overrides_env_var():
    """Test that explicit env parameter overrides environment variable."""
    # Set environment variable to dev
    os.environ["SIREN_ENV"] = "dev"

    try:
        # But explicitly pass prod
        client = SirenClient(api_key="test_key", env="prod")
        assert client.env == "prod"
        assert client.base_url == "https://api.trysiren.io"
    finally:
        # Clean up
        del os.environ["SIREN_ENV"]


def test_siren_client_invalid_environment():
    """Test that SirenClient raises error for invalid environment."""
    try:
        SirenClient(api_key="test_key", env="invalid")
        assert False, "Should have raised ValueError for invalid environment"
    except ValueError as e:
        assert "Invalid environment 'invalid'" in str(e)
