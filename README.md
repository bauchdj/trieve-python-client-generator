# Borea Python Client Generator

This repository contains a Python SDK generator. It generates a Python client library from an OpenAPI specification.

## Setup

### Prerequisites

-   Python 3.8 or higher
-   pip (Python package installer)

### Quick Setup (Recommended)

Run the automated setup script:

```bash
./setup.sh
```

This script will:

1. Create a Python virtual environment (`.venv`)
2. Activate the virtual environment
3. Install all required dependencies

Available options:

```bash
./setup.sh [OPTIONS]

Options:
  -r, --recreate    Recreate virtual environment (deletes existing .venv)
  -i, --reinstall   Reinstall all requirements
  -h, --help        Show this help message
```

### Manual Setup

If you prefer to set up manually, follow these steps:

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

-   On macOS/Linux:

```bash
source .venv/bin/activate
```

-   On Windows:

```bash
.venv\Scripts\activate
```

3. Install the package dependencies:

```bash
pip install -r src/requirements.txt
```

## Usage

### Running the Python SDK Generator

1. Ensure you have a valid OpenAPI specification file (`openapi.json`) in the root directory or provide the path via the `--input` option or in the `generator.input` setting in `borea.config.json`.

2. Run the SDK generator:

```bash
python -m src.python_sdk_generator.python_sdk_generator
```

3. Show this help message with `--help`:

```bash
Usage: python -m src.python_sdk_generator.python_sdk_generator
           [OPTIONS]

  Generate a Python SDK from an OpenAPI specification.

Options:
  --input PATH           OpenAPI specification file (JSON or YAML)
  -o, --sdk-output PATH  Output directory for the generated SDK
  --models-output PATH   Output directory for generated models (default: <sdk-output>/models)
  --tests BOOLEAN        Generate tests (default: False)
  --config TEXT          Path to borea.config.json
  --help                 Show this message and exit.
```

The generator will create the Python client library based on the OpenAPI specification.

### Configuration

The project uses `borea.config.json` for configuration settings. The default configuration includes:

```json
{
	"generator": {
		"input": "openapi.json",
		"sdkOutput": "generated_sdk",
		"modelsOutput": "models",
		"tests": false
	},
	"ignores": []
}
```

You can modify this file to add specific patterns or files to ignore during the generation process.
Any file or folders matching a glob pattern will not be created or overwritten.

You can also include the generation parameters.

## Running Tests

**To be implemented...**

To run the test suite:

```bash
python -m pytest
```

## Project Structure

-   `src/` - Contains the source code for the SDK generator
-   `openapi.json` - OpenAPI specification file or wherever you decide to put it
-   `borea.config.json` - Configuration file for the generator
-   `.venv/` - Python virtual environment (created during setup)

## License

This project is licensed under the terms specified in the LICENSE file.
