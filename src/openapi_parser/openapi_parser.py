import json
from typing import Any, Dict, List, Optional, Union
from models import *

class OpenAPIParser:
    """
    A parser to extract relevant API operation details from an OpenAPI specification.
    """
    def __init__(self, openapi_path: str):
        """
        Initialize the parser by loading the OpenAPI specification.
        """
        with open(openapi_path, "r") as f:
            self.openapi_spec = json.load(f)
        self.paths = self.openapi_spec.get("paths", {})
        self.components = self.openapi_spec.get("components", {}).get("schemas", {})

    def parse(self) -> OpenAPIMetadata:
        """
        Parse the OpenAPI spec and return a list of operations filtered by criteria.
        """
        operations = []
        http_params = []
        for path, methods in self.paths.items():
            for method, details in methods.items():
                if "operationId" not in details:
                    continue
                operation = self._parse_operation(path, method, details)
                for http_param in operation.parameters:
                    self._add_unique(http_params, http_param.dict(by_alias=True))
                operations.append(operation)
        headers = [Parameter(**http_param) for http_param in http_params if "header" in http_param["in"]]
        return OpenAPIMetadata(operations=operations, headers=headers)

    def _add_unique(self, headers_list: List[Dict[str, Any]], new_header: Dict[str, Any]) -> None:
        """Add a dictionary to the list only if 'name' and 'in' fields are unique."""
        if not any(h["name"] == new_header["name"] and h["in"] == new_header["in"] for h in headers_list):
            headers_list.append(new_header)

    def _parse_operation(self, path: str, method: str, details: Dict[str, Any]) -> Operation:
        """
        Extract relevant details for an API operation.
        """
        return Operation(
            tag=details.get("tags", [""])[0],
            operationId=details["operationId"],
            method=method.upper(),
            path=path,
            summary=details.get("summary", ""),
            description=details.get("description", ""),
            parameters=self._parse_parameters(details.get("parameters", [])),
            request_body=self._parse_request_body(details.get("requestBody", {}))
        )

    def _parse_parameters(self, parameters: List[Dict[str, Any]]) -> List[Parameter]:
        """
        Extract and format parameter details.
        """
        params = []
        for param in parameters:
            # "in" is a key word in Python so param_data had to be used
            param_data = {
                "name": param["name"],
                "in": param["in"],
                "required": param.get("required", False),
                "type": self._resolve_type(param.get("schema", {})),
                "description": param.get("description", "")
            }
            params.append(Parameter(**param_data))
        return params

    def _parse_request_body(self, request_body: Dict[str, Any]) -> Union[RequestBody, bool]:
        """
        Extract and format request body details.
        """
        if not request_body:
            return False

        content = request_body.get("content", {})
        json_schema = content.get("application/json", {}).get("schema", {})
        required = request_body.get("required")
        json_schema_type = self._resolve_type(json_schema)
        nested_json_schema_refs = self._extract_refs(json_schema)
        nested_json_schemas = self._resolve_nested_types(json_schema)

        return RequestBody(
            required=required,
            type=json_schema_type,
            nested_json_schema_refs=nested_json_schema_refs,
            nested_json_schemas=nested_json_schemas,
            length_nested_json_schemas=len(nested_json_schemas)
        )

    def _resolve_type(self, schema: Dict[str, Any]) -> str:
        """
        Resolve and return the type of a given schema.
        """
        if "$ref" in schema:
            return schema["$ref"].split("/")[-1]
        if "allOf" in schema:
            return " & ".join([self._resolve_type(sub) for sub in schema["allOf"]])
        if "oneOf" in schema or "anyOf" in schema:
            return " | ".join([self._resolve_type(sub) for sub in schema.get("oneOf", []) + schema.get("anyOf", [])])
        if "not" in schema:
            return f"Not[{self._resolve_type(schema['not'])}]"
        return schema.get("type", "any")

    def _extract_refs(self, schema: Dict[str, Any]) -> List[str]:
        """
        Recursively extract referenced schema names.
        """
        refs = []
        if "$ref" in schema:
            ref_name = schema["$ref"].split("/")[-1]
            refs.append(ref_name)
            if ref_name in self.components:
                refs.extend(self._extract_refs(self.components[ref_name]))
        for key in ["allOf", "oneOf", "anyOf", "not"]:
            if key in schema:
                for sub_schema in schema[key] if isinstance(schema[key], list) else [schema[key]]:
                    refs.extend(self._extract_refs(sub_schema))
        return refs

    def _resolve_nested_types(self, schema: Dict[str, Any]) -> List[str]:
        """
        Recursively resolve nested types within a schema.
        """
        nested_types = []
        if "type" in schema:
            nested_types.append(schema)
        if "$ref" in schema:
            ref_name = schema["$ref"].split("/")[-1]
            if ref_name in self.components:
                nested_types.extend(self._resolve_nested_types(self.components[ref_name]))
        for key in ["allOf", "oneOf", "anyOf", "not"]:
            if key in schema:
                for sub_schema in schema[key] if isinstance(schema[key], list) else [schema[key]]:
                    nested_types.extend(self._resolve_nested_types(sub_schema))
        return nested_types

if __name__ == "__main__":
    parser = OpenAPIParser("openapi.json")
    operations = parser.parse() 
    print('Path Operations:', json.dumps(operations.dict(), indent=2))
