from typing import Any, Dict, List, Optional, Union
from src.trieve_api_client import TrieveAPIClient
from models.models import *

class UserClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def update_user(
        self,
        tr_organization: str,
        role: int,
        user_id: Optional[str] = None,
    ) -> Any:
        """Update a user's information for the org specified via header. If the user_id is not provided, the auth'ed user will be updated. If the user_id is provided, the role of the auth'ed user or api key must be an admin (1) or owner (2) of the organization.

        Args:
            tr_organization: The organization id to use for the request
            role: Either 0 (user), 1 (admin), or 2 (owner). If not provided, the current role will be used. The auth'ed user must have a role greater than or equal to the role being assigned.
            user_id: The id of the user to update, if not provided, the auth'ed user will be updated. If provided, the role of the auth'ed user or api key must be an admin (1) or owner (2) of the organization.

        Returns:
            Response data
        """
        path = f"/api/user"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = {
            "role": role if role is not None else None,
            "user_id": user_id if user_id is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self._make_request(
            method="PUT",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_user_api_keys(
        self,
    ) -> Any:
        """Get the api keys which belong to the auth'ed user. The actual api key values are not returned, only the ids, names, and creation dates.

        Returns:
            Response data
        """
        path = f"/api/user/api_key"
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

    def delete_user_api_key(
        self,
        api_key_id: str,
    ) -> Any:
        """Delete an api key for the auth'ed user.

        Args:
            api_key_id: The id of the api key to delete

        Returns:
            Response data
        """
        path = f"/api/user/api_key/{api_key_id}"
        params = {}
        headers = {}
        json_data = None

        response = self._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
