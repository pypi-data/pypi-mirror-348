# SPDX-FileCopyrightText: 2025-present Shane Rogers <shane@teer.ai>
#
# SPDX-License-Identifier: MIT

import os
from typing import Optional, Dict, Any

from .http import HttpClient
from .resources import Ingest, BillingResource
from .types import (
    AnthropicCache,
    OpenAICache,
    GoogleCache,
    CacheObject,
    UsageObject,
    IngestPayload,
    Provider,
    MetadataObject,
    PlatformObject,
)

# Default API key environment variable name
TEER_API_KEY_ENV = "TEER_SECRET_API_KEY"

# Default base URL
DEFAULT_BASE_URL = "https://track.teer.ai"


class TeerClient:
    """
    Teer API client for tracking LLM usage and other metrics.

    Usage:
        # Initialize with default settings (reads from TEER_SECRET_API_KEY env var)
        client = TeerClient()

        # Or initialize with explicit API key
        client = TeerClient(api_key="your-api-key")

        # Or initialize with custom base URL for development
        client = TeerClient(base_url="http://track.teer.ai:5171")

        # Send ingest data
        client.ingest.send({
            "provider": "anthropic",
            "model": "claude-3-haiku-20240307",
            "function_id": "my-function",
            "usage": {
                "input": 1000,
                "output": 2000
            }
        })
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = "v1",
    ):
        """
        Initialize the Teer client.

        Args:
            api_key: The Teer API key. If not provided, it will be read from the
                    TEER_SECRET_API_KEY environment variable.
            base_url: The base URL for the Teer API. Defaults to https://track.teer.ai.
            api_version: The API version to use. Defaults to v1.
        """
        self.api_key = api_key or os.environ.get(TEER_API_KEY_ENV)
        if not self.api_key:
            raise ValueError(
                f"No API key provided. Set the {TEER_API_KEY_ENV} environment "
                f"variable or pass an api_key parameter."
            )

        self.base_url = base_url.rstrip("/")
        self.api_version = api_version

        # Initialize the HTTP client
        self.http_client = HttpClient(api_key=self.api_key, base_url=self.api_base)

        # Initialize resources
        self.ingest = Ingest(self)
        self.billing = BillingResource(self)

    @property
    def api_base(self) -> str:
        """Get the base URL for API requests."""
        return f"{self.base_url}/{self.api_version}"


# For backwards compatibility with the old API
Teer = TeerClient

__all__ = [
    "TeerClient",
    "Teer",
    "AnthropicCache",
    "OpenAICache",
    "GoogleCache",
    "CacheObject",
    "UsageObject",
    "IngestPayload",
    "Provider",
    "MetadataObject",
    "PlatformObject",
]
