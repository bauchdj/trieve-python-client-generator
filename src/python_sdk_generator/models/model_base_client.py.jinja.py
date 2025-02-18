from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field
from ...openapi_parser.models import (HttpHeader)

class BaseClientPyJinja(BaseModel):
    """Represents the data the base_client.py.jinja template needs"""
    class_name: str
    class_docstring: str
    base_url: str
    http_headers: List[HttpHeader]

