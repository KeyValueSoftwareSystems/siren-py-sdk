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
        client._templates.base_url == client.base_url
    ), "Templates manager should use the base URL from client"


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
