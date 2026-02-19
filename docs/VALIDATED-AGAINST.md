# Validated Against Real Incidents

**Every major control in this framework addresses a documented, public AI security failure. This page is the evidence.**

> Part of [AI Runtime Behaviour Security](./)
> Last updated: February 2026

---

## How to Read This Page

The [Incident Tracker](maso/threat-intelligence/incident-tracker.md) is organised by incident — "here's what happened, here are the controls." This page inverts that view. It's organised by **control** — "here's the control, here's the evidence it addresses real threats."

Each control is mapped to the incidents it would have prevented or detected, with the specific mechanism explained. Controls validated against more incidents have a stronger evidence base. Controls validated against zero incidents are flagged — they may still be valuable, but they're based on threat modelling rather than observed attacks.

**Validation does not mean proven.** It means the control addresses a documented attack pattern. Whether the control would have *actually* prevented the incident in your environment depends on your implementation. This is retroactive analysis, not a guarantee.

---

## Validation Summary

### Controls by Evidence Strength

| Evidence Level | Criteria | Control Count |
|---------------|----------|---------------|
| **Strong** | Addresses 3+ real incidents | 5 controls |
| **Moderate** | Addresses 1–2 real incidents | 18 controls |
| **Threat-modelled** | Based on emerging threat analysis, not yet observed in production | Remaining controls |

### Most-Validated Controls

These controls are referenced across the highest number of documented incidents. They form the minimum credible defence.

| Rank | Control | Incidents | Evidence Base |
|------|---------|-----------|---------------|
| 1 | **PG-1.1** Input guardrails per agent | 8 of 10 | INC-01, 02, 03, 04, 05, 07, 08, 09 |
| 2 | **EC-2.5** LLM-as-Judge gate | 5 of 10 | INC-01, 02, 05, 09, 10 |
| 3 | **EC-1.1** Human approval for write operations | 3 of 10 | INC-01, 06, 09 |
| 3 | **DP-2.1** DLP on message bus | 3 of 10 | INC-04, 06, 07 |
| 3 | **OB-3.1** Independent observability agent | 3 of 10 | INC-07, 09, 10 |

**What this tells you:** If you implement nothing else, input guardrails per agent and an LLM-as-Judge gate address the widest range of documented attack patterns. This is consistent with the framework's core architecture — Guardrails prevent, Judge detects.

---

## Control-by-Control Validation

### Prompt, Goal & Epistemic Integrity

#### PG-1.1 — Input Guardrails Per Agent

**Evidence strength: Strong (8 incidents)**

The single most broadly validated control. Addresses the widest range of attack vectors because prompt injection — direct and indirect — is the most common AI attack primitive.

| Incident | Attack Vector | How PG-1.1 Helps |
|----------|--------------|-------------------|
| INC-01: Auto-GPT crypto transfer | Indirect injection via email | Detects injection patterns in email content before agent processes it |
| INC-02: Copilot RCE | Indirect injection via code comments | Filters injection patterns from code repository content |
| INC-03: Cursor IDE RCE | Configuration poisoning | Detects malicious patterns in configuration file content |
| INC-04: Perplexity data exfil | Indirect injection via web content | Catches injection payloads in scraped web pages |
| INC-05: PoisonedRAG | RAG corpus contamination | Identifies suspicious patterns in retrieved documents (partial — sophisticated poisoning may evade) |
| INC-07: Morris II worm | Self-replicating injection via inter-agent messages | Detects injection patterns in incoming agent-to-agent messages |
| INC-08: MCP supply chain | Poisoned MCP tool metadata | Filters injection from MCP tool descriptions and responses |
| INC-09: Banking AI fraud | Direct prompt injection via chat | Detects injection patterns in customer messages |

**Limitations:** Guardrails are pattern-based. They catch known injection techniques effectively but can be evaded by novel or highly contextual attacks. This is exactly why the framework pairs guardrails with Judge evaluation (PG-1.1 + EC-2.5).

---

#### PG-1.2 — System Prompt Isolation

**Evidence strength: Moderate (1 incident)**

| Incident | How PG-1.2 Helps |
|----------|-------------------|
| INC-02: Copilot RCE | Prevents external content (code comments) from overriding agent system instructions |

**Threat model basis:** System prompt extraction and override are well-documented attack classes. While only one tracked incident directly exploits this, the attack primitive is fundamental to prompt injection.

---

#### PG-1.3 — Immutable Task Specification

**Evidence strength: Moderate (1 incident)**

| Incident | How PG-1.3 Helps |
|----------|-------------------|
| INC-03: Cursor IDE RCE | Task definitions cannot be modified by external configuration files — prevents the path traversal attack vector |

