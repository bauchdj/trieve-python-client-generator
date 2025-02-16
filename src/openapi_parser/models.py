from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

class Parameter(BaseModel):
    """Represents an OpenAPI parameter"""
    name: str
    in_location: str = Field(..., alias="in")
    required: bool = False
    type: str
    description: str = ""

class RequestBody(BaseModel):
    """Represents an OpenAPI request body"""
    required: Optional[bool] = None
    type: str
    nested_json_schema_refs: List[str] = Field(default_factory=list)
    nested_json_schemas: List[Dict[str, Any]] = Field(default_factory=list)
    length_nested_json_schemas: int = 0

class Operation(BaseModel):
    """Represents an OpenAPI operation"""
    tag: str
    operationId: str
    method: str
    path: str
    summary: str = ""
    description: str = ""
    parameters: List[Parameter] = Field(default_factory=list)
    request_body: RequestBody = Field(default_factory=RequestBody)

class OpenAPIMetadata(BaseModel):
    """Represents the parsed OpenAPI metadata"""
    operations: List[Operation]
    headers: List[Parameter]