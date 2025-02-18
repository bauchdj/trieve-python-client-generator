from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from jinja2 import Environment, FileSystemLoader
from ..openapi_parser.models import (
    OpenAPIMetadata, Endpoint, SchemaType, HttpParameter,
    SecurityRequirement, ResponseType
)

class PythonGenerator:
    """Generates Python SDK code from language-agnostic OpenAPI metadata."""
    
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
        self.template_env = Environment(loader=FileSystemLoader(self.template_dir))

    def convert_schema_to_python_type(self, schema: SchemaType) -> str:
        """Convert a SchemaType to a Python type annotation."""
        if schema.kind == "primitive":
            type_map = {
                "string": "str",
                "integer": "int",
                "boolean": "bool",
                "number": "float",
                "array": "List",
                "object": "Dict[str, Any]",
                "void": "None",
            }
            return type_map.get(schema.name.lower(), schema.name)
        
        elif schema.kind == "array":
            if schema.items:
                item_type = self.convert_schema_to_python_type(schema.items)
                return f"List[{item_type}]"
            return "List[Any]"
        
        elif schema.kind == "object":
            if schema.original_ref:
                # Use the model name from the reference
                return schema.original_ref.split("/")[-1]
            elif schema.properties:
                props = [f"'{k}': {self.convert_schema_to_python_type(v)}" 
                        for k, v in schema.properties.items()]
                return f"Dict[str, Union[{', '.join(props)}]]"
            return "Dict[str, Any]"
        
        elif schema.kind in ("union", "intersection"):
            if not schema.types:
                return "Any"
            type_strs = [self.convert_schema_to_python_type(t) for t in schema.types]
            if schema.kind == "union":
                return f"Union[{', '.join(type_strs)}]"
            else:
                # Python doesn't have a direct way to represent intersections
                # We'll use the first type as a base
                return type_strs[0]
        
        elif schema.kind == "reference":
            return schema.name
        
        return "Any"

    def generate_method_signature(self, endpoint: Endpoint) -> Dict[str, Any]:
        """Generate a Python method signature for an endpoint."""
        params: List[str] = []
        
        # Add required parameters first
        required_params = [p for p in endpoint.parameters if p.required]
        for param in required_params:
            type_str = self.convert_schema_to_python_type(param.schema)
            params.append(f"{param.name}: {type_str}")
        
        # Add request body if required
        if endpoint.request_body and endpoint.request_body.required:
            type_str = self.convert_schema_to_python_type(endpoint.request_body)
            params.append(f"request_body: {type_str}")
        
        # Add optional parameters
        optional_params = [p for p in endpoint.parameters if not p.required]
        for param in optional_params:
            type_str = self.convert_schema_to_python_type(param.schema)
            params.append(f"{param.name}: Optional[{type_str}] = None")
        
        # Add optional request body
        if endpoint.request_body and not endpoint.request_body.required:
            type_str = self.convert_schema_to_python_type(endpoint.request_body)
            params.append(f"request_body: Optional[{type_str}] = None")
        
        # Determine return type
        return_type = "Any"
        if endpoint.responses:
            success_responses = {k: v for k, v in endpoint.responses.items() 
                              if k.startswith("2")}
            if success_responses:
                response = next(iter(success_responses.values()))
                return_type = self.convert_schema_to_python_type(response.schema)
        
        return {
            "params": params,
            "return_type": return_type
        }

    def generate_auth_methods(self, security: List[SecurityRequirement]) -> Dict[str, str]:
        """Generate authentication-related methods."""
        auth_methods = {}
        
        for sec in security:
            if sec.type == "apiKey":
                auth_methods["api_key"] = """
                def set_api_key(self, api_key: str) -> None:
                    \"\"\"Set the API key for authentication.\"\"\"
                    self.client.headers["Authorization"] = f"Bearer {api_key}"
                """
            
            elif sec.type == "http":
                if sec.scheme == "bearer":
                    auth_methods["bearer"] = """
                    def set_bearer_token(self, token: str) -> None:
                        \"\"\"Set the bearer token for authentication.\"\"\"
                        self.client.headers["Authorization"] = f"Bearer {token}"
                    """
                elif sec.scheme == "basic":
                    auth_methods["basic"] = """
                    def set_basic_auth(self, username: str, password: str) -> None:
                        \"\"\"Set basic authentication credentials.\"\"\"
                        import base64
                        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                        self.client.headers["Authorization"] = f"Basic {credentials}"
                    """
            
            elif sec.type == "oauth2":
                auth_methods["oauth2"] = """
                def set_oauth_token(self, token: str) -> None:
                    \"\"\"Set the OAuth2 token for authentication.\"\"\"
                    self.client.headers["Authorization"] = f"Bearer {token}"
                """
        
        return auth_methods

    def _clean_name(self, name: str) -> str:
        """Clean a name to be a valid Python identifier."""
        # Remove invalid characters and convert to snake_case
        name = "".join(c if c.isalnum() else "_" for c in name)
        return name.lower()

    def _group_endpoints_by_tag(self) -> Dict[str, List[Endpoint]]:
        """Group endpoints by their tags."""
        endpoints_by_tag: Dict[str, List[Endpoint]] = {}
        for endpoint in self.metadata.endpoints:
            tag = endpoint.tag or "default"
            if tag not in endpoints_by_tag:
                endpoints_by_tag[tag] = []
            endpoints_by_tag[tag].append(endpoint)
        return endpoints_by_tag

    def get_template_context(self, tag: str, endpoints: List[Endpoint]) -> Dict[str, Any]:
        """Generate the context for template rendering."""
        return {
            "class_name": self._clean_name(tag) + "Client",
            "base_class_name": self._clean_name(self.metadata.info.title) + "Client",
            "description": self.metadata.info.description,
            "endpoints": [
                {
                    "method_name": self._clean_name(ep.operation_id),
                    "signature": self.generate_method_signature(ep),
                    "http_method": ep.method,
                    "path": ep.path,
                    "docstring": ep.description or ep.summary,
                    "request_args": self._generate_request_args(ep)
                }
                for ep in endpoints
            ],
            "auth_methods": self.generate_auth_methods(self.metadata.security_schemes)
        }

    def _generate_request_args(self, endpoint: Endpoint) -> Dict[str, Any]:
        """Generate the arguments for the _request method call."""
        args = {
            "params": {},
            "headers": {},
            "json_data": None
        }
        
        # Add query and header parameters
        for param in endpoint.parameters:
            if param.location == "query":
                args["params"][param.original_name] = param.name
            elif param.location == "header":
                args["headers"][param.original_name] = param.name
        
        # Add request body
        if endpoint.request_body:
            args["json_data"] = "request_body"
        
        return args

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with the given context."""
        template = self.template_env.get_template(template_name)
        return template.render(context)

    def generate_client_code(self, tag: str, endpoints: List[Endpoint]) -> str:
        """Generate the client code for the given tag and endpoints."""
        context = self.get_template_context(tag, endpoints)
        return self.render_template("client.py.jinja", context)
