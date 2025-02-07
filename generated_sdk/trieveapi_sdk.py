from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
import requests
from models import *  # Generated models

ResponseT = TypeVar("ResponseT")


class HttpSDK:
    """Base class for HTTP SDK implementations."""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        )

    def _build_url(self, path: str) -> str:
        """Build the full URL for an API endpoint."""
        return f"{self.base_url}{path}"

    def _prepare_headers(
        self, header_params: Dict[str, str], locals_dict: Dict[str, Any]
    ) -> Dict[str, str]:
        """Prepare headers from parameters."""
        headers = {}
        for header_name, param_name in header_params.items():
            if locals_dict.get(param_name) is not None:
                headers[header_name] = str(locals_dict[param_name])
        return headers

    def _prepare_payload(self, payload_class: Any, locals_dict: Dict[str, Any]) -> str:
        """Prepare request payload from parameters."""
        payload_data = {
            param_name: value
            for param_name, value in locals_dict.items()
            if value is not None
            and param_name not in ["self", "headers", "url"]
            and not param_name.upper().startswith(("TR_", "X_"))
        }
        payload = payload_class(**payload_data)
        return payload.model_dump_json()

    def _handle_response(
        self, response: requests.Response, response_model: Any = None
    ) -> Any:
        """Handle the API response and raise appropriate exceptions."""
        try:
            response.raise_for_status()
            data = response.json()
            if response_model:
                return response_model.model_validate(data)
            return data
        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and "message" in error_data:
                    error_msg = error_data["message"]
            except:
                pass
            raise Exception(f"HTTP {response.status_code}: {error_msg}")

    def _request(
        self,
        method: str,
        path: str,
        header_params: Dict[str, str],
        payload_class: Any,
        response_model: Any,
        locals_dict: Dict[str, Any],
    ) -> Any:
        """Make an HTTP request with proper error handling."""
        url = self._build_url(path)
        headers = self._prepare_headers(header_params, locals_dict)
        json_data = self._prepare_payload(payload_class, locals_dict)
        response = self.session.request(method, url, data=json_data, headers=headers)
        return self._handle_response(response, response_model)


