# OWASP LLM Top 10 and Agentic Top 10 Mapping

> Maps infrastructure controls to the OWASP Top 10 for Large Language Model Applications (2025) and the OWASP Top 10 for Agentic AI.
>
> Part of the [AI Security Infrastructure Controls](../README.md) framework.
> Companion to [AI Runtime Behaviour Security](https://github.com/JonathanCGill/ai-runtime-behaviour-security).

---

## OWASP LLM Top 10 (2025)

### LLM01 — Prompt Injection

Manipulation of model behaviour through crafted inputs that override system instructions or extract sensitive information.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | LOG-06, NET-02, SEC-01, DAT-02 | Five-layer injection detection (LOG-06) identifies injection attempts. Network-enforced guardrail bypass prevention (NET-02) ensures all inputs transit guardrails. Credential isolation from context (SEC-01) removes high-value extraction targets. Data minimisation (DAT-02) reduces what can be extracted. |
| **Secondary** | LOG-01, LOG-02, DAT-03, DAT-06, NET-07 | I/O logging captures injection attempts for analysis. Guardrail decision logs track detection rates. PII redaction reduces extraction value. Response leakage prevention catches successful extraction. API gateway ensures single entry point. |
| **Agentic** | TOOL-02, TOOL-03, SAND-03 | Gateway enforcement (not agent self-enforcement) prevents injected tool invocations. Parameter constraints limit what injected commands can achieve. Network-restricted sandboxes prevent injected code from exfiltrating data. |

---

### LLM02 — Sensitive Information Disclosure

Model outputs that expose confidential data, PII, proprietary information, or system internals.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | DAT-03, DAT-06, SEC-01, DAT-02 | PII detection and redaction (DAT-03) on both inputs and outputs. Response leakage prevention (DAT-06) scans outputs for sensitive patterns. Credential exclusion from context (SEC-01) prevents credential disclosure. Data minimisation (DAT-02) limits what enters context. |
| **Secondary** | LOG-01, LOG-09, DAT-04, DAT-08 | I/O logging enables disclosure incident investigation. Log redaction prevents logs from becoming a secondary disclosure vector. Access-controlled RAG prevents unauthorised document retrieval. Evaluation data tokenisation protects data sent to Judge. |
| **Agentic** | SESS-02, DEL-01, SAND-02 | Session isolation prevents cross-session data leakage. Permission intersection prevents agents from accessing data via delegation. File system restrictions prevent sandbox code from reading sensitive files. |

---

### LLM03 — Supply Chain Vulnerabilities

Compromise of AI system components through malicious models, poisoned training data, compromised tools, or vulnerable dependencies.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SUP-01, SUP-02, SUP-03, SUP-04, SUP-05, SUP-06, SUP-07, SUP-08 | The entire supply chain control domain directly addresses this risk. Provenance verification (SUP-01), risk assessment (SUP-02), RAG integrity (SUP-03), fine-tuning security (SUP-04), tool auditing (SUP-05), safety model integrity (SUP-06), AI-BOM (SUP-07), and vulnerability monitoring (SUP-08). |
| **Secondary** | NET-05, SEC-08 | Ingestion/runtime separation prevents poisoned data from reaching models directly. Code scanning catches embedded malicious content. |

---

### LLM04 — Data and Model Poisoning

Intentional manipulation of training data or model weights to embed backdoors, biases, or degraded safety behaviour.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SUP-03, SUP-04, SUP-01, LOG-05 | RAG data source integrity (SUP-03) prevents poisoning through knowledge bases. Fine-tuning pipeline security (SUP-04) protects training processes. Provenance verification (SUP-01) detects model tampering. Drift detection (LOG-05) identifies behavioural changes that may indicate poisoning effects. |
| **Secondary** | NET-05, SUP-06, IAM-03, LOG-07 | Ingestion isolation separates data pipelines from runtime. Safety model integrity verification prevents poisoning of guardrails. Control plane separation protects model configurations. Log integrity prevents evidence tampering. |

---

### LLM05 — Improper Output Handling

Insufficient validation of model outputs before they are passed to downstream systems, enabling injection into those systems.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | DAT-06, LOG-02, NET-01 | Response leakage prevention (DAT-06) scans outputs before delivery. Guardrail decision logging (LOG-02) records output validation decisions. Zone architecture (NET-01) ensures outputs transit evaluation infrastructure. |
| **Secondary** | SAND-06, TOOL-03, DAT-03 | Code scanning before execution catches malicious generated code. Parameter constraints prevent injection via tool parameters. PII redaction applies to outputs. |
| **Agentic** | TOOL-02, TOOL-03, SAND-01, SAND-06 | Gateway enforcement validates tool invocations generated from model output. Parameter constraints prevent output-driven injection. Sandbox isolation contains generated code execution. Pre-execution scanning catches dangerous patterns. |

---

### LLM06 — Excessive Agency

Model or agent takes actions beyond what was intended or authorised, including unintended tool use, inappropriate parameter values, or actions exceeding scope.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | TOOL-01, TOOL-02, TOOL-03, TOOL-04, IAM-04, IAM-05 | Declared tool manifests (TOOL-01) define the boundary of permitted actions. Gateway enforcement (TOOL-02) makes the boundary real. Parameter constraints (TOOL-03) limit scope within permitted tools. Action classification (TOOL-04) routes high-impact actions to human approval. Agent tool constraints (IAM-04) and human approval routing (IAM-05) provide additional governance. |
| **Secondary** | TOOL-05, SESS-01, SESS-03, DEL-03 | Rate limiting prevents runaway behaviour. Session boundaries limit duration. Task scope constraints limit purpose. Delegation depth limits prevent recursive agency expansion. |

---

### LLM07 — System Prompt Leakage

Exposure of system prompts, instruction sets, or internal configuration through model outputs or side channels.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | IAM-03, NET-06, DAT-06, SEC-01 | Control/data plane separation (IAM-03) protects configuration from runtime access. Control plane network protection (NET-06) restricts access to system prompts. Response leakage prevention (DAT-06) scans for system prompt content in outputs. Credential isolation principles (SEC-01) extend to system prompt protection. |
| **Secondary** | LOG-06, DAT-02, SUP-06 | Injection detection catches attempts to extract system prompts. Data minimisation reduces what is included in system prompts. Safety model integrity ensures guardrails that prevent leakage are not themselves compromised. |

---

### LLM08 — Vector and Embedding Weaknesses

Attacks targeting vector databases and embedding pipelines, including embedding inversion, adversarial embedding injection, and retrieval manipulation.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SUP-03, DAT-04, NET-05, DAT-05 | RAG data source integrity (SUP-03) prevents injection of adversarial content into vector stores. Access-controlled RAG (DAT-04) enforces document-level permissions on retrieval. Ingestion/runtime separation (NET-05) isolates vector write paths from query paths. Encryption (DAT-05) protects embeddings at rest and in transit. |
| **Secondary** | LOG-01, DAT-01, SUP-07 | I/O logging captures retrieval context for investigation. Data classification at RAG boundaries identifies sensitive content. AI-BOM tracks vector database components. |

---

### LLM09 — Misinformation

Model generates factually incorrect, misleading, or fabricated information (hallucination) that is presented as authoritative.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | LOG-03, LOG-05, SUP-03 | Judge evaluation (LOG-03) provides a second opinion on output quality and factual consistency. Drift detection (LOG-05) identifies when hallucination rates increase beyond baseline. RAG data integrity (SUP-03) ensures the knowledge base contains accurate source material. |
| **Secondary** | LOG-01, DAT-06, IR-01 | I/O logging enables investigation of misinformation incidents. Output scanning can include factual consistency checks. AI-specific incident categories include misinformation events. |

---

### LLM10 — Unbounded Consumption

Resource exhaustion attacks where model or agent systems consume excessive compute, memory, storage, or API calls, causing denial of service or cost escalation.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | TOOL-05, SESS-01, SAND-04, NET-07 | Rate limiting per agent and per tool (TOOL-05) prevents invocation-based resource exhaustion. Session boundaries (SESS-01) limit total resource consumption per session. Resource limits on execution (SAND-04) cap compute and memory. API gateway (NET-07) provides a single throttling point. |
| **Secondary** | LOG-01, IR-02, IR-03 | I/O logging tracks consumption patterns. Detection triggers identify abnormal resource usage. Containment procedures include service isolation for resource exhaustion incidents. |

---

## OWASP Agentic AI Top 10

### AGT-01 — Agent Hijacking

Attacker takes control of an AI agent through prompt injection, system prompt manipulation, or context poisoning, redirecting the agent to serve the attacker's goals.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | LOG-06, TOOL-02, IAM-03, NET-02, SEC-01 | Injection detection (LOG-06) identifies hijack attempts. Gateway enforcement (TOOL-02) limits what a hijacked agent can do. Control plane separation (IAM-03) prevents runtime prompt modification. Bypass prevention (NET-02) ensures guardrails are always in the path. Credential isolation (SEC-01) removes high-value targets from context. |
| **Secondary** | SESS-01, TOOL-05, TOOL-01, SAND-03 | Session limits bound the duration of a hijacked session. Rate limits constrain the speed of malicious actions. Manifests limit available tools. Network-restricted sandboxes prevent exfiltration. |

---

### AGT-02 — Tool Misuse

Agent uses available tools in ways that were technically permitted but not intended, including chaining multiple tools to achieve unintended outcomes.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | TOOL-01, TOOL-02, TOOL-03, TOOL-04, TOOL-06 | Manifests define intended use. Gateway enforces boundaries. Parameter constraints limit scope. Action classification routes risky operations to review. Full logging enables detection of misuse patterns. |
| **Secondary** | LOG-04, SESS-03, TOOL-05 | Agent chain logging captures multi-tool sequences. Task scope limits purpose. Rate limiting prevents high-volume misuse. |

---

### AGT-03 — Privilege Escalation

Agent gains access to resources or capabilities beyond its authorised scope, either by exploiting delegation chains, impersonating other agents, or manipulating authorisation systems.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | DEL-01, DEL-05, IAM-02, IAM-04, TOOL-02 | Permission intersection (DEL-01) prevents escalation through delegation. User identity propagation (DEL-05) constrains all actions to user permissions. Least privilege (IAM-02) minimises starting permissions. Tool constraints (IAM-04) limit agent capabilities. Gateway enforcement (TOOL-02) prevents self-authorisation. |
| **Secondary** | DEL-03, DEL-04, IAM-06, IAM-08 | Depth limits reduce escalation paths. Explicit delegation authorisation prevents ad-hoc trust. Session-scoped credentials expire. Access auditing detects escalation. |

---

### AGT-04 — Insecure Tool Implementation

Tools available to agents have security vulnerabilities, including injection flaws, missing authentication, excessive permissions, or insecure defaults.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SUP-05, TOOL-02, TOOL-03, SEC-01, SEC-07 | Tool supply chain auditing (SUP-05) identifies insecure tools before deployment. Gateway enforcement (TOOL-02) mediates all tool calls. Parameter constraints (TOOL-03) prevent exploitation of vulnerable parameters. Credential isolation (SEC-01) and endpoint protection (SEC-07) secure tool authentication. |
| **Secondary** | SUP-08, TOOL-01, SEC-04 | Vulnerability monitoring tracks tool security issues. Manifests limit tool surface area. Credential scanning catches exposed tool credentials. |

---

### AGT-05 — Data Exfiltration Through Agents

Attacker uses agent tool access to extract sensitive data through permitted channels — reading files, querying databases, or calling APIs and routing results to external destinations.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | NET-04, DAT-06, TOOL-05, SAND-03, DAT-02 | Egress proxy (NET-04) controls where agents can send data. Response leakage prevention (DAT-06) scans outbound data. Rate limiting (TOOL-05) slows extraction. Network restrictions on sandboxes (SAND-03) prevent code-based exfiltration. Data minimisation (DAT-02) reduces what is available. |
| **Secondary** | TOOL-06, LOG-04, DAT-04, SAND-02 | Invocation logging captures extraction patterns. Agent chain logs reveal multi-step exfiltration. RAG access control limits document access. File system restrictions limit file access. |

---

### AGT-06 — Uncontrolled Delegation

Agent delegates tasks to other agents without proper authorisation, permission scoping, or audit trails, creating opaque chains of trust that bypass intended controls.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | DEL-01, DEL-02, DEL-03, DEL-04, DEL-05 | The entire delegation chain control domain directly addresses this risk. Permission intersection (DEL-01), audit trails (DEL-02), depth limits (DEL-03), explicit authorisation (DEL-04), and identity propagation (DEL-05). |
| **Secondary** | TOOL-02, IAM-04, LOG-04 | Gateway enforcement applies to delegation requests. Tool constraints carry through chains. Agent chain logging captures delegation events. |

---

### AGT-07 — Persistent Memory Poisoning

Attacker injects malicious content into agent memory, conversation history, or persistent state that influences future agent behaviour across sessions.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SAND-05, SESS-02, SESS-05, DAT-07 | Ephemeral environments (SAND-05) prevent persistent state. Session isolation (SESS-02) prevents cross-session contamination. Session cleanup (SESS-05) removes state on termination. Conversation history management (DAT-07) controls what persists. |
| **Secondary** | LOG-06, SUP-03, DAT-01 | Injection detection identifies poisoning attempts. RAG integrity prevents poisoning through knowledge bases. Data classification at boundaries identifies suspicious persistent content. |

---

### AGT-08 — Autonomous Action Without Oversight

Agent takes consequential real-world actions (financial transactions, communications, data modifications) without appropriate human review, either because oversight was not configured or was bypassed.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | IAM-05, TOOL-04, SESS-04 | Human approval routing (IAM-05) for high-impact actions. Action classification by reversibility (TOOL-04) determines which actions need human approval. Progressive trust (SESS-04) starts with restrictive permissions. |
| **Secondary** | TOOL-01, TOOL-02, SESS-01, DEL-03 | Manifests define the scope of autonomous action. Gateway enforces approval requirements. Session limits bound autonomous runtime. Delegation depth limits prevent deep autonomous chains. |

---

### AGT-09 — Inadequate Sandboxing

Agent-generated code executes with access to the host system, network, or persistent state, enabling system compromise, lateral movement, or persistent backdoors.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SAND-01, SAND-02, SAND-03, SAND-04, SAND-05, SAND-06 | The entire sandbox control domain directly addresses this risk. Isolation levels (SAND-01), file system restrictions (SAND-02), network restrictions (SAND-03), resource limits (SAND-04), ephemeral state (SAND-05), and pre-execution scanning (SAND-06). |
| **Secondary** | NET-01, LOG-04, TOOL-06 | Zone architecture places sandboxes in appropriate zones. Agent chain logs link code execution to agent reasoning. Tool invocation logs capture code execution context. |

---

### AGT-10 — Insufficient Logging and Monitoring

Agent actions, decisions, and tool invocations are not logged with sufficient detail to detect, investigate, or attribute incidents.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | TOOL-06, LOG-04, DEL-02, LOG-01, LOG-07 | Full tool invocation logging (TOOL-06). Agent chain reconstruction (LOG-04). Delegation chain audit trails (DEL-02). Model I/O logging (LOG-01). Log integrity protection (LOG-07). |
| **Secondary** | LOG-02, LOG-03, LOG-08, LOG-09, LOG-10 | Guardrail decision logging. Judge evaluation logging. Retention policies. PII redaction. SIEM correlation. |

---

## Control Coverage Summary

### OWASP LLM Top 10 — Primary Control Distribution

| Risk | Primary Controls |
|------|-----------------|
| LLM01 Prompt Injection | LOG-06, NET-02, SEC-01, DAT-02 |
| LLM02 Sensitive Information Disclosure | DAT-03, DAT-06, SEC-01, DAT-02 |
| LLM03 Supply Chain Vulnerabilities | SUP-01 through SUP-08 |
| LLM04 Data and Model Poisoning | SUP-03, SUP-04, SUP-01, LOG-05 |
| LLM05 Improper Output Handling | DAT-06, LOG-02, NET-01 |
| LLM06 Excessive Agency | TOOL-01 through TOOL-04, IAM-04, IAM-05 |
| LLM07 System Prompt Leakage | IAM-03, NET-06, DAT-06, SEC-01 |
| LLM08 Vector and Embedding Weaknesses | SUP-03, DAT-04, NET-05, DAT-05 |
| LLM09 Misinformation | LOG-03, LOG-05, SUP-03 |
| LLM10 Unbounded Consumption | TOOL-05, SESS-01, SAND-04, NET-07 |

### OWASP Agentic Top 10 — Primary Control Distribution

| Risk | Primary Controls |
|------|-----------------|
| AGT-01 Agent Hijacking | LOG-06, TOOL-02, IAM-03, NET-02, SEC-01 |
| AGT-02 Tool Misuse | TOOL-01 through TOOL-04, TOOL-06 |
| AGT-03 Privilege Escalation | DEL-01, DEL-05, IAM-02, IAM-04, TOOL-02 |
| AGT-04 Insecure Tool Implementation | SUP-05, TOOL-02, TOOL-03, SEC-01, SEC-07 |
| AGT-05 Data Exfiltration | NET-04, DAT-06, TOOL-05, SAND-03, DAT-02 |
| AGT-06 Uncontrolled Delegation | DEL-01 through DEL-05 |
| AGT-07 Persistent Memory Poisoning | SAND-05, SESS-02, SESS-05, DAT-07 |
| AGT-08 Autonomous Action Without Oversight | IAM-05, TOOL-04, SESS-04 |
| AGT-09 Inadequate Sandboxing | SAND-01 through SAND-06 |
| AGT-10 Insufficient Logging | TOOL-06, LOG-04, DEL-02, LOG-01, LOG-07 |

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
