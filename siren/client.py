"""Siren API client implementation."""

# siren/client.py


class SirenClient:
    """Client for interacting with the Siren API."""

    def __init__(self, api_key: str):
        """Initialize the SirenClient.

        Args:
            api_key: The API key for authentication.
        """
        self.api_key = api_key
        # We will add base_url and other configurations later
        print(f"SirenClient initialized with API key: {api_key[:5]}...")

    # MVP methods will be added here
