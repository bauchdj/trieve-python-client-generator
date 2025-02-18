from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field, RootModel

class HttpParameter(BaseModel):
    """Represents an OpenAPI parameter"""
    name: str
    in_location: str = Field(..., alias="in")
    required: bool = False
    type: str
    description: str = ""
    original_name: str = ""  # Store the original parameter name before cleaning

class HttpHeader(HttpParameter):
    """Represents an OpenAPI header parameter"""
    in_location: Literal["header"] = "header"

class SchemaMetadata(BaseModel):
    """Represents an OpenAPI request body"""
    required: Optional[bool] = None
    nullable: Optional[bool] = None
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
    parameters: List[HttpParameter] = Field(default_factory=list)
    request_body: Union[SchemaMetadata, bool] = Field(default_factory=False)

class Info(BaseModel):
    """Represents the 'info' object in OpenAPI metadata"""
    title: str
    version: str
    description: Optional[str] = ""
    termsOfService: Optional[str] = None
    contact: Optional[Dict[str, Any]] = None
    license: Optional[Dict[str, Any]] = None

class Server(BaseModel):
    """Represents a server in OpenAPI metadata"""
    url: str
    description: Optional[str] = ""
    variables: Optional[Dict[str, Dict[str, Any]]] = None

class OpenAPIMetadata(BaseModel):
    """Represents the parsed OpenAPI metadata"""
    openapi: str
    info: Info
    servers: List[Server]
    operations: List[Operation]
    headers: List[HttpParameter]
    source_file: str = ""  # Path to the source OpenAPI file