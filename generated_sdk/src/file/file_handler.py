from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ...models.models import *

if TYPE_CHECKING:
    from ..trieve_api import TrieveApi


class File:
    def __init__(self, parent: "TrieveApi"):
        """
        Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API.

        Args:
            parent: The parent client to use for the requests
        """
        self.parent = parent

    def get_dataset_files_handler(
        self,
        tr_dataset: str,
        dataset_id: str,
        page: int,
    ) -> Any:
        """
        Get all files which belong to a given dataset specified by the dataset_id parameter. 10 files are returned per page.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            dataset_id: The id of the dataset to fetch files for.
            page: The page number of files you wish to fetch. Each page contains at most 10 files.

        Returns:
            Response data
        """
        path = f"/api/dataset/files/{dataset_id}/{page}"
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

    def upload_file_handler(
        self,
        tr_dataset: str,
        base64_file: str,
        file_name: str,
        create_chunks: Optional[bool] = None,
        description: Optional[str] = None,
        group_tracking_id: Optional[str] = None,
        link: Optional[str] = None,
        metadata: Optional[Any] = None,
        pdf2md_options: Optional[Pdf2MdOptions] = None,
        rebalance_chunks: Optional[bool] = None,
        split_avg: Optional[bool] = None,
        split_delimiters: Optional[List[str]] = None,
        tag_set: Optional[List[str]] = None,
        target_splits_per_chunk: Optional[int] = None,
        time_stamp: Optional[str] = None,
    ) -> Any:
        """
        Upload a file to S3 bucket attached to your dataset. You can select between a naive chunking strategy where the text is extracted with Apache Tika and split into segments with a target number of segments per chunk OR you can use a vision LLM to convert the file to markdown and create chunks per page. Auth'ed user must be an admin or owner of the dataset's organization to upload a file.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            base64_file: Base64 encoded file. This is the standard base64url encoding.
            file_name: Name of the file being uploaded, including the extension.
            create_chunks: Create chunks is a boolean which determines whether or not to create chunks from the file. If false, you can manually chunk the file and send the chunks to the create_chunk endpoint with the file_id to associate chunks with the file. Meant mostly for advanced users.
            description: Description is an optional convience field so you do not have to remember what the file contains or is about. It will be included on the group resulting from the file which will hold its chunk.
            group_tracking_id: Group tracking id is an optional field which allows you to specify the tracking id of the group that is created from the file. Chunks created will be created with the tracking id of `group_tracking_id|<index of chunk>`
            link: Link to the file. This can also be any string. This can be used to filter when searching for the file's resulting chunks. The link value will not affect embedding creation.
            metadata: Metadata is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata. Will be passed down to the file's chunks.
            pdf2md_options: No description provided
            rebalance_chunks: Rebalance chunks is an optional field which allows you to specify whether or not to rebalance the chunks created from the file. If not specified, the default true is used. If true, Trieve will evenly distribute remainder splits across chunks such that 66 splits with a `target_splits_per_chunk` of 20 will result in 3 chunks with 22 splits each.
            split_avg: Split average will automatically split your file into multiple chunks and average all of the resulting vectors into a single output chunk. Default is false. Explicitly enabling this will cause each file to only produce a single chunk.
            split_delimiters: Split delimiters is an optional field which allows you to specify the delimiters to use when splitting the file before chunking the text. If not specified, the default [.!?\n] are used to split into sentences. However, you may want to use spaces or other delimiters.
            tag_set: Tag set is a comma separated list of tags which will be passed down to the chunks made from the file. Tags are used to filter chunks when searching. HNSW indices are created for each tag such that there is no performance loss when filtering on them.
            target_splits_per_chunk: Target splits per chunk. This is an optional field which allows you to specify the number of splits you want per chunk. If not specified, the default 20 is used. However, you may want to use a different number.
            time_stamp: Time stamp should be an ISO 8601 combined date and time without timezone. Time_stamp is used for time window filtering and recency-biasing search results. Will be passed down to the file's chunks.

        Returns:
            Response data
        """
        path = f"/api/file"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "base64_file": base64_file if base64_file is not None else None,
            "create_chunks": create_chunks if create_chunks is not None else None,
            "description": description if description is not None else None,
            "file_name": file_name if file_name is not None else None,
            "group_tracking_id": (
                group_tracking_id if group_tracking_id is not None else None
            ),
            "link": link if link is not None else None,
            "metadata": metadata if metadata is not None else None,
            "pdf2md_options": pdf2md_options if pdf2md_options is not None else None,
            "rebalance_chunks": (
                rebalance_chunks if rebalance_chunks is not None else None
            ),
            "split_avg": split_avg if split_avg is not None else None,
            "split_delimiters": (
                split_delimiters if split_delimiters is not None else None
            ),
            "tag_set": tag_set if tag_set is not None else None,
            "target_splits_per_chunk": (
                target_splits_per_chunk if target_splits_per_chunk is not None else None
            ),
            "time_stamp": time_stamp if time_stamp is not None else None,
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

    def create_presigned_url_for_csv_jsonl(
        self,
        tr_dataset: str,
        file_name: str,
        description: Optional[str] = None,
        fulltext_boost_factor: Optional[float] = None,
        group_tracking_id: Optional[str] = None,
        link: Optional[str] = None,
        mappings: Optional[ChunkReqPayloadMappings] = None,
        metadata: Optional[Any] = None,
        semantic_boost_factor: Optional[float] = None,
        tag_set: Optional[List[str]] = None,
        time_stamp: Optional[str] = None,
        upsert_by_tracking_id: Optional[bool] = None,
    ) -> Any:
        """
        This route is useful for uploading very large CSV or JSONL files. Once you have completed the upload, chunks will be automatically created from the file for each line in the CSV or JSONL file. The chunks will be indexed and searchable. Auth'ed user must be an admin or owner of the dataset's organization to upload a file.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            file_name: Name of the file being uploaded, including the extension. Will be used to determine CSV or JSONL for processing.
            description: Description is an optional convience field so you do not have to remember what the file contains or is about. It will be included on the group resulting from the file which will hold its chunk.
            fulltext_boost_factor: Amount to multiplicatevly increase the frequency of the tokens in the boost phrase for each row's chunk by. Applies to fulltext (SPLADE) and keyword (BM25) search.
            group_tracking_id: Group tracking id is an optional field which allows you to specify the tracking id of the group that is created from the file. Chunks created will be created with the tracking id of `group_tracking_id|<index of chunk>`
            link: Link to the file. This can also be any string. This can be used to filter when searching for the file's resulting chunks. The link value will not affect embedding creation.
            mappings: Specify all of the mappings between columns or fields in a CSV or JSONL file and keys in the ChunkReqPayload. Array fields like tag_set, image_urls, and group_tracking_ids can have multiple mappings. Boost phrase can also have multiple mappings which get concatenated. Other fields can only have one mapping and only the last mapping will be used.
            metadata: Metadata is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata. Will be passed down to the file's chunks.
            semantic_boost_factor: Arbitrary float (positive or negative) specifying the multiplicate factor to apply before summing the phrase vector with the chunk_html embedding vector. Applies to semantic (embedding model) search.
            tag_set: Tag set is a comma separated list of tags which will be passed down to the chunks made from the file. Each tag will be joined with what's creatd per row of the CSV or JSONL file.
            time_stamp: Time stamp should be an ISO 8601 combined date and time without timezone. Time_stamp is used for time window filtering and recency-biasing search results. Will be passed down to the file's chunks.
            upsert_by_tracking_id: Upsert by tracking_id. If true, chunks will be upserted by tracking_id. If false, chunks with the same tracking_id as another already existing chunk will be ignored. Defaults to true.

        Returns:
            Response data
        """
        path = f"/api/file/csv_or_jsonl"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        json_data = {
            "description": description if description is not None else None,
            "file_name": file_name if file_name is not None else None,
            "fulltext_boost_factor": (
                fulltext_boost_factor if fulltext_boost_factor is not None else None
            ),
            "group_tracking_id": (
                group_tracking_id if group_tracking_id is not None else None
            ),
            "link": link if link is not None else None,
            "mappings": mappings if mappings is not None else None,
            "metadata": metadata if metadata is not None else None,
            "semantic_boost_factor": (
                semantic_boost_factor if semantic_boost_factor is not None else None
            ),
            "tag_set": tag_set if tag_set is not None else None,
            "time_stamp": time_stamp if time_stamp is not None else None,
            "upsert_by_tracking_id": (
                upsert_by_tracking_id if upsert_by_tracking_id is not None else None
            ),
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

    def upload_html_page(
        self,
        data: Document,
        metadata: Any,
        scrapeId: str,
    ) -> Any:
        """
        Chunk HTML by headings and queue for indexing into the specified dataset.

        Args:
            data: No description provided
            metadata: No description provided
            scrapeId: No description provided

        Returns:
            Response data
        """
        path = f"/api/file/html_page"
        params = None
        headers = None
        json_data = {
            "data": data if data is not None else None,
            "metadata": metadata if metadata is not None else None,
            "scrapeId": scrapeId if scrapeId is not None else None,
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

    def get_file_handler(
        self,
        tr_dataset: str,
        file_id: str,
        content_type: Optional[str] = None,
    ) -> Any:
        """
        Get a signed s3 url corresponding to the file_id requested such that you can download the file.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            file_id: The id of the file to fetch
            content_type: Optional field to override the presigned url's Content-Type header

        Returns:
            Response data
        """
        path = f"/api/file/{file_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if content_type is not None:
            params["content_type"] = content_type
        json_data = None

        response = self.parent._make_request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()

    def delete_file_handler(
        self,
        tr_dataset: str,
        file_id: str,
        delete_chunks: bool,
    ) -> Any:
        """
        Delete a file from S3 attached to the server based on its id. This will disassociate chunks from the file, but only delete them all together if you specify delete_chunks to be true. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

        Args:
            tr_dataset: The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
            file_id: The id of the file to delete
            delete_chunks: Delete the chunks within the group

        Returns:
            Response data
        """
        path = f"/api/file/{file_id}"
        params = {}
        headers = {}
        if tr_dataset is not None:
            headers["TR-Dataset"] = tr_dataset
        if delete_chunks is not None:
            params["delete_chunks"] = delete_chunks
        json_data = None

        response = self.parent._make_request(
            method="DELETE",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
