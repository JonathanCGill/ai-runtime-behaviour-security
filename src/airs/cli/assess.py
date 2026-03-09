"""CLI assessment tool — classify your deployment and get a prioritized implementation plan.

Run: airs assess
"""

from __future__ import annotations

import json
import sys
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from airs.cli import app
from airs.core.controls import ControlRegistry, MATSOTier
from airs.core.models import PACEState, RiskTier
from airs.core.risk import DeploymentProfile, RiskClassifier

console = Console()


def _ask_bool(question: str, default: bool = False) -> bool:
    suffix = " [Y/n]" if default else " [y/N]"
    result = typer.prompt(question + suffix, default="y" if default else "n", show_default=False)
    return result.strip().lower() in ("y", "yes", "true", "1")


def _ask_choice(question: str, choices: list[str], default: str = "") -> str:
    choices_str = " / ".join(choices)
    result = typer.prompt(f"{question} ({choices_str})", default=default or choices[0])
    while result not in choices:
        console.print(f"[red]Please choose one of: {choices_str}[/red]")
        result = typer.prompt(f"{question} ({choices_str})", default=default or choices[0])
    return result


TIER_COLORS = {
    RiskTier.LOW: "green",
    RiskTier.MEDIUM: "yellow",
    RiskTier.HIGH: "red",
    RiskTier.CRITICAL: "bold red",
}

TIER_DESCRIPTIONS = {
    RiskTier.LOW: "Fast Lane eligible — minimal guardrails + logging + feature flag",
    RiskTier.MEDIUM: "Full guardrails + sampling Judge + periodic human review",
    RiskTier.HIGH: "Full architecture, 100% Judge evaluation, human-in-the-loop for writes",
    RiskTier.CRITICAL: "All layers + mandatory human approval + tested PACE failover",
}

PACE_TABLE = {
    RiskTier.LOW: {
        "Primary": "Guardrails active, logging enabled",
        "Alternate": "Tighten guardrails, increase logging",
        "Contingency": "Human review for all outputs",
        "Emergency": "Feature flag OFF → static fallback",
    },
    RiskTier.MEDIUM: {
        "Primary": "Guardrails + 5% Judge sampling",
        "Alternate": "Guardrails + 100% Judge evaluation",
        "Contingency": "Human approval for all outputs",
        "Emergency": "Circuit breaker → non-AI fallback",
    },
    RiskTier.HIGH: {
        "Primary": "Guardrails + 100% Judge + human review queue",
        "Alternate": "Tighten scope, block new tool access",
        "Contingency": "Read-only mode, human approval for all",
        "Emergency": "Full stop, incident response activated",
    },
    RiskTier.CRITICAL: {
        "Primary": "All layers + mandatory human approval",
        "Alternate": "Reduced scope, elevated monitoring",
        "Contingency": "Minimal operation, human decides all",
        "Emergency": "Immediate shutdown, IR team engaged",
    },
}


@app.command()
def assess(
    output_json: bool = typer.Option(False, "--json", help="Output as JSON"),
    non_interactive: bool = typer.Option(False, "--non-interactive", help="Use defaults"),
) -> None:
    """Assess your AI deployment and get a prioritized security implementation plan."""

    if not non_interactive:
        console.print()
        console.print(
            Panel(
                "[bold]AIRS Deployment Assessment[/bold]\n\n"
                "Answer the following questions about your AI deployment.\n"
                "This will classify your risk tier and recommend controls.",
                title="AI Runtime Security",
                border_style="blue",
            )
        )
        console.print()

    # Gather deployment profile
    if non_interactive:
        profile = DeploymentProfile()
    else:
        profile = _gather_profile()

    # Classify
    classifier = RiskClassifier()
    tier, risk_factors, mitigations = classifier.classify_with_reasons(profile)

    # Get recommended controls
    registry = ControlRegistry()
    maso_tier = None
    if profile.multi_agent:
        maso_tier = _infer_maso_tier(tier)
    controls = registry.prioritized_for(tier, maso_tier)

    if output_json:
        _output_json(profile, tier, risk_factors, mitigations, controls, maso_tier)
    else:
        _output_rich(profile, tier, risk_factors, mitigations, controls, maso_tier)


