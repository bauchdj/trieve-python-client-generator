from typing import Any, Callable, Dict, Optional
import httpx
from models.models import *


class TrieveAPIClient:
    def __init__(
        self,
        base_url: str = "https://api.trieve.ai",
        api_key: Optional[str] = None,
        timeout: float = 10.0,
        before_request: Optional[Callable[[httpx.Request], None]] = None,
        after_request: Optional[Callable[[httpx.Response], None]] = None,
    ):
        """
        Trieve API
        Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API.

        Args:
            base_url: The base URL for API requests
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
            before_request: Optional callback before each request
            after_request: Optional callback after each request
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.before_request = before_request
        self.after_request = after_request
        self.client = httpx.Client(timeout=timeout)

        if api_key:
            self.client.headers.update({"Authorization": f"Bearer {api_key}"})
        self.client.headers.update({"TR-Dataset": ""})
        self.client.headers.update({"TR-Organization": ""})
        self.client.headers.update({"X-API-Version": ""})

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """Make an HTTP request.

        Args:
            method: HTTP method
            path: Request path
            params: Query parameters
            headers: Additional request headers
            json_data: JSON request body

        Returns:
            httpx.Response: The response from the server
        """
        url = f"{self.base_url}/{path.lstrip('/')}"

        # Merge any additional headers with existing ones
        request_headers = self.client.headers.copy()
        if headers:
            request_headers.update(headers)

        request = self.client.build_request(
            method=method,
            url=url,
            params=params,
            headers=request_headers,
            json=json_data,
        )

        if self.before_request:
            self.before_request(request)

        response = self.client.send(request)

        if self.after_request:
            self.after_request(response)

        response.raise_for_status()
        return response

    def close(self):
        """Close the HTTP client."""
        self.client.close()
