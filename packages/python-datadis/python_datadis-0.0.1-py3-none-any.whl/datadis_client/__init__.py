"""
Datadis API Client

A Python client for interacting with the Datadis API (https://datadis.es/private-api).
"""

__version__ = "0.0.1"

import requests
from typing import Dict, Any

# Import mixins
from .consumption import ConsumptionMixin
from .supplies import SuppliesMixin
from .search import SearchMixin


class DatadisClient(ConsumptionMixin, SuppliesMixin, SearchMixin):
    """Client for interacting with the Datadis API."""

    BASE_URL = "https://datadis.es"

    def __init__(self, username: str, password: str):
        """
        Initialize a new Datadis client.

        Args:
            username: NIF of the user registered in Datadis.
            password: User's Datadis access password.
        """
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()

        # Set manual User-Agent to avoid 403 errors
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def authenticate(self) -> str:
        """
        Authenticate with the Datadis API and get an access token.

        Returns:
            str: The authentication token.

        Raises:
            ValueError: If authentication fails.
        """
        url = f"{self.BASE_URL}/nikola-auth/tokens/login"
        params = {
            "username": self.username,
            "password": self.password
        }

        response = self.session.post(url, params=params)

        if response.status_code != 200:
            raise ValueError(f"Authentication failed: {response.text}")

        self.token = response.text
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

        return self.token

    def _get(self, endpoint: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        """
        Make a GET request to the Datadis API.

        Args:
            endpoint: The API endpoint to call.
            params: Optional parameters to pass to the request.

        Returns:
            Dict[str, Any]: The JSON response.

        Raises:
            ValueError: If the request fails.
        """

        if not self.token:
            self.authenticate()

        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.get(url, params=params)

        if response.status_code in (401, 403):
            # Token might have expired or been invalidated, try to re-authenticate
            self.authenticate()
            response = self.session.get(url, params=params)

        if response.status_code != 200:
            raise ValueError(f"API request failed: {response.text}")

        return response.json()


# Convenience functions
def create_client(username: str, password: str) -> DatadisClient:
    """
    Create and authenticate a Datadis client.

    Args:
        username: NIF of the user registered in Datadis.
        password: User's Datadis access password.

    Returns:
        DatadisClient: An authenticated Datadis client.
    """
    client = DatadisClient(username, password)
    client.authenticate()
    return client


# Export for easier imports
__all__ = ["DatadisClient", "create_client"]
