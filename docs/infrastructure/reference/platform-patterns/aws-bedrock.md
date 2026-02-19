# AWS Bedrock Implementation Patterns

> **Purpose:** Platform-specific guidance for implementing the infrastructure controls on AWS using Amazon Bedrock as the model hosting platform.  
> **Status:** Reference patterns — adapt to your specific architecture and AWS account structure.

---

## Architecture Mapping

| Framework Zone | AWS Implementation |
|---------------|-------------------|
| **Zone 1 — Ingress** | Amazon API Gateway + AWS WAF + Amazon CloudFront |
| **Zone 2 — Runtime** | Amazon Bedrock (invoke endpoint), Bedrock Guardrails, Amazon OpenSearch Serverless (vector read) |
| **Zone 3 — Evaluation** | Separate Bedrock model invocation (Judge) in isolated account or VPC |
| **Zone 4 — Ingestion** | AWS Lambda / AWS Step Functions + Amazon Bedrock Knowledge Bases (ingestion), OpenSearch Serverless (vector write) |
| **Zone 5 — Control Plane** | AWS Systems Manager Parameter Store / Secrets Manager, AWS Config, IAM Identity Center |
| **Zone 6 — Logging** | Amazon CloudWatch Logs, Amazon S3 (log archive), Amazon Security Lake, SIEM integration |

---

## Identity & Access (IAM Controls)

### IAM-01/02: Authentication and Least Privilege

- Use **IAM Identity Center** for human identities with federated SSO.
- Use **IAM Roles** for all service identities — never static access keys.
- Bedrock model invocation via **IAM role-based access** with resource-based policies.
- **Resource policies** on Bedrock model endpoints restrict which IAM principals can invoke.
- Separate IAM roles for: application (invoke model), guardrail service (evaluate), ingestion (manage knowledge base), admin (configure).

### IAM-03: Control/Data Plane Separation

- **Separate AWS accounts** for control plane (model configuration, guardrail rules) and runtime (model invocation).
- Use **AWS Organizations SCPs** to prevent runtime accounts from modifying Bedrock model configurations.
- Control plane changes require **IAM Identity Center** with MFA, not programmatic access.
- Bedrock model invocation permissions ≠ Bedrock model management permissions.

### IAM-04/05: Agent Tool Constraints

- Bedrock Agents define **action groups** — each action group is a declared tool with specific API operations.
- Use **Lambda function resource policies** to restrict which Bedrock Agent can invoke which function.
- Implement approval routing via **Step Functions** for high-impact actions — the Lambda returns a "pending approval" response and waits for human input.

### IAM-06: Session-Scoped Credentials

- Use **AWS STS AssumeRole** with `DurationSeconds` set to minimum needed (15 min to 1 hour).
- Set **session tags** on STS tokens to bind to agent session ID.
- **IAM condition keys** (`aws:PrincipalTag/SessionId`) restrict token use to originating session.

---

## Logging & Observability (LOG Controls)

### LOG-01: Model I/O Logging

- Enable **Bedrock Model Invocation Logging** to CloudWatch Logs and/or S3.
- Log configuration captures: input tokens, output tokens, model ID, invocation latency.
- For full prompt/response capture, use the **S3 delivery** option (CloudWatch has size limits).
- **Important:** Bedrock invocation logging captures prompts and responses — ensure PII handling (LOG-09) is applied downstream.

### LOG-02/03: Guardrail and Judge Logging

- **Bedrock Guardrails** log trace data when enabled — includes filter decisions, blocked content, and applied policies.
- Use the `trace` field in Bedrock API responses to capture guardrail evaluation details.
- Judge invocations logged as separate Bedrock model calls with distinct logging configuration.

### LOG-04: Agent Decision Chains

- **Bedrock Agent traces** capture the full reasoning chain: rationale, action, observation, final response.
- Enable trace logging on agent invocations (`enableTrace: true`).
- Store traces in S3 with lifecycle policies matching LOG-08 retention requirements.

### LOG-05/06: Drift and Injection Detection

- Use **Amazon CloudWatch Metrics** for Bedrock invocation metrics (latency, error rates, token consumption).
- Set **CloudWatch Alarms** with anomaly detection for baseline deviation (>2σ).
- Implement custom **CloudWatch Metric Filters** on invocation logs for prompt injection pattern detection.
- Feed to **Amazon Security Lake** for cross-source correlation.

### LOG-10: SIEM Integration

