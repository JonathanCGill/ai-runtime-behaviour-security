# Azure AI Implementation Patterns

> **Purpose:** Platform-specific guidance for implementing the infrastructure controls on Azure using Azure OpenAI Service and Azure AI Studio as the model hosting platforms.  
> **Status:** Reference patterns — adapt to your specific architecture and Azure subscription structure.

---

## Architecture Mapping

| Framework Zone | Azure Implementation |
|---------------|---------------------|
| **Zone 1 — Ingress** | Azure API Management (APIM) + Azure Front Door + Azure WAF |
| **Zone 2 — Runtime** | Azure OpenAI Service (inference), Azure AI Content Safety, Azure AI Search (vector read) |
| **Zone 3 — Evaluation** | Separate Azure OpenAI deployment (Judge) in isolated resource group/subscription |
| **Zone 4 — Ingestion** | Azure Functions / Azure Data Factory + Azure AI Search (vector write), Azure AI Document Intelligence |
| **Zone 5 — Control Plane** | Azure Key Vault, Azure Policy, Azure RBAC, Entra ID Privileged Identity Management |
| **Zone 6 — Logging** | Azure Monitor / Log Analytics, Azure Storage (log archive), Microsoft Sentinel |

---

## Identity & Access (IAM Controls)

### IAM-01/02: Authentication and Least Privilege

- Use **Entra ID (Azure AD)** for all identities — human and service.
- Azure OpenAI access via **Managed Identity** — no API key in application code.
- **Azure RBAC** custom roles: `Cognitive Services OpenAI User` (invoke only), `Cognitive Services OpenAI Contributor` (manage deployments).
- Use **Entra ID Conditional Access** for human access to control plane — MFA, compliant device, trusted location.

### IAM-03: Control/Data Plane Separation

- **Separate Azure subscriptions** for control plane and runtime.
- **Azure Policy** assignments prevent runtime subscriptions from modifying AI service configurations.
- Use **Entra ID Privileged Identity Management (PIM)** for just-in-time access to control plane roles.
- Azure OpenAI model deployment changes require PIM elevation — not available via runtime identity.

### IAM-04/05: Agent Tool Constraints

- Azure AI Agent Service supports **function definitions** — each function is a declared tool.
- Use **Azure Functions** with per-function Managed Identity scoped to specific backend APIs.
- Implement approval routing via **Azure Logic Apps** with human approval connector or **Power Automate** approval flow.
- **APIM policies** validate tool invocation requests at gateway layer.

### IAM-06: Session-Scoped Credentials

- Use **Entra ID workload identity federation** for session-bound token issuance.
- Token lifetime configured via **token lifetime policies** in Entra ID.
- **Managed Identity** credential rotation handled automatically by Azure.

---

## Logging & Observability (LOG Controls)

### LOG-01: Model I/O Logging

- Enable **Azure OpenAI diagnostic logging** to Log Analytics workspace.
- Capture: `RequestResponse` log category for full prompt/completion logging.
- **Important:** Azure OpenAI can log prompts and completions — enable only with PII handling in place.
- Use **Azure Monitor data collection rules** to route logs to appropriate destinations.

### LOG-02/03: Guardrail and Judge Logging

- **Azure AI Content Safety** API returns category scores and severity — log these with the request.
- Custom guardrail logic via **APIM policies** — log policy evaluation results.
- Judge invocations logged as separate Azure OpenAI calls to a distinct deployment.

### LOG-04: Agent Decision Chains

- Azure AI Agent Service supports **trace capture** for agent reasoning chains.
- Log agent steps (thought, action, observation) to Log Analytics with correlation IDs.
- Use **Application Insights** distributed tracing for end-to-end agent chain visibility.

### LOG-05/06: Drift and Injection Detection

- **Azure Monitor alerts** with dynamic thresholds for baseline deviation.
- **Log Analytics KQL queries** for prompt injection pattern detection.
- **Microsoft Sentinel** analytics rules for AI-specific detection logic.
- Custom workbooks in Azure Monitor for AI security dashboards.

### LOG-10: SIEM Integration

- **Microsoft Sentinel** as native SIEM — direct ingestion from Log Analytics.
- For third-party SIEM: use **Azure Event Hubs** export from Log Analytics.
- Sentinel **custom analytics rules** for AI incident detection (IR-02 triggers).

