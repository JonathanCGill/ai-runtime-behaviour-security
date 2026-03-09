"""Risk classification engine.

Classifies an AI deployment into a risk tier based on context factors,
then recommends the appropriate control set.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from airs.core.models import RiskTier


class DeploymentProfile(BaseModel):
    """Describes an AI deployment for risk classification.

    Answer these questions about your deployment to get a risk tier
    and prioritized control recommendations.
    """

    # Audience & exposure
    external_facing: bool = False
    user_count: str = "small"  # small (<100), medium (100-10k), large (10k+)

    # Data sensitivity
    handles_pii: bool = False
    handles_regulated_data: bool = False  # HIPAA, SOX, GDPR-sensitive
    handles_financial_data: bool = False

    # Autonomy & impact
    can_take_actions: bool = False  # writes, API calls, transactions
    actions_are_reversible: bool = True
    max_financial_impact: str = "none"  # none, low (<$1k), medium (<$100k), high (>$100k)

    # Architecture
    multi_agent: bool = False
    uses_rag: bool = False
    uses_tools: bool = False
    uses_mcp: bool = False

    # Oversight
    human_reviews_all_outputs: bool = False
    has_existing_guardrails: bool = False

    # Regulatory
    regulated_industry: bool = False  # healthcare, finance, legal, etc.

    name: str = ""
    description: str = ""


class RiskClassifier:
    """Classifies a deployment profile into a risk tier.

    Based on the framework's risk tier criteria:
    - LOW: Internal, read-only, no regulated data, human-reviewed
    - MEDIUM: External or handles PII, but no autonomous actions
    - HIGH: Takes actions, handles regulated data, or large audience
    - CRITICAL: Irreversible high-impact actions in regulated context
    """

    def classify(self, profile: DeploymentProfile) -> RiskTier:
        score = 0
        reasons: list[str] = []

        # Audience exposure
        if profile.external_facing:
            score += 2
            reasons.append("External-facing")
        if profile.user_count == "large":
            score += 2
            reasons.append("Large user base (10k+)")
        elif profile.user_count == "medium":
            score += 1

        # Data sensitivity
        if profile.handles_regulated_data:
            score += 3
            reasons.append("Regulated data")
        if profile.handles_pii:
            score += 2
            reasons.append("Handles PII")
        if profile.handles_financial_data:
            score += 2
            reasons.append("Financial data")

        # Autonomy & impact
        if profile.can_take_actions:
            score += 2
            reasons.append("Can take actions")
            if not profile.actions_are_reversible:
                score += 3
                reasons.append("Irreversible actions")
        if profile.max_financial_impact == "high":
            score += 3
            reasons.append("High financial impact (>$100k)")
        elif profile.max_financial_impact == "medium":
            score += 2
            reasons.append("Medium financial impact")

        # Architecture complexity
        if profile.multi_agent:
            score += 2
            reasons.append("Multi-agent system")
        if profile.uses_mcp:
            score += 1
            reasons.append("Uses MCP")

        # Mitigations (reduce score)
        if profile.human_reviews_all_outputs:
            score -= 2
        if profile.has_existing_guardrails:
            score -= 1

        # Regulatory overlay
        if profile.regulated_industry:
            score += 2
            reasons.append("Regulated industry")

        # Map score to tier
        if score <= 2:
            tier = RiskTier.LOW
        elif score <= 6:
            tier = RiskTier.MEDIUM
        elif score <= 10:
            tier = RiskTier.HIGH
        else:
            tier = RiskTier.CRITICAL

        return tier

    def classify_with_reasons(
        self, profile: DeploymentProfile
    ) -> tuple[RiskTier, list[str], list[str]]:
        """Classify and return (tier, risk_factors, mitigations)."""
        risk_factors: list[str] = []
        mitigations: list[str] = []

        if profile.external_facing:
            risk_factors.append("External-facing deployment")
        if profile.user_count == "large":
            risk_factors.append("Large user base (10,000+)")
        if profile.handles_pii:
            risk_factors.append("Handles personally identifiable information")
        if profile.handles_regulated_data:
            risk_factors.append("Handles regulated data (HIPAA/SOX/GDPR)")
        if profile.handles_financial_data:
            risk_factors.append("Handles financial data")
        if profile.can_take_actions:
            risk_factors.append("AI can take autonomous actions")
        if profile.can_take_actions and not profile.actions_are_reversible:
            risk_factors.append("Actions are irreversible")
        if profile.max_financial_impact in ("medium", "high"):
            risk_factors.append(f"Financial impact: {profile.max_financial_impact}")
        if profile.multi_agent:
            risk_factors.append("Multi-agent architecture")
        if profile.uses_mcp:
            risk_factors.append("Uses Model Context Protocol (MCP)")
        if profile.regulated_industry:
            risk_factors.append("Regulated industry")

        if profile.human_reviews_all_outputs:
            mitigations.append("Human reviews all outputs")
        if profile.has_existing_guardrails:
            mitigations.append("Existing guardrails in place")
        if not profile.can_take_actions:
            mitigations.append("Read-only (no autonomous actions)")
        if not profile.external_facing:
            mitigations.append("Internal-only deployment")

        tier = self.classify(profile)
        return tier, risk_factors, mitigations
