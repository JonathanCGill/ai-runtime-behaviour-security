# Reference Architecture Worksheet

**A structured worksheet for composing framework controls into a coherent system architecture — without prescribing how.**

> *Part of [Templates](README.md) · [AI Runtime Behaviour Security](../../)*

---

## What This Worksheet Is

This is a thinking tool, not a blueprint.

The framework gives you controls, risk tiers, platform patterns, failure models, and cost budgets. This worksheet helps you **compose** those into a system architecture for your specific deployment — on your platform, within your constraints, for your risk appetite.

It does not recommend architectures. It asks the questions an architect needs to answer, in the order they typically need answering, and points to where in the framework each answer lives.

**What this is:** A structured sequence of decisions, with framework cross-references at each step.

**What this is not:** A reference architecture. There is no "right" answer to most of these questions — only answers that are appropriate for your context.

---

## Before You Start

You will need:

- Your system's **purpose and scope** (what it does, who uses it, what data it touches)
- Your organisation's **risk appetite** (or the ability to define one for this system)
- Your **platform constraints** (which cloud/infrastructure, latency budgets, cost limits)
- Familiarity with the framework's [Controls](../../core/controls.md) and [Risk Tiers](../../core/risk-tiers.md)

If you haven't classified the system yet, start with the [Cheat Sheet](../../quick-start/cheat-sheet.md). If you haven't threat-modelled it, use the [Threat Model Template](threat-model-template.md) first.

---

## Step 1: System Classification

*Framework reference: [Risk Tiers](../../core/risk-tiers.md) · [Cheat Sheet](../../quick-start/cheat-sheet.md)*

| Question | Your Answer |
|---|---|
| **System name** | |
| **What does it do?** (one sentence) | |
| **Who are the users?** (internal / external / both) | |
| **What data does it process?** (public / internal / confidential / regulated) | |
| **What decisions does it influence?** (informational / advisory / consequential / autonomous) | |
| **What's the blast radius of a bad output?** (inconvenience / operational impact / financial loss / safety risk / legal exposure) | |
| **Assigned risk tier** | ☐ Tier 1 &nbsp; ☐ Tier 2 &nbsp; ☐ Tier 3 |
| **Rationale for tier** | |

**Check yourself:** If this system were compromised tomorrow, what's the worst realistic outcome? Does your tier assignment reflect that?

---

## Step 2: Required Controls at Your Tier

*Framework reference: [Controls](../../core/controls.md) · [Cheat Sheet §2](../../quick-start/cheat-sheet.md)*

Based on your risk tier, identify which controls are required, optional, or not applicable.

### Control Layer Matrix

| Control Layer | Tier 1 Baseline | Tier 2 Baseline | Tier 3 Baseline | Your Decision |
|---|---|---|---|---|
| **Input guardrails** | Required | Required | Required | |
| **Output guardrails** | Recommended | Required | Required | |
| **LLM-as-Judge (sampled)** | Optional | Required | — | |
| **LLM-as-Judge (full, async)** | — | Option | Required | |
| **LLM-as-Judge (full, sync)** | — | — | Required | |
| **Human oversight (exception-based)** | Required | Required | Required | |
| **Human oversight (pre-release review)** | — | Option | Required | |
| **Circuit breaker** | Recommended | Required | Required | |
| **Usage logging** | Required | Required | Required | |
| **Decision chain audit** | — | Required | Required | |

*"Your Decision" column: state what you will implement, at what coverage level, and any deviations from baseline with rationale.*

### Agentic Controls (if applicable)

*Framework reference: [Agentic Controls](../../core/agentic.md)*

| Question | Your Answer |
|---|---|
| **Does the system use tools?** | ☐ Yes &nbsp; ☐ No |
| **Tool classification** (list each tool with action type) | Read: ___ / Write: ___ / Irreversible: ___ |
| **Confirmation gates** (which actions require human approval?) | |
| **Credential scoping** (per-session, per-tool, shared?) | |
| **Delegation depth** (for multi-agent: max chain length) | |

### Multi-Agent Controls (if applicable)

*Framework reference: [MASO Integration Guide](../../maso/integration/integration-guide.md)*

| Question | Your Answer |
|---|---|
| **Number of agents** | |
| **Trust model** (all same provider? mixed? cross-org?) | |
| **Message integrity** (how are inter-agent messages authenticated?) | |
| **Per-agent identity** (do agents have individual NHIs?) | |
| **Cross-agent DLP** (how is data boundary enforced between agents?) | |

---

## Step 3: Architecture Zone Mapping

*Framework reference: [Enterprise Architects](../../stakeholders/enterprise-architects.md) · Platform patterns: [AWS](../../infrastructure/reference/platform-patterns/aws-bedrock.md) · [Azure](../../infrastructure/reference/platform-patterns/azure-ai.md) · [Databricks](../../infrastructure/reference/platform-patterns/databricks.md)*

