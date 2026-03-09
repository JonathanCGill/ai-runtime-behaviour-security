"""Tests for risk classification."""

from airs.core.models import RiskTier
from airs.core.risk import DeploymentProfile, RiskClassifier


class TestRiskClassifier:
    def test_internal_readonly_is_low(self):
        profile = DeploymentProfile(
            external_facing=False,
            user_count="small",
            handles_pii=False,
            can_take_actions=False,
        )
        classifier = RiskClassifier()
        assert classifier.classify(profile) == RiskTier.LOW

    def test_external_with_pii_is_medium(self):
        profile = DeploymentProfile(
            external_facing=True,
            handles_pii=True,
        )
        classifier = RiskClassifier()
        assert classifier.classify(profile) == RiskTier.MEDIUM

    def test_regulated_with_actions_is_high(self):
        profile = DeploymentProfile(
            external_facing=True,
            handles_regulated_data=True,
            can_take_actions=True,
        )
        classifier = RiskClassifier()
        tier = classifier.classify(profile)
        assert tier in (RiskTier.HIGH, RiskTier.CRITICAL)

    def test_irreversible_financial_is_critical(self):
        profile = DeploymentProfile(
            external_facing=True,
            handles_regulated_data=True,
            handles_financial_data=True,
            can_take_actions=True,
            actions_are_reversible=False,
            max_financial_impact="high",
            regulated_industry=True,
        )
        classifier = RiskClassifier()
        assert classifier.classify(profile) == RiskTier.CRITICAL

    def test_human_review_mitigates(self):
        profile_without = DeploymentProfile(
            external_facing=True,
            handles_pii=True,
            can_take_actions=True,
        )
        profile_with = DeploymentProfile(
            external_facing=True,
            handles_pii=True,
            can_take_actions=True,
            human_reviews_all_outputs=True,
        )
        classifier = RiskClassifier()
        tier_without = classifier.classify(profile_without)
        tier_with = classifier.classify(profile_with)
        assert tier_with.value <= tier_without.value or tier_with == tier_without

    def test_classify_with_reasons(self):
        profile = DeploymentProfile(
            external_facing=True,
            handles_pii=True,
            multi_agent=True,
        )
        classifier = RiskClassifier()
        tier, factors, mitigations = classifier.classify_with_reasons(profile)
        assert "External-facing deployment" in factors
        assert "Handles personally identifiable information" in factors
        assert "Multi-agent architecture" in factors
        assert any("Read-only" in m for m in mitigations)
