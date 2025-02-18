from typing import Any, Dict, List, Optional, Union
from src.trieve_api_client import TrieveAPIClient
from models.models import *

class TopicClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def create_topic(
        self,
        tr_dataset: str,
        owner_id: str,
        first_user_message: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Any:
        """
        Create a new chat topic. Topics are attached to a owner_id's and act as a coordinator for conversation message history of gen-AI chat sessions. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            owner_id: The owner_id of the topic. This is typically a browser fingerprint or your user's id. It is used to group topics together for a user.
            first_user_message: The first message which will belong to the topic. The topic name is generated based on this message similar to how it works in the OpenAI chat UX if a name is not explicitly provided on the name request body key.
            name: The name of the topic. If this is not provided, the topic name is generated from the first_user_message.

        Returns:
            Response data
        """
        path = f"/api/topic"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "first_user_message": first_user_message if first_user_message is not None else None,
            "name": name if name is not None else None,
            "owner_id": owner_id if owner_id is not None else None,
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

    def update_topic(
        self,
        tr_dataset: str,
        name: str,
        topic_id: str,
    ) -> Any:
        """
        Update an existing chat topic. Currently, only the name of the topic can be updated. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            name: The new name of the topic. A name is not generated from this field, it is used as-is.
            topic_id: The id of the topic to target.

        Returns:
            Response data
        """
        path = f"/api/topic"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "name": name if name is not None else None,
            "topic_id": topic_id if topic_id is not None else None,
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

    def clone_topic(
        self,
        tr_dataset: str,
        owner_id: str,
        topic_id: str,
        name: Optional[str] = None,
    ) -> Any:
        """
        Create a new chat topic from a `topic_id`. The new topic will be attched to the owner_id and act as a coordinator for conversation message history of gen-AI chat sessions. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            owner_id: The owner_id of the topic. This is typically a browser fingerprint or your user's id. It is used to group topics together for a user.
            topic_id: The topic_id to clone from
            name: The name of the topic. If this is not provided, the topic name is the same as the previous topic

        Returns:
            Response data
        """
        path = f"/api/topic/clone"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "name": name if name is not None else None,
            "owner_id": owner_id if owner_id is not None else None,
            "topic_id": topic_id if topic_id is not None else None,
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

    def get_all_topics_for_owner_id(
        self,
        owner_id: str,
        tr_dataset: str,
    ) -> Any:
        """
        Get all topics belonging to an arbitary owner_id. This is useful for managing message history and chat sessions. It is common to use a browser fingerprint or your user's id as the owner_id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            owner_id: The owner_id to get topics of; A common approach is to use a browser fingerprint or your user's id
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.

        Returns:
            Response data
        """
        path = f"/api/topic/owner/{owner_id}"
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

    def delete_topic(
        self,
        tr_dataset: str,
        topic_id: str,
    ) -> Any:
        """
        Delete an existing chat topic. When a topic is deleted, all associated chat messages are also deleted. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            topic_id: The id of the topic you want to delete.

        Returns:
            Response data
        """
        path = f"/api/topic/{topic_id}"
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
