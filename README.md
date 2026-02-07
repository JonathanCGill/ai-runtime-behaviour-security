# AI Security Blueprint

Operational controls for enterprise AI systems.

![AI Security Blueprint](images/ai-security-tube-map.svg)

---

## New Here?

**[→ Quick Start](QUICK_START.md)** — Get from zero to first controls in 30 minutes.

---

## The Core Idea

| Layer | Function | Timing |
|-------|----------|--------|
| **Guardrails** | Block known-bad inputs/outputs | Real-time |
| **LLM-as-Judge** | Detect issues, surface findings | Async |
| **Human Oversight** | Decide, act, remain accountable | As needed |

**Guardrails prevent. The Judge detects. Humans decide.**

These three principles are the framework. Everything else is implementation detail that you'll adapt to your environment.

---

## Start Here

**[→ Core Framework](core/README.md)** — Everything you need to implement AI governance.

| Document | Purpose |
|----------|---------|
| [README](core/README.md) | Overview, quick start, key principles |
| [Risk Tiers](core/risk-tiers.md) | Classification and control selection |
| [Controls](core/controls.md) | Guardrails, Judge, Human Oversight |
| [Agentic](core/agentic.md) | Additional controls for agents |
| [Checklist](core/checklist.md) | Implementation tracking |
| [Emerging Controls](core/emerging-controls.md) | Multimodal, reasoning, streaming, multi-agent *(theoretical)* |

**Read the first 5 documents. That's the framework.** The sixth is forward-looking.

---

## Extensions

Reference material for deep dives and specific needs.

| Folder | Contents |
|--------|----------|
| [extensions/regulatory/](extensions/regulatory/) | ISO 42001, EU AI Act, banking guidance |
| [extensions/technical/](extensions/technical/) | Bypass prevention, infrastructure, metrics |
| [extensions/templates/](extensions/templates/) | Incident playbooks, assessments |
| [extensions/examples/](extensions/examples/) | Worked examples by use case |
| [images/](images/) | Architecture diagrams (SVG) |

---

## Insights

Standalone articles for sharing and discussion.

### Core Concepts
| Article | Summary |
|---------|---------|
| [Why Your AI Guardrails Aren't Enough](insights/why-guardrails-arent-enough.md) | The main argument — introduces the three-layer model |
| [The Judge Detects. It Doesn't Decide.](insights/judge-detects-not-decides.md) | Why async evaluation beats real-time blocking |
| [Infrastructure Beats Instructions](insights/infrastructure-beats-instructions.md) | You can't secure agents with prompts |
| [Risk Tier Is Use Case, Not Technology](insights/risk-tier-is-use-case.md) | Classification is about deployment, not capability |
| [Humans Remain Accountable](insights/humans-remain-accountable.md) | AI assists. Humans own outcomes. |

### Emerging AI Challenges
| Article | Summary |
|---------|---------|
| [Multimodal AI Breaks Your Text-Based Guardrails](insights/multimodal-breaks-guardrails.md) | Images, audio, video create new attack surfaces |
| [When AI Thinks Before It Answers](insights/when-ai-thinks.md) | Reasoning models and hidden chains |
| [When Agents Talk to Agents](insights/when-agents-talk-to-agents.md) | Multi-agent accountability gaps |
| [The Memory Problem](insights/the-memory-problem.md) | Long context and persistent memory risks |
| [You Can't Validate What Hasn't Finished](insights/you-cant-validate-unfinished.md) | Real-time streaming AI challenges |

---

## Scope

**In scope:** Custom LLM apps, AI decision support, document processing, agentic systems

**Out of scope:** 
- Vendor AI products (Copilot, Duet, etc.)
- Model training and development
- Data preparation and labelling
- Pre-deployment validation

This framework is **operationally focused** — deployment through incident response.

---

## Critical Context

**AI does not exist in isolation.** Every AI system is part of a data flow supply chain:

- **Upstream:** User inputs, databases, APIs, documents, context
- **AI Core:** Model, guardrails, prompts, tools, memory
- **Downstream:** Databases, workflows, APIs, human processes

Your controls must address the full chain. See the [Threat Model Template](extensions/templates/threat-model-template.md) for how to analyse this.

---

## Status

This is a **discussion draft**, not a finished standard.

- Some pieces are proven, some are proposals
- Feedback welcome — see [CONTRIBUTING.md](CONTRIBUTING.md)
- Will evolve as we learn
- See who's using it: [ADOPTERS.md](ADOPTERS.md)

---

## Quick Links

| Need | Go To |
|------|-------|
| Get started fast | [Quick Start](QUICK_START.md) |
| Classify a system | [Risk Tiers](core/risk-tiers.md) |
| Implement controls | [Controls](core/controls.md) |
| Deploy an agent | [Agentic](core/agentic.md) |
| Track implementation | [Checklist](core/checklist.md) |
| Test your controls | [Testing Guidance](extensions/templates/testing-guidance.md) |
| Threat model your system | [Threat Model Template](extensions/templates/threat-model-template.md) |
| ISO 42001 alignment | [extensions/regulatory/](extensions/regulatory/) |
| Infrastructure controls | [extensions/technical/](extensions/technical/) |
| Incident playbooks | [extensions/templates/](extensions/templates/) |
| See examples | [extensions/examples/](extensions/examples/) |
