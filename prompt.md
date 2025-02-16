### Python SDK Generator

**Assumptions about `openapi.json`:**

-   Each path operation has a single tag in tags array and unique `operationId`.
-   HTTP params are usually headers and should be part of the class constructor. More details later.
-   `requestBody` and `responseBody` use `application/json` or `text/plain`.
-   Models are defined in `models.py` by schema name/title given in `openapi.json`.
-   `openapi.json` is the source of truth.

---

**Project Structure:**

```
├── python_sdk_generator.py
├── README.md
├── generated_sdk
│   ├── README.md
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── models
│   │   └── models.py
│   ├── src
│   │   ├── {tag}
│   │   │   └── {tag}.py
│   │   └── {openapi_title}_sdk.py
│   └── tests
│       └── {tag}
│           └── {tag}_test.py
├── openapi.json
└── requirements.txt
```

---

**CLI Configuration:**

-   `--input <path>`: Input OpenAPI file.
-   `--sdk-output, -o <path>`: SDK output directory.
-   `--models-output <path>`: Models output directory.
-   `--tag-folders`: Organize code by OpenAPI tags.
-   `--tests`: Include test files.
-   `--x-code-samples`: Include x-codeSamples from OpenAPI in Python on operation objects.
-   `--openapi-output <path>`: OpenAPI output directory.

---

**Model Generation:**  
Generate models using `datamodel-codegen` with the following function:

```Python
    def generate_models(self) -> None:
        """Generate Pydantic models using datamodel-code-generator."""
        cmd = [
            "datamodel-codegen",
            "--input-file-type", "openapi",
            "--input", self.input_file,
            "--output", str(self.models_output / "models.py"),
            "--use-standard-collections",
            "--use-schema-description",
            "--field-constraints",
            "--strict-nullable",
            "--wrap-string-literal",
            "--enum-field-as-literal", "one",
            "--use-double-quotes",
            "--use-default-kwarg",
            "--use-annotated",
            "--use-field-description",
            "--output-model-type", "pydantic_v2.BaseModel"
        ]
        subprocess.run(cmd, check=True)
```

---

**SDK Generation (`{openapi_title}_sdk.py`):**

-   Camelcase for all classes. Snake case for everything else.
-   Handle special characters in names, such as spaces, capitals, underscores, and hyphens, when generating.
-   Methods are named after OpenAPI `operationId`.
-   By default, all methods are defined within the SDK class, but if the --tag-folders option is used, methods are grouped by OpenAPI tags, with each tag represented as a subclass of SDK placed in its own folder and file; methods are accessed via {openapi_title}\_sdk.{tag}.{operationId}, and path operations without tags are assigned to the default class.

---

**Request/Response Body Handling:**

-   Parse JSON or `text/plain` request and response bodies.
-   Resolve `$ref` schemas for request/response body types.
-   Include response types in docstrings with status codes (`200 → Type1`, `400 → Type2`).
-   Use `Union[Type1, Type2]` for multiple response types.

---

**SDK Class Features:**

-   Detect all HTTP parameters in `openapi.json` and add them to the class constructor as optional arguments.
-   Write middleware functions named after each HTTP parameter, usage: `{openapi_title}\_sdk.{http_param_name}.{method_name} or {openapi_title}\_sdk.{http_param_name}.{tag}.{method_name}`.
-   Implement before/after middleware for request handling (e.g., logging, authentication).

---

**Testing (`tag_test.py`):**

-   Unit tests for each method organized by tags.
-   Include usage examples for documentation.

---

**Task:**  
Design and implement the `python_sdk_generator.py` file to fulfill the above requirements.
