from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ...models.models import *

if TYPE_CHECKING:
    from ..trieve_api import TrieveApi


class Public:
    def __init__(self, parent: "TrieveApi"):
        """
        Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API.

        Args:
            parent: The parent client to use for the requests
        """
        self.parent = parent

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

        response = self.parent._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