---

## Network & Segmentation (NET Controls)

### NET-01: Network Zones

- Use **Azure Virtual Networks (VNets)** with Network Security Groups (NSGs) for zone segmentation.
- Azure OpenAI access via **Private Endpoints** — no public internet exposure.
- **VNet service endpoints** or **Private Link** for Azure AI Search access.
- Separate VNets for runtime and ingestion with **VNet peering** only where required (vector store replication).

### NET-02: Guardrail Bypass Prevention

- Azure OpenAI **content filtering** is enabled by default on all deployments.
- For custom guardrails: implement in **APIM policies** — all requests route through APIM.
- **NSG rules** ensure Azure OpenAI private endpoint is only reachable from the APIM subnet.
- **Azure Policy** to deny Azure OpenAI deployments without content filtering.

### NET-03: Judge Isolation

- Judge Azure OpenAI deployment in a **separate resource group** with separate VNet.
- Communication via **Private Endpoint** from runtime VNet to Judge VNet (one-way).
- Alternatively, async evaluation via **Azure Service Bus** queue — runtime pushes evaluation data, Judge pulls.

### NET-04: Agent Egress Controls

- Agent compute runs in **VNet-integrated Azure Functions** (Premium plan).
- No default internet access — outbound via **Azure Firewall** with FQDN-based rules.
- **Azure Firewall application rules** implement the egress destination allowlist.
- **NSG flow logs** captured for cross-zone traffic monitoring (NET-08).

---

## Data Protection (DAT Controls)

### DAT-03: PII Detection

- **Azure AI Content Safety** for text moderation and category detection.
- **Azure AI Language** PII detection endpoint for NER-based PII identification.
- **APIM policies** can invoke PII detection as a pre/post-processing step on every request.
- Custom regex in APIM policy fragments for domain-specific PII.

### DAT-04: Access-Controlled RAG

- **Azure AI Search** supports security filters on search queries.
- Implement document-level access by adding security metadata fields at index time.
- Use **OData `$filter`** on search queries to restrict results to user's access level.
- Entra ID group membership maps to document classification metadata.

### DAT-05: Encryption

- Azure OpenAI data encrypted at rest with **Microsoft-managed keys** (default) or **customer-managed keys** (CMK) for Tier 3+.
- Azure AI Search supports **CMK encryption** for indexes.
- All Azure service communication over TLS 1.2.
- **Azure Storage** encryption with CMK for log archives.

---

## Secrets & Credentials (SEC Controls)

### SEC-01/03: Vault and Context Isolation

- **Azure Key Vault** for all AI system secrets.
- Access via **Managed Identity** — no credentials in application code or configuration.
- Key Vault **access policies** or **RBAC** restrict which identities can read which secrets.
- **Key Vault diagnostics** log all secret access for auditing.

### SEC-04: Credential Scanning

- **Microsoft Defender for Cloud** detects exposed secrets in code and configuration.
- **Azure DevOps credential scanner** in CI/CD pipelines.
- Custom APIM policies detect credential patterns in model I/O.

---

## Incident Response (IR Controls)

### IR-04: Rollback

- Azure OpenAI deployments are **versioned** — rollback by repointing to previous model version.
- APIM policy **revisions** — rollback guardrail policies to previous revision.
- Azure AI Search index **aliases** — point to previous known-good index.
- **Azure DevOps pipelines** with approval gates for all AI component deployments.

---

## Azure-Specific Considerations

| Consideration | Guidance |
|--------------|---------|
| **Content filtering** | Azure OpenAI has mandatory content filtering that can be modified via Azure AI Content Safety. Understand the default filters and supplement with custom rules. |
| **Responsible AI** | Azure requires Responsible AI use case approval for certain model capabilities. Factor this into SUP-02 model risk assessment. |
| **Data residency** | Azure OpenAI processes data in the region of deployment. Azure AI Content Safety may process in different regions — verify data residency requirements. |
| **Provisioned throughput** | For consistent performance, use provisioned throughput units (PTUs) — avoids token-based throttling that could affect guardrail latency. |
| **Entra ID integration** | Leverage Entra ID deeply — Conditional Access, PIM, and workload identity provide strong IAM-01 through IAM-06 implementation. |

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
