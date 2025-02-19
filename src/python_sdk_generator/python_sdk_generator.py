import json
from os import name
import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import click
import black
from jinja2 import Environment, FileSystemLoader

from .models.model_client import ClientPyJinja, MethodMetadata, MethodParameter
from ..openapi_parser.openapi_parser import OpenAPIParser
from ..openapi_parser.models import (
    HttpParameter,
    OpenAPIMetadata,
    Operation,
    SchemaMetadata,
)


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
            "components": {},  # We'll get this from the original spec
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
            "--input-file-type",
            "openapi",
            "--input",
            str(openapi_file),
            "--output",
            str(self.models_dir / "models.py"),
            "--use-standard-collections",
            "--use-schema-description",
            "--field-constraints",
            "--strict-nullable",
            "--wrap-string-literal",
            "--enum-field-as-literal",
            "one",
            "--use-double-quotes",
            "--use-default-kwarg",
            "--use-annotated",
            "--use-field-description",
            "--output-model-type",
            "pydantic_v2.BaseModel",
        ]
        subprocess.run(cmd, check=True)

    def format_type(self, type_info: Union[Dict, str, None]) -> str:
        resolved_type: str = "Any"
        if type_info is None:
            pass
        elif isinstance(type_info, str) and type_info not in ["object", "array"]:
            resolved_type = self._clean_type_name(type_info)
        elif isinstance(type_info, dict):
            if "$ref" in type_info:
                resolved_type = type_info["$ref"].split("/")[-1]
            elif type_info.get("type") == "array":
                resolved_type = f"List[{self.format_type(type_info.get('items', {}))}]"
            elif "type" in type_info and type_info["type"] not in ["object", "array"]:
                resolved_type = self._clean_type_name(type_info["type"])
            elif "allOf" in type_info:
                # TODO fix this when it hits
                # not hitting...
                resolved_type = " & ".join(
                    (
                        self.format_type(item)
                        if isinstance(item, dict) and "$ref" not in item
                        else item["$ref"].split("/")[-1]
                    )
                    for item in type_info["allOf"]
                )
            elif "oneOf" in type_info:
                # not hitting...
                resolved_type = f"Union[{', '.join(self.format_type(item) for item in type_info['oneOf'])}]"
            elif "anyOf" in type_info:
                # not hitting...
                resolved_type = f"Union[{', '.join(self.format_type(item) for item in type_info['anyOf'])}]"
            elif "not" in type_info:
                # not hitting...
                resolved_type = "Any"
            else:
                pass
        else:
            pass

        # print("END", resolved_type)
        return resolved_type

    def _get_single_nested_schema(
        self, schema: Union[SchemaMetadata, None]
    ) -> Union[Dict[str, Any], None]:
        if schema is None:
            return None
        if schema.length_nested_json_schemas != 1:
            return schema.model_dump()
        schema = schema.model_dump()
        nested_schema = schema.get("nested_json_schemas", [None])[0]
        if nested_schema:
            return nested_schema
        return schema

    def _method_params_from_http_params(
        self, http_params: List[HttpParameter], cond: Callable[[HttpParameter], bool]
    ) -> List[MethodParameter]:
        """
        Returns a list of MethodParameter objects based on the given condition.
        """
        return [
            MethodParameter(
                required=http_param.required,
                name=http_param.name,
                original_name=http_param.original_name,
                type=self.format_type(http_param.type),
                description=http_param.description,
            )
            for http_param in http_params
            if cond(http_param)
        ]

    def _method_params_from_schema_props(
        self,
        schema: Dict[str, Any],
        props: List[Dict[str, Any]],
        cond: Callable[[str, bool], bool],
    ) -> List[MethodParameter]:
        default_description = "No description provided"
        schema_required = schema.get("required", [])
        is_required = lambda prop_name, prop: prop_name in schema_required or prop.get(
            "required", False
        )
        return [
            MethodParameter(
                required=is_required(prop_name, prop),
                name=prop_name,
                type=self.format_type(prop),
                description=prop.get("description", None)
                or prop.get("nested_json_schemas", [schema])[0].get("description", None)
                or default_description,
            )
            for prop_name, prop in props.items()
            if cond(prop_name, is_required(prop_name, prop))
        ]

    def _method_param_from_request_body(
        self, request_body: Dict[str, Any]
    ) -> List[MethodParameter]:
        return [
            MethodParameter(
                required=request_body.get("required", False),
                name="request_body",
                type=self.format_type(request_body.get("type", None)),
                description=request_body.get("description", "Request body"),
            )
        ]

    def _resolve_method_params(
        self, operation: Operation, schema: Union[Dict[str, Any], None]
    ) -> Tuple[List[MethodParameter], List[MethodParameter]]:
        required_http_params: List[MethodParameter] = (
            self._method_params_from_http_params(
                operation.parameters, lambda http_param: http_param.required == True
            )
        )
        optional_http_params: List[MethodParameter] = (
            self._method_params_from_http_params(
                operation.parameters, lambda http_param: http_param.required != True
            )
        )
        http_param_names = [param.name for param in operation.parameters]

        required_schema_props: List[MethodParameter] = []
        optional_schema_props: List[MethodParameter] = []
        if schema is not None:
            schema_props = schema.get("properties", None)
            if schema_props:
                required_schema_props += self._method_params_from_schema_props(
                    schema,
                    schema_props,
                    lambda prop_name, is_required: is_required
                    and prop_name not in http_param_names,
                )
                optional_schema_props += self._method_params_from_schema_props(
                    schema,
                    schema_props,
                    lambda prop_name, is_required: not is_required
                    and prop_name not in http_param_names,
                )
            elif schema.get("required", False):
                required_schema_props += self._method_param_from_request_body(schema)
            else:
                optional_schema_props += self._method_param_from_request_body(schema)

        required_method_params = required_http_params + required_schema_props
        optional_method_params = optional_http_params + optional_schema_props

        return [required_method_params, optional_method_params]

    def _generate_client_class(
        self, tag: str, tag_description: str, operations: List[Operation]
    ) -> str:
        """Generate a client class for a specific tag"""
        class_name = self._clean_name(tag) + "Client"
        formatted_title = self.metadata.info.title.replace(" ", "").replace("-", "")
        formatted_import_path = self.metadata.info.title.lower().replace(" ", "_")
        class_description = tag_description or self.metadata.info.description

        methods: List[MethodMetadata] = []
        for op in operations:
            for param in op.parameters:
                # Add original name for query parameters
                param.original_name = param.name
                param.name = self._clean_parameter_name(param.name)
                param.type = self._clean_type_name(param.type)
            if op.request_body and isinstance(op.request_body, SchemaMetadata):
                op.request_body.type = self._clean_type_name(op.request_body.type)

            http_params = op.parameters
            request_body = op.request_body
            schema: Union[Dict[str, Any], None] = self._get_single_nested_schema(
                op.request_body
            )
            required_method_params, optional_method_params = (
                self._resolve_method_params(op, schema)
            )
            methods.append(
                MethodMetadata(
                    method_name=op.operationId,
                    description=op.description,
                    required_method_params=required_method_params,
                    optional_method_params=optional_method_params,
                    http_method=op.method.upper(),
                    path=op.path,
                    http_params=http_params,
                    request_body=request_body,
                    nested_schema=schema,
                )
            )

        template_metadata = ClientPyJinja(
            parent_class_formatted_import_path=formatted_import_path,
            parent_class_formatted_name=formatted_title,
            class_name=class_name,
            description=class_description,
            methods=methods,
        )

        template = self.env.get_template("client.py.jinja")
        rendered_code = template.render(template_metadata.model_dump())

        formatted_code = black.format_str(rendered_code, mode=black.Mode())
        return formatted_code

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
            metadata=self.metadata,
        )

    def _generate_readme(self) -> str:
        """Generate README.md with SDK documentation"""
        template = self.env.get_template("README.md.jinja")
        return template.render(
            metadata=self.metadata, operations_by_tag=self._group_operations_by_tag()
        )

    def _get_tag_description(self, tag: str) -> Union[str, None]:
        for t in self.metadata.tags:
            if t == tag:
                return t.description
        return None

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
        base_client_file = (
            self._clean_file_name(self.metadata.info.title) + "_client.py"
        )
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
            tag_description = self._get_tag_description(tag)
            client_content = self._generate_client_class(
                tag, tag_description, operations
            )
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
@click.option(
    "--input",
    "input_file",
    default="openapi.json",
    type=click.Path(exists=True),
    help="OpenAPI specification file (JSON or YAML)",
)
@click.option(
    "--sdk-output",
    "-o",
    default="generated_sdk",
    type=click.Path(),
    help="Output directory for the generated SDK",
)
@click.option(
    "--models-output",
    default="generated_sdk/models",
    type=click.Path(),
    help="Output directory for generated models (default: <sdk-output>/models)",
)
@click.option(
    "--tests/--no-tests", default=False, help="Generate tests (default: False)"
)
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