The framework identifies six architecture zones. For each zone, identify what services or components fulfil that function in your deployment.

| Zone | Function | Your Platform Components | Controls Placed Here |
|---|---|---|---|
| **1. Ingress** | Request entry, authentication, rate limiting, initial filtering | | |
| **2. Runtime** | Model inference, guardrails, retrieval (if RAG) | | |
| **3. Evaluation** | LLM-as-Judge, independent assessment | | |
| **4. Ingestion** | Data pipelines, knowledge base updates, document processing | | |
| **5. Control Plane** | Configuration, policy management, secrets, IAM | | |
| **6. Logging** | Audit trail, telemetry, SIEM integration | | |

### Key Architecture Decisions

For each, note your decision and rationale:

| Decision | Options (not recommendations) | Your Choice | Rationale |
|---|---|---|---|
| **Judge placement** | Same infrastructure as runtime / separate infrastructure / separate provider | | |
| **Judge timing** | Synchronous (blocks response) / Asynchronous (background) / Sampled | | |
| **Judge model** | Same model as task / different model same provider / different provider | | |
| **Guardrail execution** | In-process / sidecar / gateway-level / managed service | | |
| **Evaluation coverage** | 100% of traffic / sampled (specify %) / risk-based (specify criteria) | | |
| **Streaming handling** | Buffer full response before evaluation / partial evaluation / accept gap | | |
| **Human review routing** | Queue in existing workflow tool / dedicated review interface / email/notification | | |
| **Logging destination** | Existing SIEM / dedicated AI audit store / both | | |

---

## Step 4: Existing Infrastructure Mapping

*Framework reference: [Infrastructure Controls](../../infrastructure/) · [Enterprise Architects §existing infrastructure](../../stakeholders/enterprise-architects.md)*

Before designing new components, identify what you already have and what it covers.

| Existing Component | What It Already Covers | AI-Specific Gap |
|---|---|---|
| *e.g., API gateway* | *Authentication, rate limiting* | *No content-aware filtering, no semantic injection detection* |
| | | |
| | | |
| | | |
| | | |
| | | |

### Gap Analysis

For each AI-specific gap identified above:

| Gap | Framework Control(s) | How You'll Address It | Build / Buy / Configure |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |

---

## Step 5: Failure Topology

*Framework reference: [PACE Resilience](../../PACE-RESILIENCE.md) · [Enterprise Architects §PACE fail postures](../../stakeholders/enterprise-architects.md)*

For each control layer in your architecture, define what happens when it fails. These are **design-time decisions**, not operational procedures.

### Fail Posture by Control Layer

| Control Layer | Fail Posture | What Changes When This Layer Is Down | Trigger Condition |
|---|---|---|---|
| **Guardrails** | ☐ Fail-open &nbsp; ☐ Fail-closed | | |
| **LLM-as-Judge** | ☐ Fail-open &nbsp; ☐ Fail-closed | | |
| **Human oversight** | ☐ Fail-open &nbsp; ☐ Fail-closed | | |

### PACE Degradation Path

Define the four states for your system:

| PACE Phase | System State | What's Active | What's Degraded | Transition Trigger |
|---|---|---|---|---|
| **Primary** | Normal operation | | — | — |
| **Alternate** | Partial degradation | | | |
| **Contingency** | Significant degradation | | | |
| **Emergency** | Non-AI fallback | | | |

### Cascade Scenarios

Define what happens when multiple controls fail simultaneously:

| Scenario | System Response | Acceptable? |
|---|---|---|
| Guardrails down + Judge operational | | ☐ Yes &nbsp; ☐ No — mitigation: |
| Judge down + guardrails operational | | ☐ Yes &nbsp; ☐ No — mitigation: |
| Both guardrails and Judge down | | ☐ Yes &nbsp; ☐ No — mitigation: |
| Human review queue at capacity | | ☐ Yes &nbsp; ☐ No — mitigation: |

### Recovery Path

| From State | To State | What Must Be Verified Before Step-Up |
|---|---|---|
| Emergency → Contingency | | |
| Contingency → Alternate | | |
| Alternate → Primary | | |

---

## Step 6: Data Flow Mapping

*Framework reference: [Data Protection](../../extensions/technical/data-protection.md) · [Testing Guidance §upstream/downstream](testing-guidance.md)*

Trace where data enters, flows through, and exits your system.

### Data Flow Table

| Data Category | Source | Enters At (Zone) | Processed By | Stored Where | Exits To | Retention |
|---|---|---|---|---|---|---|
| **User input** | | | | | | |
| **Retrieved context** (if RAG) | | | | | | |
| **Model output** | | | | | | |
| **Evaluation results** (Judge) | | | | | | |
| **Conversation history** | | | | | | |
| **Audit/telemetry** | | | | | | |

### Sensitive Data Controls

