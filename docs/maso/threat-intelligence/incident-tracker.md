# Incident Tracker

**Real-World AI Security Incidents Mapped to MASO Controls**

> Part of the [MASO Framework](../README.md) · Threat Intelligence
> Last updated: February 2026

---

## Purpose

This tracker maps publicly disclosed AI security incidents to MASO control domains, identifying which controls would have prevented, detected, or contained each incident. Every entry includes the attack vector, the multi-agent amplification risk (how the same attack would compound in a multi-agent system), and the specific MASO controls that address it.

Incidents are classified by the OWASP risk they exploit and the MASO tier at which controls would have been effective.

---

## Incident Register

### INC-01: Autonomous Agent Crypto Transfer (March 2024)

**What happened:** Researchers demonstrated that an Auto-GPT agent with cryptocurrency wallet access could be tricked into transferring funds to attacker addresses via indirect prompt injection hidden in email content. The agent processed a newsletter containing embedded instructions and initiated an unauthorised wallet transfer.

**Attack vector:** Indirect prompt injection via email content → tool execution (wallet transfer)

**OWASP mapping:** LLM01 (Prompt Injection), LLM06 (Excessive Agency), ASI02 (Unrestricted Tool Access)

**Multi-agent amplification:** In a multi-agent system, a compromised email-processing agent could pass poisoned instructions to a financial-execution agent through the message bus. The execution agent would treat the instructions as legitimate delegated tasks, with no independent verification of the original source.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| PG-1.1 Input guardrails per agent | Prompt & Goal Integrity | Block injection at email agent boundary |
| PG-1.4 Message source tagging | Prompt & Goal Integrity | Tag email-derived content as untrusted data, not instruction |
| EC-1.2 Tool allow-lists | Execution Control | Restrict wallet operations to explicitly approved task types |
| EC-2.5 LLM-as-Judge gate | Execution Control | Independent evaluation before financial execution |
| EC-1.1 Human approval for write operations | Execution Control | Human confirms all transfers at Tier 1 |

**Minimum effective tier:** Tier 1 (human approval for writes prevents execution; Tier 2 Judge gate catches it automatically)

---

### INC-02: GitHub Copilot RCE — CVE-2025-53773 (2025)

**What happened:** An attacker embedded prompt injection in public repository code comments. When a developer opened the repository with Copilot active, the injected prompt instructed Copilot to modify `.vscode/settings.json` to enable YOLO mode (auto-approve all commands). Subsequent commands executed without user approval, achieving arbitrary code execution on the developer's machine.

**Attack vector:** Indirect prompt injection via code comments → configuration modification → RCE

**OWASP mapping:** LLM01 (Prompt Injection), LLM05 (Improper Output Handling), ASI02 (Unrestricted Tool Access)

**Multi-agent amplification:** In a multi-agent coding system, a code-review agent processing the poisoned repository could pass the injected instructions to a code-generation agent, which could then modify configuration files across multiple developer environments simultaneously. The blast radius scales with the number of agents consuming the same repository.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| PG-1.1 Input guardrails per agent | Prompt & Goal Integrity | Detect injection patterns in code comments |
| PG-1.2 System prompt isolation | Prompt & Goal Integrity | Prevent external content from overriding agent instructions |
| EC-1.4 Blast radius caps | Execution Control | Limit scope of file modifications per agent |
| EC-2.5 LLM-as-Judge gate | Execution Control | Flag settings.json modification as high-risk action |
| IA-1.4 Scoped tool permissions | Identity & Access | Prevent agents from modifying IDE configuration |

**Minimum effective tier:** Tier 1 (tool scoping prevents settings modification; blast radius caps contain damage)

---

### INC-03: Cursor IDE Agentic RCE — CVE-2025-59944 (2025)

**What happened:** A case-sensitivity bug in a protected file path allowed an attacker to influence Cursor's agentic behaviour. The agent read the wrong configuration file containing hidden instructions, which escalated into remote code execution. The root cause was that the agent trusted unverified external content and treated it as authoritative.

**Attack vector:** Path traversal via case sensitivity → configuration poisoning → RCE

**OWASP mapping:** LLM01 (Prompt Injection), ASI01 (Agent Goal Hijack), ASI02 (Unrestricted Tool Access)

