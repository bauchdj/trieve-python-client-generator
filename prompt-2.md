**Task:** Generate a Python SDK based on an OpenAPI specification and its metadata.

You will receive OpenAPI metadata parsed into Pydantic models. Your task is to implement a Python SDK generator (`python_sdk_generator.py`) that produces the SDK based on this metadata.

### Input:

-   The OpenAPI metadata is provided as parsed Pydantic models:
    -   **OpenAPIMetadata**: Represents the entire OpenAPI metadata.
    -   **Info**: Represents the `info` section in OpenAPI.
    -   **Server**: Represents a server configuration in OpenAPI.
    -   **Parameter**: Represents parameters (header, query, path, or body) in OpenAPI operations.
    -   **RequestBody**: Represents the request body in an OpenAPI operation.
    -   **Operation**: Represents an individual OpenAPI operation.

### Task Breakdown:

1. **Parsing OpenAPI**:

    - Parse the paths, methods, `operationId`, tags, parameters, request/response body types, and `$ref` references.
    - Ensure the SDK methods respect the order of parameters (required first, then optional).

2. **SDK Generation**:

    - The SDK should use `httpx` for API requests.
    - Use classes named after the OpenAPI `tag`, such as `{tag}_client.py`.
    - Each method will correspond to an OpenAPI operation and be grouped by tags.
    - Function arguments will be built based on path response body properties and HTTP params (excluding headers).
    - Implement middleware support with `before_request` and `after_request` hooks (e.g., for logging and authentication).
    - Automatically detect HTTP header parameters and map them to class attributes, including security schemas.

3. **File Structure**:

    - `python_sdk_generator.py` (main generator).
    - `src/{tag}/{tag}_client.py` for tag-based SDK classes.
    - `models.py` in the `models/` folder in `generated_sdk/` for Pydantic models based on OpenAPI schemas.
    - SDK documentation will be auto-generated in the `README.md`.

4. **Middleware and Security Schemas**:

    - Implement automatic detection of HTTP header parameters and authentication schemes.

5. **Testing** (for later implementation):

    - For each generated method/class, a corresponding test will be created using `pytest`, validating the response parsing, request structure, and error handling.

6. **Requirements**:
    - Generate the `requirements.txt` for dependencies.
    - Install necessary libraries like `httpx`, `pydantic`, `datamodel-codegen`, etc.
    - Implement a simple `README.md` with SDK usage examples.

---

### **Pydantic Models (Metadata)**:

```python
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

class Parameter(BaseModel):
    """Represents an OpenAPI parameter"""
    name: str
    in_location: str = Field(..., alias="in")
    required: bool = False
    type: str
    description: str = ""

class RequestBody(BaseModel):
    """Represents an OpenAPI request body"""
    required: Optional[bool] = None
    type: str
    nested_json_schema_refs: List[str] = Field(default_factory=list)
    nested_json_schemas: List[Dict[str, Any]] = Field(default_factory=list)
    length_nested_json_schemas: int = 0

class Operation(BaseModel):
    """Represents an OpenAPI operation"""
    tag: str
    operationId: str
    method: str
    path: str
    summary: str = ""
    description: str = ""
    parameters: List[Parameter] = Field(default_factory=list)
    request_body: Union[RequestBody, bool] = Field(default_factory=False)

class Info(BaseModel):
    """Represents the 'info' object in OpenAPI metadata"""
    title: str
    version: str
    description: Optional[str] = ""
    termsOfService: Optional[str] = None
    contact: Optional[Dict[str, Any]] = None
    license: Optional[Dict[str, Any]] = None

class Server(BaseModel):
    """Represents a server in OpenAPI metadata"""
    url: str
    description: Optional[str] = ""
    variables: Optional[Dict[str, Dict[str, Any]]] = None

class OpenAPIMetadata(BaseModel):
    """Represents the parsed OpenAPI metadata"""
    openapi: str
    info: Info
    servers: List[Server]
    operations: List[Operation]
    headers: List[Parameter]
```

---

### **SDK Generator Implementation**:

1. **`python_sdk_generator.py`**:

    - The main script that will generate the SDK using the above models.
    - This script will read the OpenAPI file, parse it into the models, and generate the SDK code accordingly.
    - It will generate a tag-based directory structure, such as `src/{tag}/{tag}_client.py`, and the `models.py` in the `models/` folder.

2. **Middleware**:

    - Implement hooks for `before_request` and `after_request` to provide customization like logging and authentication.

3. **Naming Convention**:

    - Use camelCase for class names and snake_case for function names and variables.
    - Ensure tags and generated variables are cleaned to replace spaces and hyphens with underscores.

4. **Test Generation**:

    - Each generated SDK method will have an associated test.
    - Tests will validate response parsing, request structure, and error handling using OpenAPI examples.

5. **Output**:
    - The generator will produce SDK files in `src/`, model files in `models/`, and tests in `tests/`.

### **CLI Options**:

Use `click` to implement the CLI options:

-   `--input <path>`: The OpenAPI file (`json` or `yaml`).
-   `--sdk-output, -o <path>`: The directory where the SDK will be generated.
-   `--models-output <path>`: The directory for the generated models.
-   `--tests`: Flag to generate tests.

---

### **Model Generation Command (Example)**:

```bash
datamodel-codegen --input-file-type openapi \
    --input "openapi.json" --output "models.py" \
    --use-standard-collections --use-schema-description \
    --field-constraints --strict-nullable --wrap-string-literal \
    --enum-field-as-literal one --use-double-quotes \
    --use-default-kwarg --use-annotated --use-field-description \
    --output-model-type pydantic_v2.BaseModel
```

---

By implementing this, the resulting SDK will be modular, following the structure of OpenAPI metadata, and generating methods that adhere to OpenAPI specifications. The generated SDK will support middleware and flexible handling of authentication and logging.
