"""Data models for MCP server configuration."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class HttpMethod(str, Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ParameterLocation(str, Enum):
    """Parameter location in HTTP request."""

    PATH = "path"
    QUERY = "query"
    HEADER = "header"
    BODY = "body"


class ParameterType(str, Enum):
    """Parameter data types."""

    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


class Parameter(BaseModel):
    """API parameter definition."""

    name: str = Field(..., description="Parameter name")
    type: ParameterType = Field(..., description="Parameter data type")
    location: ParameterLocation = Field(
        default=ParameterLocation.QUERY, description="Parameter location"
    )
    description: Optional[str] = Field(None, description="Parameter description")
    required: bool = Field(default=False, description="Whether parameter is required")
    default: Optional[Any] = Field(None, description="Default value")
    items_type: Optional[ParameterType] = Field(
        None, description="Array item type (for array parameters)"
    )
    properties: Optional[Dict[str, "Parameter"]] = Field(
        None, description="Object properties (for object parameters)"
    )


class Authentication(BaseModel):
    """Authentication configuration."""

    type: str = Field(..., description="Authentication type (bearer, apikey, basic)")
    location: Optional[ParameterLocation] = Field(
        None, description="Location for API key (header or query)"
    )
    name: Optional[str] = Field(None, description="Name of the auth header/query parameter")
    description: Optional[str] = Field(None, description="Authentication description")


class Tool(BaseModel):
    """MCP tool definition mapping to an API endpoint."""

    name: str = Field(..., description="Tool name (must be valid Python identifier)")
    description: str = Field(..., description="Tool description for AI agents")
    endpoint: str = Field(..., description="API endpoint path (can include {param} placeholders)")
    method: HttpMethod = Field(..., description="HTTP method")
    parameters: List[Parameter] = Field(default_factory=list, description="Tool parameters")
    response_description: Optional[str] = Field(None, description="Response description")
    stream: bool = Field(default=False, description="Whether this endpoint supports streaming")


class ServerConfig(BaseModel):
    """Server-level configuration."""

    name: str = Field(..., description="MCP server name")
    version: str = Field(default="1.0.0", description="Server version")
    description: Optional[str] = Field(None, description="Server description")
    base_url: HttpUrl = Field(..., description="Base URL of the target API")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    authentication: Optional[Authentication] = Field(None, description="Authentication config")


class MCPConfig(BaseModel):
    """Complete MCP server configuration."""

    server: ServerConfig = Field(..., description="Server configuration")
    tools: List[Tool] = Field(..., description="List of tools/endpoints")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "server": {
                    "name": "example-api",
                    "version": "1.0.0",
                    "description": "Example API MCP Server",
                    "base_url": "https://api.example.com",
                    "timeout": 30,
                    "authentication": {
                        "type": "bearer",
                        "description": "Bearer token authentication"
                    }
                },
                "tools": [
                    {
                        "name": "get_user",
                        "description": "Get user information by ID",
                        "endpoint": "/users/{user_id}",
                        "method": "GET",
                        "parameters": [
                            {
                                "name": "user_id",
                                "type": "string",
                                "location": "path",
                                "description": "User ID",
                                "required": True
                            }
                        ]
                    }
                ]
            }
        }
