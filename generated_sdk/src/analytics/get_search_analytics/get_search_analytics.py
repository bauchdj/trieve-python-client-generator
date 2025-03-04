# generated by borea

# if you want to edit this file, add it to ignores in borea.config.json, glob syntax

# TODO: not implemented

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ....models.models import *

if TYPE_CHECKING:
    from ...trieve_api import TrieveApi


class GetSearchAnalytics:
    def __init__(self, parent: "TrieveApi"):
        self.parent = parent

    def get_search_analytics(
        self,
        tr_dataset: str,
        request_body: Optional[SearchAnalytics] = None,
    ) -> Any:
        """
        This route allows you to view the search analytics for a dataset.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            request_body: Request body

        Returns:
            Response data
        """
        path = f"/api/analytics/search"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = request_body.model_dump() if request_body else None

        response = self.parent._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
