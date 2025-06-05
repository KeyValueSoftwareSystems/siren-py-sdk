"""Configuration and fixtures for the test suite."""

import os
import sys

import pytest

# Ensure the 'siren' package in the parent directory can be imported:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from siren import SirenClient


@pytest.fixture
def client():
    """Provides a SirenClient instance for testing, using a dummy API key."""
    return SirenClient(api_key="test_api_key")
