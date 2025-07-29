# SPDX-FileCopyrightText: 2025-present Shane Rogers <shane@teer.ai>
#
# SPDX-License-Identifier: MIT

import requests
import logging
from typing import Dict, Any, Optional, Union

logger = logging.getLogger("teer")

class HttpClient:
    """HTTP client for making requests to the Teer API."""
    
    def __init__(self, api_key: str, base_url: str):
        """
        Initialize the HTTP client.
        
        Args:
            api_key: The Teer API key.
            base_url: The base URL for the Teer API.
        """
        self.api_key = api_key
        self.base_url = base_url
    
    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Make a request to the Teer API.
        
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
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.base_url}/{path}".rstrip('/')
        
        # Ensure we always have the Authorization and Content-Type headers
        request_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        # Add any additional headers
        if headers:
            request_headers.update(headers)
        
        try:
            logger.debug(f"Making {method} request to {url}")
            if data:
                logger.debug(f"Request data: {data}")
            
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=request_headers,
                timeout=timeout
            )
            response.raise_for_status()
            
            # Try to parse the response as JSON
            try:
                return response.json()
            except ValueError:
                # If the response is not JSON, return the text
                return {"text": response.text}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to {url}: {str(e)}")
            # Re-raise the exception for the caller to handle
            raise