def _gather_profile() -> DeploymentProfile:
    """Interactive questionnaire."""
    console.print("[bold]1. Deployment Context[/bold]")
    name = typer.prompt("  Deployment name (optional)", default="")
    external = _ask_bool("  Is this deployment external-facing (customers/public)?")
    user_count = _ask_choice("  Expected user count", ["small", "medium", "large"], "small")

    console.print()
    console.print("[bold]2. Data Sensitivity[/bold]")
    pii = _ask_bool("  Does it handle PII (names, emails, addresses)?")
    regulated = _ask_bool("  Does it handle regulated data (HIPAA, SOX, GDPR)?")
    financial = _ask_bool("  Does it handle financial data?")

    console.print()
    console.print("[bold]3. Autonomy & Impact[/bold]")
    actions = _ask_bool("  Can the AI take actions (write data, call APIs, make transactions)?")
    reversible = True
    impact = "none"
    if actions:
        reversible = _ask_bool("  Are those actions reversible?", default=True)
        impact = _ask_choice("  Maximum financial impact per action", ["none", "low", "medium", "high"], "none")

    console.print()
    console.print("[bold]4. Architecture[/bold]")
    multi_agent = _ask_bool("  Is this a multi-agent system?")
    rag = _ask_bool("  Does it use RAG (retrieval-augmented generation)?")
    tools = _ask_bool("  Does it use tools/function calling?")
    mcp = False
    if tools:
        mcp = _ask_bool("  Does it use MCP (Model Context Protocol)?")

    console.print()
    console.print("[bold]5. Existing Controls[/bold]")
    human_review = _ask_bool("  Does a human review ALL outputs before delivery?")
    existing_guardrails = _ask_bool("  Do you have existing guardrails in place?")

    console.print()
    console.print("[bold]6. Regulatory[/bold]")
    regulated_industry = _ask_bool("  Is this in a regulated industry (healthcare, finance, legal)?")

    return DeploymentProfile(
        name=name,
        external_facing=external,
        user_count=user_count,
        handles_pii=pii,
        handles_regulated_data=regulated,
        handles_financial_data=financial,
        can_take_actions=actions,
        actions_are_reversible=reversible,
        max_financial_impact=impact,
        multi_agent=multi_agent,
        uses_rag=rag,
        uses_tools=tools,
        uses_mcp=mcp,
        human_reviews_all_outputs=human_review,
        has_existing_guardrails=existing_guardrails,
        regulated_industry=regulated_industry,
    )


def _infer_maso_tier(risk_tier: RiskTier) -> MATSOTier:
    if risk_tier in (RiskTier.LOW, RiskTier.MEDIUM):
        return MATSOTier.SUPERVISED
    elif risk_tier == RiskTier.HIGH:
        return MATSOTier.MANAGED
    else:
        return MATSOTier.AUTONOMOUS