class TrieveAPISDK(HttpSDK):
    def __init__(self, api_key: str, base_url: str = "https://api.trieve.ai"):
        super().__init__(api_key, base_url)

    def send_ctr_data(
        self,
        TR_Dataset: str,
        ctr_type: CTRType,
        position: int,
        request_id: str,
        clicked_chunk_id: Optional[str] = None,
        clicked_chunk_tracking_id: Optional[str] = None,
        metadata: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send CTR Data

        This route allows you to send clickstream data to the system. Clickstream data is used to fine-tune the re-ranking of search results and recommendations.
        """
        return self._request(
            method="put",
            path="/api/analytics/ctr",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CTRDataRequestBody,
            response_model=None,
            locals_dict=locals(),
        )

    def send_event_data(
        self,
        TR_Dataset: str,
    ) -> Dict[str, Any]:
        """
        Send User Event Data

        This route allows you to send user event data to the system.
        """
        return self._request(
            method="put",
            path="/api/analytics/events",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=EventTypes,
            response_model=None,
            locals_dict=locals(),
        )

    def get_all_events(
        self,
        filter: Optional[EventAnalyticsFilter] = None,
        page: Optional[int] = None,
    ) -> GetEventsResponseBody:
        """
        Get All User Events

        This route allows you to view all user events.
        """
        return self._request(
            method="post",
            path="/api/analytics/events/all",
            header_params={},
            payload_class=GetEventsRequestBody,
            response_model=GetEventsResponseBody,
            locals_dict=locals(),
        )

    def get_ctr_analytics(
        self,
        TR_Dataset: str,
    ) -> CTRAnalyticsResponse:
        """
        Get CTR Analytics

        This route allows you to view the CTR analytics for a dataset.
        """
        return self._request(
            method="post",
            path="/api/analytics/events/ctr",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CTRAnalytics,
            response_model=CTRAnalyticsResponse,
            locals_dict=locals(),
        )

    def get_event_by_id(
        self,
        TR_Dataset: str,
        event_id: str,
    ) -> EventData:
        """
        Get User Event By ID

        This route allows you to view an user event by its ID. You can pass in any type of event and get the details for that event.
        """
        return self._request(
            method="get",
            path="/api/analytics/events/{event_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=EventData,
            locals_dict=locals(),
        )

    def get_rag_analytics(
        self,
        TR_Dataset: str,
    ) -> RAGAnalyticsResponse:
        """
        Get RAG Analytics

        This route allows you to view the RAG analytics for a dataset.
        """
        return self._request(
            method="post",
            path="/api/analytics/rag",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=RAGAnalytics,
            response_model=RAGAnalyticsResponse,
            locals_dict=locals(),
        )

    def set_rag_query_rating(
        self,
        TR_Dataset: str,
        query_id: str,
        rating: int,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Rate RAG

        This route allows you to Rate a RAG query.
        """
        return self._request(
            method="put",
            path="/api/analytics/rag",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=RateQueryRequest,
            response_model=None,
            locals_dict=locals(),
        )

    def get_recommendation_analytics(
        self,
        TR_Dataset: str,
    ) -> RecommendationAnalyticsResponse:
        """
        Get Recommendation Analytics

        This route allows you to view the recommendation analytics for a dataset.
        """
        return self._request(
            method="post",
            path="/api/analytics/recommendations",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=RecommendationAnalytics,
            response_model=RecommendationAnalyticsResponse,
            locals_dict=locals(),
        )

    def get_search_analytics(
        self,
        TR_Dataset: str,
    ) -> SearchAnalyticsResponse:
        """
        Get Search Analytics

        This route allows you to view the search analytics for a dataset.
        """
        return self._request(
            method="post",
            path="/api/analytics/search",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=SearchAnalytics,
            response_model=SearchAnalyticsResponse,
            locals_dict=locals(),
        )

    def set_search_query_rating(
        self,
        TR_Dataset: str,
        query_id: str,
        rating: int,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Rate Search

        This route allows you to Rate a search query.
        """
        return self._request(
            method="put",
            path="/api/analytics/search",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=RateQueryRequest,
            response_model=None,
            locals_dict=locals(),
        )

    def get_cluster_analytics(
        self,
        TR_Dataset: str,
    ) -> ClusterAnalyticsResponse:
        """
        Get Cluster Analytics

        This route allows you to view the cluster analytics for a dataset.
        """
        return self._request(
            method="post",
            path="/api/analytics/search/cluster",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=ClusterAnalytics,
            response_model=ClusterAnalyticsResponse,
            locals_dict=locals(),
        )

    def get_top_datasets(
        self,
        TR_Organization: str,
        type: TopDatasetsRequestTypes,
        date_range: Optional[DateRange] = None,
    ) -> Dict[str, Any]:
        """
        Get Top Datasets

        This route allows you to view the top datasets for a given type.
        """
        return self._request(
            method="post",
            path="/api/analytics/top",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=GetTopDatasetsRequestBody,
            response_model=None,
            locals_dict=locals(),
        )

    def login(
        self,
        inv_code: Optional[str] = None,
        organization_id: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Login

        This will redirect you to the OAuth provider for authentication with email/pass, SSO, Google, Github, etc.
        """
        return self._request(
            method="get",
            path="/api/auth",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def logout(
        self,
    ) -> Dict[str, Any]:
        """
        Logout

        Invalidate your current auth credential stored typically stored in a cookie. This does not invalidate your API key.
        """
        return self._request(
            method="delete",
            path="/api/auth",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def callback(
        self,
    ) -> SlimUser:
        """
        OpenID Connect callback

        This is the callback route for the OAuth provider, it should not be called directly. Redirects to browser with set-cookie header.
        """
        return self._request(
            method="get",
            path="/api/auth/callback",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=SlimUser,
            locals_dict=locals(),
        )

    def get_me(
        self,
    ) -> SlimUser:
        """
        Get Me

        Get the user corresponding to your current auth credentials.
        """
        return self._request(
            method="get",
            path="/api/auth/me",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=SlimUser,
            locals_dict=locals(),
        )

    def create_chunk(
        self,
        TR_Dataset: str,
    ) -> ReturnQueuedChunk:
        """
                Create or Upsert Chunk or Chunks

                Create new chunk(s). If the chunk has the same tracking_id as an existing chunk, the request will fail. Once a chunk is created, it can be searched for using the search endpoint.
        If uploading in bulk, the maximum amount of chunks that can be uploaded at once is 120 chunks. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="post",
            path="/api/chunk",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CreateChunkReqPayloadEnum,
            response_model=ReturnQueuedChunk,
            locals_dict=locals(),
        )

    def update_chunk(
        self,
        TR_Dataset: str,
        chunk_html: Optional[str] = None,
        chunk_id: Optional[str] = None,
        convert_html_to_text: Optional[bool] = None,
        fulltext_boost: Optional[FullTextBoost] = None,
        group_ids: Optional[List[str]] = None,
        group_tracking_ids: Optional[List[str]] = None,
        image_urls: Optional[List[str]] = None,
        link: Optional[str] = None,
        location: Optional[GeoInfo] = None,
        metadata: Optional[str] = None,
        num_value: Optional[float] = None,
        semantic_boost: Optional[SemanticBoost] = None,
        tag_set: Optional[List[str]] = None,
        time_stamp: Optional[str] = None,
        tracking_id: Optional[str] = None,
        weight: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Update Chunk

        Update a chunk. If you try to change the tracking_id of the chunk to have the same tracking_id as an existing chunk, the request will fail. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="put",
            path="/api/chunk",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=UpdateChunkReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def bulk_delete_chunk(
        self,
        TR_Dataset: str,
        filter: ChunkFilter,
    ) -> Dict[str, Any]:
        """
        Bulk Delete Chunks

        Delete multiple chunks using a filter. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="delete",
            path="/api/chunk",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=BulkDeleteChunkPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def autocomplete(
        self,
        TR_Dataset: str,
        query: Union[SearchModalities, str],
        search_type: SearchMethod,
        X_API_Version: Optional[str] = None,
        content_only: Optional[bool] = None,
        extend_results: Optional[bool] = None,
        filters: Optional[ChunkFilter] = None,
        highlight_options: Optional[HighlightOptions] = None,
        page_size: Optional[int] = None,
        remove_stop_words: Optional[bool] = None,
        score_threshold: Optional[float] = None,
        scoring_options: Optional[ScoringOptions] = None,
        slim_chunks: Optional[bool] = None,
        sort_options: Optional[SortOptions] = None,
        typo_options: Optional[TypoOptions] = None,
        use_quote_negated_terms: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> SearchResponseTypes:
        """
        Autocomplete

        This route provides the primary autocomplete functionality for the API. This prioritize prefix matching with semantic or full-text search.
        """
        return self._request(
            method="post",
            path="/api/chunk/autocomplete",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=AutocompleteReqPayload,
            response_model=SearchResponseTypes,
            locals_dict=locals(),
        )

    def count_chunks(
        self,
        TR_Dataset: str,
        query: Union[QueryTypes, SearchModalities, list[MultiQuery], str],
        search_type: CountSearchMethod,
        filters: Optional[ChunkFilter] = None,
        limit: Optional[int] = None,
        score_threshold: Optional[float] = None,
        use_quote_negated_terms: Optional[bool] = None,
    ) -> CountChunkQueryResponseBody:
        """
        Count chunks above threshold

        This route can be used to determine the number of chunk results that match a search query including score threshold and filters. It may be high latency for large limits. There is a dataset configuration imposed restriction on the maximum limit value (default 10,000) which is used to prevent DDOS attacks. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="post",
            path="/api/chunk/count",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CountChunksReqPayload,
            response_model=CountChunkQueryResponseBody,
            locals_dict=locals(),
        )

    def generate_off_chunks(
        self,
        TR_Dataset: str,
        chunk_ids: List[str],
        prev_messages: List[ChatMessageProxy],
        audio_input: Optional[str] = None,
        context_options: Optional[ContextOptions] = None,
        frequency_penalty: Optional[float] = None,
        highlight_results: Optional[bool] = None,
        image_config: Optional[ImageConfig] = None,
        image_urls: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        prompt: Optional[str] = None,
        stop_tokens: Optional[List[str]] = None,
        stream_response: Optional[bool] = None,
        temperature: Optional[float] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        RAG on Specified Chunks

        This endpoint exists as an alternative to the topic+message resource pattern where our Trieve handles chat memory. With this endpoint, the user is responsible for providing the context window and the prompt and the conversation is ephemeral.
        """
        return self._request(
            method="post",
            path="/api/chunk/generate",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=GenerateOffChunksReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def get_recommended_chunks(
        self,
        TR_Dataset: str,
        X_API_Version: Optional[str] = None,
        filters: Optional[ChunkFilter] = None,
        limit: Optional[int] = None,
        negative_chunk_ids: Optional[List[str]] = None,
        negative_tracking_ids: Optional[List[str]] = None,
        positive_chunk_ids: Optional[List[str]] = None,
        positive_tracking_ids: Optional[List[str]] = None,
        recommend_type: Optional[RecommendType] = None,
        slim_chunks: Optional[bool] = None,
        strategy: Optional[RecommendationStrategy] = None,
        user_id: Optional[str] = None,
    ) -> RecommendResponseTypes:
        """
        Get Recommended Chunks

        Get recommendations of chunks similar to the positive samples in the request and dissimilar to the negative.
        """
        return self._request(
            method="post",
            path="/api/chunk/recommend",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=RecommendChunksRequest,
            response_model=RecommendResponseTypes,
            locals_dict=locals(),
        )

    def search_chunks(
        self,
        TR_Dataset: str,
        query: Union[QueryTypes, SearchModalities, list[MultiQuery], str],
        search_type: SearchMethod,
        X_API_Version: Optional[str] = None,
        content_only: Optional[bool] = None,
        filters: Optional[ChunkFilter] = None,
        get_total_pages: Optional[bool] = None,
        highlight_options: Optional[HighlightOptions] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        remove_stop_words: Optional[bool] = None,
        score_threshold: Optional[float] = None,
        scoring_options: Optional[ScoringOptions] = None,
        slim_chunks: Optional[bool] = None,
        sort_options: Optional[SortOptions] = None,
        typo_options: Optional[TypoOptions] = None,
        use_quote_negated_terms: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> SearchResponseTypes:
        """
        Search

        This route provides the primary search functionality for the API. It can be used to search for chunks by semantic similarity, full-text similarity, or a combination of both. Results' `chunk_html` values will be modified with `<mark><b>` or custom specified tags for sub-sentence highlighting.
        """
        return self._request(
            method="post",
            path="/api/chunk/search",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=SearchChunksReqPayload,
            response_model=SearchResponseTypes,
            locals_dict=locals(),
        )

    def split_html_content(
        self,
        chunk_html: str,
        body_remove_strings: Optional[List[str]] = None,
        heading_remove_strings: Optional[List[str]] = None,
    ) -> SplitHtmlResponse:
        """
                Split HTML Content into Chunks

                This endpoint receives a single html string and splits it into chunks based on the headings and
        body content. The headings are split based on heading html tags. chunk_html has a maximum size
        of 256Kb.
        """
        return self._request(
            method="post",
            path="/api/chunk/split",
            header_params={},
            payload_class=ChunkHtmlContentReqPayload,
            response_model=SplitHtmlResponse,
            locals_dict=locals(),
        )

    def get_suggested_queries(
        self,
        TR_Dataset: str,
        context: Optional[str] = None,
        filters: Optional[ChunkFilter] = None,
        query: Optional[str] = None,
        search_type: Optional[SearchMethod] = None,
        suggestion_type: Optional[SuggestType] = None,
        suggestions_to_create: Optional[int] = None,
    ) -> SuggestedQueriesResponse:
        """
        Generate suggested queries

        This endpoint will generate 3 suggested queries based off a hybrid search using RAG with the query provided in the request body and return them as a JSON object.
        """
        return self._request(
            method="post",
            path="/api/chunk/suggestions",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=SuggestedQueriesReqPayload,
            response_model=SuggestedQueriesResponse,
            locals_dict=locals(),
        )

    def update_chunk_by_tracking_id(
        self,
        TR_Dataset: str,
        tracking_id: str,
        chunk_html: Optional[str] = None,
        convert_html_to_text: Optional[bool] = None,
        group_ids: Optional[List[str]] = None,
        group_tracking_ids: Optional[List[str]] = None,
        link: Optional[str] = None,
        metadata: Optional[str] = None,
        time_stamp: Optional[str] = None,
        weight: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Update Chunk By Tracking Id

        Update a chunk by tracking_id. This is useful for when you are coordinating with an external system and want to use the tracking_id to identify the chunk. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="put",
            path="/api/chunk/tracking_id/update",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=UpdateChunkByTrackingIdData,
            response_model=None,
            locals_dict=locals(),
        )

    def get_chunk_by_tracking_id(
        self,
        TR_Dataset: str,
        tracking_id: str,
        X_API_Version: Optional[str] = None,
    ) -> ChunkReturnTypes:
        """
        Get Chunk By Tracking Id

        Get a singular chunk by tracking_id. This is useful for when you are coordinating with an external system and want to use your own id as the primary reference for a chunk.
        """
        return self._request(
            method="get",
            path="/api/chunk/tracking_id/{tracking_id}",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=Dict[str, Any],
            response_model=ChunkReturnTypes,
            locals_dict=locals(),
        )

    def delete_chunk_by_tracking_id(
        self,
        TR_Dataset: str,
        tracking_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Chunk By Tracking Id

        Delete a chunk by tracking_id. This is useful for when you are coordinating with an external system and want to use the tracking_id to identify the chunk. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="delete",
            path="/api/chunk/tracking_id/{tracking_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_chunk_by_id(
        self,
        TR_Dataset: str,
        chunk_id: str,
        X_API_Version: Optional[str] = None,
    ) -> ChunkReturnTypes:
        """
        Get Chunk By Id

        Get a singular chunk by id.
        """
        return self._request(
            method="get",
            path="/api/chunk/{chunk_id}",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=Dict[str, Any],
            response_model=ChunkReturnTypes,
            locals_dict=locals(),
        )

    def delete_chunk(
        self,
        TR_Dataset: str,
        chunk_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Chunk

        Delete a chunk by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="delete",
            path="/api/chunk/{chunk_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def create_chunk_group(
        self,
        TR_Dataset: str,
    ) -> CreateChunkGroupResponseEnum:
        """
        Create or Upsert Group or Groups

        Create new chunk_group(s). This is a way to group chunks together. If you try to create a chunk_group with the same tracking_id as an existing chunk_group, this operation will fail. Only 1000 chunk groups can be created at a time. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="post",
            path="/api/chunk_group",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CreateChunkGroupReqPayloadEnum,
            response_model=CreateChunkGroupResponseEnum,
            locals_dict=locals(),
        )

    def update_chunk_group(
        self,
        TR_Dataset: str,
        description: Optional[str] = None,
        group_id: Optional[str] = None,
        metadata: Optional[str] = None,
        name: Optional[str] = None,
        tag_set: Optional[List[str]] = None,
        tracking_id: Optional[str] = None,
        update_chunks: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Update Group

        Update a chunk_group. One of group_id or tracking_id must be provided. If you try to change the tracking_id to one that already exists, this operation will fail. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="put",
            path="/api/chunk_group",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=UpdateChunkGroupReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def add_chunk_to_group(
        self,
        TR_Dataset: str,
        group_id: str,
        chunk_id: Optional[str] = None,
        chunk_tracking_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add Chunk to Group

        Route to add a chunk to a group. One of chunk_id or chunk_tracking_id must be provided. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="post",
            path="/api/chunk_group/chunk/{group_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=AddChunkToGroupReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def remove_chunk_from_group(
        self,
        TR_Dataset: str,
        group_id: str,
        chunk_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Remove Chunk from Group

        Route to remove a chunk from a group. Auth'ed user or api key must be an admin or owner of the dataset's organization to remove a chunk from a group.
        """
        return self._request(
            method="delete",
            path="/api/chunk_group/chunk/{group_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_groups_for_chunks(
        self,
        TR_Dataset: str,
        chunk_ids: Optional[List[str]] = None,
        chunk_tracking_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get Groups for Chunks

        Route to get the groups that a chunk is in.
        """
        return self._request(
            method="post",
            path="/api/chunk_group/chunks",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=GetGroupsForChunksReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def count_group_chunks(
        self,
        TR_Dataset: str,
        group_id: Optional[str] = None,
        group_tracking_id: Optional[str] = None,
    ) -> GetChunkGroupCountResponse:
        """
        Count Chunks in a Group

        Route to get the number of chunks that is in a group
        """
        return self._request(
            method="post",
            path="/api/chunk_group/count",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=GetChunkGroupCountRequest,
            response_model=GetChunkGroupCountResponse,
            locals_dict=locals(),
        )

    def search_over_groups(
        self,
        TR_Dataset: str,
        query: Union[QueryTypes, SearchModalities, list[MultiQuery], str],
        search_type: SearchMethod,
        X_API_Version: Optional[str] = None,
        filters: Optional[ChunkFilter] = None,
        get_total_pages: Optional[bool] = None,
        group_size: Optional[int] = None,
        highlight_options: Optional[HighlightOptions] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        remove_stop_words: Optional[bool] = None,
        score_threshold: Optional[float] = None,
        slim_chunks: Optional[bool] = None,
        sort_options: Optional[SortOptions] = None,
        typo_options: Optional[TypoOptions] = None,
        use_quote_negated_terms: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> SearchOverGroupsResponseTypes:
        """
        Search Over Groups

        This route allows you to get groups as results instead of chunks. Each group returned will have the matching chunks sorted by similarity within the group. This is useful for when you want to get groups of chunks which are similar to the search query. If choosing hybrid search, the top chunk of each group will be re-ranked using scores from a cross encoder model. Compatible with semantic, fulltext, or hybrid search modes.
        """
        return self._request(
            method="post",
            path="/api/chunk_group/group_oriented_search",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=SearchOverGroupsReqPayload,
            response_model=SearchOverGroupsResponseTypes,
            locals_dict=locals(),
        )

    def get_recommended_groups(
        self,
        TR_Dataset: str,
        X_API_Version: Optional[str] = None,
        filters: Optional[ChunkFilter] = None,
        group_size: Optional[int] = None,
        limit: Optional[int] = None,
        negative_group_ids: Optional[List[str]] = None,
        negative_group_tracking_ids: Optional[List[str]] = None,
        positive_group_ids: Optional[List[str]] = None,
        positive_group_tracking_ids: Optional[List[str]] = None,
        recommend_type: Optional[RecommendType] = None,
        slim_chunks: Optional[bool] = None,
        strategy: Optional[RecommendationStrategy] = None,
        user_id: Optional[str] = None,
    ) -> RecommendGroupsResponse:
        """
        Get Recommended Groups

        Route to get recommended groups. This route will return groups which are similar to the groups in the request body. You must provide at least one positive group id or group tracking id.
        """
        return self._request(
            method="post",
            path="/api/chunk_group/recommend",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=RecommendGroupsReqPayload,
            response_model=RecommendGroupsResponse,
            locals_dict=locals(),
        )

    def search_within_group(
        self,
        TR_Dataset: str,
        query: Union[QueryTypes, SearchModalities, list[MultiQuery], str],
        search_type: SearchMethod,
        X_API_Version: Optional[str] = None,
        content_only: Optional[bool] = None,
        filters: Optional[ChunkFilter] = None,
        get_total_pages: Optional[bool] = None,
        group_id: Optional[str] = None,
        group_tracking_id: Optional[str] = None,
        highlight_options: Optional[HighlightOptions] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        remove_stop_words: Optional[bool] = None,
        score_threshold: Optional[float] = None,
        slim_chunks: Optional[bool] = None,
        sort_options: Optional[SortOptions] = None,
        typo_options: Optional[TypoOptions] = None,
        use_quote_negated_terms: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> SearchGroupResponseTypes:
        """
        Search Within Group

        This route allows you to search only within a group. This is useful for when you only want search results to contain chunks which are members of a specific group. If choosing hybrid search, the results will be re-ranked using scores from a cross encoder model.
        """
        return self._request(
            method="post",
            path="/api/chunk_group/search",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=SearchWithinGroupReqPayload,
            response_model=SearchGroupResponseTypes,
            locals_dict=locals(),
        )

    def get_chunks_in_group_by_tracking_id(
        self,
        TR_Dataset: str,
        group_tracking_id: str,
        page: int,
        X_API_Version: Optional[str] = None,
    ) -> GetChunksInGroupResponse:
        """
        Get Chunks in Group by Tracking ID

        Route to get all chunks for a group. The response is paginated, with each page containing 10 chunks. Support for custom page size is coming soon. Page is 1-indexed.
        """
        return self._request(
            method="get",
            path="/api/chunk_group/tracking_id/{group_tracking_id}/{page}",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=Dict[str, Any],
            response_model=GetChunksInGroupResponse,
            locals_dict=locals(),
        )

    def get_group_by_tracking_id(
        self,
        TR_Dataset: str,
        tracking_id: str,
    ) -> ChunkGroupAndFileId:
        """
                Get Group by Tracking ID

                Fetch the group with the given tracking id.
        get_group_by_tracking_id
        """
        return self._request(
            method="get",
            path="/api/chunk_group/tracking_id/{tracking_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=ChunkGroupAndFileId,
            locals_dict=locals(),
        )

    def add_chunk_to_group_by_tracking_id(
        self,
        TR_Dataset: str,
        tracking_id: str,
        chunk_id: Optional[str] = None,
        chunk_tracking_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add Chunk to Group by Tracking ID

        Route to add a chunk to a group by tracking id. One of chunk_id or chunk_tracking_id must be provided. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="post",
            path="/api/chunk_group/tracking_id/{tracking_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=AddChunkToGroupReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def delete_group_by_tracking_id(
        self,
        TR_Dataset: str,
        delete_chunks: bool,
        tracking_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Group by Tracking ID

        Delete a chunk_group with the given tracking id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="delete",
            path="/api/chunk_group/tracking_id/{tracking_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_chunk_group(
        self,
        TR_Dataset: str,
        group_id: str,
    ) -> ChunkGroupAndFileId:
        """
        Get Group

        Fetch the group with the given id.
        """
        return self._request(
            method="get",
            path="/api/chunk_group/{group_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=ChunkGroupAndFileId,
            locals_dict=locals(),
        )

    def delete_chunk_group(
        self,
        TR_Dataset: str,
        delete_chunks: bool,
        group_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Group

        This will delete a chunk_group. If you set delete_chunks to true, it will also delete the chunks within the group. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="delete",
            path="/api/chunk_group/{group_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_chunks_in_group(
        self,
        TR_Dataset: str,
        group_id: str,
        page: Optional[int],
        X_API_Version: Optional[str] = None,
    ) -> GetChunksInGroupResponse:
        """
        Get Chunks in Group

        Route to get all chunks for a group. The response is paginated, with each page containing 10 chunks. Page is 1-indexed.
        """
        return self._request(
            method="get",
            path="/api/chunk_group/{group_id}/{page}",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=Dict[str, Any],
            response_model=GetChunksInGroupResponse,
            locals_dict=locals(),
        )

    def get_chunks_by_ids(
        self,
        TR_Dataset: str,
        ids: List[str],
        X_API_Version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get Chunks By Ids

        Get multiple chunks by multiple ids.
        """
        return self._request(
            method="post",
            path="/api/chunks",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=GetChunksData,
            response_model=None,
            locals_dict=locals(),
        )

    def scroll_dataset_chunks(
        self,
        TR_Dataset: str,
        filters: Optional[ChunkFilter] = None,
        offset_chunk_id: Optional[str] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[SortByField] = None,
    ) -> ScrollChunksResponseBody:
        """
        Scroll Chunks

        Get paginated chunks from your dataset with filters and custom sorting. If sort by is not specified, the results will sort by the id's of the chunks in ascending order. Sort by and offset_chunk_id cannot be used together; if you want to scroll with a sort by then you need to use a must_not filter with the ids you have already seen. There is a limit of 1000 id's in a must_not filter at a time.
        """
        return self._request(
            method="post",
            path="/api/chunks/scroll",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=ScrollChunksReqPayload,
            response_model=ScrollChunksResponseBody,
            locals_dict=locals(),
        )

    def get_chunks_by_tracking_ids(
        self,
        TR_Dataset: str,
        tracking_ids: List[str],
        X_API_Version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get Chunks By Tracking Ids

        Get multiple chunks by ids.
        """
        return self._request(
            method="post",
            path="/api/chunks/tracking",
            header_params={
                "TR-Dataset": "TR_Dataset",
                "X-API-Version": "X_API_Version",
            },
            payload_class=GetTrackingChunksData,
            response_model=None,
            locals_dict=locals(),
        )

    def create_dataset(
        self,
        TR_Organization: str,
        dataset_name: str,
        crawl_options: Optional[CrawlOptions] = None,
        server_configuration: Optional[DatasetConfigurationDTO] = None,
        tracking_id: Optional[str] = None,
    ) -> Dataset:
        """
        Create Dataset

        Dataset will be created in the org specified via the TR-Organization header. Auth'ed user must be an owner of the organization to create a dataset.
        """
        return self._request(
            method="post",
            path="/api/dataset",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=CreateDatasetReqPayload,
            response_model=Dataset,
            locals_dict=locals(),
        )

    def update_dataset(
        self,
        TR_Organization: str,
        crawl_options: Optional[CrawlOptions] = None,
        dataset_id: Optional[str] = None,
        dataset_name: Optional[str] = None,
        new_tracking_id: Optional[str] = None,
        server_configuration: Optional[DatasetConfigurationDTO] = None,
        tracking_id: Optional[str] = None,
    ) -> Dataset:
        """
        Update Dataset by ID or Tracking ID

        One of id or tracking_id must be provided. The auth'ed user must be an owner of the organization to update a dataset.
        """
        return self._request(
            method="put",
            path="/api/dataset",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=UpdateDatasetReqPayload,
            response_model=Dataset,
            locals_dict=locals(),
        )

    def batch_create_datasets(
        self,
        TR_Organization: str,
        datasets: List[CreateBatchDataset],
        upsert: Optional[bool] = None,
    ) -> Datasets:
        """
        Batch Create Datasets

        Datasets will be created in the org specified via the TR-Organization header. Auth'ed user must be an owner of the organization to create datasets. If a tracking_id is ignored due to it already existing on the org, the response will not contain a dataset with that tracking_id and it can be assumed that a dataset with the missing tracking_id already exists.
        """
        return self._request(
            method="post",
            path="/api/dataset/batch_create_datasets",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=CreateDatasetBatchReqPayload,
            response_model=Datasets,
            locals_dict=locals(),
        )

    def clear_dataset(
        self,
        TR_Dataset: str,
        dataset_id: str,
    ) -> Dict[str, Any]:
        """
        Clear Dataset

        Removes all chunks, files, and groups from the dataset while retaining the analytics and dataset itself. The auth'ed user must be an owner of the organization to clear a dataset.
        """
        return self._request(
            method="put",
            path="/api/dataset/clear/{dataset_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_dataset_crawl_options(
        self,
        TR_Dataset: str,
        dataset_id: str,
    ) -> GetCrawlOptionsResponse:
        """
        Get Dataset Crawl Options

        Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/dataset/crawl_options/{dataset_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=GetCrawlOptionsResponse,
            locals_dict=locals(),
        )

    def get_events(
        self,
        TR_Dataset: str,
        event_types: Optional[List[EventTypeRequest]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> EventReturn:
        """
        Get events for the dataset

        Get events for the dataset specified by the TR-Dataset header.
        """
        return self._request(
            method="post",
            path="/api/dataset/events",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=GetEventsData,
            response_model=EventReturn,
            locals_dict=locals(),
        )

    def get_dataset_files_handler(
        self,
        TR_Dataset: str,
        dataset_id: str,
        page: int,
    ) -> FileData:
        """
        Get Files for Dataset

        Get all files which belong to a given dataset specified by the dataset_id parameter. 10 files are returned per page.
        """
        return self._request(
            method="get",
            path="/api/dataset/files/{dataset_id}/{page}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=FileData,
            locals_dict=locals(),
        )

    def get_all_tags(
        self,
        TR_Dataset: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> GetAllTagsResponse:
        """
        Get All Tags

        Scroll through all tags in the dataset and get the number of chunks in the dataset with that tag plus the total number of unique tags for the whole datset.
        """
        return self._request(
            method="post",
            path="/api/dataset/get_all_tags",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=GetAllTagsReqPayload,
            response_model=GetAllTagsResponse,
            locals_dict=locals(),
        )

    def get_groups_for_dataset(
        self,
        TR_Dataset: str,
        dataset_id: str,
        page: int,
    ) -> GroupData:
        """
        Get Groups for Dataset

        Fetch the groups which belong to a dataset specified by its id.
        """
        return self._request(
            method="get",
            path="/api/dataset/groups/{dataset_id}/{page}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=GroupData,
            locals_dict=locals(),
        )

    def get_datasets_from_organization(
        self,
        TR_Organization: str,
        organization_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get Datasets from Organization

        Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/dataset/organization/{organization_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_pagefind_index_for_dataset(
        self,
        TR_Dataset: str,
    ) -> GetPagefindIndexResponse:
        """
        Get Pagefind Index Url for Dataset

        Returns the root URL for your pagefind index, will error if pagefind is not enabled
        """
        return self._request(
            method="get",
            path="/api/dataset/pagefind",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=GetPagefindIndexResponse,
            locals_dict=locals(),
        )

    def create_pagefind_index_for_dataset(
        self,
        TR_Dataset: str,
    ) -> Dict[str, Any]:
        """
                Create Pagefind Index for Dataset

                Uses pagefind to index the dataset and store the result into a CDN for retrieval. The auth'ed
        user must be an admin of the organization to create a pagefind index for a dataset.
        """
        return self._request(
            method="put",
            path="/api/dataset/pagefind",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_dataset_by_tracking_id(
        self,
        TR_Organization: str,
        tracking_id: str,
    ) -> Dataset:
        """
        Get Dataset by Tracking ID

        Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/dataset/tracking_id/{tracking_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=Dataset,
            locals_dict=locals(),
        )

    def delete_dataset_by_tracking_id(
        self,
        TR_Dataset: str,
        tracking_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Dataset by Tracking ID

        Auth'ed user must be an owner of the organization to delete a dataset.
        """
        return self._request(
            method="delete",
            path="/api/dataset/tracking_id/{tracking_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_usage_by_dataset_id(
        self,
        TR_Dataset: str,
        dataset_id: str,
    ) -> DatasetUsageCount:
        """
        Get Usage By Dataset ID

        Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/dataset/usage/{dataset_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=DatasetUsageCount,
            locals_dict=locals(),
        )

    def get_dataset(
        self,
        TR_Dataset: str,
        dataset_id: str,
    ) -> Dataset:
        """
        Get Dataset By ID

        Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/dataset/{dataset_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=Dataset,
            locals_dict=locals(),
        )

    def delete_dataset(
        self,
        TR_Dataset: str,
        dataset_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Dataset

        Auth'ed user must be an owner of the organization to delete a dataset.
        """
        return self._request(
            method="delete",
            path="/api/dataset/{dataset_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def create_etl_job(
        self,
        TR_Dataset: str,
        prompt: str,
        include_images: Optional[bool] = None,
        model: Optional[str] = None,
        tag_enum: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create ETL Job

        This endpoint is used to create a new ETL job for a dataset.
        """
        return self._request(
            method="post",
            path="/api/etl/create_job",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CreateSchemaReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def upload_file_handler(
        self,
        TR_Dataset: str,
        base64_file: str,
        file_name: str,
        create_chunks: Optional[bool] = None,
        description: Optional[str] = None,
        group_tracking_id: Optional[str] = None,
        link: Optional[str] = None,
        metadata: Optional[str] = None,
        pdf2md_options: Optional[Pdf2MdOptions] = None,
        rebalance_chunks: Optional[bool] = None,
        split_avg: Optional[bool] = None,
        split_delimiters: Optional[List[str]] = None,
        tag_set: Optional[List[str]] = None,
        target_splits_per_chunk: Optional[int] = None,
        time_stamp: Optional[str] = None,
    ) -> UploadFileResponseBody:
        """
        Upload File

        Upload a file to S3 bucket attached to your dataset. You can select between a naive chunking strategy where the text is extracted with Apache Tika and split into segments with a target number of segments per chunk OR you can use a vision LLM to convert the file to markdown and create chunks per page. Auth'ed user must be an admin or owner of the dataset's organization to upload a file.
        """
        return self._request(
            method="post",
            path="/api/file",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=UploadFileReqPayload,
            response_model=UploadFileResponseBody,
            locals_dict=locals(),
        )

    def create_presigned_url_for_csv_jsonl(
        self,
        TR_Dataset: str,
        file_name: str,
        description: Optional[str] = None,
        fulltext_boost_factor: Optional[float] = None,
        group_tracking_id: Optional[str] = None,
        link: Optional[str] = None,
        mappings: Optional[list[ChunkReqPayloadMapping]] = None,
        metadata: Optional[str] = None,
        semantic_boost_factor: Optional[float] = None,
        tag_set: Optional[List[str]] = None,
        time_stamp: Optional[str] = None,
        upsert_by_tracking_id: Optional[bool] = None,
    ) -> CreatePresignedUrlForCsvJsonResponseBody:
        """
        Create Presigned CSV/JSONL S3 PUT URL

        This route is useful for uploading very large CSV or JSONL files. Once you have completed the upload, chunks will be automatically created from the file for each line in the CSV or JSONL file. The chunks will be indexed and searchable. Auth'ed user must be an admin or owner of the dataset's organization to upload a file.
        """
        return self._request(
            method="post",
            path="/api/file/csv_or_jsonl",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CreatePresignedUrlForCsvJsonlReqPayload,
            response_model=CreatePresignedUrlForCsvJsonResponseBody,
            locals_dict=locals(),
        )

    def upload_html_page(
        self,
        data: Document,
        metadata: str,
        scrapeid: str,
    ) -> Dict[str, Any]:
        """
        Upload HTML Page

        Chunk HTML by headings and queue for indexing into the specified dataset.
        """
        return self._request(
            method="post",
            path="/api/file/html_page",
            header_params={},
            payload_class=UploadHtmlPageReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def get_file_handler(
        self,
        TR_Dataset: str,
        file_id: str,
        content_type: Optional[str] = None,
    ) -> FileDTO:
        """
        Get File Signed URL

        Get a signed s3 url corresponding to the file_id requested such that you can download the file.
        """
        return self._request(
            method="get",
            path="/api/file/{file_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=FileDTO,
            locals_dict=locals(),
        )

    def delete_file_handler(
        self,
        TR_Dataset: str,
        delete_chunks: bool,
        file_id: str,
    ) -> Dict[str, Any]:
        """
        Delete File

        Delete a file from S3 attached to the server based on its id. This will disassociate chunks from the file, but only delete them all together if you specify delete_chunks to be true. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="delete",
            path="/api/file/{file_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Health Check

        Confirmation that the service is healthy and can make embedding vectors
        """
        return self._request(
            method="get",
            path="/api/health",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def post_invitation(
        self,
        TR_Organization: str,
        app_url: str,
        email: str,
        redirect_uri: str,
        user_role: int,
    ) -> Dict[str, Any]:
        """
        Send Invitation

        Invitations act as a way to invite users to join an organization. After a user is invited, they will automatically be added to the organization with the role specified in the invitation once they set their. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="post",
            path="/api/invitation",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=InvitationData,
            response_model=None,
            locals_dict=locals(),
        )

    def delete_invitation(
        self,
        TR_Organization: str,
        invitation_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Invitation

        Delete an invitation by id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="delete",
            path="/api/invitation/{invitation_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_invitations(
        self,
        TR_Organization: str,
        organization_id: str,
    ) -> Dict[str, Any]:
        """
        Get Invitations

        Get all invitations for the organization. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/invitations/{organization_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def create_message(
        self,
        TR_Dataset: str,
        topic_id: str,
        audio_input: Optional[str] = None,
        concat_user_messages_query: Optional[bool] = None,
        context_options: Optional[ContextOptions] = None,
        filters: Optional[ChunkFilter] = None,
        highlight_options: Optional[HighlightOptions] = None,
        image_urls: Optional[List[str]] = None,
        llm_options: Optional[LLMOptions] = None,
        new_message_content: Optional[str] = None,
        no_result_message: Optional[str] = None,
        only_include_docs_used: Optional[bool] = None,
        page_size: Optional[int] = None,
        score_threshold: Optional[float] = None,
        search_query: Optional[str] = None,
        search_type: Optional[SearchMethod] = None,
        sort_options: Optional[SortOptions] = None,
        use_group_search: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create message

        Create message. Messages are attached to topics in order to coordinate memory of gen-AI chat sessions.Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="post",
            path="/api/message",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CreateMessageReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def edit_message(
        self,
        TR_Dataset: str,
        message_sort_order: int,
        topic_id: str,
        audio_input: Optional[str] = None,
        concat_user_messages_query: Optional[bool] = None,
        context_options: Optional[ContextOptions] = None,
        filters: Optional[ChunkFilter] = None,
        highlight_options: Optional[HighlightOptions] = None,
        image_urls: Optional[List[str]] = None,
        llm_options: Optional[LLMOptions] = None,
        new_message_content: Optional[str] = None,
        no_result_message: Optional[str] = None,
        only_include_docs_used: Optional[bool] = None,
        page_size: Optional[int] = None,
        score_threshold: Optional[float] = None,
        search_query: Optional[str] = None,
        search_type: Optional[SearchMethod] = None,
        sort_options: Optional[SortOptions] = None,
        use_group_search: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Edit message

        Edit message which exists within the topic's chat history. This will delete the message and replace it with a new message. The new message will be generated by the AI based on the new content provided in the request body. The response will include Chunks first on the stream if the topic is using RAG. The structure will look like `[chunks]||mesage`. See docs.trieve.ai for more information. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="put",
            path="/api/message",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=EditMessageReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def regenerate_message(
        self,
        TR_Dataset: str,
        topic_id: str,
        concat_user_messages_query: Optional[bool] = None,
        context_options: Optional[ContextOptions] = None,
        filters: Optional[ChunkFilter] = None,
        highlight_options: Optional[HighlightOptions] = None,
        llm_options: Optional[LLMOptions] = None,
        no_result_message: Optional[str] = None,
        only_include_docs_used: Optional[bool] = None,
        page_size: Optional[int] = None,
        score_threshold: Optional[float] = None,
        search_query: Optional[str] = None,
        search_type: Optional[SearchMethod] = None,
        sort_options: Optional[SortOptions] = None,
        use_group_search: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Regenerate message

        Regenerate the assistant response to the last user message of a topic. This will delete the last message and replace it with a new message. The response will include Chunks first on the stream if the topic is using RAG. The structure will look like `[chunks]||mesage`. See docs.trieve.ai for more information. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="delete",
            path="/api/message",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=RegenerateMessageReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def regenerate_message_patch(
        self,
        TR_Dataset: str,
        topic_id: str,
        concat_user_messages_query: Optional[bool] = None,
        context_options: Optional[ContextOptions] = None,
        filters: Optional[ChunkFilter] = None,
        highlight_options: Optional[HighlightOptions] = None,
        llm_options: Optional[LLMOptions] = None,
        no_result_message: Optional[str] = None,
        only_include_docs_used: Optional[bool] = None,
        page_size: Optional[int] = None,
        score_threshold: Optional[float] = None,
        search_query: Optional[str] = None,
        search_type: Optional[SearchMethod] = None,
        sort_options: Optional[SortOptions] = None,
        use_group_search: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Regenerate message

        Regenerate the assistant response to the last user message of a topic. This will delete the last message and replace it with a new message. The response will include Chunks first on the stream if the topic is using RAG. The structure will look like `[chunks]||mesage`. See docs.trieve.ai for more information. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="patch",
            path="/api/message",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=RegenerateMessageReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def get_message_by_id(
        self,
        TR_Dataset: str,
        message_id: str,
    ) -> Message:
        """
        Get a message by its ID

        Quickly get the full object for a given message. From the message, you can get the topic and all messages which exist on that topic.
        """
        return self._request(
            method="get",
            path="/api/message/{message_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=Message,
            locals_dict=locals(),
        )

    def get_all_topic_messages(
        self,
        TR_Dataset: str,
        messages_topic_id: str,
    ) -> Dict[str, Any]:
        """
        Get all messages for a given topic

        If the topic is a RAG topic then the response will include Chunks first on each message. The structure will look like `[chunks]||mesage`. See docs.trieve.ai for more information.
        """
        return self._request(
            method="get",
            path="/api/messages/{messages_topic_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def create_organization(
        self,
        name: str,
    ) -> Organization:
        """
        Create Organization

        Create a new organization. The auth'ed user who creates the organization will be the default owner of the organization.
        """
        return self._request(
            method="post",
            path="/api/organization",
            header_params={},
            payload_class=CreateOrganizationReqPayload,
            response_model=Organization,
            locals_dict=locals(),
        )

    def update_organization(
        self,
        TR_Organization: str,
        name: Optional[str] = None,
    ) -> Organization:
        """
        Update Organization

        Update an organization. Only the owner of the organization can update it.
        """
        return self._request(
            method="put",
            path="/api/organization",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=UpdateOrganizationReqPayload,
            response_model=Organization,
            locals_dict=locals(),
        )

    def get_organization_api_keys(
        self,
        TR_Organization: str,
    ) -> Dict[str, Any]:
        """
        Get Organization Api Keys

        Get the api keys which belong to the organization. The actual api key values are not returned, only the ids, names, and creation dates.
        """
        return self._request(
            method="get",
            path="/api/organization/api_key",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def create_organization_api_key(
        self,
        TR_Organization: str,
        name: str,
        role: int,
        dataset_ids: Optional[List[str]] = None,
        default_params: Optional[ApiKeyRequestParams] = None,
        expires_at: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ) -> CreateApiKeyResponse:
        """
        Create Organization Api Key

        Create a new api key for the organization. Successful response will contain the newly created api key.
        """
        return self._request(
            method="post",
            path="/api/organization/api_key",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=CreateApiKeyReqPayload,
            response_model=CreateApiKeyResponse,
            locals_dict=locals(),
        )

    def delete_organization_api_key(
        self,
        TR_Organization: str,
        api_key_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Organization Api Key

        Delete an api key for the auth'ed organization.
        """
        return self._request(
            method="delete",
            path="/api/organization/api_key/{api_key_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def update_all_org_dataset_configs(
        self,
        TR_Organization: str,
        dataset_config: str,
    ) -> Dict[str, Any]:
        """
        Update All Dataset Configurations

        Update the configurations for all datasets in an organization. Only the specified keys in the configuration object will be changed per dataset such that you can preserve dataset unique values. Auth'ed user or api key must have an owner role for the specified organization.
        """
        return self._request(
            method="post",
            path="/api/organization/update_dataset_configs",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=UpdateAllOrgDatasetConfigsReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def get_organization_usage(
        self,
        TR_Organization: str,
        organization_id: str,
    ) -> OrganizationUsageCount:
        """
        Get Organization Usage

        Fetch the current usage specification of an organization by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/organization/usage/{organization_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=OrganizationUsageCount,
            locals_dict=locals(),
        )

    def get_organization_users(
        self,
        TR_Organization: str,
        organization_id: str,
    ) -> Dict[str, Any]:
        """
        Get Organization Users

        Fetch the users of an organization by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/organization/users/{organization_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_organization(
        self,
        TR_Organization: str,
        organization_id: str,
    ) -> OrganizationWithSubAndPlan:
        """
        Get Organization

        Fetch the details of an organization by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/organization/{organization_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=OrganizationWithSubAndPlan,
            locals_dict=locals(),
        )

    def delete_organization(
        self,
        TR_Organization: str,
        organization_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Organization

        Delete an organization by its id. The auth'ed user must be an owner of the organization to delete it.
        """
        return self._request(
            method="delete",
            path="/api/organization/{organization_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def public_page(
        self,
        dataset_id: str,
    ) -> Dict[str, Any]:
        """ """
        return self._request(
            method="get",
            path="/api/public_page/{dataset_id}",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def create_setup_checkout_session(
        self,
        organization_id: str,
    ) -> CreateSetupCheckoutSessionResPayload:
        """
        Create checkout session setup

        Create a checkout session (setup)
        """
        return self._request(
            method="post",
            path="/api/stripe/checkout/setup/{organization_id}",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=CreateSetupCheckoutSessionResPayload,
            locals_dict=locals(),
        )

    def get_all_invoices(
        self,
        organization_id: str,
    ) -> Dict[str, Any]:
        """
        Get All Invoices

        Get a list of all invoices
        """
        return self._request(
            method="get",
            path="/api/stripe/invoices/{organization_id}",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def direct_to_payment_link(
        self,
        organization_id: str,
        plan_id: str,
    ) -> Dict[str, Any]:
        """
        Checkout

        Get a 303 SeeOther redirect link to the stripe checkout page for the plan and organization
        """
        return self._request(
            method="get",
            path="/api/stripe/payment_link/{plan_id}/{organization_id}",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_all_plans(
        self,
    ) -> Dict[str, Any]:
        """
        Get All Plans

        Get a list of all plans
        """
        return self._request(
            method="get",
            path="/api/stripe/plans",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def cancel_subscription(
        self,
        TR_Organization: str,
        subscription_id: str,
    ) -> Dict[str, Any]:
        """
        Cancel Subscription

        Cancel a subscription by its id
        """
        return self._request(
            method="delete",
            path="/api/stripe/subscription/{subscription_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def update_subscription_plan(
        self,
        TR_Organization: str,
        plan_id: str,
        subscription_id: str,
    ) -> Dict[str, Any]:
        """
        Update Subscription Plan

        Update a subscription to a new plan
        """
        return self._request(
            method="patch",
            path="/api/stripe/subscription_plan/{subscription_id}/{plan_id}",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def create_topic(
        self,
        TR_Dataset: str,
        owner_id: str,
        first_user_message: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Topic:
        """
        Create Topic

        Create a new chat topic. Topics are attached to a owner_id's and act as a coordinator for conversation message history of gen-AI chat sessions. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="post",
            path="/api/topic",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CreateTopicReqPayload,
            response_model=Topic,
            locals_dict=locals(),
        )

    def update_topic(
        self,
        TR_Dataset: str,
        name: str,
        topic_id: str,
    ) -> Dict[str, Any]:
        """
        Update Topic

        Update an existing chat topic. Currently, only the name of the topic can be updated. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="put",
            path="/api/topic",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=UpdateTopicReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def clone_topic(
        self,
        TR_Dataset: str,
        owner_id: str,
        topic_id: str,
        name: Optional[str] = None,
    ) -> Topic:
        """
        Clone Topic

        Create a new chat topic from a `topic_id`. The new topic will be attched to the owner_id and act as a coordinator for conversation message history of gen-AI chat sessions. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="post",
            path="/api/topic/clone",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=CloneTopicReqPayload,
            response_model=Topic,
            locals_dict=locals(),
        )

    def get_all_topics_for_owner_id(
        self,
        TR_Dataset: str,
        owner_id: str,
    ) -> Dict[str, Any]:
        """
        Get All Topics for Owner ID

        Get all topics belonging to an arbitary owner_id. This is useful for managing message history and chat sessions. It is common to use a browser fingerprint or your user's id as the owner_id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="get",
            path="/api/topic/owner/{owner_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def delete_topic(
        self,
        TR_Dataset: str,
        topic_id: str,
    ) -> Dict[str, Any]:
        """
        Delete Topic

        Delete an existing chat topic. When a topic is deleted, all associated chat messages are also deleted. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.
        """
        return self._request(
            method="delete",
            path="/api/topic/{topic_id}",
            header_params={"TR-Dataset": "TR_Dataset"},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def update_user(
        self,
        TR_Organization: str,
        role: int,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update User Org Role

        Update a user's information for the org specified via header. If the user_id is not provided, the auth'ed user will be updated. If the user_id is provided, the role of the auth'ed user or api key must be an admin (1) or owner (2) of the organization.
        """
        return self._request(
            method="put",
            path="/api/user",
            header_params={"TR-Organization": "TR_Organization"},
            payload_class=UpdateUserOrgRoleReqPayload,
            response_model=None,
            locals_dict=locals(),
        )

    def get_user_api_keys(
        self,
    ) -> Dict[str, Any]:
        """
        Get User Api Keys

        Get the api keys which belong to the auth'ed user. The actual api key values are not returned, only the ids, names, and creation dates.
        """
        return self._request(
            method="get",
            path="/api/user/api_key",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def delete_user_api_key(
        self,
        api_key_id: str,
    ) -> Dict[str, Any]:
        """
        Delete User Api Key

        Delete an api key for the auth'ed user.
        """
        return self._request(
            method="delete",
            path="/api/user/api_key/{api_key_id}",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )

    def get_metrics(
        self,
    ) -> Dict[str, Any]:
        """
        Get Prometheus Metrics

        This route allows you to view the number of items in each queue in the Prometheus format.
        """
        return self._request(
            method="post",
            path="/metrics",
            header_params={},
            payload_class=Dict[str, Any],
            response_model=None,
            locals_dict=locals(),
        )
