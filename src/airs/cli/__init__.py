"""AIRS CLI — assessment tool and framework utilities."""

import typer

app = typer.Typer(
    name="airs",
    help="AI Runtime Security — assessment and implementation toolkit",
    no_args_is_help=True,
)

# Import subcommands to register them
from airs.cli import assess as _assess  # noqa: F401, E402
