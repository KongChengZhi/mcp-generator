"""Code generator for MCP servers."""

import logging
from pathlib import Path
from typing import Optional

from jinja2 import Environment, PackageLoader, select_autoescape

from ..models import MCPConfig

logger = logging.getLogger(__name__)


class CodeGenerator:
    """Generates MCP server code from configuration."""

    def __init__(self):
        """Initialize code generator."""
        # Set up Jinja2 environment
        self.env = Environment(
            loader=PackageLoader("mcp_generator", "templates"),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self, config: MCPConfig, output_dir: Path) -> None:
        """
        Generate MCP server code.

        Args:
            config: MCP configuration
            output_dir: Output directory for generated code

        Raises:
            OSError: If directory creation or file writing fails
        """
        # Create output directory
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Generating MCP server code in {output_dir}")

        # Generate server.py
        self._generate_file(
            template_name="server.py.j2",
            output_path=output_dir / "server.py",
            context={"config": config},
        )

        # Generate requirements.txt
        self._generate_file(
            template_name="requirements.txt.j2",
            output_path=output_dir / "requirements.txt",
            context={"config": config},
        )

        # Generate README.md
        self._generate_file(
            template_name="README.md.j2",
            output_path=output_dir / "README.md",
            context={"config": config},
        )

        # Generate .gitignore
        self._generate_file(
            template_name=".gitignore.j2",
            output_path=output_dir / ".gitignore",
            context={"config": config},
        )

        logger.info("Code generation completed successfully")
        logger.info(f"Generated files:")
        logger.info(f"  - {output_dir / 'server.py'}")
        logger.info(f"  - {output_dir / 'requirements.txt'}")
        logger.info(f"  - {output_dir / 'README.md'}")
        logger.info(f"  - {output_dir / '.gitignore'}")

    def _generate_file(
        self, template_name: str, output_path: Path, context: dict
    ) -> None:
        """
        Generate a single file from template.

        Args:
            template_name: Name of the template file
            output_path: Output file path
            context: Template context variables
        """
        template = self.env.get_template(template_name)
        content = template.render(**context)

        output_path.write_text(content, encoding="utf-8")
        logger.debug(f"Generated {output_path}")

    def preview(self, config: MCPConfig, template_name: str = "server.py.j2") -> str:
        """
        Preview generated code without writing to disk.

        Args:
            config: MCP configuration
            template_name: Template to preview

        Returns:
            Generated code content
        """
        template = self.env.get_template(template_name)
        return template.render(config=config)