**Multi-agent amplification:** A configuration-poisoning attack in a multi-agent system could compromise the orchestrator's task definitions, redirecting all downstream agents. If the orchestrator reads poisoned configuration, every agent it spawns inherits the attacker's instructions.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| PG-1.3 Immutable task specification | Prompt & Goal Integrity | Task definitions cannot be modified by external content |
| PG-2.2 Goal integrity monitoring | Prompt & Goal Integrity | Detect deviation from original task objectives |
| SC-1.1 Component inventory (AIBOM) | Supply Chain | Track all configuration sources; detect unauthorised changes |
| IA-2.6 Secrets exclusion from context | Identity & Access | Configuration files with credentials isolated from agent context |

**Minimum effective tier:** Tier 2 (goal integrity monitoring detects the deviation; immutable task specs prevent it)

---

### INC-04: Perplexity Comet Browser Agent Data Exfiltration (2024–2025)

**What happened:** Researchers demonstrated that Perplexity's AI-powered browser agent could be manipulated through prompt injection in web page content to exfiltrate sensitive data from the user's browsing session. The agent processed web content containing hidden instructions and followed them.

**Attack vector:** Indirect prompt injection via web content → data exfiltration through agent browsing actions

**OWASP mapping:** LLM01 (Prompt Injection), LLM02 (Sensitive Information Disclosure), ASI04 (Inadequate Sandboxing)

**Multi-agent amplification:** A browsing agent in a multi-agent system could exfiltrate data and pass it to other agents through the message bus. If the exfiltrated data includes credentials or internal URLs, downstream agents could use them to access additional systems.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| DP-1.1 Data classification labels | Data Protection | Classify browsing data; prevent cross-boundary transfer |
| DP-2.1 DLP on message bus | Data Protection | Detect sensitive data in inter-agent messages |
| EC-1.4 Blast radius caps | Execution Control | Limit browsing agent's access to user session data |
| OB-2.1 Anomaly scoring | Observability | Flag unusual data transfer patterns |

**Minimum effective tier:** Tier 1 (data classification prevents exfiltration; DLP catches it at the bus)

---

### INC-05: PoisonedRAG — Knowledge Base Contamination (2024)

**What happened:** Researchers demonstrated that adding just 5 malicious documents to a corpus of millions caused the targeted AI to return attacker-desired false answers 90% of the time for specific trigger queries. The poisoning was undetectable because the AI was technically performing retrieval correctly — the retrieved content itself was compromised.

**Attack vector:** Data poisoning via RAG corpus → misinformation delivery

**OWASP mapping:** LLM04 (Data and Model Poisoning), LLM08 (Vector and Embedding Weaknesses), LLM09 (Misinformation)

**Multi-agent amplification:** This is where multi-agent dynamics make the attack dramatically worse. A research agent retrieves poisoned data. An analysis agent synthesises it into a report. A presentation agent formats it for stakeholders. By the third agent, the poisoned claim has been cited, elaborated, and presented with high confidence. No agent in the chain has independent verification capability. This is exactly the epistemic failure mode MASO's Prompt, Goal & Epistemic Integrity domain was designed to address.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| DP-2.2 RAG integrity with freshness | Data Protection | Validate document provenance and freshness metadata |
| PG-2.5 Claim provenance enforcement | Prompt & Goal Integrity | Unverified agent claims cannot be treated as facts |
| PG-2.6 Self-referential evidence prohibition | Prompt & Goal Integrity | Agents cannot cite other agents' output as primary evidence |
| PG-2.7 Uncertainty preservation | Prompt & Goal Integrity | Confidence scores propagate through chain; don't inflate |
| PG-3.5 Challenger agent | Prompt & Goal Integrity | Adversarial agent attacks primary hypothesis |

**Minimum effective tier:** Tier 2 (provenance enforcement and uncertainty preservation catch the propagation; Tier 3 challenger agent provides active defence)

---

### INC-06: Samsung Confidential Code Leak via ChatGPT (2023)

**What happened:** Samsung engineers pasted proprietary source code into ChatGPT for debugging assistance, leaking confidential intellectual property. Samsung subsequently banned internal use of external AI tools. Similar incidents were reported at JPMorgan, Goldman Sachs, and other financial institutions.

**Attack vector:** User error / policy violation → data exfiltration to external AI provider

**OWASP mapping:** LLM02 (Sensitive Information Disclosure), ASI06 (Inadequate Data Controls)

