import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from jinja2 import Environment, FileSystemLoader

from ..openapi_parser.openapi_parser import OpenAPIParser
from ..openapi_parser.models import OpenAPIMetadata, Operation, SchemaMetadata

class SDKGenerator:
    def __init__(
        self,
        metadata: OpenAPIMetadata,
        output_dir: Path,
        models_dir: Path,
        generate_tests: bool = True,
    ):
        self.metadata = metadata
        self.output_dir = output_dir
        self.models_dir = models_dir
        self.generate_tests = generate_tests
        self.template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))

    def _clean_tag_name(self, tag: str) -> str:
        """Clean tag name to be a valid Python identifier"""
        return tag.lower().replace(" ", "_").replace("-", "_")

    def _clean_name(self, name: str) -> str:
        """Clean name to be a valid Python identifier"""
        # Remove spaces and dashes, convert to camel case
        words = name.replace("-", " ").replace("_", " ").split()
        return "".join(word.capitalize() for word in words)

    def _clean_parameter_name(self, name: str) -> str:
        """Clean parameter name to be a valid Python identifier"""
        # Convert hyphens to underscores
        return name.replace("-", "_").replace(" ", "_").lower()

    def _clean_type_name(self, type_name: str) -> str:
        """Clean type name to be a valid Python type"""
        type_map = {
            "string": "str",
            "integer": "int",
            "boolean": "bool",
            "number": "float",
            "array": "List",
            "object": "Dict[str, Any]",
        }
        return type_map.get(type_name.lower(), type_name)

    def _clean_file_name(self, name: str) -> str:
        """Clean name to be a valid file name"""
        # Convert to snake case
        name = name.replace("-", " ")
        words = name.split()
        return "_".join(word.lower() for word in words)

    def _group_operations_by_tag(self) -> Dict[str, List[Operation]]:
        """Group operations by their tags"""
        operations_by_tag: Dict[str, List[Operation]] = {}
        for op in self.metadata.operations:
            tag = self._clean_tag_name(op.tag)
            if tag not in operations_by_tag:
                operations_by_tag[tag] = []
            operations_by_tag[tag].append(op)
        return operations_by_tag

    def _generate_models(self):
        """Generate Pydantic models using datamodel-code-generator"""
        # Create a copy of the original OpenAPI spec with our metadata
        openapi_spec = {
            "openapi": self.metadata.openapi,
            "info": self.metadata.info.model_dump(),
            "servers": [s.model_dump() for s in self.metadata.servers],
            "paths": {},  # We'll get this from the original spec
            "components": {}  # We'll get this from the original spec
        }

        # Get the original spec from the parser
        with open(str(Path(self.metadata.source_file).resolve())) as f:
            original_spec = json.load(f)
            openapi_spec["paths"] = original_spec.get("paths", {})
            openapi_spec["components"] = original_spec.get("components", {})

        # Write the complete spec
        openapi_file = self.output_dir / "openapi.json"
        with open(openapi_file, "w") as f:
            json.dump(openapi_spec, f, indent=2)

        # Generate models
        self.models_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            "datamodel-codegen",
            "--input-file-type", "openapi",
            "--input", str(openapi_file),
            "--output", str(self.models_dir / "models.py"),
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

    def _generate_client_class(self, tag: str, operations: List[Operation]) -> str:
        """Generate a client class for a specific tag"""
        template = self.env.get_template("client.py.jinja")
        class_name = self._clean_name(tag) + "Client"
        # Clean parameter names and types in operations

        for op in operations:
            for param in op.parameters:
                # Add original name for query parameters
                param.original_name = param.name
                param.name = self._clean_parameter_name(param.name)
                param.type = self._clean_type_name(param.type)
            if op.request_body and isinstance(op.request_body, SchemaMetadata):
                op.request_body.type = self._clean_type_name(op.request_body.type)

        # removes nested models for jinja templating. SchemaMetadata model is causing 'is mapping' to be False when it should be True in jinja
        operations = [op.model_dump() for op in operations]
        metadata = self.metadata.model_dump()

        return template.render(
            tag=tag,
            operations=operations,
            class_name=class_name,
            metadata=metadata
        )

    def _generate_base_client(self) -> str:
        """Generate the base client class"""
        template = self.env.get_template("base_client.py.jinja")
        return template.render(metadata=self.metadata)

    def _generate_tests(self, tag: str, operations: List[Operation]) -> str:
        """Generate tests for a specific tag"""
        template = self.env.get_template("test_client.py.jinja")
        return template.render(
            tag=tag,
            operations=operations,
            class_name=self._clean_name(tag) + "Client",
            metadata=self.metadata
        )

    def _generate_readme(self) -> str:
        """Generate README.md with SDK documentation"""
        template = self.env.get_template("README.md.jinja")
        return template.render(
            metadata=self.metadata,
            operations_by_tag=self._group_operations_by_tag()
        )

    def generate(self):
        """Generate the complete SDK"""
        # Create directory structure
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        src_dir = self.output_dir / "src"
        src_dir.mkdir(exist_ok=True)
        tests_dir = self.output_dir / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Generate models
        self._generate_models()

        # Generate base client
        base_client_name = self._clean_name(self.metadata.info.title)
        base_client_file = self._clean_file_name(self.metadata.info.title) + "_client.py"
        base_client_path = src_dir / base_client_file
        base_client_content = self._generate_base_client()
        base_client_path.write_text(base_client_content)

        # Generate tag-specific clients
        operations_by_tag = self._group_operations_by_tag()
        for tag, operations in operations_by_tag.items():
            # Generate client
            tag_dir = src_dir / tag
            tag_dir.mkdir(exist_ok=True)
            client_path = tag_dir / f"{tag}_client.py"
            client_content = self._generate_client_class(tag, operations)
            client_path.write_text(client_content)

            if self.generate_tests:
                # Generate tests
                test_dir = tests_dir / tag
                test_dir.mkdir(exist_ok=True)
                test_path = test_dir / f"{tag}_test.py"
                test_content = self._generate_tests(tag, operations)
                test_path.write_text(test_content)

        # Generate README
        readme_path = self.output_dir / "README.md"
        readme_content = self._generate_readme()
        readme_path.write_text(readme_content)

@click.command()
@click.option("--input", "input_file", default="openapi.json", type=click.Path(exists=True),
              help="OpenAPI specification file (JSON or YAML)")
@click.option("--sdk-output", "-o", default="generated_sdk", type=click.Path(),
              help="Output directory for the generated SDK")
@click.option("--models-output", default="generated_sdk/models", type=click.Path(),
              help="Output directory for generated models (default: <sdk-output>/models)")
@click.option("--tests/--no-tests", default=False,
              help="Generate tests (default: False)")
def main(input_file: str, sdk_output: str, models_output: Optional[str], tests: bool):
    """Generate a Python SDK from an OpenAPI specification."""
    # Parse OpenAPI spec
    openapi_path = str(Path(input_file).resolve())
    parser = OpenAPIParser(openapi_path=openapi_path)
    metadata = parser.parse()

    # Set up paths
    sdk_dir = Path(sdk_output)
    models_dir = Path(models_output) if models_output else sdk_dir / "models"

    # Generate SDK
    generator = SDKGenerator(metadata, sdk_dir, models_dir, tests)
    generator.generate()

    print(f"Successfully generated SDK in: {sdk_dir}")

if __name__ == "__main__":
    main()