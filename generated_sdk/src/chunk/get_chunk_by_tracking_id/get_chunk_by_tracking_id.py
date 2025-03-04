# generated by borea

# if you want to edit this file, add it to ignores in borea.config.json, glob syntax

# TODO: not implemented

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ....models.models import *

if TYPE_CHECKING:
    from ...trieve_api import TrieveApi


class GetChunkByTrackingId:
    def __init__(self, parent: "TrieveApi"):
        self.parent = parent

    def get_chunk_by_tracking_id(
        self,
        tr_dataset: str,
        tracking_id: str,
        x_api_version: Optional[APIVersion] = None,
    ) -> Any:
        """
        Get a singular chunk by tracking_id. This is useful for when you are coordinating with an external system and want to use your own id as the primary reference for a chunk.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            tracking_id: tracking_id of the chunk you want to fetch
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.

        Returns:
            Response data
        """
        path = f"/api/chunk/tracking_id/{tracking_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = None

        response = self.parent._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
