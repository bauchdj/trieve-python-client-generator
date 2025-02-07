# Python SDK Generator

A tool for automatically generating a Python SDK from an OpenAPI specification. This generator creates a fully functional, type-safe Python client library with Pydantic models for request/response validation.

## Features

-   Generates Pydantic models from OpenAPI schemas
-   Creates a typed Python client with all API endpoints
-   Handles request/response serialization
-   Includes proper error handling
-   Generates comprehensive documentation
-   Uses modern Python features and type hints
-   Supports custom output directory

## Prerequisites

-   Python 3.9 or higher
-   pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd python-sdk-generator
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Generate an SDK using the default settings:

```bash
python PythonSDKGenerator.py
```

This will:

-   Look for `openapi.json` in the current directory
-   Generate the SDK in a `generated_sdk` directory

### Advanced Usage

Specify a custom OpenAPI specification file and output directory:

```bash
python PythonSDKGenerator.py --spec path/to/your/openapi.json --output-dir path/to/output
```

### Command Line Arguments

-   `--spec`: Path to the OpenAPI specification file (default: openapi.json)
-   `--output-dir`: Directory where the SDK will be generated (default: ./generated_sdk)

## Generated SDK Structure

The generator creates the following files in the output directory:

-   `models.py`: Pydantic models for all schemas defined in the OpenAPI spec
-   `{project_name}_sdk.py`: Main SDK class with all API endpoint methods
-   `requirements.txt`: Dependencies required by the generated SDK
-   `README.md`: Documentation for using the generated SDK

## Generated SDK Usage

```python
from project_sdk import ProjectSDK

# Initialize the SDK
sdk = ProjectSDK(
    api_key="your_api_key",
    base_url="https://api.example.com"  # Optional, defaults to the URL from OpenAPI spec
)

# Make API calls
response = await sdk.some_endpoint(param1="value1", param2="value2")
```

## Features of Generated SDK

-   Type hints for all parameters and return values
-   Automatic request/response serialization using Pydantic
-   Proper error handling with descriptive error messages
-   Support for query parameters, path parameters, and request bodies
-   Automatic header management
-   Built-in retry logic for failed requests
-   Comprehensive docstrings for all methods

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