- Use **Amazon Security Lake** as the normalisation layer (OCSF format).
- Export to enterprise SIEM via Security Lake subscriber or S3 export.
- **CloudWatch Logs subscription filters** for real-time streaming to SIEM.

---

## Network & Segmentation (NET Controls)

### NET-01: Network Zones

- Use **separate VPCs** for runtime (Zone 2) and ingestion (Zone 4).
- Bedrock Guardrails run in AWS-managed infrastructure — use **VPC endpoints** (`com.amazonaws.region.bedrock-runtime`) for private connectivity.
- **VPC endpoint policies** restrict which IAM principals can use the endpoint.
- Use **AWS PrivateLink** for all Bedrock API access — no internet-routed traffic.

### NET-02: Guardrail Bypass Prevention

- Bedrock Guardrails are **applied at the API level** — configure guardrail ID on model invocations.
- Use **IAM policies** to deny `bedrock:InvokeModel` without guardrail specification.
- **SCP** at org level: deny Bedrock invocations that don't include a guardrailIdentifier.

### NET-03: Judge Isolation

- Judge model invoked from a **separate VPC** or **separate AWS account**.
- **Cross-account IAM role** for Judge invocation with minimal permissions.
- Judge VPC has no inbound routes from runtime VPC — data pushed via **SQS** or **EventBridge**.

### NET-04: Agent Egress Controls

- Agent Lambda functions run in **VPCs with no internet gateway**.
- Outbound access via **VPC endpoints** for AWS services and **NAT Gateway with security group restrictions** for external tools.
- Use **AWS Network Firewall** for domain-based egress filtering on external tool calls.
- **VPC Flow Logs** capture all network traffic for NET-08 monitoring.

---

## Data Protection (DAT Controls)

### DAT-03: PII Detection

- **Amazon Comprehend** for NER-based PII detection on model I/O.
- **Bedrock Guardrails PII filters** for built-in detection of common PII types.
- Custom regex patterns via **Lambda@Edge** or pre-processing Lambda for domain-specific PII.

### DAT-04: Access-Controlled RAG

- **Bedrock Knowledge Bases** support metadata filtering on retrieval.
- Implement document-level access control by adding classification metadata at ingestion.
- Use **OpenSearch Serverless** fine-grained access control for field-level security on embeddings.
- **Pre-filter** approach: add metadata filter to Knowledge Base query matching user's permissions.

### DAT-05: Encryption

- Bedrock data encrypted at rest with **AWS KMS** — use CMK (customer-managed key) for Tier 3+.
- OpenSearch Serverless collections encrypted with KMS.
- S3 log buckets encrypted with separate KMS key.
- All Bedrock API calls over TLS 1.2 via PrivateLink endpoints.

---

## Secrets & Credentials (SEC Controls)

### SEC-01/03: Vault and Context Isolation

- Use **AWS Secrets Manager** for all AI system credentials.
- Agent Lambda functions retrieve credentials from Secrets Manager at invocation — credentials not stored in environment variables.
- Bedrock Agent action groups use **Lambda execution roles** — no credentials in agent prompts.

### SEC-04: Credential Scanning

- **Amazon Macie** for scanning S3 logs for credential patterns.
- **CodeGuru Security** for scanning AI application code.
- Custom guardrail rules in Bedrock for credential pattern detection in I/O.

---

## Incident Response (IR Controls)

### IR-04: Rollback

- Bedrock model versions pinned — rollback by changing the model ID in configuration.
- Bedrock Guardrail versions — create new version, point to previous known-good version.
- Knowledge Base rollback: re-sync from known-good S3 source data.
- **AWS CodePipeline** with manual approval gates for all AI component deployments.

---

## AWS-Specific Considerations

| Consideration | Guidance |
|--------------|---------|
| **Bedrock Guardrails limitations** | Bedrock Guardrails run in AWS-managed infrastructure — you control configuration but not the execution environment. Supplement with custom guardrail logic for domain-specific requirements. |
| **Multi-region** | Bedrock model availability varies by region. Design for single-region deployment per AI system instance. |
| **Cost management** | Enable Bedrock model invocation metrics for cost tracking. Use SESS-01 token limits to prevent denial-of-wallet. |
| **Model access** | Bedrock requires explicit model access grants per account. Use this as an additional control point (SUP-01). |
| **CloudTrail** | Enable CloudTrail for all Bedrock management API calls. This covers control plane auditing (IAM-08). |

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