def _output_rich(
    profile: DeploymentProfile,
    tier: RiskTier,
    risk_factors: list[str],
    mitigations: list[str],
    controls: list,
    maso_tier: MATSOTier | None,
) -> None:
    console.print()

    # Risk tier result
    color = TIER_COLORS[tier]
    console.print(Panel(
        f"[{color}]Risk Tier: {tier.value.upper()}[/{color}]\n\n"
        f"{TIER_DESCRIPTIONS[tier]}",
        title="Assessment Result",
        border_style=color,
    ))

    # Risk factors
    if risk_factors:
        console.print()
        console.print("[bold]Risk Factors:[/bold]")
        for f in risk_factors:
            console.print(f"  [red]![/red] {f}")

    if mitigations:
        console.print()
        console.print("[bold]Mitigating Factors:[/bold]")
        for m in mitigations:
            console.print(f"  [green]+[/green] {m}")

    # MASO tier
    if maso_tier:
        console.print()
        console.print(f"[bold]Multi-Agent Tier:[/bold] {maso_tier.value.title()}")

    # PACE posture
    console.print()
    pace_table = Table(title="PACE Resilience Posture", show_header=True)
    pace_table.add_column("State", style="bold", width=14)
    pace_table.add_column("Posture")

    pace_data = PACE_TABLE[tier]
    state_colors = {"Primary": "green", "Alternate": "yellow", "Contingency": "red", "Emergency": "bold red"}
    for state, desc in pace_data.items():
        pace_table.add_row(f"[{state_colors[state]}]{state}[/{state_colors[state]}]", desc)
    console.print(pace_table)

    # Recommended controls
    console.print()
    ctrl_table = Table(title=f"Recommended Controls ({len(controls)} total)", show_header=True)
    ctrl_table.add_column("#", width=4)
    ctrl_table.add_column("ID", width=10)
    ctrl_table.add_column("Control", width=35)
    ctrl_table.add_column("Layer", width=16)
    ctrl_table.add_column("Priority")

    for i, c in enumerate(controls, 1):
        priority = "Implement first" if i <= 3 else ("Phase 2" if i <= 8 else "Phase 3")
        p_color = "green" if i <= 3 else ("yellow" if i <= 8 else "dim")
        ctrl_table.add_row(
            str(i),
            c.id,
            c.name,
            c.layer.value.replace("_", " ").title(),
            f"[{p_color}]{priority}[/{p_color}]",
        )
    console.print(ctrl_table)

    # Implementation hints for top 3
    console.print()
    console.print(Panel("[bold]Quick Start — Top 3 Controls[/bold]", border_style="green"))
    for c in controls[:3]:
        console.print(f"\n  [bold]{c.id}: {c.name}[/bold]")
        console.print(f"  {c.description}")
        if c.implementation_hint:
            console.print(f"  [dim]Hint: {c.implementation_hint}[/dim]")

    # Code snippet
    console.print()
    console.print(Panel(
        _generate_code_snippet(tier, maso_tier),
        title="Getting Started with airs SDK",
        border_style="blue",
    ))


def _output_json(
    profile: DeploymentProfile,
    tier: RiskTier,
    risk_factors: list[str],
    mitigations: list[str],
    controls: list,
    maso_tier: MATSOTier | None,
) -> None:
    output = {
        "profile": profile.model_dump(),
        "assessment": {
            "risk_tier": tier.value,
            "maso_tier": maso_tier.value if maso_tier else None,
            "risk_factors": risk_factors,
            "mitigations": mitigations,
        },
        "controls": [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "layer": c.layer.value,
                "domain": c.domain.value,
                "implementation_hint": c.implementation_hint,
                "owasp_refs": c.owasp_refs,
                "priority": i + 1,
            }
            for i, c in enumerate(controls)
        ],
        "pace_posture": PACE_TABLE[tier],
    }
    console.print_json(json.dumps(output, indent=2))


def _generate_code_snippet(tier: RiskTier, maso_tier: MATSOTier | None) -> str:
    snippet = '''from airs.runtime import (
    SecurityPipeline, GuardrailChain, RegexGuardrail,
    CircuitBreaker, PACEController,
)
from airs.core.models import AIRequest, AIResponse

# Build the three-layer pipeline
pipeline = SecurityPipeline(
    guardrails=GuardrailChain([RegexGuardrail()]),
    circuit_breaker=CircuitBreaker(),
    pace=PACEController(),
)

# Evaluate input
request = AIRequest(input_text=user_input)
input_result = await pipeline.evaluate_input(request)
if not input_result.allowed:
    return fallback_response(input_result)

# Call your AI model
ai_output = await your_model(request.input_text)
response = AIResponse(request_id=request.request_id, output_text=ai_output)

# Evaluate output
output_result = await pipeline.evaluate_output(request, response)
if not output_result.allowed:
    return fallback_response(output_result)

return ai_output'''
    return snippet
