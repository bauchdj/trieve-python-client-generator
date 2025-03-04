# generated by borea

# if you want to edit this file, add it to ignores in borea.config.json, glob syntax

# TODO: not implemented

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ....models.models import *

if TYPE_CHECKING:
    from ...trieve_api import TrieveApi


class GetMe:
    def __init__(self, parent: "TrieveApi"):
        self.parent = parent

    def get_me(
        self,
    ) -> Any:
        """
        Get the user corresponding to your current auth credentials.

        Returns:
            Response data
        """
        path = f"/api/auth/me"
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
