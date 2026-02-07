# Blueprint Reframing Guide

## The Shift

| OLD Framing | NEW Framing |
|-------------|-------------|
| "This framework proposes..." | "The industry is converging on..." |
| "Our three-layer model" | "The three-layer pattern" |
| "Blueprint recommends..." | "Effective implementations include..." |
| "Novel approach" | "Emerging consensus" |
| "Framework adoption" | "Pattern implementation" |

---

## Core Messaging Changes

### Before (Framework Creator)
> "The AI Security Blueprint provides a framework for controlling AI systems through three layers: Guardrails, Judge, and Human Oversight."

### After (Pattern Synthesizer)
> "AI systems require runtime behavioral controls because traditional design-time testing is insufficient. The industry is converging on a three-layer pattern: Guardrails prevent known-bad, Judge detects unknown-bad, Humans decide edge cases. This guide explains how to implement it."

---

## Specific Files to Revise

### 1. README.md

**Current opening (likely):**
Something about "This framework..." or "The Blueprint provides..."

**Revised opening:**
```markdown
# AI Security Blueprint

## The Problem

Traditional software assurance relies on design-time testing. AI breaks this model — non-deterministic outputs, emergent behavior, and adversarial inputs mean you can't fully test before deployment.

## The Pattern

The industry is converging on **runtime behavioral monitoring** with three layers:

- **Guardrails** prevent known-bad (fast, deterministic)
- **Judge** detects unknown-bad (LLM evaluates LLM)  
- **Human Oversight** decides edge cases (accountability for high-stakes)

This isn't a new invention. NVIDIA, LangChain, Anthropic, and others implement variations. OWASP describes the risks. NIST and ISO describe governance.

## What This Guide Provides

A practical synthesis: how to understand the pattern, select appropriate controls, and implement them proportionate to risk.
```

---

### 2. core/three-layer-model.md (or equivalent)

**Remove:** Any language suggesting this is novel or proprietary

**Add:** Section on "Where This Pattern Exists"
```markdown
## Where This Pattern Exists

This isn't theoretical. Production implementations include:

| Platform | How They Implement It |
|----------|----------------------|
| NVIDIA NeMo Guardrails | 5 rail types (input, dialog, retrieval, execution, output) |
| LangChain | Middleware + human-in-the-loop |
| Anthropic Claude | Constitutional AI + usage policies |
| OpenAI | Moderation API + custom instructions |
| Galileo | Eval-to-guardrail lifecycle |

What's missing is a clear explanation of *why* this pattern is necessary and *how* to implement it proportionate to risk. That's what this guide provides.
```

---

### 3. QUICK_START.md

**Reframe from:** "Adopt this framework"

**Reframe to:** "Implement this pattern"

```markdown
# Quick Start: Implementing Behavioral Controls for AI

## Why You're Here

You're building AI systems and need to answer: "How do we know it's working correctly?"

Traditional testing is necessary but insufficient. You need runtime behavioral monitoring.

## The Pattern

1. **Guardrails** — Block known-bad inputs/outputs (fast, rules-based)
2. **Judge** — Evaluate outputs for unknown-bad (LLM-based, slower)
3. **Human Oversight** — Review high-stakes decisions (async, accountable)

## What to Do

1. **Classify your use case** — What's the risk if it goes wrong?
2. **Select controls** — Proportionate to that risk
3. **Implement monitoring** — Not just logging, but active evaluation
4. **Establish escalation** — When does a human get involved?

[Continue with existing content, reframed...]
```

---

### 4. Any "About" or "Introduction" content

**Remove:**
- "This framework was developed to..."
- "The Blueprint recommends..."
- "Our approach differs from..."

**Replace with:**
- "This pattern addresses..."
- "Effective implementations include..."
- "The key insight is..."

---

### 5. Governance / Regulatory Sections

**Keep:** These are valuable — mapping to ISO 42001, EU AI Act, etc.

**Reframe:** 
```markdown
## Regulatory Alignment

The three-layer pattern maps to regulatory expectations:

| Regulation | What It Requires | How the Pattern Addresses It |
|------------|------------------|------------------------------|
| EU AI Act | Human oversight for high-risk | HITL layer for CRITICAL tier |
| ISO 42001 | AI risk management | Risk-tiered control selection |
| NIST AI RMF | Measure and manage | Judge provides continuous measurement |
```

---

## Tone Adjustments

### Avoid
- "We believe..."
- "This framework asserts..."
- "Our model shows..."
- "The Blueprint's unique contribution..."

### Use Instead
- "The pattern works because..."
- "Implementations show that..."
- "The evidence suggests..."
- "Practitioners report that..."

---

## What Stays the Same

- **The three-layer model itself** — it's solid
- **Risk tiering** — genuinely useful
- **Control selection guidance** — practical value
- **Regulatory crosswalks** — unique contribution
- **Implementation checklists** — operational value

The *content* is good. The *framing* needs to shift from "creator" to "synthesizer."

---

## One-Line Summary

**Old:** "Here's a framework I created for AI security."

**New:** "Here's the pattern everyone's converging on, clearly explained, with practical implementation guidance."
