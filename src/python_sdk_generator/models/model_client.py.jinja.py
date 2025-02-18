from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field
from ...openapi_parser.models import ( HttpParameter, SchemaMetadata)

class MethodParameter(BaseModel):
    """Represents the data necessary to write method params, param types, and param docstrings"""
    name: str
    type: str
    docstring: str

class MethodMetadata(BaseModel):
    """Represent the data necessary to generate method"""
    name: str
    params: List[MethodParameter]
    path: str
    http_param: List[HttpParameter]
    request_body: SchemaMetadata

class ClientPyJinja(BaseModel):
    """Represents the data the client.py.jinja template needs"""
    class_name: str
    class_docstring: str
    methods: List[MethodMetadata] = Field(default_factory=[])

