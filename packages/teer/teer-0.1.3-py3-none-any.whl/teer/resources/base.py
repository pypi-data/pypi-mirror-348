# SPDX-FileCopyrightText: 2025-present Shane Rogers <shane@teer.ai>
#
# SPDX-License-Identifier: MIT

from typing import Dict, Any, Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from .. import TeerClient

logger = logging.getLogger("teer")


class BaseResource:
    """Base class for all Teer API resources."""

    def __init__(self, client: "TeerClient", resource_path: str):
        """
        Initialize the base resource.

        Args:
            client: The Teer client instance.
            resource_path: The path to the resource, e.g., "ingest".
        """
        self.client = client
        self.base_url = f"{client.api_base}/{resource_path}"

    def _request(
        self,
        method: str,
        path: str = "",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        """
        Make a request to the Teer API using the shared HTTP client.

        Args:
            method: The HTTP method to use (GET, POST, etc.).
            path: The path to append to the base URL.
            params: Query parameters for the request.
            data: JSON data for the request body.
            headers: Additional headers to include in the request.
            timeout: Request timeout in seconds.

        Returns:
            The response from the Teer API.

        Raises:
            Exception: If the request fails.
        """
        # Calculate the full path relative to the resource base URL
        resource_path = path.lstrip("/") if path else ""

        # Extract the resource-specific part of the URL
        # e.g., if base_url is "https://track.teer.ai/v1/ingest",
        # we want to extract "ingest" to append to the path
        resource_name = self.base_url.split("/")[-1]

        # Construct the full path for the HTTP client
        # The HTTP client's base URL is already set to the API base (e.g., "https://track.teer.ai/v1")
        full_path = f"{resource_name}/{resource_path}".rstrip("/")
        if not full_path:
            full_path = resource_name

        logger.debug(f"Making {method} request to {full_path}")
        if data:
            logger.debug(f"Request data: {data}")

        # Use the shared HTTP client to make the request
        try:
            return self.client.http_client.request(
                method=method,
                path=full_path,
                params=params,
                data=data,
                headers=headers,
                timeout=timeout,
            )
        except Exception as e:
            logger.error(f"Error making request to {full_path}: {str(e)}")
            # Re-raise the exception for the caller to handle
            raise
