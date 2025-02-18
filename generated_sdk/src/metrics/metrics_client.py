from typing import Any, Dict, List, Optional, Union
from src.trieve_api_client import TrieveAPIClient
from models.models import *

class MetricsClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def get_metrics(
        self,
    ) -> Any:
        """
        This route allows you to view the number of items in each queue in the Prometheus format.

        Returns:
            Response data
        """
        path = f"/metrics"
        params = None
        headers = None
        json_data = None

        response = self._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
