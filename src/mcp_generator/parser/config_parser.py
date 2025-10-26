"""Configuration file parser."""

import json
from pathlib import Path
from typing import Union

import yaml
from pydantic import ValidationError

from ..models import MCPConfig


class ConfigParser:
    """Parses MCP configuration files."""

    @staticmethod
    def parse_file(file_path: Union[str, Path]) -> MCPConfig:
        """
        Parse configuration from a YAML or JSON file.

        Args:
            file_path: Path to configuration file

        Returns:
            Parsed MCP configuration

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
            ValidationError: If configuration is invalid
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        # Read file content
        content = file_path.read_text(encoding="utf-8")

        # Parse based on file extension
        suffix = file_path.suffix.lower()

        try:
            if suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(content)
            elif suffix == ".json":
                data = json.loads(content)
            else:
                raise ValueError(
                    f"Unsupported file format: {suffix}. "
                    f"Supported formats: .yaml, .yml, .json"
                )
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to parse file: {e}") from e

        # Validate and create model
        try:
            return MCPConfig(**data)
        except ValidationError as e:
            # Re-raise the original ValidationError so upstream handlers (CLI) can
            # correctly display detailed validation information.
            raise e

    @staticmethod
    def parse_dict(data: dict) -> MCPConfig:
        """
        Parse configuration from a dictionary.

        Args:
            data: Configuration data

        Returns:
            Parsed MCP configuration

        Raises:
            ValidationError: If configuration is invalid
        """
        return MCPConfig(**data)
