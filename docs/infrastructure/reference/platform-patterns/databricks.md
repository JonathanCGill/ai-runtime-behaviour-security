# Databricks Implementation Patterns

> **Purpose:** Platform-specific guidance for implementing the infrastructure controls on Databricks using Model Serving, Mosaic AI Gateway, and Unity Catalog as the AI platform.  
> **Status:** Reference patterns — adapt to your specific workspace architecture and cloud provider.

---

## Architecture Mapping

| Framework Zone | Databricks Implementation |
|---------------|--------------------------|
| **Zone 1 — Ingress** | Mosaic AI Gateway + cloud provider load balancer/WAF |
| **Zone 2 — Runtime** | Model Serving endpoints, Mosaic AI Guardrails, Vector Search (read), Mosaic AI Agent Framework |
| **Zone 3 — Evaluation** | Separate Model Serving endpoint (Judge) or Mosaic AI Agent Evaluation |
| **Zone 4 — Ingestion** | Delta Live Tables / Databricks Jobs + Vector Search (write), Document ingestion pipelines |
| **Zone 5 — Control Plane** | Unity Catalog (governance), Workspace Admin Console, Databricks Secrets |
| **Zone 6 — Logging** | Inference Tables, System Tables, Unity Catalog audit logs, lakehouse SIEM integration |

---

## Identity & Access (IAM Controls)

### IAM-01/02: Authentication and Least Privilege

- Use **Unity Catalog** for fine-grained access control across all data and AI assets.
- Model Serving endpoints authenticated via **Databricks PATs**, **OAuth M2M**, or **service principals**.
- **Unity Catalog privileges** control who can: query models (EXECUTE), manage endpoints (MANAGE), register models (CREATE MODEL).
- Use **Databricks service principals** for all automated AI system identities — not user PATs.

### IAM-03: Control/Data Plane Separation

- **Unity Catalog metastore** is the control plane for data governance — separate from compute.
- Use **workspace-level isolation** — control plane workspace separate from runtime workspace.
- Model registration in Unity Catalog requires specific privileges — runtime invoke does not grant registration/modification rights.
- **Account-level groups** for control plane administrators, managed via IdP federation.

### IAM-04/05: Agent Tool Constraints

- **Mosaic AI Agent Framework** defines tools as Python functions with specific schemas.
- Use **Unity Catalog functions** to register tools — access controlled by Unity Catalog privileges.
- Implement tool authorization via **custom middleware** in the agent serving code that validates tool calls against a manifest before execution.
- Human approval routing via external workflow system (e.g., Databricks Jobs with manual approval task).

### IAM-06: Session-Scoped Credentials

- Use **Databricks OAuth M2M** tokens with short expiry for service-to-service auth.
- Agent sessions should use **per-request token exchange** rather than long-lived tokens.
- Secrets API credentials accessed via **Databricks Secrets** scope — mounted at runtime, not stored in notebooks.

---

## Logging & Observability (LOG Controls)

### LOG-01: Model I/O Logging

- **Inference Tables** automatically capture all model serving requests and responses.
- Inference Tables stored as Delta tables — queryable via SQL, integrated with Unity Catalog governance.
- Schema includes: request timestamp, input payload, output payload, endpoint name, model version, latency.
- **Important:** Inference Tables capture full payloads — apply PII handling (LOG-09) downstream.

### LOG-02/03: Guardrail and Judge Logging

- **Mosaic AI Gateway guardrails** log safety filter decisions as part of the gateway trace.
- Custom guardrail logic can log to a **dedicated Delta table** with guardrail decision schema.
- Judge evaluations logged to a **separate Delta table** with evaluation scores, verdicts, and reasoning.
- Use **Mosaic AI Agent Evaluation** for systematic Judge evaluation logging.

### LOG-04: Agent Decision Chains

- **MLflow Tracing** captures agent execution traces: LLM calls, tool invocations, retriever calls.
- Traces stored as structured data — queryable for forensic reconstruction.
- Enable tracing on agent endpoints: traces logged to inference tables alongside I/O.

### LOG-05/06: Drift and Injection Detection

- **Databricks Lakehouse Monitoring** for model serving metrics (latency, throughput, error rates).
- Custom monitoring via **scheduled Databricks Jobs** that query inference tables for:
  - Guardrail block rate changes
  - Response length distribution shifts
  - Token consumption anomalies
  - Prompt injection pattern matching (regex on inference table inputs)
- **Alerts** via Databricks SQL Alerts or integration with PagerDuty/Slack.

### LOG-10: SIEM Integration

- **System Tables** provide audit logs for workspace-level events.
- Inference Tables and custom log tables accessible via **Delta Sharing** for SIEM ingestion.
- Export to cloud-native SIEM (Sentinel, Security Lake, Chronicle) via **Delta Live Tables** streaming to cloud storage.
- **Unity Catalog audit logs** feed into SIEM for access pattern analysis.

---

## Network & Segmentation (NET Controls)

### NET-01: Network Zones

