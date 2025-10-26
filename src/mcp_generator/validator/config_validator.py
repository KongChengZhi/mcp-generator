"""Configuration validator."""

import re
from typing import List

from ..models import MCPConfig, Tool


class ConfigValidator:
    """Validates MCP configuration."""

    PYTHON_IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

    @classmethod
    def validate(cls, config: MCPConfig) -> List[str]:
        """
        Validate the configuration and return a list of errors.

        Args:
            config: MCP configuration to validate

        Returns:
            List of error messages (empty if valid)
        """
        errors: List[str] = []

        # Validate server config
        if not config.server.name:
            errors.append("Server name is required")

        # Validate tools
        if not config.tools:
            errors.append("At least one tool is required")

        tool_names = set()
        for tool in config.tools:
            # Check for duplicate tool names
            if tool.name in tool_names:
                errors.append(f"Duplicate tool name: {tool.name}")
            tool_names.add(tool.name)

            # Validate tool name is a valid Python identifier
            if not cls.PYTHON_IDENTIFIER_PATTERN.match(tool.name):
                errors.append(
                    f"Tool name '{tool.name}' is not a valid Python identifier"
                )

            # Validate endpoint
            if not tool.endpoint.startswith("/"):
                errors.append(
                    f"Tool '{tool.name}': endpoint must start with '/'"
                )

            # Validate parameters
            errors.extend(cls._validate_tool_parameters(tool))

        return errors

    @classmethod
    def _validate_tool_parameters(cls, tool: Tool) -> List[str]:
        """Validate tool parameters."""
        errors: List[str] = []
        param_names = set()

        # Extract path parameters from endpoint
        path_params = re.findall(r"\{([^}]+)\}", tool.endpoint)

        for param in tool.parameters:
            # Check for duplicate parameter names
            if param.name in param_names:
                errors.append(
                    f"Tool '{tool.name}': duplicate parameter name '{param.name}'"
                )
            param_names.add(param.name)

            # Validate parameter name
            if not cls.PYTHON_IDENTIFIER_PATTERN.match(param.name):
                errors.append(
                    f"Tool '{tool.name}': parameter name '{param.name}' "
                    f"is not a valid Python identifier"
                )

            # Check array parameters have items_type
            if param.type.value == "array" and not param.items_type:
                errors.append(
                    f"Tool '{tool.name}': array parameter '{param.name}' "
                    f"must specify items_type"
                )

            # Check object parameters have properties
            if param.type.value == "object" and not param.properties:
                errors.append(
                    f"Tool '{tool.name}': object parameter '{param.name}' "
                    f"must specify properties"
                )

        # Check that all path parameters are defined
        for path_param in path_params:
            if path_param not in param_names:
                errors.append(
                    f"Tool '{tool.name}': path parameter '{path_param}' "
                    f"in endpoint is not defined in parameters"
                )

        # Check that all path location parameters are in the endpoint
        for param in tool.parameters:
            if param.location.value == "path" and param.name not in path_params:
                errors.append(
                    f"Tool '{tool.name}': parameter '{param.name}' "
                    f"is marked as path but not in endpoint"
                )

        return errors
