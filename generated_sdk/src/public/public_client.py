from typing import Any, Dict, List, Optional, Union
from ..trieve_api_client import TrieveAPIClient
from ...models.models import *

class PublicClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def public_page(
        self,
        dataset_id: str,
    ) -> Any:
        """
        

        Args:
            dataset_id: The id or tracking_id of the dataset you want to get the demo page for.

        Returns:
            Response data
        """
        path = f"/api/public_page/{dataset_id}"
        params = {}
        headers = {}
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