**Multi-agent amplification:** In a multi-agent system with external model providers, data shared with one agent's model provider is effectively shared with all agents using that provider. If Agent A sends proprietary code to Provider X for analysis, and Agent B also uses Provider X, the data boundary has been breached at the provider level even if inter-agent controls are perfect.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| DP-1.1 Data classification labels | Data Protection | Classify code as confidential; block external transmission |
| DP-2.1 DLP on message bus | Data Protection | Detect code patterns in outbound messages |
| DP-1.3 Memory isolation | Data Protection | Prevent context leakage between agent sessions |
| SC-2.1 AIBOM with provider mapping | Supply Chain | Know which data reaches which external provider |

**Minimum effective tier:** Tier 1 (data classification and DLP prevent the leak)

---

### INC-07: AI Worm Proof-of-Concept — Morris II (February 2025)

**What happened:** Researchers demonstrated a self-replicating AI worm that spread between autonomous agents through prompt injection. The worm injected itself into AI-generated content. When a compromised agent communicated with another through email or chat, hidden instructions in the message infected the receiving agent, which then propagated the worm to other agents it communicated with.

**Attack vector:** Self-replicating prompt injection via inter-agent communication → cascading compromise

**OWASP mapping:** LLM01 (Prompt Injection), ASI01 (Agent Goal Hijack), ASI03 (Insecure Agent Communication), ASI08 (Agent Memory Poisoning)

**Multi-agent amplification:** This attack is inherently multi-agent. It cannot exist in a single-agent system. The worm exploits the communication channel between agents — exactly the inter-agent message bus that MASO treats as a first-class security control point. Every agent in the chain becomes both victim and vector.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| PG-1.1 Input guardrails per agent | Prompt & Goal Integrity | Detect injection patterns in incoming messages |
| PG-2.1 Inter-agent injection detection | Prompt & Goal Integrity | Judge evaluates all inter-agent messages for injection |
| PG-1.4 Message source tagging | Prompt & Goal Integrity | Distinguish instruction from data in messages |
| EC-1.5 Interaction timeout | Execution Control | Cap propagation chains at max turn count |
| OB-3.1 Independent observability agent | Observability | Detect anomalous communication patterns across the system |
| OB-3.2 Circuit breaker | Observability | Kill switch terminates all agent communication |

**Minimum effective tier:** Tier 2 (inter-agent injection detection + Judge gate blocks propagation; Tier 3 independent observability agent detects system-wide anomaly)

---

### INC-08: MCP Server Supply Chain Attacks (2025)

**What happened:** Multiple reports documented vulnerabilities in Model Context Protocol (MCP) servers, including the Toxic Agent Flow exploit in GitHub's MCP server. Attackers exploited MCP tool descriptions and resource listings to inject instructions that influenced model behaviour. With tens of thousands of MCP servers published online, the supply chain attack surface expanded rapidly.

**Attack vector:** Poisoned MCP tool metadata → indirect prompt injection → unauthorised actions

**OWASP mapping:** LLM03 (Supply Chain Vulnerabilities), LLM01 (Prompt Injection), ASI02 (Unrestricted Tool Access)

**Multi-agent amplification:** Multi-agent systems consume multiple MCP servers — one per specialist agent is a common pattern. A single poisoned MCP server can compromise the agent that uses it, which then becomes a vector for poisoning other agents through the message bus. The supply chain risk scales multiplicatively with the number of MCP integrations.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| SC-1.2 Signed tool manifests | Supply Chain | Verify MCP server integrity before connection |
| SC-2.2 MCP server vetting | Supply Chain | Pre-approve MCP servers; deny unsigned/unvetted |
| SC-2.3 Runtime component audit | Supply Chain | Continuous verification of active MCP connections |
| PG-1.1 Input guardrails per agent | Prompt & Goal Integrity | Filter injection from MCP tool responses |
| IA-1.4 Scoped tool permissions | Identity & Access | Limit what each MCP server can access |

**Minimum effective tier:** Tier 2 (signed manifests + vetting + runtime audit provide defence in depth)

---

### INC-09: Financial Services AI Banking Assistant Fraud (June 2025)

**What happened:** Attackers sent crafted messages through a banking app's AI chat interface that tricked the AI into bypassing transaction verification steps. The AI approved fraudulent transfers because the attacker's instructions overrode the normal security protocols. The company lost approximately $250,000 before detecting the attack.