---

#### PG-1.4 — Message Source Tagging

**Evidence strength: Moderate (2 incidents)**

| Incident | How PG-1.4 Helps |
|----------|-------------------|
| INC-01: Auto-GPT crypto transfer | Tags email-derived content as untrusted data, not instruction — agent processes it as data, not commands |
| INC-07: Morris II worm | Distinguishes legitimate inter-agent instructions from data payloads — worm content tagged as data, not instruction |

**Why this matters:** The root cause of most indirect injection attacks is that AI systems treat all input as potential instruction. Message source tagging enforces the instruction/data boundary at the protocol level.

---

#### PG-2.1 — Inter-Agent Injection Detection

**Evidence strength: Moderate (1 incident)**

| Incident | How PG-2.1 Helps |
|----------|-------------------|
| INC-07: Morris II worm | Judge evaluates all inter-agent messages for injection patterns — blocks worm propagation at the message bus |

**Threat model basis:** This control is purpose-built for the Morris II attack class. As multi-agent systems become more common, inter-agent injection will become a primary attack vector.

---

#### PG-2.5 — Claim Provenance Enforcement

**Evidence strength: Moderate (1 incident)**

| Incident | How PG-2.5 Helps |
|----------|-------------------|
| INC-05: PoisonedRAG | Unverified agent claims cannot be treated as facts — forces provenance tracking back to original source, exposing the poisoned documents |

---

#### PG-2.6 — Self-Referential Evidence Prohibition

**Evidence strength: Moderate (1 incident)**

| Incident | How PG-2.6 Helps |
|----------|-------------------|
| INC-05: PoisonedRAG | Agents cannot cite other agents' output as primary evidence — breaks the amplification chain where Agent B cites Agent A's poisoned claim as a source |

---

#### PG-2.7 — Uncertainty Preservation

**Evidence strength: Moderate (1 incident)**

| Incident | How PG-2.7 Helps |
|----------|-------------------|
| INC-05: PoisonedRAG | Confidence scores propagate through agent chains without inflation — a 60% confidence claim from Agent A cannot become 95% confidence at Agent C |

---

#### PG-2.9 — Model Diversity Policy

**Evidence strength: Moderate (1 incident)**

| Incident | How PG-2.9 Helps |
|----------|-------------------|
| INC-10: JudgeDeceiver | Judge uses a different model/provider than task agents — adversarial optimisation against the task model doesn't transfer to the Judge |

**Why this matters:** JudgeDeceiver works by optimising against a known model. Model diversity raises the attack cost from "optimise against one model" to "optimise against multiple unknown models simultaneously."

---

#### PG-3.5 — Challenger Agent

**Evidence strength: Moderate (2 incidents)**

| Incident | How PG-3.5 Helps |
|----------|-------------------|
| INC-05: PoisonedRAG | Adversarial agent actively attacks the primary hypothesis — challenges the poisoned claim with counter-evidence |
| INC-10: JudgeDeceiver | Adversarial agent tests Judge decisions — detects when the Judge has been manipulated |

---

### Identity & Access

#### IA-1.4 — Scoped Tool Permissions

**Evidence strength: Moderate (2 incidents)**

| Incident | How IA-1.4 Helps |
|----------|-------------------|
| INC-02: Copilot RCE | Prevents agents from modifying IDE configuration files — even if injection succeeds, the agent can't write to settings.json |
| INC-08: MCP supply chain | Limits what each MCP server can access — poisoned server's blast radius is contained to its scoped permissions |

---

#### IA-2.6 — Secrets Exclusion from Context

**Evidence strength: Moderate (1 incident)**

| Incident | How IA-2.6 Helps |
|----------|-------------------|
| INC-03: Cursor IDE RCE | Configuration files with credentials are isolated from agent context — path traversal can't reach sensitive configuration |

---

### Data Protection

#### DP-1.1 — Data Classification Labels

**Evidence strength: Moderate (2 incidents)**

| Incident | How DP-1.1 Helps |
|----------|-------------------|
| INC-04: Perplexity data exfil | Classifies browsing session data and prevents cross-boundary transfer |
| INC-06: Samsung code leak | Classifies proprietary code as confidential and blocks external transmission |

---

#### DP-1.3 — Memory Isolation

**Evidence strength: Moderate (1 incident)**

| Incident | How DP-1.3 Helps |
|----------|-------------------|
| INC-06: Samsung code leak | Prevents context leakage between agent sessions — data shared with one session doesn't persist to others |

---

#### DP-2.1 — DLP on Message Bus

