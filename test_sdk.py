import os
from dotenv import load_dotenv

from generated_sdk.src.trieve_api import TrieveApi
from generated_sdk.models.models import (
    CreateChunkReqPayloadEnum,
    CreateSingleChunkReqPayload,
    CreateBatchChunkReqPayload,
)

# Load environment variables from .env file
load_dotenv()

# Initialize the SDK with environment variables
tr_dataset_id = os.getenv("TRIEVE_DATASET_ID")
api_key = os.getenv("TRIEVE_API_KEY")

# Create SDK instance
sdk = TrieveApi(api_key=api_key)


def test_create_chunk(request_body: CreateChunkReqPayloadEnum):
    """Test creating a new chunk"""
    try:
        result = sdk.chunk.create_chunk(
            tr_dataset=tr_dataset_id,
            request_body=request_body,
        )
        print("Created chunk:", result)
    except Exception as e:
        print(f"Error creating chunk: {e}")


def test_search_chunks(query: str):
    """Test searching chunks functionality"""
    try:
        # result = sdk.chunk.search_chunks(
        result = sdk.chunk.search_chunks(
            tr_dataset=tr_dataset_id, query=query, search_type="semantic", page=5
        )
        print("Search results:", result)
    except Exception as e:
        print(f"Error searching chunks: {e}")


def test_delete_chuck(chunk_id: str):
    """Test deleting the new chunk"""
    try:
        result = sdk.chunk.delete_chunk(tr_dataset=tr_dataset_id, chunk_id=chunk_id)
        print("Created chunk:", result)
    except Exception as e:
        print(f"Error creating chunk: {e}")


def main():
    if not api_key:
        print("Please set TRIEVE_API_KEY in your .env file")
        exit(1)

    print(f"Testing SDK")

    # Create a chunk
    # create_response = test_create_chunk()

    response_search = test_search_chunks("bird")
    print(response_search)

    # Delete the chunk
    # chunk_id = create_response["id"]
    # test_delete_chuck(chunk_id)


if __name__ == "__main__":
    main()
