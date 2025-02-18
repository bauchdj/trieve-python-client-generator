from typing import Any, Dict, List, Optional, Union
from src.trieve_api_client import TrieveAPIClient
from models.models import *

class OrganizationClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def create_organization(
        self,
        name: str,
    ) -> Any:
        """
        Create a new organization. The auth'ed user who creates the organization will be the default owner of the organization.

        Args:
            name: The arbitrary name which will be used to identify the organization. This name must be unique.

        Returns:
            Response data
        """
        path = f"/api/organization"
        params = None
        headers = None
        json_data = {
            "name": name if name is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def update_organization(
        self,
        tr_organization: str,
        name: Optional[str] = None,
        partner_configuration: Optional[Any] = None,
    ) -> Any:
        """
        Update an organization. Only the owner of the organization can update it.

        Args:
            tr_organization: The organization id to use for the request
            name: The new name of the organization. If not provided, the name will not be updated.
            partner_configuration: New details for the partnership configuration. If not provided, the partnership configuration will not be updated.

        Returns:
            Response data
        """
        path = f"/api/organization"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = {
            "name": name if name is not None else None,
            "partner_configuration": partner_configuration if partner_configuration is not None else None,
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

    def get_organization_api_keys(
        self,
        tr_organization: str,
    ) -> Any:
        """
        Get the api keys which belong to the organization. The actual api key values are not returned, only the ids, names, and creation dates.

        Args:
            tr_organization: The organization id to use for the request.

        Returns:
            Response data
        """
        path = f"/api/organization/api_key"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def create_organization_api_key(
        self,
        tr_organization: str,
        name: str,
        role: int,
        dataset_ids: Optional[List[str]] = None,
        default_params: Optional[ApiKeyRequestParams] = None,
        expires_at: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ) -> Any:
        """
        Create a new api key for the organization. Successful response will contain the newly created api key.

        Args:
            tr_organization: The organization id to use for the request.
            name: The name which will be assigned to the new api key.
            role: The role which will be assigned to the new api key. Either 0 (read), 1 (Admin) or 2 (Owner). The auth'ed user must have a role greater than or equal to the role being assigned.
            dataset_ids: The dataset ids which the api key will have access to. If not provided or empty, the api key will have access to all datasets in the dataset.
            default_params: The default parameters which will be forcibly used when the api key is given on a request. If not provided, the api key will not have default parameters.
            expires_at: The expiration date of the api key. If not provided, the api key will not expire. This should be provided in UTC time.
            scopes: The routes which the api key will have access to. If not provided or empty, the api key will have access to all routes. Specify the routes as a list of strings. For example, ["GET /api/dataset", "POST /api/dataset"].

        Returns:
            Response data
        """
        path = f"/api/organization/api_key"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = {
            "dataset_ids": dataset_ids if dataset_ids is not None else None,
            "default_params": default_params if default_params is not None else None,
            "expires_at": expires_at if expires_at is not None else None,
            "name": name if name is not None else None,
            "role": role if role is not None else None,
            "scopes": scopes if scopes is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def delete_organization_api_key(
        self,
        api_key_id: str,
        tr_organization: str,
    ) -> Any:
        """
        Delete an api key for the auth'ed organization.

        Args:
            api_key_id: The id of the api key to delete
            tr_organization: The organization id to use for the request.

        Returns:
            Response data
        """
        path = f"/api/organization/api_key/{api_key_id}"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = None

        response = self._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def update_all_org_dataset_configs(
        self,
        tr_organization: str,
        dataset_config: Any,
    ) -> Any:
        """
        Update the configurations for all datasets in an organization. Only the specified keys in the configuration object will be changed per dataset such that you can preserve dataset unique values. Auth'ed user or api key must have an owner role for the specified organization.

        Args:
            tr_organization: The organization id to use for the request
            dataset_config: The new configuration for all datasets in the organization. Only the specified keys in the configuration object will be changed per dataset such that you can preserve dataset unique values.

        Returns:
            Response data
        """
        path = f"/api/organization/update_dataset_configs"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = {
            "dataset_config": dataset_config if dataset_config is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_organization_usage(
        self,
        tr_organization: str,
        organization_id: str,
    ) -> Any:
        """
        Fetch the current usage specification of an organization by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_organization: The organization id to use for the request
            organization_id: The id of the organization you want to fetch the usage of.

        Returns:
            Response data
        """
        path = f"/api/organization/usage/{organization_id}"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_organization_users(
        self,
        tr_organization: str,
        organization_id: str,
    ) -> Any:
        """
        Fetch the users of an organization by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_organization: The organization id to use for the request
            organization_id: The id of the organization you want to fetch the users of.

        Returns:
            Response data
        """
        path = f"/api/organization/users/{organization_id}"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_organization(
        self,
        tr_organization: str,
        organization_id: str,
    ) -> Any:
        """
        Fetch the details of an organization by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_organization: The organization id to use for the request
            organization_id: The id of the organization you want to fetch.

        Returns:
            Response data
        """
        path = f"/api/organization/{organization_id}"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def delete_organization(
        self,
        tr_organization: str,
        organization_id: str,
    ) -> Any:
        """
        Delete an organization by its id. The auth'ed user must be an owner of the organization to delete it.

        Args:
            tr_organization: The organization id to use for the request
            organization_id: The id of the organization you want to fetch.

        Returns:
            Response data
        """
        path = f"/api/organization/{organization_id}"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = None

        response = self._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