| Data Type | Where It Appears | Protection Mechanism | What Happens If DLP Fails |
|---|---|---|---|
| PII | | | |
| Credentials/secrets | | | |
| Regulated data | | | |
| Proprietary/confidential | | | |

---

## Step 7: Latency and Cost Budget

*Framework reference: [Cost & Latency](../../extensions/technical/cost-and-latency.md) · [Enterprise Architects §cost and latency](../../stakeholders/enterprise-architects.md)*

| Budget Dimension | Your Constraint | Framework Baseline for Your Tier |
|---|---|---|
| **End-to-end latency (p50)** | | |
| **End-to-end latency (p99)** | | |
| **Evaluation cost per 1K transactions** | | |
| **Monthly evaluation budget** | | |
| **Expected transaction volume** | | |

### Cost Allocation

| Component | Added Latency | Cost per 1K Txn | Justification |
|---|---|---|---|
| Input guardrails | | | |
| Output guardrails | | | |
| LLM-as-Judge | | | |
| Logging/telemetry | | | |
| Human review (per escalation) | | | |
| **Total** | | | |

**Check yourself:** Does the total fit within your latency and cost constraints? If not, what trade-offs are you making, and are they acceptable at your tier?

---

## Step 8: Deployment-Specific Considerations

Answer only the sections relevant to your deployment type.

### If RAG

*Framework reference: [RAG Security](../../extensions/technical/rag-security.md)*

| Question | Your Answer |
|---|---|
| What is the document source? (internal, external, user-uploaded, mixed) | |
| How is the retrieval corpus protected from poisoning? | |
| Is retrieved content evaluated before it reaches the model? | |
| How do you handle citation/attribution? | |

### If Streaming

*Framework reference: [Streaming Controls](../../core/streaming-controls.md)*

| Question | Your Answer |
|---|---|
| How much of the response is buffered before evaluation? | |
| What happens if evaluation flags content mid-stream? | |
| How does partial output retraction work for your interface? | |

### If Multimodal

*Framework reference: [Multimodal Controls](../../core/multimodal-controls.md)*

| Question | Your Answer |
|---|---|
| Which modalities are inputs? (text, image, audio, video, file) | |
| Which modalities are outputs? | |
| What modality-specific evaluation exists for each? | |

---

## Step 9: Validation Checklist

Before considering the architecture complete, verify:

### Design Completeness

- [ ] Every required control at your tier has a component in the architecture
- [ ] Every control has a defined fail posture
- [ ] PACE degradation path is defined (all four phases)
- [ ] Recovery (step-back-up) path is defined
- [ ] Data flow is mapped end-to-end, including evaluation and audit data
- [ ] Latency and cost budgets are within constraints — or deviations are documented
- [ ] Existing infrastructure is mapped and gaps are identified
- [ ] Sensitive data controls are defined for every location where sensitive data appears

### Independence Checks

- [ ] Judge model is independent from task model (different model or different provider)
- [ ] Guardrail failure does not cascade to Judge failure (different failure domain)
- [ ] Circuit breaker operates at infrastructure layer, independent of AI stack
- [ ] Human review path functions when all automated controls are down
- [ ] Non-AI fallback path exists and has been verified

### Operational Readiness

- [ ] Logging captures enough to reconstruct any transaction end-to-end
- [ ] Alert routing is defined (who gets notified, when, through what channel)
- [ ] Escalation path is defined from automated alert through to incident response
- [ ] Testing plan exists for each PACE transition (see [Testing Guidance](testing-guidance.md))
- [ ] Human reviewers have been identified and briefed (roles, SLAs, tooling)

---

## What This Worksheet Produces

When complete, you should have:

1. **A system classification** with documented rationale
2. **A control selection** matched to your tier, with any deviations justified
3. **A zone-by-zone architecture** showing where controls live on your platform
4. **A gap analysis** showing what your existing infrastructure covers and what's new
5. **A failure topology** with defined PACE phases, fail postures, and recovery paths
6. **A data flow map** showing where sensitive data appears and how it's protected
7. **A cost/latency budget** confirming your controls fit within constraints

This is not a document to file. It's a set of decisions to implement. The architecture is complete when every question has an answer you can defend and every answer has a component in your design.

---

## Where to Go Next

| Next Step | Resource |
|---|---|
| Document the system | [Model Card Template](model-card-template.md) |
| Test the controls | [Testing Guidance](testing-guidance.md) |
| Build incident response | [Incident Playbook](ai-incident-playbook.md) |
| Platform-specific implementation | [AWS Bedrock](../../infrastructure/reference/platform-patterns/aws-bedrock.md) · [Azure AI](../../infrastructure/reference/platform-patterns/azure-ai.md) · [Databricks](../../infrastructure/reference/platform-patterns/databricks.md) |
| See a full transaction trace | [Runtime Telemetry Reference](../../extensions/technical/runtime-telemetry-reference.md) |

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
