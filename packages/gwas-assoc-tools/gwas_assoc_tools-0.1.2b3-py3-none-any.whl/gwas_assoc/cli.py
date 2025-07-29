import logging
import sys
from pathlib import Path

import click
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from gwas_assoc.commands.validate import SnpValidator
from gwas_assoc.utils.console import console, print_error

# Configure logging with Rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


@click.group()
def cli() -> None:
    """GWAS Association Tools - utilities for GWAS data validation."""
    console.print(
        Panel(
            "GWAS Association Tools",
            subtitle="Utilities for GWAS data validation",
            border_style="blue",
        )
    )


@cli.command()
@click.argument("_file", type=click.Path(exists=True))
def validate(_file: str) -> None:
    """Validate SNPs in an Excel file."""
    file_path = Path(_file)

    console.print(f"Starting validation of [bold]{file_path}[/]")

    # Use progress spinner during validation
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("SNP validation complete.", total=None)

        try:
            validator = SnpValidator()
            result = validator.validate_snps(file_path)
            progress.update(task, completed=True)
        except Exception as e:
            progress.update(
                task, completed=True, description="[error]Validation error![/]"
            )
            print_error(f"Validation failed: {str(e)}", exception=e)
            sys.exit(1)

    if result:
        console.print("[success]✓ Validation completed successfully[/]")
    else:
        console.print("[error]✗ Validation failed[/]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
