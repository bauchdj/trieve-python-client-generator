from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ...models.models import *

if TYPE_CHECKING:
    from ..trieve_api import TrieveApi


class Health:
    def __init__(self, parent: "TrieveApi"):
        """
        Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API.

        Args:
            parent: The parent client to use for the requests
        """
        self.parent = parent

    def health_check(
        self,
    ) -> Any:
        """
        Confirmation that the service is healthy and can make embedding vectors

        Returns:
            Response data
        """
        path = f"/api/health"
        params = None
        headers = None
        json_data = None

        response = self.parent._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
