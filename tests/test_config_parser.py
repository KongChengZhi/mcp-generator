"""Tests for configuration parser."""

import pytest
from pydantic import ValidationError

from mcp_generator.models import MCPConfig
from mcp_generator.parser import ConfigParser


def test_parse_dict():
    """Test parsing configuration from dictionary."""
    config_dict = {
        "server": {
            "name": "test-api",
            "version": "1.0.0",
            "base_url": "https://api.example.com",
        },
        "tools": [
            {
                "name": "get_user",
                "description": "Get user",
                "endpoint": "/users/{user_id}",
                "method": "GET",
                "parameters": [
                    {
                        "name": "user_id",
                        "type": "string",
                        "location": "path",
                        "required": True,
                    }
                ],
            }
        ],
    }

    config = ConfigParser.parse_dict(config_dict)
    assert isinstance(config, MCPConfig)
    assert config.server.name == "test-api"
    assert len(config.tools) == 1
    assert config.tools[0].name == "get_user"


def test_parse_invalid_config():
    """Test parsing invalid configuration."""
    invalid_config = {
        "server": {
            "name": "test-api",
            # Missing base_url
        },
        "tools": [],
    }

    with pytest.raises(ValidationError):
        ConfigParser.parse_dict(invalid_config)