**Evidence strength: Strong (3 incidents)**

| Incident | How DP-2.1 Helps |
|----------|-------------------|
| INC-04: Perplexity data exfil | Detects sensitive data (PII, credentials, internal URLs) in inter-agent messages |
| INC-06: Samsung code leak | Detects code patterns in outbound messages to external providers |
| INC-07: Morris II worm | Detects anomalous content patterns in inter-agent communication — worm payloads differ from normal message patterns |

---

#### DP-2.2 — RAG Integrity with Freshness

**Evidence strength: Moderate (1 incident)**

| Incident | How DP-2.2 Helps |
|----------|-------------------|
| INC-05: PoisonedRAG | Validates document provenance and freshness metadata — poisoned documents without valid provenance are flagged |

---

### Execution Control

#### EC-1.1 — Human Approval for Write Operations

**Evidence strength: Strong (3 incidents)**

| Incident | How EC-1.1 Helps |
|----------|-------------------|
| INC-01: Auto-GPT crypto transfer | Human confirms all financial transactions — injection succeeds but transfer is blocked pending human approval |
| INC-06: Samsung code leak | Human reviews outbound data transfers — code submission to external AI caught at review step |
| INC-09: Banking AI fraud | All financial transactions require human confirmation — the most basic control for the most damaging outcome |

**Why this is non-negotiable for high-risk operations:** Three separate incidents across different domains (crypto, code IP, banking) would have been prevented by this single control. If your AI system can take actions with financial or legal consequences, human approval for writes is the minimum.

---

#### EC-1.2 — Tool Allow-Lists

**Evidence strength: Moderate (1 incident)**

| Incident | How EC-1.2 Helps |
|----------|-------------------|
| INC-01: Auto-GPT crypto transfer | Restricts wallet operations to explicitly approved task types — even if the agent is instructed to transfer, the tool isn't available for that task context |

---

#### EC-1.4 — Blast Radius Caps

**Evidence strength: Moderate (2 incidents)**

| Incident | How EC-1.4 Helps |
|----------|-------------------|
| INC-02: Copilot RCE | Limits scope of file modifications per agent — even if injection succeeds, the agent can only modify files within its scope |
| INC-04: Perplexity data exfil | Limits browsing agent's access to user session data — exfiltration scope is contained |

---

#### EC-1.5 — Interaction Timeout

**Evidence strength: Moderate (1 incident)**

| Incident | How EC-1.5 Helps |
|----------|-------------------|
| INC-07: Morris II worm | Caps propagation chains at maximum turn count — worm can't replicate indefinitely because agent interactions are bounded |

---

#### EC-2.5 — LLM-as-Judge Gate

**Evidence strength: Strong (5 incidents)**

The second most broadly validated control after input guardrails.

