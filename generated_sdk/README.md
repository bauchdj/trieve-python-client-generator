# Trieve API Python SDK

Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API.

Version: 0.13.0

## Installation

```bash
pip install trieve-api
```

## Usage

First, initialize the client:

```python
from trieve_api import TrieveAPIClient

client = TrieveAPIClient(
    base_url="https://api.trieve.ai",  # Optional, defaults to this URL
    api_key="your_api_key",  # Optional
    timeout=10.0,  # Optional, defaults to 10 seconds
)
```

### Available Operations

#### Analytics

##### `send_ctr_data`

This route allows you to send clickstream data to the system. Clickstream data is used to fine-tune the re-ranking of search results and recommendations.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.send_ctr_data(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `send_event_data`

This route allows you to send user event data to the system.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.send_event_data(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_all_events`

This route allows you to view all user events.

```python
# Parameters
request_body = {}  # Add your request body here

# Make request
response = client.get_all_events(
    request_body=request_body,
)
```

##### `get_ctr_analytics`

This route allows you to view the CTR analytics for a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_ctr_analytics(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_event_by_id`

This route allows you to view an user event by its ID. You can pass in any type of event and get the details for that event.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
event_id = "value"  # The event id to use for the request

# Make request
response = client.get_event_by_id(
    tr_dataset=tr_dataset,
    event_id=event_id,
)
```

##### `get_rag_analytics`

This route allows you to view the RAG analytics for a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_rag_analytics(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `set_rag_query_rating`

This route allows you to Rate a RAG query.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.set_rag_query_rating(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_recommendation_analytics`

This route allows you to view the recommendation analytics for a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_recommendation_analytics(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_search_analytics`

This route allows you to view the search analytics for a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_search_analytics(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `set_search_query_rating`

This route allows you to Rate a search query.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.set_search_query_rating(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_cluster_analytics`

This route allows you to view the cluster analytics for a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_cluster_analytics(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_top_datasets`

This route allows you to view the top datasets for a given type.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.get_top_datasets(
    tr_organization=tr_organization,
    request_body=request_body,
)
```


#### Auth

##### `login`

This will redirect you to the OAuth provider for authentication with email/pass, SSO, Google, Github, etc.

```python
# Parameters
organization_id = None  # ID of organization to authenticate into
redirect_uri = None  # URL to redirect to after successful login
inv_code = None  # Code sent via email as a result of successful call to send_invitation

# Make request
response = client.login(
    organization_id=organization_id,
    redirect_uri=redirect_uri,
    inv_code=inv_code,
)
```

##### `logout`

Invalidate your current auth credential stored typically stored in a cookie. This does not invalidate your API key.

```python
# Make request
response = client.logout()
```

##### `callback`

This is the callback route for the OAuth provider, it should not be called directly. Redirects to browser with set-cookie header.

```python
# Make request
response = client.callback()
```

##### `get_me`

Get the user corresponding to your current auth credentials.

```python
# Make request
response = client.get_me()
```


#### Chunk

##### `create_chunk`

Create new chunk(s). If the chunk has the same tracking_id as an existing chunk, the request will fail. Once a chunk is created, it can be searched for using the search endpoint.
If uploading in bulk, the maximum amount of chunks that can be uploaded at once is 120 chunks. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.create_chunk(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `update_chunk`

Update a chunk. If you try to change the tracking_id of the chunk to have the same tracking_id as an existing chunk, the request will fail. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.update_chunk(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `bulk_delete_chunk`

Delete multiple chunks using a filter. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.bulk_delete_chunk(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `autocomplete`

This route provides the primary autocomplete functionality for the API. This prioritize prefix matching with semantic or full-text search.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
request_body = {}  # Add your request body here

# Make request
response = client.autocomplete(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    request_body=request_body,
)
```

##### `count_chunks`

This route can be used to determine the number of chunk results that match a search query including score threshold and filters. It may be high latency for large limits. There is a dataset configuration imposed restriction on the maximum limit value (default 10,000) which is used to prevent DDOS attacks. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.count_chunks(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `generate_off_chunks`

This endpoint exists as an alternative to the topic+message resource pattern where our Trieve handles chat memory. With this endpoint, the user is responsible for providing the context window and the prompt and the conversation is ephemeral.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.generate_off_chunks(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_recommended_chunks`

Get recommendations of chunks similar to the positive samples in the request and dissimilar to the negative.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
request_body = {}  # Add your request body here

# Make request
response = client.get_recommended_chunks(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    request_body=request_body,
)
```

##### `search_chunks`

This route provides the primary search functionality for the API. It can be used to search for chunks by semantic similarity, full-text similarity, or a combination of both. Results' `chunk_html` values will be modified with `<mark><b>` or custom specified tags for sub-sentence highlighting.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
request_body = {}  # Add your request body here

# Make request
response = client.search_chunks(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    request_body=request_body,
)
```

##### `split_html_content`

This endpoint receives a single html string and splits it into chunks based on the headings and
body content. The headings are split based on heading html tags. chunk_html has a maximum size
of 256Kb.

```python
# Parameters
request_body = {}  # Add your request body here

# Make request
response = client.split_html_content(
    request_body=request_body,
)
```

##### `get_suggested_queries`

This endpoint will generate 3 suggested queries based off a hybrid search using RAG with the query provided in the request body and return them as a JSON object.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_suggested_queries(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `update_chunk_by_tracking_id`

Update a chunk by tracking_id. This is useful for when you are coordinating with an external system and want to use the tracking_id to identify the chunk. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.update_chunk_by_tracking_id(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_chunk_by_tracking_id`

Get a singular chunk by tracking_id. This is useful for when you are coordinating with an external system and want to use your own id as the primary reference for a chunk.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
tracking_id = "value"  # tracking_id of the chunk you want to fetch

# Make request
response = client.get_chunk_by_tracking_id(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    tracking_id=tracking_id,
)
```

##### `delete_chunk_by_tracking_id`

Delete a chunk by tracking_id. This is useful for when you are coordinating with an external system and want to use the tracking_id to identify the chunk. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
tracking_id = "value"  # tracking_id of the chunk you want to delete

# Make request
response = client.delete_chunk_by_tracking_id(
    tr_dataset=tr_dataset,
    tracking_id=tracking_id,
)
```

##### `get_chunk_by_id`

Get a singular chunk by id.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
chunk_id = "value"  # Id of the chunk you want to fetch.

# Make request
response = client.get_chunk_by_id(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    chunk_id=chunk_id,
)
```

##### `delete_chunk`

Delete a chunk by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
chunk_id = "value"  # Id of the chunk you want to fetch.

# Make request
response = client.delete_chunk(
    tr_dataset=tr_dataset,
    chunk_id=chunk_id,
)
```

##### `get_chunks_by_ids`

Get multiple chunks by multiple ids.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
request_body = {}  # Add your request body here

# Make request
response = client.get_chunks_by_ids(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    request_body=request_body,
)
```

##### `scroll_dataset_chunks`

Get paginated chunks from your dataset with filters and custom sorting. If sort by is not specified, the results will sort by the id's of the chunks in ascending order. Sort by and offset_chunk_id cannot be used together; if you want to scroll with a sort by then you need to use a must_not filter with the ids you have already seen. There is a limit of 1000 id's in a must_not filter at a time.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.scroll_dataset_chunks(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_chunks_by_tracking_ids`

Get multiple chunks by ids.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
request_body = {}  # Add your request body here

# Make request
response = client.get_chunks_by_tracking_ids(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    request_body=request_body,
)
```


#### Chunk_Group

##### `create_chunk_group`

Create new chunk_group(s). This is a way to group chunks together. If you try to create a chunk_group with the same tracking_id as an existing chunk_group, this operation will fail. Only 1000 chunk groups can be created at a time. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.create_chunk_group(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `update_chunk_group`

Update a chunk_group. One of group_id or tracking_id must be provided. If you try to change the tracking_id to one that already exists, this operation will fail. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.update_chunk_group(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `add_chunk_to_group`

Route to add a chunk to a group. One of chunk_id or chunk_tracking_id must be provided. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
group_id = "value"  # Id of the group to add the chunk to as a bookmark
request_body = {}  # Add your request body here

# Make request
response = client.add_chunk_to_group(
    tr_dataset=tr_dataset,
    group_id=group_id,
    request_body=request_body,
)
```

##### `remove_chunk_from_group`

Route to remove a chunk from a group. Auth'ed user or api key must be an admin or owner of the dataset's organization to remove a chunk from a group.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
group_id = "value"  # Id of the group you want to remove the chunk from.
chunk_id = None  # Id of the chunk you want to remove from the group
request_body = {}  # Add your request body here

# Make request
response = client.remove_chunk_from_group(
    tr_dataset=tr_dataset,
    group_id=group_id,
    chunk_id=chunk_id,
    request_body=request_body,
)
```

##### `get_groups_for_chunks`

Route to get the groups that a chunk is in.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_groups_for_chunks(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `count_group_chunks`

Route to get the number of chunks that is in a group

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.count_group_chunks(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `search_over_groups`

This route allows you to get groups as results instead of chunks. Each group returned will have the matching chunks sorted by similarity within the group. This is useful for when you want to get groups of chunks which are similar to the search query. If choosing hybrid search, the top chunk of each group will be re-ranked using scores from a cross encoder model. Compatible with semantic, fulltext, or hybrid search modes.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
request_body = {}  # Add your request body here

# Make request
response = client.search_over_groups(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    request_body=request_body,
)
```

##### `get_recommended_groups`

Route to get recommended groups. This route will return groups which are similar to the groups in the request body. You must provide at least one positive group id or group tracking id.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
request_body = {}  # Add your request body here

# Make request
response = client.get_recommended_groups(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    request_body=request_body,
)
```

##### `search_within_group`

This route allows you to search only within a group. This is useful for when you only want search results to contain chunks which are members of a specific group. If choosing hybrid search, the results will be re-ranked using scores from a cross encoder model.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
x_api_version = None  # The API version to use for this request. Defaults to V2 for orgs created after July 12, 2024 and V1 otherwise.
request_body = {}  # Add your request body here

# Make request
response = client.search_within_group(
    tr_dataset=tr_dataset,
    x_api_version=x_api_version,
    request_body=request_body,
)
```

##### `get_chunks_in_group_by_tracking_id`

Route to get all chunks for a group. The response is paginated, with each page containing 10 chunks. Support for custom page size is coming soon. Page is 1-indexed.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
group_tracking_id = "value"  # The id of the group to get the chunks from
x_api_version = None  # The version of the API to use for the request
page = 123  # The page of chunks to get from the group

# Make request
response = client.get_chunks_in_group_by_tracking_id(
    tr_dataset=tr_dataset,
    group_tracking_id=group_tracking_id,
    x_api_version=x_api_version,
    page=page,
)
```

##### `get_group_by_tracking_id`

Fetch the group with the given tracking id.
get_group_by_tracking_id

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
tracking_id = "value"  # The tracking id of the group to fetch.

# Make request
response = client.get_group_by_tracking_id(
    tr_dataset=tr_dataset,
    tracking_id=tracking_id,
)
```

##### `add_chunk_to_group_by_tracking_id`

Route to add a chunk to a group by tracking id. One of chunk_id or chunk_tracking_id must be provided. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
tracking_id = "value"  # Tracking id of the group to add the chunk to as a bookmark
request_body = {}  # Add your request body here

# Make request
response = client.add_chunk_to_group_by_tracking_id(
    tr_dataset=tr_dataset,
    tracking_id=tracking_id,
    request_body=request_body,
)
```

##### `delete_group_by_tracking_id`

Delete a chunk_group with the given tracking id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
tracking_id = "value"  # Tracking id of the chunk_group to delete
delete_chunks = True  # Delete the chunks within the group

# Make request
response = client.delete_group_by_tracking_id(
    tr_dataset=tr_dataset,
    tracking_id=tracking_id,
    delete_chunks=delete_chunks,
)
```

##### `get_chunk_group`

Fetch the group with the given id.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
group_id = "value"  # Id of the group you want to fetch.

# Make request
response = client.get_chunk_group(
    tr_dataset=tr_dataset,
    group_id=group_id,
)
```

##### `delete_chunk_group`

This will delete a chunk_group. If you set delete_chunks to true, it will also delete the chunks within the group. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
group_id = "value"  # Id of the group you want to fetch.
delete_chunks = True  # Delete the chunks within the group

# Make request
response = client.delete_chunk_group(
    tr_dataset=tr_dataset,
    group_id=group_id,
    delete_chunks=delete_chunks,
)
```

##### `get_chunks_in_group`

Route to get all chunks for a group. The response is paginated, with each page containing 10 chunks. Page is 1-indexed.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
group_id = "value"  # Id of the group you want to fetch.
x_api_version = None  # The version of the API to use for the request
page = 123  # The page of chunks to get from the group

# Make request
response = client.get_chunks_in_group(
    tr_dataset=tr_dataset,
    group_id=group_id,
    x_api_version=x_api_version,
    page=page,
)
```

##### `get_groups_for_dataset`

Fetch the groups which belong to a dataset specified by its id.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
dataset_id = "value"  # The id of the dataset to fetch groups for.
page = 123  # The page of groups to fetch. Page is 1-indexed.

# Make request
response = client.get_groups_for_dataset(
    tr_dataset=tr_dataset,
    dataset_id=dataset_id,
    page=page,
)
```


#### Crawl

##### `get_crawl_requests_for_dataset`

This endpoint is used to get all crawl requests for a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id to use for the request
page = None  # The page number to retrieve
limit = None  # The number of items to retrieve per page

# Make request
response = client.get_crawl_requests_for_dataset(
    tr_dataset=tr_dataset,
    page=page,
    limit=limit,
)
```

##### `create_crawl`

This endpoint is used to create a new crawl request for a dataset. The request payload should contain the crawl options to use for the crawl.

```python
# Parameters
tr_dataset = "value"  # The dataset id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.create_crawl(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `update_crawl_request`

This endpoint is used to update an existing crawl request for a dataset. The request payload should contain the crawl id and the crawl options to update for the crawl.

```python
# Parameters
tr_dataset = "value"  # The dataset id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.update_crawl_request(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `delete_crawl_request`

This endpoint is used to delete an existing crawl request for a dataset. The request payload should contain the crawl id to delete.

```python
# Parameters
tr_dataset = "value"  # The dataset id to use for the request
crawl_id = "value"  # The id of the crawl to delete

# Make request
response = client.delete_crawl_request(
    tr_dataset=tr_dataset,
    crawl_id=crawl_id,
)
```


#### Dataset

##### `create_dataset`

Dataset will be created in the org specified via the TR-Organization header. Auth'ed user must be an owner of the organization to create a dataset.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.create_dataset(
    tr_organization=tr_organization,
    request_body=request_body,
)
```

##### `update_dataset`

One of id or tracking_id must be provided. The auth'ed user must be an owner of the organization to update a dataset.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.update_dataset(
    tr_organization=tr_organization,
    request_body=request_body,
)
```

##### `batch_create_datasets`

Datasets will be created in the org specified via the TR-Organization header. Auth'ed user must be an owner of the organization to create datasets. If a tracking_id is ignored due to it already existing on the org, the response will not contain a dataset with that tracking_id and it can be assumed that a dataset with the missing tracking_id already exists.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.batch_create_datasets(
    tr_organization=tr_organization,
    request_body=request_body,
)
```

##### `clear_dataset`

Removes all chunks, files, and groups from the dataset while retaining the analytics and dataset itself. The auth'ed user must be an owner of the organization to clear a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
dataset_id = "value"  # The id of the dataset you want to clear.

# Make request
response = client.clear_dataset(
    tr_dataset=tr_dataset,
    dataset_id=dataset_id,
)
```

##### `get_events`

Get events for the dataset specified by the TR-Dataset header.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_events(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_all_tags`

Scroll through all tags in the dataset and get the number of chunks in the dataset with that tag plus the total number of unique tags for the whole datset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_all_tags(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_datasets_from_organization`

Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
organization_id = "value"  # id of the organization you want to retrieve datasets for
limit = None  # The number of records to return
offset = None  # The number of records to skip

# Make request
response = client.get_datasets_from_organization(
    tr_organization=tr_organization,
    organization_id=organization_id,
    limit=limit,
    offset=offset,
)
```

##### `get_pagefind_index_for_dataset`

Returns the root URL for your pagefind index, will error if pagefind is not enabled

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.

# Make request
response = client.get_pagefind_index_for_dataset(
    tr_dataset=tr_dataset,
)
```

##### `create_pagefind_index_for_dataset`

Uses pagefind to index the dataset and store the result into a CDN for retrieval. The auth'ed
user must be an admin of the organization to create a pagefind index for a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.

# Make request
response = client.create_pagefind_index_for_dataset(
    tr_dataset=tr_dataset,
)
```

##### `get_dataset_by_tracking_id`

Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
tracking_id = "value"  # The tracking id of the dataset you want to retrieve.

# Make request
response = client.get_dataset_by_tracking_id(
    tr_organization=tr_organization,
    tracking_id=tracking_id,
)
```

##### `delete_dataset_by_tracking_id`

Auth'ed user must be an owner of the organization to delete a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
tracking_id = "value"  # The tracking id of the dataset you want to delete.

# Make request
response = client.delete_dataset_by_tracking_id(
    tr_dataset=tr_dataset,
    tracking_id=tracking_id,
)
```

##### `get_usage_by_dataset_id`

Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
dataset_id = "value"  # The id of the dataset you want to retrieve usage for.

# Make request
response = client.get_usage_by_dataset_id(
    tr_dataset=tr_dataset,
    dataset_id=dataset_id,
)
```

##### `get_dataset`

Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
dataset_id = "value"  # The id of the dataset you want to retrieve.

# Make request
response = client.get_dataset(
    tr_dataset=tr_dataset,
    dataset_id=dataset_id,
)
```

##### `delete_dataset`

Auth'ed user must be an owner of the organization to delete a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
dataset_id = "value"  # The id of the dataset you want to delete.

# Make request
response = client.delete_dataset(
    tr_dataset=tr_dataset,
    dataset_id=dataset_id,
)
```

##### `create_etl_job`

This endpoint is used to create a new ETL job for a dataset.

```python
# Parameters
tr_dataset = "value"  # The dataset id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.create_etl_job(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```


#### File

##### `get_dataset_files_handler`

Get all files which belong to a given dataset specified by the dataset_id parameter. 10 files are returned per page.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
dataset_id = "value"  # The id of the dataset to fetch files for.
page = 123  # The page number of files you wish to fetch. Each page contains at most 10 files.

# Make request
response = client.get_dataset_files_handler(
    tr_dataset=tr_dataset,
    dataset_id=dataset_id,
    page=page,
)
```

##### `upload_file_handler`

Upload a file to S3 bucket attached to your dataset. You can select between a naive chunking strategy where the text is extracted with Apache Tika and split into segments with a target number of segments per chunk OR you can use a vision LLM to convert the file to markdown and create chunks per page. Auth'ed user must be an admin or owner of the dataset's organization to upload a file.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.upload_file_handler(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `create_presigned_url_for_csv_jsonl`

This route is useful for uploading very large CSV or JSONL files. Once you have completed the upload, chunks will be automatically created from the file for each line in the CSV or JSONL file. The chunks will be indexed and searchable. Auth'ed user must be an admin or owner of the dataset's organization to upload a file.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.create_presigned_url_for_csv_jsonl(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `upload_html_page`

Chunk HTML by headings and queue for indexing into the specified dataset.

```python
# Parameters
request_body = {}  # Add your request body here

# Make request
response = client.upload_html_page(
    request_body=request_body,
)
```

##### `get_file_handler`

Get a signed s3 url corresponding to the file_id requested such that you can download the file.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
file_id = "value"  # The id of the file to fetch
content_type = None  # Optional field to override the presigned url's Content-Type header

# Make request
response = client.get_file_handler(
    tr_dataset=tr_dataset,
    file_id=file_id,
    content_type=content_type,
)
```

##### `delete_file_handler`

Delete a file from S3 attached to the server based on its id. This will disassociate chunks from the file, but only delete them all together if you specify delete_chunks to be true. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
file_id = "value"  # The id of the file to delete
delete_chunks = True  # Delete the chunks within the group

# Make request
response = client.delete_file_handler(
    tr_dataset=tr_dataset,
    file_id=file_id,
    delete_chunks=delete_chunks,
)
```


#### Health

##### `health_check`

Confirmation that the service is healthy and can make embedding vectors

```python
# Make request
response = client.health_check()
```


#### Invitation

##### `post_invitation`

Invitations act as a way to invite users to join an organization. After a user is invited, they will automatically be added to the organization with the role specified in the invitation once they set their. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.post_invitation(
    tr_organization=tr_organization,
    request_body=request_body,
)
```

##### `delete_invitation`

Delete an invitation by id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
invitation_id = "value"  # The id of the invitation to delete

# Make request
response = client.delete_invitation(
    tr_organization=tr_organization,
    invitation_id=invitation_id,
)
```

##### `get_invitations`

Get all invitations for the organization. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
organization_id = "value"  # The organization id to get invitations for

# Make request
response = client.get_invitations(
    tr_organization=tr_organization,
    organization_id=organization_id,
)
```


#### Message

##### `create_message`

Create message. Messages are attached to topics in order to coordinate memory of gen-AI chat sessions.Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.create_message(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `edit_message`

This will delete the specified message and replace it with a new message. All messages after the message being edited in the sort order will be deleted. The new message will be generated by the AI based on the new content provided in the request body. The response will include Chunks first on the stream if the topic is using RAG. The structure will look like `[chunks]||mesage`. See docs.trieve.ai for more information. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.edit_message(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `regenerate_message`

Regenerate the assistant response to the last user message of a topic. This will delete the last message and replace it with a new message. The response will include Chunks first on the stream if the topic is using RAG. The structure will look like `[chunks]||mesage`. See docs.trieve.ai for more information. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.regenerate_message(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `regenerate_message_patch`

Regenerate the assistant response to the last user message of a topic. This will delete the last message and replace it with a new message. The response will include Chunks first on the stream if the topic is using RAG. The structure will look like `[chunks]||mesage`. See docs.trieve.ai for more information. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.regenerate_message_patch(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_tool_function_params`

This endpoint will generate the parameters for a tool function based on the user's message and image URL provided in the request body. The response will include the parameters for the tool function as a JSON object.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.get_tool_function_params(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_message_by_id`

Quickly get the full object for a given message. From the message, you can get the topic and all messages which exist on that topic.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
message_id = "value"  # The ID of the message to get.

# Make request
response = client.get_message_by_id(
    tr_dataset=tr_dataset,
    message_id=message_id,
)
```

##### `get_all_topic_messages`

If the topic is a RAG topic then the response will include Chunks first on each message. The structure will look like `[chunks]||mesage`. See docs.trieve.ai for more information.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
messages_topic_id = "value"  # The ID of the topic to get messages for.

# Make request
response = client.get_all_topic_messages(
    tr_dataset=tr_dataset,
    messages_topic_id=messages_topic_id,
)
```


#### Organization

##### `create_organization`

Create a new organization. The auth'ed user who creates the organization will be the default owner of the organization.

```python
# Parameters
request_body = {}  # Add your request body here

# Make request
response = client.create_organization(
    request_body=request_body,
)
```

##### `update_organization`

Update an organization. Only the owner of the organization can update it.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.update_organization(
    tr_organization=tr_organization,
    request_body=request_body,
)
```

##### `get_organization_api_keys`

Get the api keys which belong to the organization. The actual api key values are not returned, only the ids, names, and creation dates.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request.

# Make request
response = client.get_organization_api_keys(
    tr_organization=tr_organization,
)
```

##### `create_organization_api_key`

Create a new api key for the organization. Successful response will contain the newly created api key.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request.
request_body = {}  # Add your request body here

# Make request
response = client.create_organization_api_key(
    tr_organization=tr_organization,
    request_body=request_body,
)
```

##### `delete_organization_api_key`

Delete an api key for the auth'ed organization.

```python
# Parameters
api_key_id = "value"  # The id of the api key to delete
tr_organization = "value"  # The organization id to use for the request.

# Make request
response = client.delete_organization_api_key(
    api_key_id=api_key_id,
    tr_organization=tr_organization,
)
```

##### `update_all_org_dataset_configs`

Update the configurations for all datasets in an organization. Only the specified keys in the configuration object will be changed per dataset such that you can preserve dataset unique values. Auth'ed user or api key must have an owner role for the specified organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.update_all_org_dataset_configs(
    tr_organization=tr_organization,
    request_body=request_body,
)
```

##### `get_organization_usage`

Fetch the current usage specification of an organization by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
organization_id = "value"  # The id of the organization you want to fetch the usage of.

# Make request
response = client.get_organization_usage(
    tr_organization=tr_organization,
    organization_id=organization_id,
)
```

##### `get_organization_users`

Fetch the users of an organization by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
organization_id = "value"  # The id of the organization you want to fetch the users of.

# Make request
response = client.get_organization_users(
    tr_organization=tr_organization,
    organization_id=organization_id,
)
```

##### `get_organization`

Fetch the details of an organization by its id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
organization_id = "value"  # The id of the organization you want to fetch.

# Make request
response = client.get_organization(
    tr_organization=tr_organization,
    organization_id=organization_id,
)
```

##### `delete_organization`

Delete an organization by its id. The auth'ed user must be an owner of the organization to delete it.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
organization_id = "value"  # The id of the organization you want to fetch.

# Make request
response = client.delete_organization(
    tr_organization=tr_organization,
    organization_id=organization_id,
)
```


#### Public

##### `public_page`



```python
# Parameters
dataset_id = "value"  # The id or tracking_id of the dataset you want to get the demo page for.

# Make request
response = client.public_page(
    dataset_id=dataset_id,
)
```


#### Stripe

##### `create_setup_checkout_session`

Create a checkout session (setup)

```python
# Parameters
organization_id = "value"  # The id of the organization to create setup checkout session for.

# Make request
response = client.create_setup_checkout_session(
    organization_id=organization_id,
)
```

##### `get_all_invoices`

Get a list of all invoices

```python
# Parameters
organization_id = "value"  # The id of the organization to get invoices for.

# Make request
response = client.get_all_invoices(
    organization_id=organization_id,
)
```

##### `direct_to_payment_link`

Get a 303 SeeOther redirect link to the stripe checkout page for the plan and organization

```python
# Parameters
plan_id = "value"  # id of the plan you want to subscribe to
organization_id = "value"  # id of the organization you want to subscribe to the plan

# Make request
response = client.direct_to_payment_link(
    plan_id=plan_id,
    organization_id=organization_id,
)
```

##### `get_all_plans`

Get a list of all plans

```python
# Make request
response = client.get_all_plans()
```

##### `cancel_subscription`

Cancel a subscription by its id

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
subscription_id = "value"  # id of the subscription you want to cancel

# Make request
response = client.cancel_subscription(
    tr_organization=tr_organization,
    subscription_id=subscription_id,
)
```

##### `update_subscription_plan`

Update a subscription to a new plan

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
subscription_id = "value"  # id of the subscription you want to update
plan_id = "value"  # id of the plan you want to subscribe to

# Make request
response = client.update_subscription_plan(
    tr_organization=tr_organization,
    subscription_id=subscription_id,
    plan_id=plan_id,
)
```


#### Topic

##### `create_topic`

Create a new chat topic. Topics are attached to a owner_id's and act as a coordinator for conversation message history of gen-AI chat sessions. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.create_topic(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `update_topic`

Update an existing chat topic. Currently, only the name of the topic can be updated. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.update_topic(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `clone_topic`

Create a new chat topic from a `topic_id`. The new topic will be attched to the owner_id and act as a coordinator for conversation message history of gen-AI chat sessions. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
request_body = {}  # Add your request body here

# Make request
response = client.clone_topic(
    tr_dataset=tr_dataset,
    request_body=request_body,
)
```

##### `get_all_topics_for_owner_id`

Get all topics belonging to an arbitary owner_id. This is useful for managing message history and chat sessions. It is common to use a browser fingerprint or your user's id as the owner_id. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
owner_id = "value"  # The owner_id to get topics of; A common approach is to use a browser fingerprint or your user's id
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.

# Make request
response = client.get_all_topics_for_owner_id(
    owner_id=owner_id,
    tr_dataset=tr_dataset,
)
```

##### `delete_topic`

Delete an existing chat topic. When a topic is deleted, all associated chat messages are also deleted. Auth'ed user or api key must have an admin or owner role for the specified dataset's organization.

```python
# Parameters
tr_dataset = "value"  # The dataset id or tracking_id to use for the request. We assume you intend to use an id if the value is a valid uuid.
topic_id = "value"  # The id of the topic you want to delete.

# Make request
response = client.delete_topic(
    tr_dataset=tr_dataset,
    topic_id=topic_id,
)
```


#### User

##### `update_user`

Update a user's information for the org specified via header. If the user_id is not provided, the auth'ed user will be updated. If the user_id is provided, the role of the auth'ed user or api key must be an admin (1) or owner (2) of the organization.

```python
# Parameters
tr_organization = "value"  # The organization id to use for the request
request_body = {}  # Add your request body here

# Make request
response = client.update_user(
    tr_organization=tr_organization,
    request_body=request_body,
)
```

##### `get_user_api_keys`

Get the api keys which belong to the auth'ed user. The actual api key values are not returned, only the ids, names, and creation dates.

```python
# Make request
response = client.get_user_api_keys()
```

##### `delete_user_api_key`

Delete an api key for the auth'ed user.

```python
# Parameters
api_key_id = "value"  # The id of the api key to delete

# Make request
response = client.delete_user_api_key(
    api_key_id=api_key_id,
)
```


#### Metrics

##### `get_metrics`

This route allows you to view the number of items in each queue in the Prometheus format.

```python
# Make request
response = client.get_metrics()
```



## Middleware

You can add middleware functions to be called before and after each request:

```python
def before_request(request):
    print(f"About to make request: {request.method} {request.url}")

def after_request(response):
    print(f"Got response: {response.status_code}")

client = TrieveAPIClient(
    before_request=before_request,
    after_request=after_request,
)
```

## Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest`

## License

BSL
