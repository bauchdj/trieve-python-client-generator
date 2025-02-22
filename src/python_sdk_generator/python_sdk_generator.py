import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import click
import black
from jinja2 import Environment, FileSystemLoader

from .models.schema_model import SchemaPyJinja
from .models.base_client_models import (
    BaseClientPyJinja,
    OpenAPITagMetadata,
)
from .models.client_models import ClientPyJinja, MethodMetadata, MethodParameter
from .file_writer import ConfigurableFileWriter
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
        config_path: Optional[str] = None,
    ):
        self.metadata = metadata
        self.output_dir = output_dir
        self.models_dir = models_dir
        self.generate_tests = generate_tests
        self.template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        self.file_writer = ConfigurableFileWriter(config_path)

    def _clean_lower(self, tag: str) -> str:
        """Clean tag name to be a valid Python identifier"""
        return tag.lower().replace(" ", "_").replace("-", "_")

    def _clean_capitalize(self, name: str) -> str:
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

    def _clean_schema_name(self, name: str) -> str:
        """Clean name to be a valid Python identifier"""
        return name.replace("-", "_").replace(" ", "_")

    def _replace_dashes_with_underscores(self, name: str) -> str:
        """Replace dashes with underscores"""
        return name.replace("-", "_")

    def _replace_spaces_with_underscores(self, name: str) -> str:
        """Replace spaces with underscores"""
        return name.replace(" ", "_")

    def _format_description(self, description: str) -> str:
        """Format description to be a valid Python docstring"""
        return (
            description.replace("\\t", "")
            .replace("\\n", "")
            .replace("\\r", "")
            .replace('"', "'")
        )

    def _group_operations_by_tag(
        self,
    ) -> Tuple[Dict[str, List[Operation]], Dict[str, OpenAPITagMetadata]]:
        """Group operations by their tags"""
        operations_by_tag: Dict[str, List[Operation]] = {}
        tag_metadata_by_tag: Dict[str, OpenAPITagMetadata] = {}
        for op in self.metadata.operations:
            tag = op.tag
            tag_lowered = self._clean_lower(tag)
            if tag_lowered not in operations_by_tag:
                operations_by_tag[tag_lowered] = []
            operations_by_tag[tag_lowered].append(op)

            tag_capitalized = self._clean_capitalize(tag)
            tag_filename = tag_lowered + "_handler"

            tag_metadata_by_tag[tag_lowered] = OpenAPITagMetadata(
                tag=tag,
                tag_dir=tag_lowered,
                tag_filename=tag_filename,
                tag_class_name=tag_capitalized,
                tag_prop_name=tag_lowered,
                tag_description="",
            )

        return operations_by_tag, tag_metadata_by_tag

    def _generate_models(self):
        """Generate Pydantic models using datamodel-code-generator"""

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
        self,
        class_name: str,
        tag_description: str,
        operations: List[Operation],
        parent_class_name: str,
        base_client_filename: str,
    ) -> str:
        """Generate a client class for a specific tag"""
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
                    method_name=op.operation_id,
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
            parent_class_name=parent_class_name,
            parent_filename=base_client_filename,
            class_name=class_name,
            description=class_description,
            methods=methods,
        ).model_dump()

        return self._render_template_and_format_code(
            "client.py.jinja", template_metadata=template_metadata
        )

    def _generate_base_client(
        self, parent_class_name: str, tags: List[OpenAPITagMetadata]
    ) -> str:
        """Generate the base client class"""
        http_headers = self.metadata.headers
        template_metadata = BaseClientPyJinja(
            class_name=parent_class_name,
            class_title=self.metadata.info.title,
            class_description=self.metadata.info.description,
            base_url=self.metadata.servers[0].url,
            http_headers=http_headers,
            tags=tags,
        ).model_dump()

        return self._render_template_and_format_code(
            "base_client.py.jinja", template_metadata=template_metadata
        )

    def _generate_schema_files(self, file_ext: str, models_filename: str) -> None:
        """Generate individual schema files for each component in the models_output directory."""
        self.file_writer.create_directory(str(self.models_dir))

        # init_file = self.models_dir / "__init__.py"
        # self.file_writer.write(str(init_file), "")

        schemas = {
            **self.metadata.components.schemas,
            # **self.metadata.components.securitySchemes,
        }

        for schema_name, schema_data in schemas.items():
            file_name = self._clean_schema_name(schema_name) + file_ext
            file_path = self.models_dir / file_name
            description = schema_data.get("description", "")
            description = self._format_description(description)

            template_metadata = SchemaPyJinja(
                schema_name=schema_name,
                schema_data=schema_data,
                models_filename=models_filename,
                description=description,
            ).model_dump()

            rendered_code = self._render_template_and_format_code(
                "schema.py.jinja", template_metadata=template_metadata
            )
            self.file_writer.write(str(file_path), rendered_code)

    def _render_template_and_format_code(
        self, template_name: str, template_metadata: Any
    ) -> str:
        template = self.env.get_template(template_name)
        try:
            rendered_code = template.render(template_metadata)
        except Exception as e:
            click.echo(template_metadata)
            raise e
        try:
            formatted_code = black.format_str(rendered_code, mode=black.Mode())
        except Exception as e:
            click.echo(rendered_code)
            print(template_metadata.get("description"))
            raise e
        return formatted_code

    def _generate_tests(self, tag: str, operations: List[Operation]) -> str:
        """Generate tests for a specific tag"""
        template = self.env.get_template("test_client.py.jinja")
        rendered_code = template.render(
            tag=tag,
            operations=operations,
            class_name=self._clean_capitalize(tag),
            metadata=self.metadata,
        )
        formatted_code = black.format_str(rendered_code, mode=black.Mode())
        return formatted_code

    def _generate_readme(self, operations_by_tag: Dict[str, List[Operation]]) -> str:
        """Generate README.md with SDK documentation"""
        template = self.env.get_template("README.md.jinja")
        rendered_code = template.render(
            metadata=self.metadata, operations_by_tag=operations_by_tag
        )
        return rendered_code

    def _get_tag_description(self, tag: str) -> Union[str, None]:
        for t in self.metadata.tags:
            if t == tag:
                return t.description
        return None

    def generate(self) -> None:
        """Generate the SDK."""
        file_ext = ".py"

        # Create output directories
        self.file_writer.create_directory(str(self.output_dir))

        # Write the complete spec
        openapi_file = self.output_dir / "openapi.json"
        self.file_writer.write(
            str(openapi_file), json.dumps(self.metadata.openapi, indent=2)
        )

        # Generate models
        openapi_path = str(Path(self.metadata.source_file))
        models_file = "models"
        models_file_path = models_file + file_ext
        self.file_writer.generate_python_models(
            str(self.models_dir), models_file_path, openapi_path
        )

        # Generate schema files
        self._generate_schema_files(file_ext, models_file)

        # Generate base client
        src_dir = self.output_dir / "src"
        self.file_writer.create_directory(str(src_dir))

        # Generate test directory if needed
        test_dir = self.output_dir / "tests"
        if self.generate_tests:
            self.file_writer.create_directory(str(test_dir))

        # Parent Class Formatted Path and Name
        parent_class_name = self._clean_capitalize(self.metadata.info.title)

        # Group operations by tag
        operations_by_tag, tag_metadata_by_tag = self._group_operations_by_tag()

        # Generate base client
        base_client_filename = self._clean_file_name(self.metadata.info.title)
        base_client_file = base_client_filename + file_ext
        base_client_path = src_dir / base_client_file
        base_client_content = self._generate_base_client(
            parent_class_name, tag_metadata_by_tag.values()
        )
        self.file_writer.write(str(base_client_path), base_client_content)

        for tag, operations in operations_by_tag.items():
            tag_metadata = tag_metadata_by_tag[tag]
            tag_dir_path = src_dir / tag_metadata.tag_dir
            tag_test_dir_path = test_dir / tag_metadata.tag_dir
            self.file_writer.create_directory(str(tag_dir_path))
            if self.generate_tests:
                self.file_writer.create_directory(str(tag_test_dir_path))

            for op in operations:
                handler_file_dir_path = tag_dir_path / op.operation_id
                self.file_writer.create_directory(str(handler_file_dir_path))
                handler_file = op.operation_id + file_ext
                handler_file_path = handler_file_dir_path / handler_file
                operation_handler_content = ""
                self.file_writer.write(
                    str(handler_file_path), operation_handler_content
                )

                # Generate tests
                if self.generate_tests:
                    handler_test_file_dir_path = tag_test_dir_path / op.operation_id
                    self.file_writer.create_directory(str(handler_test_file_dir_path))
                    handler_test_file = op.operation_id + "_test" + file_ext
                    handler_test_file_path = (
                        handler_test_file_dir_path / handler_test_file
                    )
                    test_content = ""
                    # test_content = self._generate_tests(tag, operations)
                    self.file_writer.write(str(handler_test_file_path), test_content)

        # Generate README
        readme_path = self.output_dir / "README.md"
        readme_content = self._generate_readme(operations_by_tag)
        self.file_writer.write(str(readme_path), readme_content)


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
    required=False,
    type=click.Path(),
    help="Output directory for generated models (default: <sdk-output>/models)",
)
@click.option(
    "--tests/--no-tests", default=False, help="Generate tests (default: False)"
)
@click.option("--config", required=False, type=str, help="Path to borea.config.json")
def main(
    input_file: str,
    sdk_output: str,
    models_output: Optional[str],
    tests: bool,
    config: Optional[str],
):
    """Generate a Python SDK from an OpenAPI specification."""
    openapi_path = str(Path(input_file).resolve())
    parser = OpenAPIParser(openapi_path)
    metadata = parser.parse()
    sdk_output_path = Path(sdk_output)
    models_output_path = (
        Path(models_output) if models_output else sdk_output_path / "models"
    )

    generator = SDKGenerator(
        metadata,
        sdk_output_path,
        models_output_path,
        generate_tests=tests,
        config_path=config,
    )
    generator.generate()

    click.echo(f"Successfully generated SDK in: {sdk_output}")


if __name__ == "__main__":
    main()