| Incident | How EC-2.5 Helps |
|----------|-------------------|
| INC-01: Auto-GPT crypto transfer | Independent evaluation flags unauthorised financial action before execution |
| INC-02: Copilot RCE | Flags settings.json modification as high-risk action inconsistent with coding task |
| INC-05: PoisonedRAG | Evaluates output quality and detects claims inconsistent with known facts (partial — depends on Judge's knowledge) |
| INC-09: Banking AI fraud | Independent evaluation of transaction legitimacy before execution |
| INC-10: JudgeDeceiver | This incident *attacks* the Judge — but hardened Judge with multiple criteria reduces single-point manipulation |

**Important caveat:** INC-10 demonstrates that the Judge itself can be attacked. EC-2.5 is critical but not sufficient alone — it needs to be paired with model diversity (PG-2.9), independent observability (OB-3.1), and for highest-risk decisions, multi-judge consensus (EC-3.1).

---

#### EC-2.6 — Decision Commit Protocol

**Evidence strength: Moderate (1 incident)**

| Incident | How EC-2.6 Helps |
|----------|-------------------|
| INC-09: Banking AI fraud | Committed transaction decisions cannot be reversed without human authorisation — prevents rapid-fire fraudulent transfers |

---

#### EC-3.1 — Multi-Judge Consensus

**Evidence strength: Moderate (1 incident)**

| Incident | How EC-3.1 Helps |
|----------|-------------------|
| INC-10: JudgeDeceiver | Multiple independent judges for high-risk decisions — attacker must bypass all judges simultaneously, which requires optimising against multiple unknown models |

---

### Observability

#### OB-2.1 — Anomaly Scoring

**Evidence strength: Moderate (2 incidents)**

| Incident | How OB-2.1 Helps |
|----------|-------------------|
| INC-04: Perplexity data exfil | Flags unusual data transfer patterns — browsing agent suddenly exfiltrating session data is anomalous |
| INC-09: Banking AI fraud | Flags unusual transaction patterns — rapid or large transfers that deviate from baseline |

---

#### OB-3.1 — Independent Observability Agent

**Evidence strength: Strong (3 incidents)**

| Incident | How OB-3.1 Helps |
|----------|-------------------|
| INC-07: Morris II worm | Detects anomalous communication patterns across the entire system — worm propagation creates observable spikes in inter-agent traffic |
| INC-09: Banking AI fraud | Separate monitoring agent with own model detects patterns invisible to individual agents |
| INC-10: JudgeDeceiver | Cross-checks Judge decisions using independent model — catches Judge manipulation that individual agents can't detect |

---

#### OB-3.2 — Circuit Breaker

**Evidence strength: Moderate (1 incident)**

| Incident | How OB-3.2 Helps |
|----------|-------------------|
| INC-07: Morris II worm | Kill switch terminates all agent communication — stops worm propagation system-wide when detected |

---

### Supply Chain

#### SC-1.1 — Component Inventory (AIBOM)

**Evidence strength: Moderate (1 incident)**

| Incident | How SC-1.1 Helps |
|----------|-------------------|
| INC-03: Cursor IDE RCE | Tracks all configuration sources and detects unauthorised changes — the path traversal attack modifies a tracked component |

---

#### SC-1.2 — Signed Tool Manifests

**Evidence strength: Moderate (1 incident)**

| Incident | How SC-1.2 Helps |
|----------|-------------------|
| INC-08: MCP supply chain | Verifies MCP server integrity before connection — unsigned or tampered servers are rejected |

---

#### SC-2.1 — AIBOM with Provider Mapping

**Evidence strength: Moderate (1 incident)**

| Incident | How SC-2.1 Helps |
|----------|-------------------|
| INC-06: Samsung code leak | Maps which data reaches which external provider — reveals the data exposure before it occurs |

---

#### SC-2.2 — MCP Server Vetting

**Evidence strength: Moderate (1 incident)**

| Incident | How SC-2.2 Helps |
|----------|-------------------|
| INC-08: MCP supply chain | Pre-approves MCP servers through a vetting process — denies connection to unsigned or unvetted servers |

---

#### SC-2.3 — Runtime Component Audit

**Evidence strength: Moderate (1 incident)**

| Incident | How SC-2.3 Helps |
|----------|-------------------|
| INC-08: MCP supply chain | Continuous verification of active MCP connections — detects if a previously vetted server has been compromised or swapped |

---

## Validation Coverage Map

### By MASO Domain

| Domain | Controls Validated | Total Controls | Coverage |
|--------|-------------------|----------------|----------|
| Prompt, Goal & Epistemic Integrity | 10 | 20 | 50% |
| Identity & Access | 2 | ~12 | ~17% |
| Data Protection | 5 | ~12 | ~42% |
| Execution Control | 8 | ~15 | ~53% |
| Observability | 3 | ~12 | 25% |
| Supply Chain | 4 | ~10 | 40% |

### What's Not Yet Validated

Controls in these categories are based on threat modelling and architectural reasoning, not observed incidents:

- **Epistemic integrity** (PG-2.4 consensus diversity gate, PG-2.8 assumption isolation) — These address the non-adversarial failure modes that emerge from multi-agent interaction. No public incident reports exist because organisations either aren't detecting them or aren't disclosing them. The threat model is strong ([Emerging Threats ET-02, ET-05](maso/threat-intelligence/emerging-threats.md)), but the evidence is research-based, not incident-based.

- **Advanced Identity & Access** (zero-trust agent credentials, non-human identity lifecycle) — These extend standard NHI patterns to AI agents. The patterns are proven in traditional service-to-service authentication; the extension to AI agents is logical but not yet documented in public incidents.

- **Tier 3 autonomous controls** (self-healing PACE, adversarial testing suites, independent kill switch) — These are designed for fully autonomous multi-agent systems, which are still rare in production. The controls are architecturally sound but won't be incident-validated until autonomous systems are common enough to be attacked.

---

## How This Page Evolves

This is a living document. As new AI security incidents are publicly disclosed:

1. They're added to the [Incident Tracker](maso/threat-intelligence/incident-tracker.md)
2. The control mappings on this page are updated
3. Controls that were "threat-modelled only" may be upgraded to "incident-validated"
4. New controls may be added if incidents reveal gaps

If you know of a public AI security incident not listed here, [open an issue](https://github.com/JonathanCGill/ai-runtime-behaviour-security/issues). We'll map it to controls and update both pages.

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
