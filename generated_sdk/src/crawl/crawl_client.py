from typing import Any, Dict, List, Optional, Union
from src.trieve_api_client import TrieveAPIClient
from models.models import *

class CrawlClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def get_crawl_requests_for_dataset(
        self,
        tr_dataset: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Any:
        """This endpoint is used to get all crawl requests for a dataset.

        Args:
            tr_dataset: The dataset id to use for the request
            page: The page number to retrieve
            limit: The number of items to retrieve per page

        Returns:
            Response data
        """
        path = f"/api/crawl"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def create_crawl(
        self,
        tr_dataset: str,
        crawl_options: CrawlOptions,
    ) -> Any:
        """This endpoint is used to create a new crawl request for a dataset. The request payload should contain the crawl options to use for the crawl.

        Args:
            tr_dataset: The dataset id to use for the request
            crawl_options: Options for setting up the crawl which will populate the dataset.

        Returns:
            Response data
        """
        path = f"/api/crawl"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "crawl_options": crawl_options if crawl_options is not None else None,
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

    def update_crawl_request(
        self,
        tr_dataset: str,
        crawl_id: str,
        crawl_options: CrawlOptions,
    ) -> Any:
        """This endpoint is used to update an existing crawl request for a dataset. The request payload should contain the crawl id and the crawl options to update for the crawl.

        Args:
            tr_dataset: The dataset id to use for the request
            crawl_id: Crawl ID to update
            crawl_options: Options for setting up the crawl which will populate the dataset.

        Returns:
            Response data
        """
        path = f"/api/crawl"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "crawl_id": crawl_id if crawl_id is not None else None,
            "crawl_options": crawl_options if crawl_options is not None else None,
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

    def delete_crawl_request(
        self,
        tr_dataset: str,
        crawl_id: str,
    ) -> Any:
        """This endpoint is used to delete an existing crawl request for a dataset. The request payload should contain the crawl id to delete.

        Args:
            tr_dataset: The dataset id to use for the request
            crawl_id: The id of the crawl to delete

        Returns:
            Response data
        """
        path = f"/api/crawl/{crawl_id}"
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
