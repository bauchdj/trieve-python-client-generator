from typing import Any, Dict, List, Optional, Union
from src.trieve_api_client import TrieveAPIClient
from models.models import *

class ChunkGroupClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def create_chunk_group(
        self,
        tr_dataset: str,
        request_body: Optional[CreateChunkGroupReqPayloadEnum] = None,
    ) -> Any:
        """
        Create new chunk_group(s). This is a way to group chunks together. If you try to create a chunk_group with the same tracking_id as an existing chunk_group, this operation will fail. Only 1000 chunk groups can be created at a time. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            request_body: Request body

        Returns:
            Response data
        """
        path = f"/api/chunk_group"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = request_body.model_dump() if request_body else None

        response = self._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def update_chunk_group(
        self,
        tr_dataset: str,
        description: Optional[str] = None,
        group_id: Optional[str] = None,
        metadata: Optional[Any] = None,
        name: Optional[str] = None,
        tag_set: Optional[List[str]] = None,
        tracking_id: Optional[str] = None,
        update_chunks: Optional[bool] = None,
    ) -> Any:
        """
        Update a chunk_group. One of group_id or tracking_id must be provided. If you try to change the tracking_id to one that already exists, this operation will fail. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            description: Description to assign to the chunk_group. Convenience field for you to avoid having to remember what the group is for. If not provided, the description will not be updated.
            group_id: Id of the chunk_group to update.
            metadata: Optional metadata to assign to the chunk_group. This is a JSON object that can store any additional information you want to associate with the chunks inside of the chunk_group.
            name: Name to assign to the chunk_group. Does not need to be unique. If not provided, the name will not be updated.
            tag_set: Optional tags to assign to the chunk_group. This is a list of strings that can be used to categorize the chunks inside the chunk_group.
            tracking_id: Tracking Id of the chunk_group to update.
            update_chunks: Flag to update the chunks in the group. If true, each chunk in the group will be updated
by appending the group's tags to the chunk's tags. Default is false.

        Returns:
            Response data
        """
        path = f"/api/chunk_group"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "description": description if description is not None else None,
            "group_id": group_id if group_id is not None else None,
            "metadata": metadata if metadata is not None else None,
            "name": name if name is not None else None,
            "tag_set": tag_set if tag_set is not None else None,
            "tracking_id": tracking_id if tracking_id is not None else None,
            "update_chunks": update_chunks if update_chunks is not None else None,
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

    def add_chunk_to_group(
        self,
        tr_dataset: str,
        group_id: str,
        chunk_id: Optional[str] = None,
        chunk_tracking_id: Optional[str] = None,
    ) -> Any:
        """
        Route to add a chunk to a group. One of chunk_id or chunk_tracking_id must be provided. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            group_id: Id of the group to add the chunk to as a bookmark
            chunk_id: Id of the chunk to make a member of the group.
            chunk_tracking_id: Tracking Id of the chunk to make a member of the group.

        Returns:
            Response data
        """
        path = f"/api/chunk_group/chunk/{group_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "chunk_id": chunk_id if chunk_id is not None else None,
            "chunk_tracking_id": chunk_tracking_id if chunk_tracking_id is not None else None,
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

    def remove_chunk_from_group(
        self,
        tr_dataset: str,
        group_id: str,
        chunk_id: Optional[str] = None,
    ) -> Any:
        """
        Route to remove a chunk from a group. Auth'ed user or api key must be an admin or owner of the dataset's organization to remove a chunk from a group.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            group_id: Id of the group you want to remove the chunk from.
            chunk_id: Id of the chunk you want to remove from the group

        Returns:
            Response data
        """
        path = f"/api/chunk_group/chunk/{group_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if chunk_id is not None:
            params["chunk_id"] = chunk_id
        json_data = {
            "chunk_id": chunk_id if chunk_id is not None else None,
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_groups_for_chunks(
        self,
        tr_dataset: str,
        chunk_ids: Optional[List[str]] = None,
        chunk_tracking_ids: Optional[List[str]] = None,
    ) -> Any:
        """
        Route to get the groups that a chunk is in.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            chunk_ids: No description provided
            chunk_tracking_ids: No description provided

        Returns:
            Response data
        """
        path = f"/api/chunk_group/chunks"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "chunk_ids": chunk_ids if chunk_ids is not None else None,
            "chunk_tracking_ids": chunk_tracking_ids if chunk_tracking_ids is not None else None,
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

    def count_group_chunks(
        self,
        tr_dataset: str,
        group_id: Optional[str] = None,
        group_tracking_id: Optional[str] = None,
    ) -> Any:
        """
        Route to get the number of chunks that is in a group

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            group_id: The Id of the group to get the count for, is not required if group_tracking_id is provided.
            group_tracking_id: The tracking id of the group to get the count for, is not required if group_id is provided.

        Returns:
            Response data
        """
        path = f"/api/chunk_group/count"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "group_id": group_id if group_id is not None else None,
            "group_tracking_id": group_tracking_id if group_tracking_id is not None else None,
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

    def search_over_groups(
        self,
        tr_dataset: str,
        query: QueryTypes,
        search_type: SearchMethod,
        x_api_version: Optional[APIVersion] = None,
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
    ) -> Any:
        """
        This route allows you to get groups as results instead of chunks. Each group returned will have the matching chunks sorted by similarity within the group. This is useful for when you want to get groups of chunks which are similar to the search query. If choosing hybrid search, the top chunk of each group will be re-ranked using scores from a cross encoder model. Compatible with semantic, fulltext, or hybrid search modes.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            query: No description provided
            search_type: No description provided
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
            filters: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.
            get_total_pages: Get total page count for the query accounting for the applied filters. Defaults to false, but can be set to true when the latency penalty is acceptable (typically 50-200ms).
            group_size: Group_size is the number of chunks to fetch for each group. The default is 3. If a group has less than group_size chunks, all chunks will be returned. If this is set to a large number, we recommend setting slim_chunks to true to avoid returning the content and chunk_html of the chunks so as to lower the amount of time required for content download and serialization.
            highlight_options: Highlight Options lets you specify different methods to highlight the chunks in the result set. If not specified, this defaults to the score of the chunks.
            page: Page of group results to fetch. Page is 1-indexed.
            page_size: Page size is the number of group results to fetch. The default is 10.
            remove_stop_words: If true, stop words (specified in server/src/stop-words.txt in the git repo) will be removed. Queries that are entirely stop words will be
preserved.
            score_threshold: Set score_threshold to a float to filter out chunks with a score below the threshold. This threshold applies before weight and bias modifications. If not specified, this defaults to 0.0.
            slim_chunks: Set slim_chunks to true to avoid returning the content and chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement (typicall 10-50ms). Default is false.
            sort_options: Sort Options lets you specify different methods to rerank the chunks in the result set. If not specified, this defaults to the score of the chunks.
            typo_options: Typo Options lets you specify different methods to correct typos in the query. If not specified, typos will not be corrected.
            use_quote_negated_terms: If true, quoted and - prefixed words will be parsed from the queries and used as required and negated words respectively. Default is false.
            user_id: The user_id is the id of the user who is making the request. This is used to track user interactions with the search results.

        Returns:
            Response data
        """
        path = f"/api/chunk_group/group_oriented_search"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = {
            "filters": filters if filters is not None else None,
            "get_total_pages": get_total_pages if get_total_pages is not None else None,
            "group_size": group_size if group_size is not None else None,
            "highlight_options": highlight_options if highlight_options is not None else None,
            "page": page if page is not None else None,
            "page_size": page_size if page_size is not None else None,
            "query": query if query is not None else None,
            "remove_stop_words": remove_stop_words if remove_stop_words is not None else None,
            "score_threshold": score_threshold if score_threshold is not None else None,
            "search_type": search_type if search_type is not None else None,
            "slim_chunks": slim_chunks if slim_chunks is not None else None,
            "sort_options": sort_options if sort_options is not None else None,
            "typo_options": typo_options if typo_options is not None else None,
            "use_quote_negated_terms": use_quote_negated_terms if use_quote_negated_terms is not None else None,
            "user_id": user_id if user_id is not None else None,
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

    def get_recommended_groups(
        self,
        tr_dataset: str,
        x_api_version: Optional[APIVersion] = None,
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
    ) -> Any:
        """
        Route to get recommended groups. This route will return groups which are similar to the groups in the request body. You must provide at least one positive group id or group tracking id.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
            filters: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.
            group_size: The number of chunks to fetch for each group. This is the number of chunks which will be returned in the response for each group. The default is 3. If this is set to a large number, we recommend setting slim_chunks to true to avoid returning the content and chunk_html of the chunks so as to reduce latency due to content download and serialization.
            limit: The number of groups to return. This is the number of groups which will be returned in the response. The default is 10.
            negative_group_ids: The ids of the groups to be used as negative examples for the recommendation. The groups in this array will be used to filter out similar groups.
            negative_group_tracking_ids: The ids of the groups to be used as negative examples for the recommendation. The groups in this array will be used to filter out similar groups.
            positive_group_ids: The ids of the groups to be used as positive examples for the recommendation. The groups in this array will be used to find similar groups.
            positive_group_tracking_ids: The ids of the groups to be used as positive examples for the recommendation. The groups in this array will be used to find similar groups.
            recommend_type: The type of recommendation to make. This lets you choose whether to recommend based off of `semantic` or `fulltext` similarity. The default is `semantic`.
            slim_chunks: Set slim_chunks to true to avoid returning the content and chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement (typicall 10-50ms). Default is false.
            strategy: Strategy to use for recommendations, either "average_vector" or "best_score". The default is "average_vector". The "average_vector" strategy will construct a single average vector from the positive and negative samples then use it to perform a pseudo-search. The "best_score" strategy is more advanced and navigates the HNSW with a heuristic of picking edges where the point is closer to the positive samples than it is the negatives.
            user_id: The user_id is the id of the user who is making the request. This is used to track user interactions with the rrecommendation results.

        Returns:
            Response data
        """
        path = f"/api/chunk_group/recommend"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = {
            "filters": filters if filters is not None else None,
            "group_size": group_size if group_size is not None else None,
            "limit": limit if limit is not None else None,
            "negative_group_ids": negative_group_ids if negative_group_ids is not None else None,
            "negative_group_tracking_ids": negative_group_tracking_ids if negative_group_tracking_ids is not None else None,
            "positive_group_ids": positive_group_ids if positive_group_ids is not None else None,
            "positive_group_tracking_ids": positive_group_tracking_ids if positive_group_tracking_ids is not None else None,
            "recommend_type": recommend_type if recommend_type is not None else None,
            "slim_chunks": slim_chunks if slim_chunks is not None else None,
            "strategy": strategy if strategy is not None else None,
            "user_id": user_id if user_id is not None else None,
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

    def search_within_group(
        self,
        tr_dataset: str,
        query: QueryTypes,
        search_type: SearchMethod,
        x_api_version: Optional[APIVersion] = None,
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
    ) -> Any:
        """
        This route allows you to search only within a group. This is useful for when you only want search results to contain chunks which are members of a specific group. If choosing hybrid search, the results will be re-ranked using scores from a cross encoder model.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            query: No description provided
            search_type: No description provided
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
            content_only: Set content_only to true to only returning the chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement (typically 10-50ms). Default is false.
            filters: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.
            get_total_pages: Get total page count for the query accounting for the applied filters. Defaults to false, but can be set to true when the latency penalty is acceptable (typically 50-200ms).
            group_id: Group specifies the group to search within. Results will only consist of chunks which are bookmarks within the specified group.
            group_tracking_id: Group_tracking_id specifies the group to search within by tracking id. Results will only consist of chunks which are bookmarks within the specified group. If both group_id and group_tracking_id are provided, group_id will be used.
            highlight_options: Highlight Options lets you specify different methods to highlight the chunks in the result set. If not specified, this defaults to the score of the chunks.
            page: The page of chunks to fetch. Page is 1-indexed.
            page_size: The page size is the number of chunks to fetch. This can be used to fetch more than 10 chunks at a time.
            remove_stop_words: If true, stop words (specified in server/src/stop-words.txt in the git repo) will be removed. Queries that are entirely stop words will be preserved.
            score_threshold: Set score_threshold to a float to filter out chunks with a score below the threshold. This threshold applies before weight and bias modifications. If not specified, this defaults to 0.0.
            slim_chunks: Set slim_chunks to true to avoid returning the content and chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement (typicall 10-50ms). Default is false.
            sort_options: Sort Options lets you specify different methods to rerank the chunks in the result set. If not specified, this defaults to the score of the chunks.
            typo_options: Typo Options lets you specify different methods to correct typos in the query. If not specified, typos will not be corrected.
            use_quote_negated_terms: If true, quoted and - prefixed words will be parsed from the queries and used as required and negated words respectively. Default is false.
            user_id: The user_id is the id of the user who is making the request. This is used to track user interactions with the search results.

        Returns:
            Response data
        """
        path = f"/api/chunk_group/search"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = {
            "content_only": content_only if content_only is not None else None,
            "filters": filters if filters is not None else None,
            "get_total_pages": get_total_pages if get_total_pages is not None else None,
            "group_id": group_id if group_id is not None else None,
            "group_tracking_id": group_tracking_id if group_tracking_id is not None else None,
            "highlight_options": highlight_options if highlight_options is not None else None,
            "page": page if page is not None else None,
            "page_size": page_size if page_size is not None else None,
            "query": query if query is not None else None,
            "remove_stop_words": remove_stop_words if remove_stop_words is not None else None,
            "score_threshold": score_threshold if score_threshold is not None else None,
            "search_type": search_type if search_type is not None else None,
            "slim_chunks": slim_chunks if slim_chunks is not None else None,
            "sort_options": sort_options if sort_options is not None else None,
            "typo_options": typo_options if typo_options is not None else None,
            "use_quote_negated_terms": use_quote_negated_terms if use_quote_negated_terms is not None else None,
            "user_id": user_id if user_id is not None else None,
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

    def get_chunks_in_group_by_tracking_id(
        self,
        tr_dataset: str,
        group_tracking_id: str,
        page: int,
        x_api_version: Optional[APIVersion] = None,
    ) -> Any:
        """
        Route to get all chunks for a group. The response is paginated, with each page containing 10 chunks. Support for custom page size is coming soon. Page is 1-indexed.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            group_tracking_id: The id of the group to get the chunks from
            page: The page of chunks to get from the group
            x_api_version: The version of the API to use for the request

        Returns:
            Response data
        """
        path = f"/api/chunk_group/tracking_id/{group_tracking_id}/{page}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_group_by_tracking_id(
        self,
        tr_dataset: str,
        tracking_id: str,
    ) -> Any:
        """
        Fetch the group with the given tracking id.
get_group_by_tracking_id

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            tracking_id: The tracking id of the group to fetch.

        Returns:
            Response data
        """
        path = f"/api/chunk_group/tracking_id/{tracking_id}"
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

    def add_chunk_to_group_by_tracking_id(
        self,
        tr_dataset: str,
        tracking_id: str,
        chunk_id: Optional[str] = None,
        chunk_tracking_id: Optional[str] = None,
    ) -> Any:
        """
        Route to add a chunk to a group by tracking id. One of chunk_id or chunk_tracking_id must be provided. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            tracking_id: Tracking id of the group to add the chunk to as a bookmark
            chunk_id: Id of the chunk to make a member of the group.
            chunk_tracking_id: Tracking Id of the chunk to make a member of the group.

        Returns:
            Response data
        """
        path = f"/api/chunk_group/tracking_id/{tracking_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "chunk_id": chunk_id if chunk_id is not None else None,
            "chunk_tracking_id": chunk_tracking_id if chunk_tracking_id is not None else None,
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

    def delete_group_by_tracking_id(
        self,
        tr_dataset: str,
        tracking_id: str,
        delete_chunks: bool,
    ) -> Any:
        """
        Delete a chunk_group with the given tracking id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            tracking_id: Tracking id of the chunk_group to delete
            delete_chunks: Delete the chunks within the group

        Returns:
            Response data
        """
        path = f"/api/chunk_group/tracking_id/{tracking_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if delete_chunks is not None:
            params["delete_chunks"] = delete_chunks
        json_data = None

        response = self._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_chunk_group(
        self,
        tr_dataset: str,
        group_id: str,
    ) -> Any:
        """
        Fetch the group with the given id.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            group_id: Id of the group you want to fetch.

        Returns:
            Response data
        """
        path = f"/api/chunk_group/{group_id}"
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

    def delete_chunk_group(
        self,
        tr_dataset: str,
        group_id: str,
        delete_chunks: bool,
    ) -> Any:
        """
        This will delete a chunk_group. If you set delete_chunks to true, it will also delete the chunks within the group. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            group_id: Id of the group you want to fetch.
            delete_chunks: Delete the chunks within the group

        Returns:
            Response data
        """
        path = f"/api/chunk_group/{group_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if delete_chunks is not None:
            params["delete_chunks"] = delete_chunks
        json_data = None

        response = self._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_chunks_in_group(
        self,
        tr_dataset: str,
        group_id: str,
        page: int,
        x_api_version: Optional[APIVersion] = None,
    ) -> Any:
        """
        Route to get all chunks for a group. The response is paginated, with each page containing 10 chunks. Page is 1-indexed.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            group_id: Id of the group you want to fetch.
            page: The page of chunks to get from the group
            x_api_version: The version of the API to use for the request

        Returns:
            Response data
        """
        path = f"/api/chunk_group/{group_id}/{page}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = None

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def get_groups_for_dataset(
        self,
        tr_dataset: str,
        dataset_id: str,
        page: int,
    ) -> Any:
        """
        Fetch the groups which belong to a dataset specified by its id.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            dataset_id: The id of the dataset to fetch groups for.
            page: The page of groups to fetch. Page is 1-indexed.

        Returns:
            Response data
        """
        path = f"/api/dataset/groups/{dataset_id}/{page}"
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
