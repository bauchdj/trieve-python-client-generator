import os
from dotenv import load_dotenv
from generated_sdk.trieveapi_sdk import TrieveAPISDK
from generated_sdk.models import *

# Load environment variables from .env file
load_dotenv()

# Initialize the SDK with environment variables
tr_dataset_id = os.getenv("TRIEVE_DATASET_ID")
api_key = os.getenv("TRIEVE_API_KEY")

# Create SDK instance
sdk = TrieveAPISDK(api_key=api_key)

def test_search_chunks():
    """Test searching chunks functionality"""
    try:
        result = sdk.search_chunks(
            TR_Dataset=tr_dataset_id,
            query="bird",
            search_type="semantic",
            page=5
        )
        print("Search results:", result)
    except Exception as e:
        print(f"Error searching chunks: {e}")

def test_create_chunk():
    """Test creating a new chunk"""
    try:
        result = sdk.create_chunk(
            TR_Dataset=tr_dataset_id,
        )
        print("Created chunk:", result)
    except Exception as e:
        print(f"Error creating chunk: {e}")

if __name__ == "__main__":
    if not api_key:
        print("Please set TRIEVE_API_KEY in your .env file")
        exit(1)
        
    print(f"Testing SDK")
    test_search_chunks()
    # test_create_chunk()