**Attack vector:** Direct prompt injection via chat → security bypass → fraudulent transactions

**OWASP mapping:** LLM01 (Prompt Injection), LLM06 (Excessive Agency), ASI09 (Inadequate Human Oversight)

**Multi-agent amplification:** In a multi-agent banking system, a compromised customer-facing agent could delegate fraudulent transactions to a back-office execution agent, using legitimate delegation channels. The execution agent would see a properly formatted request from an authorised agent — the fraud would be invisible at the execution layer.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| EC-1.1 Human approval for write operations | Execution Control | All financial transactions require human confirmation |
| EC-2.5 LLM-as-Judge gate | Execution Control | Independent evaluation of transaction legitimacy |
| EC-2.6 Decision commit protocol | Execution Control | Committed decisions cannot be reversed without human auth |
| PG-1.1 Input guardrails per agent | Prompt & Goal Integrity | Detect injection patterns in customer messages |
| OB-2.1 Anomaly scoring | Observability | Flag unusual transaction patterns |

**Minimum effective tier:** Tier 1 (human approval for writes is the minimum — no AI should autonomously approve financial transactions without it)

---

### INC-10: LLM-as-Judge Manipulation — JudgeDeceiver (2024–2025)

**What happened:** Researchers demonstrated JudgeDeceiver, an optimisation-based attack that injects a crafted sequence into a candidate response such that an LLM-as-Judge selects the attacker's response regardless of quality. This has implications for LLM-powered search ranking, reinforcement learning with AI feedback, and tool selection systems.

**Attack vector:** Adversarial optimisation → Judge manipulation → compromised evaluation

**OWASP mapping:** LLM01 (Prompt Injection), ASI07 (Insecure AI Evaluation)

**Multi-agent amplification:** If the Judge layer itself is compromised, every control that depends on Judge evaluation is bypassed simultaneously. In MASO, the Judge gate (EC-2.5) is a critical control point — manipulating it undermines execution control, goal integrity monitoring, and output validation across the entire multi-agent system.

**MASO controls that address this:**

| Control | Domain | Effect |
|---------|--------|--------|
| EC-2.5 LLM-as-Judge gate (hardened) | Execution Control | Multiple judge criteria reduce single-point manipulation |
| PG-2.9 Model diversity policy | Prompt & Goal Integrity | Judge uses different model/provider than task agents |
| OB-3.1 Independent observability agent | Observability | Separate monitoring agent with own model; cross-checks Judge |
| PG-3.5 Challenger agent | Prompt & Goal Integrity | Adversarial agent tests Judge decisions |
| EC-3.1 Multi-judge consensus | Execution Control | Multiple independent judges for high-risk decisions |

**Minimum effective tier:** Tier 3 (defending the Judge requires model diversity, independent observability, and challenger agents — this is an advanced threat)

---

## Incident Statistics

| Category | Count | Most Common OWASP Risk |
|----------|-------|----------------------|
| Prompt injection (direct + indirect) | 6 | LLM01 |
| Data exfiltration / disclosure | 3 | LLM02 |
| Supply chain compromise | 2 | LLM03 |
| Knowledge base poisoning | 1 | LLM04 |
| Tool/agency abuse | 4 | LLM06 / ASI02 |
| Judge/evaluation manipulation | 1 | ASI07 |

**Most referenced MASO controls across all incidents:**

| Control | Incidents Addressed |
|---------|-------------------|
| PG-1.1 Input guardrails per agent | 8/10 |
| EC-2.5 LLM-as-Judge gate | 5/10 |
| EC-1.1 Human approval for writes | 3/10 |
| DP-2.1 DLP on message bus | 3/10 |
| OB-3.1 Independent observability agent | 3/10 |

---

## How to Use This Tracker

**For risk assessments:** Reference specific incidents when justifying control investments. Each incident includes the MASO controls that would have prevented or contained it.

**For red team planning:** Use the attack vectors as starting points for testing your multi-agent system against known real-world patterns. See the [Red Team Playbook](../red-team/red-team-playbook.md) for structured test scenarios.

**For executive briefings:** The incident statistics and dollar-value losses (INC-09: $250K) provide concrete evidence for security investment decisions.

**For control gap analysis:** If your deployment lacks any control referenced in the "MASO controls that address this" column, you have a known exposure to a real-world attack pattern.
---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
