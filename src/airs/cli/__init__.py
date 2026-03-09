"""AIRS CLI — assessment tool and framework utilities."""

import typer

from airs import __version__

app = typer.Typer(
    name="airs",
    help="AI Runtime Security — assessment and implementation toolkit",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Show the AIRS SDK version."""
    typer.echo(f"airs {__version__}")


@app.command()
def controls(
    risk_tier: str = typer.Option("medium", "--tier", help="Risk tier: low, medium, high, critical"),
) -> None:
    """List recommended controls for a risk tier."""
    from rich.console import Console
    from rich.table import Table

    from airs.core.controls import ControlRegistry
    from airs.core.models import RiskTier

    console = Console()
    tier_map = {t.value: t for t in RiskTier}
    tier = tier_map.get(risk_tier.lower())
    if not tier:
        console.print(f"[red]Unknown tier: {risk_tier}. Use: low, medium, high, critical[/red]")
        raise typer.Exit(1)

    registry = ControlRegistry()
    results = registry.prioritized_for(tier)

    table = Table(title=f"Controls for {tier.value.upper()} risk tier ({len(results)} total)")
    table.add_column("#", width=4)
    table.add_column("ID", width=10)
    table.add_column("Control", width=35)
    table.add_column("Layer", width=16)
    table.add_column("Hint")

    for i, c in enumerate(results, 1):
        table.add_row(str(i), c.id, c.name, c.layer.value.replace("_", " ").title(), c.implementation_hint[:80])

    console.print(table)


# Import and register assess command
from airs.cli.assess import assess_cmd  # noqa: E402

app.command(name="assess", help="Assess your AI deployment and get a prioritized security implementation plan.")(assess_cmd)
