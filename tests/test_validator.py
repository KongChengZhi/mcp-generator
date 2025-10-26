"""Tests for configuration validator."""

from mcp_generator.models import (
    HttpMethod,
    MCPConfig,
    Parameter,
    ParameterLocation,
    ParameterType,
    ServerConfig,
    Tool,
)
from mcp_generator.validator import ConfigValidator


def test_valid_config():
    """Test validation of valid configuration."""
    config = MCPConfig(
        server=ServerConfig(
            name="test-api",
            version="1.0.0",
            base_url="https://api.example.com",
        ),
        tools=[
            Tool(
                name="get_user",
                description="Get user",
                endpoint="/users/{user_id}",
                method=HttpMethod.GET,
                parameters=[
                    Parameter(
                        name="user_id",
                        type=ParameterType.STRING,
                        location=ParameterLocation.PATH,
                        required=True,
                    )
                ],
            )
        ],
    )

    errors = ConfigValidator.validate(config)
    assert len(errors) == 0


def test_duplicate_tool_names():
    """Test validation fails with duplicate tool names."""
    config = MCPConfig(
        server=ServerConfig(
            name="test-api",
            base_url="https://api.example.com",
        ),
        tools=[
            Tool(
                name="get_user",
                description="Get user",
                endpoint="/users/{id}",
                method=HttpMethod.GET,
            ),
            Tool(
                name="get_user",
                description="Get user again",
                endpoint="/users/{id}",
                method=HttpMethod.GET,
            ),
        ],
    )

    errors = ConfigValidator.validate(config)
    assert any("Duplicate tool name" in error for error in errors)


def test_invalid_tool_name():
    """Test validation fails with invalid tool name."""
    config = MCPConfig(
        server=ServerConfig(
            name="test-api",
            base_url="https://api.example.com",
        ),
        tools=[
            Tool(
                name="get-user",  # Invalid: contains hyphen
                description="Get user",
                endpoint="/users/{id}",
                method=HttpMethod.GET,
            )
        ],
    )

    errors = ConfigValidator.validate(config)
    assert any("not a valid Python identifier" in error for error in errors)


def test_path_parameter_not_in_endpoint():
    """Test validation fails when path parameter is not in endpoint."""
    config = MCPConfig(
        server=ServerConfig(
            name="test-api",
            base_url="https://api.example.com",
        ),
        tools=[
            Tool(
                name="get_user",
                description="Get user",
                endpoint="/users/123",  # No placeholder
                method=HttpMethod.GET,
                parameters=[
                    Parameter(
                        name="user_id",
                        type=ParameterType.STRING,
                        location=ParameterLocation.PATH,
                        required=True,
                    )
                ],
            )
        ],
    )

    errors = ConfigValidator.validate(config)
    assert any("marked as path but not in endpoint" in error for error in errors)
