# SPDX-FileCopyrightText: 2025-present Shane Rogers <shane@teer.ai>
#
# SPDX-License-Identifier: MIT

from typing import Dict, Any, Optional, TYPE_CHECKING
from .base import BaseResource
from ..types import IngestPayload

if TYPE_CHECKING:
    from .. import TeerClient


class Ingest(BaseResource):
    """
    Ingest resource for sending usage data to Teer.

    This resource is used to send LLM usage data and other metrics to Teer.
    """

    def __init__(self, client: "TeerClient"):
        """
        Initialize the Ingest resource.

        Args:
            client: The Teer client instance.
        """
        super().__init__(client, "ingest")

    def send(
        self,
        payload: IngestPayload,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 10,
    ) -> Dict[str, Any]:
        """
        Send usage data to Teer.

        Args:
            payload: The data to send. Should include provider, model, function_id, and usage.
                     See the IngestPayload type for details on the expected structure.
            headers: Additional headers to include in the request.
            timeout: Request timeout in seconds. Defaults to 10 seconds.

        Returns:
            The response from the Teer API.

        Raises:
            Exception: If the request fails.
        """
        return self._request("POST", data=payload, headers=headers, timeout=timeout)