- Databricks workspaces deploy in **customer-managed VPCs/VNets** — configure security groups per zone.
- Model Serving endpoints support **Private Link** for private network access.
- **Serverless compute** for Model Serving runs in Databricks-managed infrastructure — use Private Link for network isolation.
- Separate workspaces for ingestion and runtime with distinct network configurations.

### NET-02: Guardrail Bypass Prevention

- **Mosaic AI Gateway** sits in front of model endpoints — all requests route through it.
- Configure guardrails as **AI Gateway policies** — applied at the gateway level, not the model level.
- Network configuration ensures model serving endpoints are only reachable via the gateway (Private Link + security groups).

### NET-03: Judge Isolation

- Judge model served on a **separate Model Serving endpoint** with separate compute.
- Evaluation data pushed to Judge via **Delta table** — Judge reads from table, writes evaluations back.
- No direct network path from Judge to runtime model endpoint.

### NET-04: Agent Egress Controls

- Agent code runs in **serverless compute** or **cluster compute** — network egress controlled by workspace network configuration.
- Use cloud-native egress controls (AWS Security Groups / Azure NSGs) for outbound destination restriction.
- **Unity Catalog external connections** control which external data sources agents can access.

---

## Data Protection (DAT Controls)

### DAT-03: PII Detection

- Custom PII detection via **Databricks SQL UDFs** or **Python UDFs** applied to inference tables.
- Integrate cloud PII services (Comprehend, AI Language) via **external function** calls.
- **Mosaic AI Gateway** supports custom payload validation that can include PII scanning.

### DAT-04: Access-Controlled RAG

- **Vector Search** endpoints support filtered search with metadata predicates.
- Document-level access control via Unity Catalog — documents carry access metadata from ingestion.
- **Pre-filter** vector search queries with user permission metadata before similarity ranking.
- Unity Catalog **row-level security** can be applied to source documents before embedding.

### DAT-05: Encryption

- Delta tables encrypted at rest by default (cloud provider encryption).
- **Customer-managed keys** supported via cloud KMS integration for Tier 3+.
- All Databricks API communication over TLS 1.2.
- Vector Search indexes encrypted with workspace encryption settings.

---

## Secrets & Credentials (SEC Controls)

### SEC-01/03: Vault and Context Isolation

- **Databricks Secrets** for AI system credentials — scoped by workspace and access control list.
- Secrets accessed via `dbutils.secrets.get()` — never displayed in notebook outputs (redacted automatically).
- For cross-workspace secrets, use cloud-native vault (AWS Secrets Manager, Azure Key Vault) accessed via **external connections**.
- Agent tool credentials stored in secrets scopes, injected at runtime by middleware, never in model context.

### SEC-08: Code Scanning

- **Databricks notebooks** support version control via **Repos** — integrate with CI/CD scanning.
- Use pre-commit hooks on the Git repository backing Databricks Repos for credential scanning.

---

## Supply Chain (SUP Controls)

### SUP-01: Model Provenance

- **Unity Catalog model registry** provides model versioning, lineage, and provenance tracking.
- Model versions linked to: training run (MLflow), training data (Delta table lineage), deployer identity.
- **Model signatures** define expected input/output schemas — validate at serving time.

### SUP-07: AI-BOM

- Unity Catalog provides a natural inventory: models, endpoints, functions, connections, data assets.
- **MLflow model metadata** tracks: framework, dependencies, environment, creation timestamp.
- **Unity Catalog lineage** shows data-to-model-to-endpoint relationships.

---

## Incident Response (IR Controls)

### IR-04: Rollback

- Model Serving endpoints support **traffic routing** between model versions — instant rollback by shifting traffic.
- Unity Catalog model versions are immutable — previous versions always available.
- Vector Search indexes can be rebuilt from Delta table source data.
- **Databricks Jobs** with approval gates (webhook-based) for deployment automation.

---

## Databricks-Specific Considerations

| Consideration | Guidance |
|--------------|---------|
| **Unity Catalog** | Unity Catalog is the backbone of Databricks governance. Leverage it as the primary control for IAM-01, IAM-02, DAT-04, SUP-01, and SUP-07 rather than building parallel systems. |
| **Inference Tables** | Inference Tables are Delta tables — they inherit all Delta Lake capabilities (ACID, time travel, schema enforcement). Use time travel for forensic investigation and schema enforcement for log integrity. |
| **Serverless vs. Classic compute** | Serverless Model Serving provides faster scaling but limited network customisation. Classic compute offers full VPC control. Choose based on NET-01 requirements per risk tier. |
| **MLflow integration** | MLflow is deeply integrated — use it for model tracking, experiment logging, and trace capture rather than building custom logging. |
| **Multi-cloud** | Databricks runs on AWS, Azure, and GCP. The Databricks-layer controls (Unity Catalog, AI Gateway) are consistent across clouds, but network controls (NET-01 through NET-08) use cloud-specific primitives. |
| **Mosaic AI Gateway** | AI Gateway provides built-in rate limiting, guardrails, and usage tracking. Configure these as the first layer, then supplement with custom controls for domain-specific requirements. |

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
