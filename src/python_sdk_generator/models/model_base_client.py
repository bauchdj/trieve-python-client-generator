from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field
from ...openapi_parser.models import HttpHeader

# class OpenAPITagMetadata(BaseModel):
#     """Represents the data necessary to import and append classes as properties"""
#     tag_folder: str
#     tag_filename: str
#     tag_class_name: str
#     tag_prop_name: str


class BaseClientPyJinja(BaseModel):
    """Represents the data the base_client.py.jinja template needs"""

    class_name: str
    class_docstring: str
    base_url: str
    http_headers: List[HttpHeader]
    # tags: List[OpenAPITagMetadata]
