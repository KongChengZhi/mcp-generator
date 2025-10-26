"""Command-line interface for MCP Generator."""

import logging
import sys
from pathlib import Path

import click
from pydantic import ValidationError
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.syntax import Syntax

from ..generator import CodeGenerator
from ..parser import ConfigParser
from ..validator import ConfigValidator

# Set up console and logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="0.1.0", prog_name="mcp-generator")
def cli():
    """MCP Generator - Generate MCP server code for HTTP backends."""
    pass


@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default="./generated",
    help="Output directory for generated code",
)
@click.option(
    "--validate-only",
    is_flag=True,
    help="Only validate configuration without generating code",
)
def generate(config_file: str, output: str, validate_only: bool):
    """Generate MCP server code from configuration file."""
    try:
        console.print(f"\n[bold blue]Reading configuration from {config_file}...[/bold blue]")

        # Parse configuration
        config = ConfigParser.parse_file(config_file)
        console.print("[green]✓[/green] Configuration parsed successfully")

        # Validate configuration
        console.print("\n[bold blue]Validating configuration...[/bold blue]")
        errors = ConfigValidator.validate(config)

        if errors:
            console.print("\n[bold red]✗ Validation failed with the following errors:[/bold red]")
            for error in errors:
                console.print(f"  [red]•[/red] {error}")
            sys.exit(1)

        console.print("[green]✓[/green] Configuration validated successfully")

        # Display summary
        console.print(
            Panel(
                f"[bold]Server:[/bold] {config.server.name} v{config.server.version}\n"
                f"[bold]Target API:[/bold] {config.server.base_url}\n"
                f"[bold]Tools:[/bold] {len(config.tools)}",
                title="Configuration Summary",
                border_style="blue",
            )
        )

        if validate_only:
            console.print("\n[green]Validation completed. Skipping code generation.[/green]")
            return

        # Generate code
        console.print(f"\n[bold blue]Generating code in {output}...[/bold blue]")
        generator = CodeGenerator()
        generator.generate(config, Path(output))

        console.print(
            Panel(
                f"[green]✓ Code generated successfully![/green]\n\n"
                f"[bold]Output directory:[/bold] {Path(output).absolute()}\n\n"
                f"[bold]Next steps:[/bold]\n"
                f"1. cd {output}\n"
                f"2. pip install -r requirements.txt\n"
                f"3. python server.py",
                title="Success",
                border_style="green",
            )
        )

    except FileNotFoundError as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {e}")
        sys.exit(1)
    except ValidationError as e:
        console.print(f"\n[bold red]✗ Configuration validation error:[/bold red]")
        console.print(e)
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]✗ Unexpected error:[/bold red] {e}")
        logger.exception("Unexpected error occurred")
        sys.exit(1)


@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
def validate(config_file: str):
    """Validate configuration file without generating code."""
    ctx = click.get_current_context()
    ctx.invoke(generate, config_file=config_file, output="./generated", validate_only=True)


@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--template",
    type=click.Choice(["server", "readme", "requirements"]),
    default="server",
    help="Template to preview",
)
def preview(config_file: str, template: str):
    """Preview generated code without writing to disk."""
    try:
        console.print(f"\n[bold blue]Reading configuration from {config_file}...[/bold blue]")

        # Parse configuration
        config = ConfigParser.parse_file(config_file)

        # Map template names to file names
        template_map = {
            "server": "server.py.j2",
            "readme": "README.md.j2",
            "requirements": "requirements.txt.j2",
        }

        # Generate preview
        generator = CodeGenerator()
        content = generator.preview(config, template_map[template])

        # Display preview
        syntax = Syntax(
            content,
            "python" if template == "server" else "markdown" if template == "readme" else "text",
            theme="monokai",
            line_numbers=True,
        )

        console.print(f"\n[bold]Preview of {template}:[/bold]\n")
        console.print(syntax)

    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {e}")
        logger.exception("Error occurred during preview")
        sys.exit(1)


@cli.command()
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default="./config.yaml",
    help="Output file path",
)
def init(output: str):
    """Create a sample configuration file."""
    sample_config = """server:
  name: "example-api"
  version: "1.0.0"
  description: "Example API MCP Server"
  base_url: "https://api.example.com"
  timeout: 30
  authentication:
    type: "bearer"
    description: "Bearer token authentication"

tools:
  - name: "get_user"
    description: "Get user information by ID"
    endpoint: "/users/{user_id}"
    method: "GET"
    parameters:
      - name: "user_id"
        type: "string"
        location: "path"
        description: "User ID"
        required: true

  - name: "create_post"
    description: "Create a new post"
    endpoint: "/posts"
    method: "POST"
    parameters:
      - name: "title"
        type: "string"
        location: "body"
        description: "Post title"
        required: true
      - name: "content"
        type: "string"
        location: "body"
        description: "Post content"
        required: true
      - name: "tags"
        type: "array"
        location: "body"
        description: "Post tags"
        items_type: "string"
"""

    output_path = Path(output)
    if output_path.exists():
        if not click.confirm(f"\n{output} already exists. Overwrite?"):
            console.print("[yellow]Aborted.[/yellow]")
            return

    output_path.write_text(sample_config, encoding="utf-8")
    console.print(
        Panel(
            f"[green]✓ Sample configuration created![/green]\n\n"
            f"[bold]File:[/bold] {output_path.absolute()}\n\n"
            f"[bold]Next steps:[/bold]\n"
            f"1. Edit {output} to match your API\n"
            f"2. mcp-gen generate {output}",
            title="Success",
            border_style="green",
        )
    )


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
