from typing import Any, Dict, List, Optional, Union
from ..trieve_api_client import TrieveAPIClient
from ...models.models import *


class DatasetClient(TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def create_dataset(
        self,
        tr_organization: str,
        dataset_name: str,
        server_configuration: Optional[DatasetConfigurationDTO] = None,
        tracking_id: Optional[str] = None,
    ) -> Any:
        """
        Dataset will be created in the org specified via the TR-Organization header. Auth'ed user must be an owner of the organization to create a dataset.

        Args:
            tr_organization: The organization id to use for the request
            dataset_name: Name of the dataset.
            server_configuration: Lets you specify the configuration for a dataset
            tracking_id: Optional tracking ID for the dataset. Can be used to track the dataset in external systems. Must be unique within the organization. Strongly recommended to not use a valid uuid value as that will not work with the TR-Dataset header.

        Returns:
            Response data
        """
        path = f"/api/dataset"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = {
            "dataset_name": dataset_name if dataset_name is not None else None,
            "server_configuration": (
                server_configuration if server_configuration is not None else None
            ),
            "tracking_id": tracking_id if tracking_id is not None else None,
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

    def update_dataset(
        self,
        tr_organization: str,
        dataset_id: Optional[str] = None,
        dataset_name: Optional[str] = None,
        new_tracking_id: Optional[str] = None,
        server_configuration: Optional[DatasetConfigurationDTO] = None,
        tracking_id: Optional[str] = None,
    ) -> Any:
        """
        One of id or tracking_id must be provided. The auth'ed user must be an owner of the organization to update a dataset.

        Args:
            tr_organization: The organization id to use for the request
            dataset_id: The id of the dataset you want to update.
            dataset_name: The new name of the dataset. Must be unique within the organization. If not provided, the name will not be updated.
            new_tracking_id: Optional new tracking ID for the dataset. Can be used to track the dataset in external systems. Must be unique within the organization. If not provided, the tracking ID will not be updated. Strongly recommended to not use a valid uuid value as that will not work with the TR-Dataset header.
            server_configuration: Lets you specify the configuration for a dataset
            tracking_id: The tracking ID of the dataset you want to update.

        Returns:
            Response data
        """
        path = f"/api/dataset"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = {
            "dataset_id": dataset_id if dataset_id is not None else None,
            "dataset_name": dataset_name if dataset_name is not None else None,
            "new_tracking_id": new_tracking_id if new_tracking_id is not None else None,
            "server_configuration": (
                server_configuration if server_configuration is not None else None
            ),
            "tracking_id": tracking_id if tracking_id is not None else None,
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

    def batch_create_datasets(
        self,
        tr_organization: str,
        datasets: List[CreateBatchDataset],
        upsert: Optional[bool] = None,
    ) -> Any:
        """
        Datasets will be created in the org specified via the TR-Organization header. Auth'ed user must be an owner of the organization to create datasets. If a tracking_id is ignored due to it already existing on the org, the response will not contain a dataset with that tracking_id and it can be assumed that a dataset with the missing tracking_id already exists.

        Args:
            tr_organization: The organization id to use for the request
            datasets: List of datasets to create
            upsert: Upsert when a dataset with one of the specified tracking_ids already exists. By default this is false and specified datasets with a tracking_id that already exists in the org will not be ignored. If true, the existing dataset will be updated with the new dataset's details.

        Returns:
            Response data
        """
        path = f"/api/dataset/batch_create_datasets"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = {
            "datasets": datasets if datasets is not None else None,
            "upsert": upsert if upsert is not None else None,
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

    def clear_dataset(
        self,
        tr_dataset: str,
        dataset_id: str,
    ) -> Any:
        """
        Removes all chunks, files, and groups from the dataset while retaining the analytics and dataset itself. The auth'ed user must be an owner of the organization to clear a dataset.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            dataset_id: The id of the dataset you want to clear.

        Returns:
            Response data
        """
        path = f"/api/dataset/clear/{dataset_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = None

        response = self._make_request(
            method="PUT",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_events(
        self,
        tr_dataset: str,
        event_types: Optional[List[EventTypeRequest]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Any:
        """
        Get events for the dataset specified by the TR-Dataset header.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            event_types: The types of events to get. Leave undefined to get all events.
            page: The page number to get. Default is 1.
            page_size: The number of items per page. Default is 10.

        Returns:
            Response data
        """
        path = f"/api/dataset/events"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "event_types": event_types if event_types is not None else None,
            "page": page if page is not None else None,
            "page_size": page_size if page_size is not None else None,
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

    def get_all_tags(
        self,
        tr_dataset: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Any:
        """
        Scroll through all tags in the dataset and get the number of chunks in the dataset with that tag plus the total number of unique tags for the whole datset.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            page: Page number to return, 1-indexed. Default is 1.
            page_size: Number of items to return per page. Default is 20.

        Returns:
            Response data
        """
        path = f"/api/dataset/get_all_tags"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "page": page if page is not None else None,
            "page_size": page_size if page_size is not None else None,
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

    def get_datasets_from_organization(
        self,
        tr_organization: str,
        organization_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Any:
        """
        Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_organization: The organization id to use for the request
            organization_id: id of the organization you want to retrieve datasets for
            limit: The number of records to return
            offset: The number of records to skip

        Returns:
            Response data
        """
        path = f"/api/dataset/organization/{organization_id}"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_pagefind_index_for_dataset(
        self,
        tr_dataset: str,
    ) -> Any:
        """
        Returns the root URL for your pagefind index, will error if pagefind is not enabled

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.

        Returns:
            Response data
        """
        path = f"/api/dataset/pagefind"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def create_pagefind_index_for_dataset(
        self,
        tr_dataset: str,
    ) -> Any:
        """
                Uses pagefind to index the dataset and store the result into a CDN for retrieval. The auth'ed
        user must be an admin of the organization to create a pagefind index for a dataset.

                Args:
                    tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.

                Returns:
                    Response data
        """
        path = f"/api/dataset/pagefind"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = None

        response = self._make_request(
            method="PUT",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_dataset_by_tracking_id(
        self,
        tr_organization: str,
        tracking_id: str,
    ) -> Any:
        """
        Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_organization: The organization id to use for the request
            tracking_id: The tracking id of the dataset you want to retrieve.

        Returns:
            Response data
        """
        path = f"/api/dataset/tracking_id/{tracking_id}"
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

    def delete_dataset_by_tracking_id(
        self,
        tr_dataset: str,
        tracking_id: str,
    ) -> Any:
        """
        Auth'ed user must be an owner of the organization to delete a dataset.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            tracking_id: The tracking id of the dataset you want to delete.

        Returns:
            Response data
        """
        path = f"/api/dataset/tracking_id/{tracking_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = None

        response = self._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_usage_by_dataset_id(
        self,
        tr_dataset: str,
        dataset_id: str,
    ) -> Any:
        """
        Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            dataset_id: The id of the dataset you want to retrieve usage for.

        Returns:
            Response data
        """
        path = f"/api/dataset/usage/{dataset_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_dataset(
        self,
        tr_dataset: str,
        dataset_id: str,
    ) -> Any:
        """
        Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            dataset_id: The id of the dataset you want to retrieve.

        Returns:
            Response data
        """
        path = f"/api/dataset/{dataset_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def delete_dataset(
        self,
        tr_dataset: str,
        dataset_id: str,
    ) -> Any:
        """
        Auth'ed user must be an owner of the organization to delete a dataset.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            dataset_id: The id of the dataset you want to delete.

        Returns:
            Response data
        """
        path = f"/api/dataset/{dataset_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = None

        response = self._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def create_etl_job(
        self,
        tr_dataset: str,
        prompt: str,
        include_images: Optional[bool] = None,
        model: Optional[str] = None,
        tag_enum: Optional[List[str]] = None,
    ) -> Any:
        """
        This endpoint is used to create a new ETL job for a dataset.

        Args:
            tr_dataset: The dataset id to use for the request
            prompt: No description provided
            include_images: No description provided
            model: No description provided
            tag_enum: No description provided

        Returns:
            Response data
        """
        path = f"/api/etl/create_job"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "include_images": include_images if include_images is not None else None,
            "model": model if model is not None else None,
            "prompt": prompt if prompt is not None else None,
            "tag_enum": tag_enum if tag_enum is not None else None,
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
