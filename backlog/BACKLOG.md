# Framework Backlog

> Items for future consideration. Not committed changes — open questions and potential enhancements.

## Source: Bornet et al. (March 2025) — SPAR Framework & Five-Level Agentic AI Progression Review

Reviewed against MASO and the AI Runtime Behaviour Security framework. Analysis date: March 2026.

Bornet et al. (572 pages, 27 co-authors) is a non-technical, business-leader-oriented playbook. Two core contributions: the SPAR Framework (Sense, Plan, Act, Reflect) as a capability model for evaluating agent behaviour, and a Five-Level Agentic AI Progression Framework (L0 manual → L5 fully autonomous) as a maturity taxonomy where higher isn't always better. Also covers memory architecture types (semantic, episodic, procedural), the "Agent Economy" concept, implementation pitfalls, and governance.

### Item 1: SPAR-Mapped Threat View

**Status:** Under consideration
**Effort:** Low — cross-reference table, no structural change
**Value:** High — bridges SPAR-familiar teams to MASO

SPAR is a capability model (what an agent does). MASO is a security control model (what must be secured). They are complementary. Each SPAR phase maps to MASO control domains:

| SPAR Phase | What It Covers | MASO Domain(s) That Secure It |
|---|---|---|
| **Sense** | Perception, input processing, context retrieval | Domain 0 (Prompt/Goal/Epistemic Integrity), Domain 2 (Data Protection — RAG integrity, memory poisoning) |
| **Plan** | Goal decomposition, strategy selection, delegation | Domain 0 (Goal integrity monitoring), Domain 3 (Execution Control — delegation contracts) |
| **Act** | Tool invocation, code execution, external calls | Domain 3 (Execution Control — sandboxing, parameter allow-lists), Domain 1 (Identity & Access — NHI, scoped credentials) |
| **Reflect** | Self-evaluation, error correction, learning | Domain 4 (Observability — drift detection, anomaly scoring), Domain 0 (Epistemic Integrity — hallucination amplification, uncertainty stripping) |

Novel insight: SPAR isn't just a capability model — it's a natural attack surface decomposition. Each phase has qualitatively different threat profiles. "Sense-phase attacks" (prompt injection, RAG poisoning), "Plan-phase attacks" (goal hijacking, delegation exploitation), "Act-phase attacks" (tool misuse, privilege escalation), "Reflect-phase attacks" (memory poisoning, drift concealment). Neither Bornet nor MASO currently use this framing.

### Item 2: Tier 3 Split — Rejected

**Status:** Rejected
**Rationale:** The distinction between "delegated" (L4) and "fully autonomous" (L5) is a narrative device for business audiences, not a meaningful security control boundary. Autonomy is effectively binary — the agent either has permission to act without prior human approval or it doesn't. Accountability remains with a human regardless. What changes between "delegated" and "autonomous" is review timing (sync vs async), which is a monitoring policy detail, not a tier boundary. MASO's existing Tier 2→3 jump already captures the real decision: do you require human approval before action, or don't you.

### Item 3: Agent Economy — Emerging Threat Entry

**Status:** Under consideration
**Effort:** Low — add entry to existing Emerging Threats register
**Value:** Medium — positions MASO ahead of the curve

The Agent Economy concept (agents as economic actors, inter-org agent interactions, agent marketplaces) is not currently addressed. When agents operate across organizational boundaries:

- Identity & Access (Domain 1) needs cross-org federation
- Supply Chain (Domain 5) needs inter-org trust chains
- Execution Control (Domain 3) needs billing/budget constraints as a control surface

Candidate for addition to `docs/maso/threat-intelligence/emerging-threats.md`.

### Item 4: Consolidated Governance Navigation

**Status:** Under consideration
**Effort:** Low-Medium — curation of existing content, not new controls
**Value:** Medium — serves the business-leader audience Bornet targets

MASO's operational governance is embedded throughout the framework (PACE escalation authorities, tier progression prerequisites, AI governance committee requirements). There is no single document that consolidates the operational governance model. A governance navigation doc would collect governance-relevant controls from across MASO into one reference — useful for the same audience Bornet targets.

Distinct from `docs/GOVERNANCE.md` which covers project governance (versioning, contributions).

### Item 5: Memory Control Type Labels

**Status:** Under consideration
**Effort:** Low — annotation to existing `docs/core/memory-and-context.md`
**Value:** Low-Medium — accessibility improvement

Explicitly label which memory type (semantic, episodic, procedural) each existing control in the memory & context doc protects. MASO already covers all three types with appropriate controls. The change is labelling, not content.

### Alignment Notes

**Strongest alignment:** Both frameworks share the principle that higher autonomy isn't always better. Bornet says it from a business strategy perspective; MASO says it from a security posture perspective. Together they make a compelling case from both angles.

**Bornet's implementation pitfalls** (workflow integration, error handling, agent control, data quality) map directly to existing MASO content: progression doc covers skip-step failures, PACE covers error handling, Execution Control covers agent control, and Data Reality covers data quality. MASO's coverage is more detailed. No new content needed — the value is positioning for audiences familiar with Bornet.

**Bornet's Five-Level model** maps approximately to MASO's progression (No AI → Assisted → Supported → Supervised → Autonomous) with the noted rejection of the L4/L5 split.
