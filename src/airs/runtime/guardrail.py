"""Layer 1: Guardrails — fast, deterministic checks on input and output.

Guardrails block known-bad patterns. They are cheap (~10ms), deterministic,
and catch the obvious stuff. They do NOT catch novel attacks or subtle
policy violations — that's what the Judge layer is for.
"""

from __future__ import annotations

import re
import time
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from airs.core.models import ControlLayer, GuardrailVerdict, LayerResult


class GuardrailResult(BaseModel):
    """Result from a single guardrail check."""

    name: str
    verdict: GuardrailVerdict
    reason: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class Guardrail(ABC):
    """Base class for guardrail implementations.

    Subclass this to implement custom guardrail checks.
    Each guardrail should be fast (<50ms) and deterministic.
    """

    name: str = "base_guardrail"

    @abstractmethod
    def check_input(self, text: str, **kwargs: Any) -> GuardrailResult:
        """Check input text. Return PASS, BLOCK, or FLAG."""
        ...

    @abstractmethod
    def check_output(self, text: str, **kwargs: Any) -> GuardrailResult:
        """Check output text. Return PASS, BLOCK, or FLAG."""
        ...


class RegexGuardrail(Guardrail):
    """Guardrail based on regex pattern matching.

    Detects known-bad patterns like prompt injection attempts,
    PII patterns, or policy-violating content.
    """

    name = "regex_guardrail"

    def __init__(
        self,
        input_patterns: dict[str, str] | None = None,
        output_patterns: dict[str, str] | None = None,
        block_on_match: bool = True,
    ) -> None:
        self._input_patterns = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in (input_patterns or self._default_input_patterns()).items()
        }
        self._output_patterns = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in (output_patterns or self._default_output_patterns()).items()
        }
        self._block_on_match = block_on_match

    def check_input(self, text: str, **kwargs: Any) -> GuardrailResult:
        for name, pattern in self._input_patterns.items():
            if pattern.search(text):
                verdict = GuardrailVerdict.BLOCK if self._block_on_match else GuardrailVerdict.FLAG
                return GuardrailResult(
                    name=self.name,
                    verdict=verdict,
                    reason=f"Input matched pattern: {name}",
                    metadata={"pattern": name},
                )
        return GuardrailResult(name=self.name, verdict=GuardrailVerdict.PASS)

    def check_output(self, text: str, **kwargs: Any) -> GuardrailResult:
        for name, pattern in self._output_patterns.items():
            if pattern.search(text):
                verdict = GuardrailVerdict.BLOCK if self._block_on_match else GuardrailVerdict.FLAG
                return GuardrailResult(
                    name=self.name,
                    verdict=verdict,
                    reason=f"Output matched pattern: {name}",
                    metadata={"pattern": name},
                )
        return GuardrailResult(name=self.name, verdict=GuardrailVerdict.PASS)

    @staticmethod
    def _default_input_patterns() -> dict[str, str]:
        return {
            "prompt_injection_ignore": r"ignore\s+(all\s+)?(previous|above|prior)\s+(instructions|prompts|rules)",
            "prompt_injection_system": r"(you\s+are|act\s+as|pretend|new\s+instructions?|system\s*prompt)",
            "prompt_injection_jailbreak": r"(DAN|do\s+anything\s+now|jailbreak|bypass\s+(safety|filter|guard))",
            "prompt_injection_delimiter": r"(\[INST\]|\[\/INST\]|<\|system\|>|<\|user\|>|<<SYS>>)",
        }

    @staticmethod
    def _default_output_patterns() -> dict[str, str]:
        return {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "email_address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        }


class ContentPolicyGuardrail(Guardrail):
    """Keyword-based content policy filter.

    Blocks content containing terms from a configurable blocklist.
    This is the simplest possible content filter — production systems
    should use ML-based toxicity classifiers.
    """

    name = "content_policy"

    def __init__(self, blocked_terms: list[str] | None = None) -> None:
        self._blocked = [t.lower() for t in (blocked_terms or [])]

    def check_input(self, text: str, **kwargs: Any) -> GuardrailResult:
        return self._check(text)

    def check_output(self, text: str, **kwargs: Any) -> GuardrailResult:
        return self._check(text)

    def _check(self, text: str) -> GuardrailResult:
        text_lower = text.lower()
        for term in self._blocked:
            if term in text_lower:
                return GuardrailResult(
                    name=self.name,
                    verdict=GuardrailVerdict.BLOCK,
                    reason=f"Content policy violation: blocked term detected",
                )
        return GuardrailResult(name=self.name, verdict=GuardrailVerdict.PASS)


class GuardrailChain:
    """Chains multiple guardrails. Stops on first BLOCK.

    This is the Layer 1 entry point for the security pipeline.
    """

    def __init__(self, guardrails: list[Guardrail] | None = None) -> None:
        self._guardrails = guardrails or []

    def add(self, guardrail: Guardrail) -> "GuardrailChain":
        self._guardrails.append(guardrail)
        return self

    def check_input(self, text: str, **kwargs: Any) -> LayerResult:
        start = time.monotonic()
        for g in self._guardrails:
            result = g.check_input(text, **kwargs)
            if result.verdict == GuardrailVerdict.BLOCK:
                return LayerResult(
                    layer=ControlLayer.GUARDRAIL,
                    passed=False,
                    verdict=result.verdict.value,
                    reason=result.reason,
                    latency_ms=(time.monotonic() - start) * 1000,
                    metadata={"guardrail": result.name, **result.metadata},
                )
        return LayerResult(
            layer=ControlLayer.GUARDRAIL,
            passed=True,
            verdict=GuardrailVerdict.PASS.value,
            latency_ms=(time.monotonic() - start) * 1000,
        )

    def check_output(self, text: str, **kwargs: Any) -> LayerResult:
        start = time.monotonic()
        flagged = False
        flag_reasons: list[str] = []

        for g in self._guardrails:
            result = g.check_output(text, **kwargs)
            if result.verdict == GuardrailVerdict.BLOCK:
                return LayerResult(
                    layer=ControlLayer.GUARDRAIL,
                    passed=False,
                    verdict=result.verdict.value,
                    reason=result.reason,
                    latency_ms=(time.monotonic() - start) * 1000,
                    metadata={"guardrail": result.name, **result.metadata},
                )
            if result.verdict == GuardrailVerdict.FLAG:
                flagged = True
                flag_reasons.append(result.reason)

        verdict = GuardrailVerdict.FLAG if flagged else GuardrailVerdict.PASS
        return LayerResult(
            layer=ControlLayer.GUARDRAIL,
            passed=True,  # FLAG still passes, but routes to judge
            verdict=verdict.value,
            reason="; ".join(flag_reasons) if flagged else "",
            latency_ms=(time.monotonic() - start) * 1000,
        )
