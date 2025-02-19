from typing import Any, Dict, List, Optional, Union
from ..trieve_api_client import TrieveAPIClient
from ...models.models import *

class ChunkClient (TrieveAPIClient):
    """Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API."""

    def create_chunk(
        self,
        tr_dataset: str,
        request_body: Optional[CreateChunkReqPayloadEnum] = None,
    ) -> Any:
        """
        Create new chunk(s). If the chunk has the same tracking_id as an existing chunk, the request will fail. Once a chunk is created, it can be searched for using the search endpoint.
If uploading in bulk, the maximum amount of chunks that can be uploaded at once is 120 chunks. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            request_body: Request body

        Returns:
            Response data
        """
        path = f"/api/chunk"
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

    def update_chunk(
        self,
        tr_dataset: str,
        chunk_html: Optional[str] = None,
        chunk_id: Optional[str] = None,
        convert_html_to_text: Optional[bool] = None,
        fulltext_boost: Optional[FullTextBoost] = None,
        group_ids: Optional[List[str]] = None,
        group_tracking_ids: Optional[List[str]] = None,
        image_urls: Optional[List[str]] = None,
        link: Optional[str] = None,
        location: Optional[GeoInfo] = None,
        metadata: Optional[Any] = None,
        num_value: Optional[float] = None,
        semantic_boost: Optional[SemanticBoost] = None,
        tag_set: Optional[List[str]] = None,
        time_stamp: Optional[str] = None,
        tracking_id: Optional[str] = None,
        weight: Optional[float] = None,
    ) -> Any:
        """
        Update a chunk. If you try to change the tracking_id of the chunk to have the same tracking_id as an existing chunk, the request will fail. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            chunk_html: HTML content of the chunk you want to update. This can also be plaintext. The innerText of the HTML will be used to create the embedding vector. The point of using HTML is for convienience, as some users have applications where users submit HTML content. If no chunk_html is provided, the existing chunk_html will be used.
            chunk_id: Id of the chunk you want to update. You can provide either the chunk_id or the tracking_id. If both are provided, the chunk_id will be used.
            convert_html_to_text: Convert HTML to raw text before processing to avoid adding noise to the vector embeddings. By default this is true. If you are using HTML content that you want to be included in the vector embeddings, set this to false.
            fulltext_boost: Boost the presence of certain tokens for fulltext (SPLADE) and keyword (BM25) search. I.e. boosting title phrases to priortize title matches or making sure that the listing for AirBNB itself ranks higher than companies who make software for AirBNB hosts by boosting the in-document-frequency of the AirBNB token (AKA word) for its official listing. Conceptually it multiples the in-document-importance second value in the tuples of the SPLADE or BM25 sparse vector of the chunk_html innerText for all tokens present in the boost phrase by the boost factor like so: (token, in-document-importance) -> (token, in-document-importance*boost_factor).
            group_ids: Group ids are the ids of the groups that the chunk should be placed into. This is useful for when you want to update a chunk and add it to a group or multiple groups in one request.
            group_tracking_ids: Group tracking_ids are the tracking_ids of the groups that the chunk should be placed into. This is useful for when you want to update a chunk and add it to a group or multiple groups in one request.
            image_urls: Image urls are a list of urls to images that are associated with the chunk. This is useful for when you want to associate images with a chunk. If no image_urls are provided, the existing image_urls will be used.
            link: Link of the chunk you want to update. This can also be any string. Frequently, this is a link to the source of the chunk. The link value will not affect the embedding creation. If no link is provided, the existing link will be used.
            location: Location that you want to use as the center of the search.
            metadata: The metadata is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata. If no metadata is provided, the existing metadata will be used.
            num_value: Num value is an arbitrary numerical value that can be used to filter chunks. This is useful for when you want to filter chunks by numerical value. If no num_value is provided, the existing num_value will be used.
            semantic_boost: Semantic boosting moves the dense vector of the chunk in the direction of the distance phrase for semantic search. I.e. you can force a cluster by moving every chunk for a PDF closer to its title or push a chunk with a chunk_html of "iphone" 25% closer to the term "flagship" by using the distance phrase "flagship" and a distance factor of 0.25. Conceptually it's drawing a line (euclidean/L2 distance) between the vector for the innerText of the chunk_html and distance_phrase then moving the vector of the chunk_html distance_factor*L2Distance closer to or away from the distance_phrase point along the line between the two points.
            tag_set: Tag set is a list of tags. This can be used to filter chunks by tag. Unlike with metadata filtering, HNSW indices will exist for each tag such that there is not a performance hit for filtering on them. If no tag_set is provided, the existing tag_set will be used.
            time_stamp: Time_stamp should be an ISO 8601 combined date and time without timezone. It is used for time window filtering and recency-biasing search results. If no time_stamp is provided, the existing time_stamp will be used.
            tracking_id: Tracking_id of the chunk you want to update. This is required to match an existing chunk.
            weight: Weight is a float which can be used to bias search results. This is useful for when you want to bias search results for a chunk. The magnitude only matters relative to other chunks in the chunk's dataset dataset. If no weight is provided, the existing weight will be used.

        Returns:
            Response data
        """
        path = f"/api/chunk"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "chunk_html": chunk_html if chunk_html is not None else None,
            "chunk_id": chunk_id if chunk_id is not None else None,
            "convert_html_to_text": convert_html_to_text if convert_html_to_text is not None else None,
            "fulltext_boost": fulltext_boost if fulltext_boost is not None else None,
            "group_ids": group_ids if group_ids is not None else None,
            "group_tracking_ids": group_tracking_ids if group_tracking_ids is not None else None,
            "image_urls": image_urls if image_urls is not None else None,
            "link": link if link is not None else None,
            "location": location if location is not None else None,
            "metadata": metadata if metadata is not None else None,
            "num_value": num_value if num_value is not None else None,
            "semantic_boost": semantic_boost if semantic_boost is not None else None,
            "tag_set": tag_set if tag_set is not None else None,
            "time_stamp": time_stamp if time_stamp is not None else None,
            "tracking_id": tracking_id if tracking_id is not None else None,
            "weight": weight if weight is not None else None,
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

    def bulk_delete_chunk(
        self,
        tr_dataset: str,
        filter: ChunkFilter,
    ) -> Any:
        """
        Delete multiple chunks using a filter. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            filter: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.

        Returns:
            Response data
        """
        path = f"/api/chunk"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "filter": filter if filter is not None else None,
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

    def autocomplete(
        self,
        tr_dataset: str,
        query: SearchModalities,
        search_type: SearchMethod,
        x_api_version: Optional[APIVersion] = None,
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
    ) -> Any:
        """
        This route provides the primary autocomplete functionality for the API. This prioritize prefix matching with semantic or full-text search.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            query: No description provided
            search_type: No description provided
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
            content_only: Set content_only to true to only returning the chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement (typically 10-50ms). Default is false.
            extend_results: If specified to true, this will extend the search results to include non-exact prefix matches of the same search_type such that a full page_size of results are returned. Default is false.
            filters: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.
            highlight_options: Highlight Options lets you specify different methods to highlight the chunks in the result set. If not specified, this defaults to the score of the chunks.
            page_size: Page size is the number of chunks to fetch. This can be used to fetch more than 10 chunks at a time.
            remove_stop_words: If true, stop words (specified in server/src/stop-words.txt in the git repo) will be removed. Queries that are entirely stop words will be preserved.
            score_threshold: Set score_threshold to a float to filter out chunks with a score below the threshold. This threshold applies before weight and bias modifications. If not specified, this defaults to 0.0.
            scoring_options: Scoring options provides ways to modify the sparse or dense vector created for the query in order to change how potential matches are scored. If not specified, this defaults to no modifications.
            slim_chunks: Set slim_chunks to true to avoid returning the content and chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement (typically 10-50ms). Default is false.
            sort_options: Sort Options lets you specify different methods to rerank the chunks in the result set. If not specified, this defaults to the score of the chunks.
            typo_options: Typo Options lets you specify different methods to correct typos in the query. If not specified, typos will not be corrected.
            use_quote_negated_terms: If true, quoted and - prefixed words will be parsed from the queries and used as required and negated words respectively. Default is false.
            user_id: User ID is the id of the user who is making the request. This is used to track user interactions with the search results.

        Returns:
            Response data
        """
        path = f"/api/chunk/autocomplete"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = {
            "content_only": content_only if content_only is not None else None,
            "extend_results": extend_results if extend_results is not None else None,
            "filters": filters if filters is not None else None,
            "highlight_options": highlight_options if highlight_options is not None else None,
            "page_size": page_size if page_size is not None else None,
            "query": query if query is not None else None,
            "remove_stop_words": remove_stop_words if remove_stop_words is not None else None,
            "score_threshold": score_threshold if score_threshold is not None else None,
            "scoring_options": scoring_options if scoring_options is not None else None,
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

    def count_chunks(
        self,
        tr_dataset: str,
        query: QueryTypes,
        search_type: CountSearchMethod,
        filters: Optional[ChunkFilter] = None,
        limit: Optional[int] = None,
        score_threshold: Optional[float] = None,
        use_quote_negated_terms: Optional[bool] = None,
    ) -> Any:
        """
        This route can be used to determine the number of chunk results that match a search query including score threshold and filters. It may be high latency for large limits. There is a dataset configuration imposed restriction on the maximum limit value (default 10,000) which is used to prevent DDOS attacks. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            query: No description provided
            search_type: No description provided
            filters: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.
            limit: Set limit to restrict the maximum number of chunks to count. This is useful for when you want to reduce the latency of the count operation. By default the limit will be the number of chunks in the dataset.
            score_threshold: Set score_threshold to a float to filter out chunks with a score below the threshold. This threshold applies before weight and bias modifications. If not specified, this defaults to 0.0.
            use_quote_negated_terms: If true, quoted and - prefixed words will be parsed from the queries and used as required and negated words respectively. Default is false.

        Returns:
            Response data
        """
        path = f"/api/chunk/count"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "filters": filters if filters is not None else None,
            "limit": limit if limit is not None else None,
            "query": query if query is not None else None,
            "score_threshold": score_threshold if score_threshold is not None else None,
            "search_type": search_type if search_type is not None else None,
            "use_quote_negated_terms": use_quote_negated_terms if use_quote_negated_terms is not None else None,
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

    def generate_off_chunks(
        self,
        tr_dataset: str,
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
    ) -> Any:
        """
        This endpoint exists as an alternative to the topic+message resource pattern where our Trieve handles chat memory. With this endpoint, the user is responsible for providing the context window and the prompt and the conversation is ephemeral.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            chunk_ids: The ids of the chunks to be retrieved and injected into the context window for RAG.
            prev_messages: The previous messages to be placed into the chat history. There must be at least one previous message.
            audio_input: Audio input to be used in the chat. This will be used to generate the audio tokens for the model. The default is None.
            context_options: Context options to use for the completion. If not specified, all options will default to false.
            frequency_penalty: Frequency penalty is a number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim. Default is 0.7.
            highlight_results: Set highlight_results to false for a slight latency improvement (1-10ms). If not specified, this defaults to true. This will add `<mark><b>` tags to the chunk_html of the chunks to highlight matching splits.
            image_config: Configuration for sending images to the llm
            image_urls: Image URLs to be used in the chat. These will be used to generate the image tokens for the model. The default is None.
            max_tokens: The maximum number of tokens to generate in the chat completion. Default is None.
            presence_penalty: Presence penalty is a number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Default is 0.7.
            prompt: Prompt will be used to tell the model what to generate in the next message in the chat. The default is 'Respond to the previous instruction and include the doc numbers that you used in square brackets at the end of the sentences that you used the docs for:'. You can also specify an empty string to leave the final message alone such that your user's final message can be used as the prompt. See docs.trieve.ai or contact us for more information.
            stop_tokens: Stop tokens are up to 4 sequences where the API will stop generating further tokens. Default is None.
            stream_response: Whether or not to stream the response. If this is set to true or not included, the response will be a stream. If this is set to false, the response will be a normal JSON response. Default is true.
            temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. Default is 0.5.
            user_id: User ID is the id of the user who is making the request. This is used to track user interactions with the RAG results.

        Returns:
            Response data
        """
        path = f"/api/chunk/generate"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "audio_input": audio_input if audio_input is not None else None,
            "chunk_ids": chunk_ids if chunk_ids is not None else None,
            "context_options": context_options if context_options is not None else None,
            "frequency_penalty": frequency_penalty if frequency_penalty is not None else None,
            "highlight_results": highlight_results if highlight_results is not None else None,
            "image_config": image_config if image_config is not None else None,
            "image_urls": image_urls if image_urls is not None else None,
            "max_tokens": max_tokens if max_tokens is not None else None,
            "presence_penalty": presence_penalty if presence_penalty is not None else None,
            "prev_messages": prev_messages if prev_messages is not None else None,
            "prompt": prompt if prompt is not None else None,
            "stop_tokens": stop_tokens if stop_tokens is not None else None,
            "stream_response": stream_response if stream_response is not None else None,
            "temperature": temperature if temperature is not None else None,
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

    def get_recommended_chunks(
        self,
        tr_dataset: str,
        x_api_version: Optional[APIVersion] = None,
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
    ) -> Any:
        """
        Get recommendations of chunks similar to the positive samples in the request and dissimilar to the negative.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
            filters: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.
            limit: The number of chunks to return. This is the number of chunks which will be returned in the response. The default is 10.
            negative_chunk_ids: The ids of the chunks to be used as negative examples for the recommendation. The chunks in this array will be used to filter out similar chunks.
            negative_tracking_ids: The tracking_ids of the chunks to be used as negative examples for the recommendation. The chunks in this array will be used to filter out similar chunks.
            positive_chunk_ids: The ids of the chunks to be used as positive examples for the recommendation. The chunks in this array will be used to find similar chunks.
            positive_tracking_ids: The tracking_ids of the chunks to be used as positive examples for the recommendation. The chunks in this array will be used to find similar chunks.
            recommend_type: The type of recommendation to make. This lets you choose whether to recommend based off of `semantic` or `fulltext` similarity. The default is `semantic`.
            slim_chunks: Set slim_chunks to true to avoid returning the content and chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement (typicall 10-50ms). Default is false.
            strategy: Strategy to use for recommendations, either "average_vector" or "best_score". The default is "average_vector". The "average_vector" strategy will construct a single average vector from the positive and negative samples then use it to perform a pseudo-search. The "best_score" strategy is more advanced and navigates the HNSW with a heuristic of picking edges where the point is closer to the positive samples than it is the negatives.
            user_id: User ID is the id of the user who is making the request. This is used to track user interactions with the recommendation results.

        Returns:
            Response data
        """
        path = f"/api/chunk/recommend"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = {
            "filters": filters if filters is not None else None,
            "limit": limit if limit is not None else None,
            "negative_chunk_ids": negative_chunk_ids if negative_chunk_ids is not None else None,
            "negative_tracking_ids": negative_tracking_ids if negative_tracking_ids is not None else None,
            "positive_chunk_ids": positive_chunk_ids if positive_chunk_ids is not None else None,
            "positive_tracking_ids": positive_tracking_ids if positive_tracking_ids is not None else None,
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

    def search_chunks(
        self,
        tr_dataset: str,
        query: QueryTypes,
        search_type: SearchMethod,
        x_api_version: Optional[APIVersion] = None,
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
    ) -> Any:
        """
        This route provides the primary search functionality for the API. It can be used to search for chunks by semantic similarity, full-text similarity, or a combination of both. Results' `chunk_html` values will be modified with `<mark><b>` or custom specified tags for sub-sentence highlighting.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            query: No description provided
            search_type: No description provided
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
            content_only: Set content_only to true to only returning the chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement (typically 10-50ms). Default is false.
            filters: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.
            get_total_pages: Get total page count for the query accounting for the applied filters. Defaults to false, but can be set to true when the latency penalty is acceptable (typically 50-200ms).
            highlight_options: Highlight Options lets you specify different methods to highlight the chunks in the result set. If not specified, this defaults to the score of the chunks.
            page: Page of chunks to fetch. Page is 1-indexed.
            page_size: Page size is the number of chunks to fetch. This can be used to fetch more than 10 chunks at a time.
            remove_stop_words: If true, stop words (specified in server/src/stop-words.txt in the git repo) will be removed. Queries that are entirely stop words will be preserved.
            score_threshold: Set score_threshold to a float to filter out chunks with a score below the threshold for cosine distance metric. For Manhattan Distance, Euclidean Distance, and Dot Product, it will filter out scores above the threshold distance. This threshold applies before weight and bias modifications. If not specified, this defaults to no threshold. A threshold of 0 will default to no threshold.
            scoring_options: Scoring options provides ways to modify the sparse or dense vector created for the query in order to change how potential matches are scored. If not specified, this defaults to no modifications.
            slim_chunks: Set slim_chunks to true to avoid returning the content and chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement (typically 10-50ms). Default is false.
            sort_options: Sort Options lets you specify different methods to rerank the chunks in the result set. If not specified, this defaults to the score of the chunks.
            typo_options: Typo Options lets you specify different methods to correct typos in the query. If not specified, typos will not be corrected.
            use_quote_negated_terms: If true, quoted and - prefixed words will be parsed from the queries and used as required and negated words respectively. Default is false.
            user_id: User ID is the id of the user who is making the request. This is used to track user interactions with the search results.

        Returns:
            Response data
        """
        path = f"/api/chunk/search"
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
            "highlight_options": highlight_options if highlight_options is not None else None,
            "page": page if page is not None else None,
            "page_size": page_size if page_size is not None else None,
            "query": query if query is not None else None,
            "remove_stop_words": remove_stop_words if remove_stop_words is not None else None,
            "score_threshold": score_threshold if score_threshold is not None else None,
            "scoring_options": scoring_options if scoring_options is not None else None,
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

    def split_html_content(
        self,
        chunk_html: str,
        body_remove_strings: Optional[List[str]] = None,
        heading_remove_strings: Optional[List[str]] = None,
    ) -> Any:
        """
        This endpoint receives a single html string and splits it into chunks based on the headings and
body content. The headings are split based on heading html tags. chunk_html has a maximum size
of 256Kb.

        Args:
            chunk_html: The HTML content to be split into chunks
            body_remove_strings: Text strings to remove from body when creating chunks for each page
            heading_remove_strings: Text strings to remove from headings when creating chunks for each page

        Returns:
            Response data
        """
        path = f"/api/chunk/split"
        params = None
        headers = None
        json_data = {
            "body_remove_strings": body_remove_strings if body_remove_strings is not None else None,
            "chunk_html": chunk_html if chunk_html is not None else None,
            "heading_remove_strings": heading_remove_strings if heading_remove_strings is not None else None,
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

    def get_suggested_queries(
        self,
        tr_dataset: str,
        context: Optional[str] = None,
        filters: Optional[ChunkFilter] = None,
        query: Optional[str] = None,
        search_type: Optional[SearchMethod] = None,
        suggestion_type: Optional[SuggestType] = None,
        suggestions_to_create: Optional[int] = None,
    ) -> Any:
        """
        This endpoint will generate 3 suggested queries based off a hybrid search using RAG with the query provided in the request body and return them as a JSON object.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            context: Context is the context of the query. This can be any string under 15 words and 200 characters. The context will be used to generate the suggested queries. Defaults to None.
            filters: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.
            query: The query to base the generated suggested queries off of using RAG. A hybrid search for 10 chunks from your dataset using this query will be performed and the context of the chunks will be used to generate the suggested queries.
            search_type: No description provided
            suggestion_type: No description provided
            suggestions_to_create: The number of suggested queries to create, defaults to 10

        Returns:
            Response data
        """
        path = f"/api/chunk/suggestions"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "context": context if context is not None else None,
            "filters": filters if filters is not None else None,
            "query": query if query is not None else None,
            "search_type": search_type if search_type is not None else None,
            "suggestion_type": suggestion_type if suggestion_type is not None else None,
            "suggestions_to_create": suggestions_to_create if suggestions_to_create is not None else None,
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

    def update_chunk_by_tracking_id(
        self,
        tr_dataset: str,
        tracking_id: str,
        chunk_html: Optional[str] = None,
        convert_html_to_text: Optional[bool] = None,
        group_ids: Optional[List[str]] = None,
        group_tracking_ids: Optional[List[str]] = None,
        link: Optional[str] = None,
        metadata: Optional[Any] = None,
        time_stamp: Optional[str] = None,
        weight: Optional[float] = None,
    ) -> Any:
        """
        Update a chunk by tracking_id. This is useful for when you are coordinating with an external system and want to use the tracking_id to identify the chunk. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            tracking_id: Tracking_id of the chunk you want to update. This is required to match an existing chunk.
            chunk_html: HTML content of the chunk you want to update. This can also be plaintext. The innerText of the HTML will be used to create the embedding vector. The point of using HTML is for convienience, as some users have applications where users submit HTML content. If no chunk_html is provided, the existing chunk_html will be used.
            convert_html_to_text: Convert HTML to raw text before processing to avoid adding noise to the vector embeddings. By default this is true. If you are using HTML content that you want to be included in the vector embeddings, set this to false.
            group_ids: Group ids are the ids of the groups that the chunk should be placed into. This is useful for when you want to update a chunk and add it to a group or multiple groups in one request.
            group_tracking_ids: Group tracking_ids are the tracking_ids of the groups that the chunk should be placed into. This is useful for when you want to update a chunk and add it to a group or multiple groups in one request.
            link: Link of the chunk you want to update. This can also be any string. Frequently, this is a link to the source of the chunk. The link value will not affect the embedding creation. If no link is provided, the existing link will be used.
            metadata: The metadata is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata. If no metadata is provided, the existing metadata will be used.
            time_stamp: Time_stamp should be an ISO 8601 combined date and time without timezone. It is used for time window filtering and recency-biasing search results. If no time_stamp is provided, the existing time_stamp will be used.
            weight: Weight is a float which can be used to bias search results. This is useful for when you want to bias search results for a chunk. The magnitude only matters relative to other chunks in the chunk's dataset dataset. If no weight is provided, the existing weight will be used.

        Returns:
            Response data
        """
        path = f"/api/chunk/tracking_id/update"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "chunk_html": chunk_html if chunk_html is not None else None,
            "convert_html_to_text": convert_html_to_text if convert_html_to_text is not None else None,
            "group_ids": group_ids if group_ids is not None else None,
            "group_tracking_ids": group_tracking_ids if group_tracking_ids is not None else None,
            "link": link if link is not None else None,
            "metadata": metadata if metadata is not None else None,
            "time_stamp": time_stamp if time_stamp is not None else None,
            "tracking_id": tracking_id if tracking_id is not None else None,
            "weight": weight if weight is not None else None,
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

        response = self._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def delete_chunk_by_tracking_id(
        self,
        tr_dataset: str,
        tracking_id: str,
    ) -> Any:
        """
        Delete a chunk by tracking_id. This is useful for when you are coordinating with an external system and want to use the tracking_id to identify the chunk. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            tracking_id: tracking_id of the chunk you want to delete

        Returns:
            Response data
        """
        path = f"/api/chunk/tracking_id/{tracking_id}"
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

    def get_chunk_by_id(
        self,
        tr_dataset: str,
        chunk_id: str,
        x_api_version: Optional[APIVersion] = None,
    ) -> Any:
        """
        Get a singular chunk by id.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            chunk_id: Id of the chunk you want to fetch.
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.

        Returns:
            Response data
        """
        path = f"/api/chunk/{chunk_id}"
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

    def delete_chunk(
        self,
        tr_dataset: str,
        chunk_id: str,
    ) -> Any:
        """
        Delete a chunk by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            chunk_id: Id of the chunk you want to fetch.

        Returns:
            Response data
        """
        path = f"/api/chunk/{chunk_id}"
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

    def get_chunks_by_ids(
        self,
        tr_dataset: str,
        ids: List[str],
        x_api_version: Optional[APIVersion] = None,
    ) -> Any:
        """
        Get multiple chunks by multiple ids.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            ids: No description provided
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.

        Returns:
            Response data
        """
        path = f"/api/chunks"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = {
            "ids": ids if ids is not None else None,
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

    def scroll_dataset_chunks(
        self,
        tr_dataset: str,
        filters: Optional[ChunkFilter] = None,
        offset_chunk_id: Optional[str] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[SortByField] = None,
    ) -> Any:
        """
        Get paginated chunks from your dataset with filters and custom sorting. If sort by is not specified, the results will sort by the id's of the chunks in ascending order. Sort by and offset_chunk_id cannot be used together; if you want to scroll with a sort by then you need to use a must_not filter with the ids you have already seen. There is a limit of 1000 id's in a must_not filter at a time.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            filters: ChunkFilter is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata.
            offset_chunk_id: Offset chunk id is the id of the chunk to start the page from. If not specified, this defaults to the first chunk in the dataset sorted by id ascending.
            page_size: Page size is the number of chunks to fetch. This can be used to fetch more than 10 chunks at a time.
            sort_by: No description provided

        Returns:
            Response data
        """
        path = f"/api/chunks/scroll"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "filters": filters if filters is not None else None,
            "offset_chunk_id": offset_chunk_id if offset_chunk_id is not None else None,
            "page_size": page_size if page_size is not None else None,
            "sort_by": sort_by if sort_by is not None else None,
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

    def get_chunks_by_tracking_ids(
        self,
        tr_dataset: str,
        tracking_ids: List[str],
        x_api_version: Optional[APIVersion] = None,
    ) -> Any:
        """
        Get multiple chunks by ids.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            tracking_ids: No description provided
            x_api_version: The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.

        Returns:
            Response data
        """
        path = f"/api/chunks/tracking"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if x_api_version is not None:
            headers["X-API-Version"] = x_api_version
        json_data = {
            "tracking_ids": tracking_ids if tracking_ids is not None else None,
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
