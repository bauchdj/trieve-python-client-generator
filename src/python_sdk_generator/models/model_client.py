from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field
from ...openapi_parser.models import ( HttpParameter, SchemaMetadata)

class MethodParameter(BaseModel):
    """Represents the data necessary to write method params, param types, and param docstrings"""
    name: str
    original_name: Optional[str] = None
    type: str
    docstring: str

class MethodMetadata(BaseModel):
    """Represent the data necessary to generate method"""
    method_name: str
    required_method_params: List[MethodParameter]
    optional_method_params: List[MethodParameter]
    path: str
    request_body: Optional[SchemaMetadata] = None

class ClientPyJinja(BaseModel):
    """Represents the data the client.py.jinja template needs"""
    parent_class_formatted_import_path: str
    parent_class_formatted_name: str
    class_name: str
    class_docstring: str
    methods: List[MethodMetadata] = Field(default_factory=[])

