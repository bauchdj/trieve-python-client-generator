import json
import os
import subprocess
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import black
import re

class PythonSDKGenerator:
    def __init__(self, openapi_path: str, output_dir: Optional[str] = None):
        '''Initialize the SDK Generator with the path to the OpenAPI specification.
        
        Args:
            openapi_path: Path to the OpenAPI JSON specification file
            output_dir: Optional directory where the SDK will be generated. If not provided,
                       a 'generated_sdk' directory will be created in the current directory.
        '''
        self.openapi_path = openapi_path
        with open(openapi_path, 'r') as f:
            self.spec = json.load(f)
        
        self.project_name = self.spec['info']['title'].replace(' ', '')
        self.base_url = self.spec['servers'][0]['url']
        
        # Set up output directory
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'generated_sdk')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_models(self) -> None:
        '''Generate Pydantic models using datamodel-codegen.'''
        output_file = os.path.join(self.output_dir, 'models.py')
        cmd = [
            "datamodel-codegen",
            "--input-file-type", "openapi",
            "--input", self.openapi_path,
            "--output", output_file,
            "--target-python-version", "3.9",
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

    def _format_param_name(self, name: str) -> str:
        '''Format parameter name to be Python-friendly.
        
        Args:
            name: Original parameter name
            
        Returns:
            Formatted parameter name
        '''
        # Replace special characters and convert to snake_case
        name = name.replace('-', '_')
        if name.startswith('TR_'):
            return name
        if name.startswith('X_'):
            return name
        return name.lower()

    def _get_array_type(self, items: Dict[str, Any]) -> str:
        '''Get the type for an array property.
        
        Args:
            items: Schema for array items
            
        Returns:
            Python type annotation for the array
        '''
        if '$ref' in items:
            item_type = items['$ref'].split('/')[-1]
        elif items.get('type') == 'array':
            item_type = self._get_array_type(items.get('items', {}))
        else:
            type_mapping = {
                'string': 'str',
                'integer': 'int',
                'number': 'float',
                'boolean': 'bool',
                'object': 'Dict[str, Any]'
            }
            item_type = type_mapping.get(items.get('type', 'string'), 'Any')
            
        return f"List[{item_type}]"

    def _is_primitive_type(self, type_info: Dict[str, Any]) -> bool:
        '''Check if a type is a primitive type or has oneOf/anyOf with primitive types.
        
        Args:
            type_info: Type information from OpenAPI spec
            
        Returns:
            True if the type is primitive or has primitive subtypes
        '''
        # Direct primitive types
        if type_info.get('type') in ['string', 'number', 'integer', 'boolean']:
            return True
            
        # Check if it's an object with only string properties
        if type_info.get('type') == 'object' and type_info.get('properties'):
            return all(prop.get('type') == 'string' for prop in type_info['properties'].values())
            
        # Check if it has oneOf/anyOf with primitive types or string-only objects
        if type_info.get('oneOf') or type_info.get('anyOf'):
            subtypes = type_info.get('oneOf') or type_info.get('anyOf')
            return any(
                subtype.get('type') in ['string', 'number', 'integer', 'boolean'] or
                (subtype.get('type') == 'object' and subtype.get('properties') and
                 all(prop.get('type') == 'string' for prop in subtype['properties'].values()))
                for subtype in subtypes
            )
            
        return False

    def _collect_primitive_types(self, schema: Dict[str, Any]) -> Set[str]:
        """Recursively collect all primitive types from a schema."""
        primitive_types = set()
        
        # Direct primitive type
        if schema.get('type') in ['string', 'integer', 'number', 'boolean']:
            primitive_types.add(self._map_type(schema['type']))
            return primitive_types
            
        # Handle oneOf and anyOf
        for subtype in schema.get('oneOf', []) + schema.get('anyOf', []):
            if '$ref' in subtype:
                ref = subtype['$ref'].split('/')[-1]
                ref_schema = self.spec['components']['schemas'][ref]
                primitive_types.update(self._collect_primitive_types(ref_schema))
            else:
                primitive_types.update(self._collect_primitive_types(subtype))
                
        return primitive_types

    def _map_type(self, openapi_type: str) -> str:
        """Map OpenAPI types to Python types."""
        type_map = {
            'string': 'str',
            'integer': 'int',
            'number': 'float',
            'boolean': 'bool'
        }
        return type_map.get(openapi_type, openapi_type)

    def _resolve_root_model_types(self, schema: Dict[str, Any], schema_name: str) -> str:
        # Handle arrays
        if schema.get('type') == 'array':
            items = schema['items']
            if '$ref' in items:
                item_type = items['$ref'].split('/')[-1]
            else:
                item_type = 'Any'
            return f'list[{item_type}]'
            
        # Handle oneOf and anyOf
        if schema.get('oneOf') or schema.get('anyOf'):
            union_types = schema.get('oneOf', []) + schema.get('anyOf', [])
            resolved_types = [schema_name]  # Always include the schema name
            
            # Resolve reference types
            for type_info in union_types:
                if '$ref' in type_info:
                    ref_type = type_info['$ref'].split('/')[-1]
                    resolved_types.append(ref_type)
                elif type_info.get('type') == 'array':
                    items = type_info['items']
                    if '$ref' in items:
                        item_type = items['$ref'].split('/')[-1]
                    else:
                        item_type = 'Any'
                    resolved_types.append(f'list[{item_type}]')
                    
            # Add all primitive types found in the schema and its subtypes
            primitive_types = self._collect_primitive_types(schema)
            resolved_types.extend(primitive_types)
                    
            # Remove duplicates while preserving order
            resolved_types = list(dict.fromkeys(resolved_types))
                    
            return f"Union[{', '.join(resolved_types)}]"
                
        return schema_name

    def _get_model_params(self, schema_ref: str) -> List[Tuple[str, str, bool]]:
        '''Extract parameters from a model reference, preserving model types.
        
        Args:
            schema_ref: Reference to a schema in the OpenAPI spec
            
        Returns:
            List of tuples containing (param_name, param_type, required)
        '''
        schema_name = schema_ref.split('/')[-1]
        try:
            schema = self.spec['components']['schemas'][schema_name]
        except KeyError:
            return [(self._format_param_name(schema_name), schema_name, True)]
            
        params = []
        required_fields = schema.get('required', [])
        
        # Handle enum types
        if schema.get('type') == 'string' and schema.get('enum'):
            return [(self._format_param_name(schema_name), schema_name, True)]
            
        for prop_name, prop_data in schema.get('properties', {}).items():
            is_required = prop_name in required_fields
            formatted_name = self._format_param_name(prop_name)
            
            if '$ref' in prop_data:
                # This is a reference to another model
                ref_type = prop_data['$ref'].split('/')[-1]
                resolved_type = self._resolve_root_model_types(self.spec['components']['schemas'][ref_type], ref_type)
                params.append((formatted_name, resolved_type, is_required))
            elif 'allOf' in prop_data:
                # Handle allOf by taking the first reference
                if prop_data['allOf'] and '$ref' in prop_data['allOf'][0]:
                    ref_type = prop_data['allOf'][0]['$ref'].split('/')[-1]
                    resolved_type = self._resolve_root_model_types(self.spec['components']['schemas'][ref_type], ref_type)
                    params.append((formatted_name, resolved_type, is_required))
                else:
                    params.append((formatted_name, 'Dict[str, Any]', is_required))
            else:
                # Handle primitive types and arrays
                if prop_data.get('type') == 'array':
                    items_type = prop_data.get('items', {})
                    if '$ref' in items_type:
                        ref_type = items_type['$ref'].split('/')[-1]
                        resolved_type = self._resolve_root_model_types(self.spec['components']['schemas'][ref_type], ref_type)
                        param_type = f'List[{resolved_type}]'
                    else:
                        param_type = self._get_array_type(items_type)
                else:
                    type_mapping = {
                        'string': 'str',
                        'integer': 'int',
                        'number': 'float',
                        'boolean': 'bool',
                        'object': 'Dict[str, Any]'
                    }
                    param_type = type_mapping.get(prop_data.get('type', 'string'), 'Any')
                
                if prop_data.get('nullable', False) or not is_required:
                    param_type = f"Optional[{param_type}]"
                params.append((formatted_name, param_type, is_required))
        
        return sorted(params, key=lambda x: (not x[2], x[0]))

    def generate_sdk(self) -> str:
        '''Generate the HTTP SDK class code.
        
        Returns:
            String containing the generated SDK class code
        '''
        sdk_code = [
            "from typing import Any, Dict, List, Optional, Union, TypeVar, Generic",
            "import requests",
            "from models import *  # Generated models",
            "",
            "ResponseT = TypeVar('ResponseT')",
            "",
            "class HttpSDK:",
            "    '''Base class for HTTP SDK implementations.'''",
            "    def __init__(self, api_key: str, base_url: str):",
            "        self.api_key = api_key",
            "        self.base_url = base_url.rstrip('/')",
            "        self.session = requests.Session()",
            "        self.session.headers.update({",
            "            'Authorization': f'Bearer {api_key}',",
            "            'Content-Type': 'application/json'",
            "        })",
            "",
            "    def _build_url(self, path: str) -> str:",
            "        '''Build the full URL for an API endpoint.'''",
            "        return f'{self.base_url}{path}'",
            "",
            "    def _prepare_headers(self, header_params: Dict[str, str], locals_dict: Dict[str, Any]) -> Dict[str, str]:",
            "        '''Prepare headers from parameters.'''",
            "        headers = {}",
            "        for header_name, param_name in header_params.items():",
            "            if locals_dict.get(param_name) is not None:",
            "                headers[header_name] = str(locals_dict[param_name])",
            "        return headers",
            "",
            "    def _prepare_payload(self, payload_class: Any, locals_dict: Dict[str, Any]) -> str:",
            "        '''Prepare request payload from parameters.'''",
            "        payload_data = {",
            "            param_name: value",
            "            for param_name, value in locals_dict.items()",
            "            if value is not None",
            "            and param_name not in ['self', 'headers', 'url']",
            "            and not param_name.upper().startswith(('TR_', 'X_'))",
            "        }",
            "        payload = payload_class(**payload_data)",
            "        return payload.model_dump_json()",
            "",
            "    def _handle_response(self, response: requests.Response, response_model: Any = None) -> Any:",
            "        '''Handle the API response and raise appropriate exceptions.'''",
            "        try:",
            "            response.raise_for_status()",
            "            data = response.json()",
            "            if response_model:",
            "                return response_model.model_validate(data)",
            "            return data",
            "        except requests.exceptions.HTTPError as e:",
            "            error_msg = str(e)",
            "            try:",
            "                error_data = response.json()",
            "                if isinstance(error_data, dict) and 'message' in error_data:",
            "                    error_msg = error_data['message']",
            "            except:",
            "                pass",
            "            raise Exception(f'HTTP {response.status_code}: {error_msg}')",
            "",
            "    def _request(",
            "        self,",
            "        method: str,",
            "        path: str,",
            "        header_params: Dict[str, str],",
            "        payload_class: Any,",
            "        response_model: Any,",
            "        locals_dict: Dict[str, Any],",
            "    ) -> Any:",
            "        '''Make an HTTP request with proper error handling.'''",
            "        url = self._build_url(path)",
            "        headers = self._prepare_headers(header_params, locals_dict)",
            "        json_data = self._prepare_payload(payload_class, locals_dict)",
            "        response = self.session.request(method, url, data=json_data, headers=headers)",
            "        return self._handle_response(response, response_model)",
            "",
            f"class {self.project_name}SDK(HttpSDK):",
            f"    def __init__(self, api_key: str, base_url: str = \"{self.base_url}\"):",
            "        super().__init__(api_key, base_url)",
            ""
        ]

        # Generate methods for each endpoint
        for path, methods in self.spec['paths'].items():
            for method, operation in methods.items():
                method_name = operation['operationId']
                params: List[Tuple[str, str, bool]] = []
                
                # Get response type
                response_model = None
                if '200' in operation.get('responses', {}):
                    response_content = operation['responses']['200'].get('content', {})
                    if 'application/json' in response_content:
                        schema = response_content['application/json'].get('schema', {})
                        if '$ref' in schema:
                            response_model = schema['$ref'].split('/')[-1]
                
                # Get request body model
                request_model = None
                if 'requestBody' in operation:
                    content = operation['requestBody']['content']
                    if 'application/json' in content:
                        schema = content['application/json']['schema']
                        if '$ref' in schema:
                            request_model = schema['$ref'].split('/')[-1]
                
                # Get path parameters
                for param in operation.get('parameters', []):
                    param_type = 'str'  # Default to string
                    param_name = self._format_param_name(param['name'])
                    if 'schema' in param:
                        if '$ref' in param['schema']:
                            param_type = param['schema']['$ref'].split('/')[-1]
                        else:
                            type_mapping = {
                                'string': 'str',
                                'integer': 'int',
                                'number': 'float',
                                'boolean': 'bool'
                            }
                            param_type = type_mapping.get(param['schema'].get('type', 'string'), 'str')
                            if param['schema'].get('nullable', False):
                                param_type = f"Optional[{param_type}]"
                    params.append((param_name, param_type, param['required']))

                # Get request body parameters if present
                if request_model:
                    # Add the request model as a parameter
                    params.extend(self._get_model_params(f'#/components/schemas/{request_model}'))

                # Sort parameters - required first, then optional
                params.sort(key=lambda x: (not x[2], x[0]))
                
                # Generate method signature with proper return type
                return_type = f"{response_model}" if response_model else "Dict[str, Any]"
                
                # Generate method
                sdk_code.extend([
                    f"    def {method_name}(",
                    "        self,"
                ])
                
                # Add parameters on separate lines
                for name, type_, required in params:
                    if required:
                        sdk_code.append(f"        {name}: {type_},")
                    else:
                        # Avoid double Optional
                        if type_.startswith('Optional['):
                            sdk_code.append(f"        {name}: {type_} = None,")
                        else:
                            sdk_code.append(f"        {name}: Optional[{type_}] = None,")
                
                # Create docstring
                docstring = [
                    f"    ) -> {return_type}:",
                    f"        '''",
                    f"        {operation.get('summary', '')}",
                    f"",
                    f"        {operation.get('description', '')}",
                    f"        '''",
                ]
                
                # Create header params mapping
                header_params = ", ".join([f"'{p[0].replace('_', '-')}': '{p[0]}'" for p in params if p[0].upper().startswith(('TR_', 'X_'))])
                
                # Add method implementation
                implementation = [
                    "        return self._request(",
                    f"            method='{method}',",
                    f"            path='{path}',",
                    f"            header_params={{{header_params}}},",
                    f"            payload_class={request_model or 'Dict[str, Any]'},",
                    f"            response_model={response_model or 'None'},",
                    "            locals_dict=locals(),",
                    "        )",
                ]
                
                sdk_code.extend(docstring + implementation)
                


        # Format the code using black
        sdk_code = "\n".join(sdk_code)
        try:
            sdk_code = black.format_str(sdk_code, mode=black.FileMode())
        except:
            pass  # If black formatting fails, use unformatted code
            
        return sdk_code

    def generate_files(self) -> None:
        '''Generate all necessary files for the SDK.'''
        # Generate models
        self.generate_models()
        
        # Generate SDK
        sdk_code = self.generate_sdk()
        
        # Write SDK to file
        sdk_filename = os.path.join(self.output_dir, f"{self.project_name.lower()}_sdk.py")
        with open(sdk_filename, 'w') as f:
            f.write(sdk_code)
        
        # Generate requirements.txt
        requirements = [
            "requests>=2.31.0",
            "pydantic>=2.0.0",
            "typing-extensions>=4.7.0"
        ]
        requirements_file = os.path.join(self.output_dir, 'requirements.txt')
        with open(requirements_file, 'w') as f:
            f.write('\n'.join(requirements))
        
        # Generate README.md
        readme_template = '''# {name} SDK

This SDK provides a Python interface to the {name} API.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from {name_lower}_sdk import {name}SDK

# Initialize the SDK
sdk = {name}SDK(api_key="your_api_key")

# Example usage (replace with actual method names and parameters)
response = sdk.some_method(param1="value1", param2="value2")
```

## Documentation

For detailed API documentation, please refer to the OpenAPI specification.
'''
        readme = readme_template.format(
            name=self.project_name,
            name_lower=self.project_name.lower()
        )
        readme_file = os.path.join(self.output_dir, 'README.md')
        with open(readme_file, 'w') as f:
            f.write(readme)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Python SDK from OpenAPI specification')
    parser.add_argument('--spec', type=str, default='openapi.json',
                        help='Path to OpenAPI specification file (default: openapi.json)')
    parser.add_argument('--output-dir', type=str,
                        help='Directory where the SDK will be generated (default: ./generated_sdk)')
    
    args = parser.parse_args()
    
    generator = PythonSDKGenerator(args.spec, args.output_dir)
    generator.generate_files()
    print(f"SDK generated successfully in: {generator.output_dir}")