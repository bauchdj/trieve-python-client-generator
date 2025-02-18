from typing import Any, Dict, List, Optional, Union
from src.trieve_api_client import TrieveAPIClient
from models.models import *

class HealthClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def health_check(
        self,
    ) -> Any:
        """Confirmation that the service is healthy and can make embedding vectors

        Returns:
            Response data
        """
        path = f"/api/health"
        params = None
        headers = None
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
