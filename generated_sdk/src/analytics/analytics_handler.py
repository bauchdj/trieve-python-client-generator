from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ...models.models import *

if TYPE_CHECKING:
    from ..trieve_api import TrieveApi


class Analytics:
    def __init__(self, parent: "TrieveApi"):
        """
        Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API.

        Args:
            parent: The parent client to use for the requests
        """
        self.parent = parent

    def send_ctr_data(
        self,
        tr_dataset: str,
        ctr_type: CTRType,
        position: int,
        request_id: str,
        clicked_chunk_id: Optional[str] = None,
        clicked_chunk_tracking_id: Optional[str] = None,
        metadata: Optional[Any] = None,
    ) -> Any:
        """
        This route allows you to send clickstream data to the system. Clickstream data is used to fine-tune the re-ranking of search results and recommendations.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            ctr_type: No description provided
            position: The position of the clicked chunk
            request_id: The request id for the CTR data
            clicked_chunk_id: The ID of chunk that was clicked
            clicked_chunk_tracking_id: The tracking ID of the chunk that was clicked
            metadata: Any metadata you want to include with the event i.e. action, user_id, etc.

        Returns:
            Response data
        """
        path = f"/api/analytics/ctr"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "clicked_chunk_id": (
                clicked_chunk_id if clicked_chunk_id is not None else None
            ),
            "clicked_chunk_tracking_id": (
                clicked_chunk_tracking_id
                if clicked_chunk_tracking_id is not None
                else None
            ),
            "ctr_type": ctr_type if ctr_type is not None else None,
            "metadata": metadata if metadata is not None else None,
            "position": position if position is not None else None,
            "request_id": request_id if request_id is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self.parent._make_request(
            method="PUT",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def send_event_data(
        self,
        tr_dataset: str,
        request_body: Optional[EventTypes] = None,
    ) -> Any:
        """
        This route allows you to send user event data to the system.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            request_body: Request body

        Returns:
            Response data
        """
        path = f"/api/analytics/events"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = request_body.model_dump() if request_body else None

        response = self.parent._make_request(
            method="PUT",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_all_events(
        self,
        filter: Optional[EventAnalyticsFilter] = None,
        page: Optional[int] = None,
    ) -> Any:
        """
        This route allows you to view all user events.

        Args:
            filter: Filter to apply to the events when querying for them
            page: Page of results to return

        Returns:
            Response data
        """
        path = f"/api/analytics/events/all"
        params = None
        headers = None
        json_data = {
            "filter": filter if filter is not None else None,
            "page": page if page is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self.parent._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_ctr_analytics(
        self,
        tr_dataset: str,
        request_body: Optional[CTRAnalytics] = None,
    ) -> Any:
        """
        This route allows you to view the CTR analytics for a dataset.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            request_body: Request body

        Returns:
            Response data
        """
        path = f"/api/analytics/events/ctr"
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

    def get_event_by_id(
        self,
        tr_dataset: str,
        event_id: str,
    ) -> Any:
        """
        This route allows you to view an user event by its ID. You can pass in any type of event and get the details for that event.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            event_id: The event id to use for the request

        Returns:
            Response data
        """
        path = f"/api/analytics/events/{event_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = None

        response = self.parent._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_rag_analytics(
        self,
        tr_dataset: str,
        request_body: Optional[RAGAnalytics] = None,
    ) -> Any:
        """
        This route allows you to view the RAG analytics for a dataset.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            request_body: Request body

        Returns:
            Response data
        """
        path = f"/api/analytics/rag"
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

    def set_rag_query_rating(
        self,
        tr_dataset: str,
        query_id: str,
        rating: int,
        note: Optional[str] = None,
    ) -> Any:
        """
        This route allows you to Rate a RAG query.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            query_id: No description provided
            rating: No description provided
            note: No description provided

        Returns:
            Response data
        """
        path = f"/api/analytics/rag"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "note": note if note is not None else None,
            "query_id": query_id if query_id is not None else None,
            "rating": rating if rating is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self.parent._make_request(
            method="PUT",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_recommendation_analytics(
        self,
        tr_dataset: str,
        request_body: Optional[RecommendationAnalytics] = None,
    ) -> Any:
        """
        This route allows you to view the recommendation analytics for a dataset.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            request_body: Request body

        Returns:
            Response data
        """
        path = f"/api/analytics/recommendations"
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

    def set_search_query_rating(
        self,
        tr_dataset: str,
        query_id: str,
        rating: int,
        note: Optional[str] = None,
    ) -> Any:
        """
        This route allows you to Rate a search query.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            query_id: No description provided
            rating: No description provided
            note: No description provided

        Returns:
            Response data
        """
        path = f"/api/analytics/search"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "note": note if note is not None else None,
            "query_id": query_id if query_id is not None else None,
            "rating": rating if rating is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self.parent._make_request(
            method="PUT",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_cluster_analytics(
        self,
        tr_dataset: str,
        request_body: Optional[ClusterAnalytics] = None,
    ) -> Any:
        """
        This route allows you to view the cluster analytics for a dataset.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            request_body: Request body

        Returns:
            Response data
        """
        path = f"/api/analytics/search/cluster"
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

    def get_top_datasets(
        self,
        tr_organization: str,
        type: TopDatasetsRequestTypes,
        date_range: Optional[DateRange] = None,
    ) -> Any:
        """
        This route allows you to view the top datasets for a given type.

        Args:
            tr_organization: The organization id to use for the request
            type: No description provided
            date_range: DateRange is a JSON object which can be used to filter chunks by a range of dates. This leverages the time_stamp field on chunks in your dataset. You can specify this if you want values in a certain range. You must provide ISO 8601 combined date and time without timezone.

        Returns:
            Response data
        """
        path = f"/api/analytics/top"
        params = {}
        headers = {}
        if tr_organization is not None:
            headers["TR-Organization"] = tr_organization
        json_data = {
            "date_range": date_range if date_range is not None else None,
            "type": type if type is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self.parent._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
