"""Console utilities for rich terminal output."""

from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich.table import Table
from rich.theme import Theme

# Set up Rich theme for consistent styling across the application
THEME = Theme(
    {
        "info": "dim cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "highlight": "bold cyan",
        "filename": "blue underline",
        "metric": "magenta",
        "header": "bold",
    }
)

# Create a globally accessible console instance
console = Console(theme=THEME)


def display_validation_summary(
    filename: str,
    format_type: str,
    checks: List[Dict[str, str]],
    verbose: bool = False,
) -> None:
    """Display a summary of validation results.

    Args:
        filename: Name of the file that was validated
        format_type: Format of the file (csv, tsv, etc.)
        checks: List of check results as dictionaries with keys
            'name', 'status', 'details'
        verbose: Whether to show detailed output
    """
    # Count successes and failures
    successes = sum(1 for check in checks if check["status"] == "pass")
    failures = len(checks) - successes

    # Create header panel
    status = "SUCCESS" if failures == 0 else "FAILED"
    status_style = "success" if failures == 0 else "error"

    console.print(
        Panel(
            f"Validated [filename]{filename}[/] ([italic]{format_type}[/] format)\n"
            f"Result: [{status_style}]{status}[/] "
            f"({successes}/{len(checks)} checks passed)",
            title="Validation Summary",
            border_style="blue" if failures == 0 else "red",
        )
    )

    # Create results table
    if verbose or failures > 0:
        results_table = Table()
        results_table.add_column("Check", style="cyan")
        results_table.add_column("Status", style="bold")
        results_table.add_column("Details")

        for check in checks:
            status_icon = "✓" if check["status"] == "pass" else "✗"
            status_style = "green" if check["status"] == "pass" else "red"
            results_table.add_row(
                check["name"],
                f"[{status_style}]{status_icon}[/]",
                check["details"],
            )

        console.print(results_table)


def progress_spinner(description: str) -> Status:
    """Create a spinner for long-running operations.

    Args:
        description: Text to display with the spinner

    Returns:
        A context manager for the spinner
    """
    return console.status(f"[bold blue]{description}[/]", spinner="dots")


def print_error(message: str, exception: Optional[Exception] = None) -> None:
    """Print an error message with optional exception details.

    Args:
        message: The error message to display
        exception: Optional exception to show details for
    """
    console.print(f"[error]Error:[/] {message}")
    if exception:
        console.print_exception()
