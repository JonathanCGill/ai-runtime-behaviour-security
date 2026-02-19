# Supply Chain Security Controls

> Part of the [AI Security Infrastructure Controls](../README.md) framework.
> Companion to [AI Runtime Behaviour Security](https://github.com/JonathanCGill/ai-runtime-behaviour-security).

---

## Overview

AI supply chains extend far beyond traditional software dependencies. They include foundation models with opaque training data, fine-tuning datasets that can introduce backdoors, RAG knowledge bases that become part of the model's effective reasoning, third-party tools and plugins that agents invoke autonomously, and guardrail/safety models that are themselves machine learning systems. Compromise at any point in this chain can undermine every downstream security control.

These eight controls establish verification, provenance, and integrity requirements across the full AI supply chain.

---

## SUP-01 — Verify Model Provenance and Integrity

**Risk Tiers:** All

### Objective

Ensure that every model deployed in production can be traced to a verified source, with cryptographic proof that it has not been modified since publication.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Source verification** | Models must be obtained from verified publishers or approved internal registries. No models downloaded from unverified sources, community forks, or anonymous uploads. |
| **Cryptographic integrity** | Record and verify cryptographic hashes (SHA-256 minimum) for all model artifacts at download, storage, and deployment. Any hash mismatch blocks deployment. |
| **Signature validation** | Where model publishers provide digital signatures, validate signatures before deployment. Maintain a registry of trusted signing keys. |
| **Model registry** | Maintain a centralised registry of all approved models with: publisher identity, version, hash, download source, approval date, approver, and risk tier classification. |
| **Version pinning** | Production deployments must reference specific model versions, never "latest" or floating tags. Version changes require re-approval. |

### Relationship to Three Layers

| Layer | How SUP-01 Supports It |
|-------|----------------------|
| **Guardrails** | Guardrails can only enforce policy if the model they protect is the model that was tested. A substituted model may respond differently to the same guardrail configuration. |
| **Judge** | Judge evaluation baselines are model-specific. A different model invalidates calibration data and threshold settings. |
| **Human Oversight** | Provenance records give human reviewers confidence that the model in production matches what was assessed and approved. |

---

## SUP-02 — Assess Model Risk Before Adoption

**Risk Tiers:** All

### Objective

Evaluate every model against security, safety, and operational risk criteria before it is approved for use in any environment.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Pre-adoption assessment** | Every model must undergo a documented risk assessment before deployment. Assessment scope includes: training data provenance, known vulnerabilities, licence terms, capability profile, and alignment evaluation results. |
| **Risk classification** | Assign a risk tier to each model based on: capability level, deployment context (internal vs. customer-facing), data access scope, autonomy level, and regulatory exposure. |
| **Red team evaluation** | For Tier 2+ deployments, conduct adversarial testing (prompt injection, jailbreak, data extraction) against the specific model version before approval. |
| **Licence compliance** | Verify that model licence terms permit the intended use case. Flag models with restrictive licences, non-commercial clauses, or unclear IP provenance. |
| **Re-assessment triggers** | Define events that trigger re-assessment: model version updates, deployment context changes, new vulnerability disclosures, regulatory changes, or elapsed time thresholds. |

### Relationship to Three Layers

| Layer | How SUP-02 Supports It |
|-------|----------------------|
| **Guardrails** | Risk assessment identifies which guardrail configurations are needed for a specific model's known weaknesses and capability profile. |
| **Judge** | Assessment results inform Judge evaluation criteria and threshold calibration for the specific model. |
| **Human Oversight** | Risk classification determines the level of human oversight required — higher-risk models require more frequent and more granular human review. |

---

## SUP-03 — Verify RAG Data Source Integrity

**Risk Tiers:** Tier 2+

### Objective

Ensure that data ingested into retrieval-augmented generation (RAG) knowledge bases is from verified sources, has not been tampered with, and does not introduce poisoned or adversarial content into the model's effective context.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Source allowlisting** | Maintain an explicit allowlist of approved data sources for each RAG knowledge base. Only data from allowlisted sources may be ingested. |
| **Content scanning** | Scan all ingested content for: prompt injection payloads, adversarial content designed to manipulate model behaviour, malware or malicious scripts, and content that violates data classification policy. |
| **Provenance tracking** | Record provenance metadata for every document in the knowledge base: source, ingestion timestamp, ingestion pipeline version, content hash, and approver (for manually curated content). |
| **Integrity monitoring** | Continuously verify that knowledge base contents match their recorded hashes. Alert on any unexpected modification. |
| **Separation from runtime** | RAG ingestion pipelines must be separated from runtime query paths (see NET-05). Ingestion processes should never have direct access to the model runtime environment. |

### Relationship to Three Layers

| Layer | How SUP-03 Supports It |
|-------|----------------------|
| **Guardrails** | Input guardrails inspect prompts, but RAG content bypasses prompt-level inspection because it enters via the retrieval path. Source integrity is the guardrail for this vector. |
| **Judge** | Judge can evaluate whether retrieved content appears anomalous relative to the knowledge base's expected domain, but only if the baseline is trustworthy. |
| **Human Oversight** | Provenance records enable human reviewers to trace any problematic output back to the specific RAG source that contributed to it. |

---

## SUP-04 — Secure Fine-Tuning Pipeline

**Risk Tiers:** Tier 2+

### Objective

Protect fine-tuning processes from data poisoning, unauthorised modification, and supply chain compromise that could embed backdoors or degrade model safety.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Training data validation** | All fine-tuning datasets must undergo review for: data quality, label accuracy, adversarial examples, PII content, and alignment with intended behaviour. |
| **Pipeline access control** | Fine-tuning pipelines require authenticated access with role-based permissions. Training job submission is restricted to authorised personnel. |
| **Environment isolation** | Fine-tuning environments are isolated from production inference environments. No shared compute, storage, or network paths. |
| **Artifact versioning** | Every fine-tuned model version is stored with: base model reference, training dataset reference, hyperparameters, training logs, and output hash. |
| **Post-training evaluation** | Fine-tuned models must pass safety and security evaluation (including adversarial testing) before deployment. Evaluation results are recorded and linked to the model version. |
| **Rollback capability** | Maintain the ability to revert to the previous model version if post-deployment monitoring detects degraded safety or security behaviour. |

### Relationship to Three Layers

| Layer | How SUP-04 Supports It |
|-------|----------------------|
| **Guardrails** | A poisoned fine-tuned model may learn to evade specific guardrail patterns. Pipeline security prevents this attack vector. |
| **Judge** | Post-training evaluation provides the Judge with a validated baseline. Changes in Judge scores after fine-tuning indicate potential problems. |
| **Human Oversight** | Artifact versioning and training logs give human reviewers a complete audit trail of what changed and why. |

---

## SUP-05 — Audit Tool and Plugin Supply Chain

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Ensure that tools and plugins available to AI agents are from verified sources, have been assessed for security risk, and are maintained under version control with integrity verification.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Tool registry** | Maintain a centralised registry of all approved tools and plugins. Each entry includes: publisher, version, hash, capabilities, required permissions, risk classification, and approval date. |
| **Source verification** | Tools must be obtained from verified publishers or approved internal repositories. No tools from unverified sources or community repositories without security review. |
| **Security assessment** | Every tool undergoes security assessment before approval: code review (or vendor assessment for closed-source), dependency analysis, permission requirements analysis, and adversarial testing of tool behaviour. |
| **Version control** | Tool versions are pinned in production. Updates require re-assessment and re-approval. Automatic updates are prohibited. |
| **Dependency analysis** | Analyse tool dependencies for known vulnerabilities. Transitive dependencies are included in the analysis scope. |
| **Capability declaration** | Tools must declare their capabilities and required permissions in a machine-readable manifest. Undeclared capabilities are blocked at the gateway (see TOOL-01, TOOL-02). |

### Relationship to Three Layers

| Layer | How SUP-05 Supports It |
|-------|----------------------|
| **Guardrails** | Tool manifests feed guardrail policy — the guardrail knows what the tool is allowed to do and blocks invocations outside declared scope. |
| **Judge** | Judge can evaluate whether tool invocation patterns match the declared capability profile, detecting anomalous usage that may indicate compromise. |
| **Human Oversight** | The tool registry provides human reviewers with a complete inventory of what agents can do, enabling informed approval decisions. |

---

## SUP-06 — Verify Guardrail and Safety Model Integrity

**Risk Tiers:** All

### Objective

Guardrails and Judge models are themselves machine learning systems (or rule engines). Their integrity must be verified with the same rigour applied to the primary model, because compromise of safety systems is the highest-impact supply chain attack.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Integrity verification** | Guardrail models and rule configurations are subject to the same hash verification and signature validation as primary models (SUP-01). |
| **Independent sourcing** | Where possible, guardrail and Judge models should come from different providers or model families than the primary model. This reduces the risk of correlated failure. |
| **Configuration version control** | Guardrail rule sets and Judge prompts/configurations are stored in version-controlled repositories with audit trails. Changes require approval. |
| **Tamper detection** | Monitor guardrail and Judge model artifacts for unauthorised modification. Alert on any change that bypasses the approved change process. |
| **Update validation** | Updates to guardrail or Judge models/configurations must pass regression testing against known attack patterns and edge cases before deployment. |

### Relationship to Three Layers

| Layer | How SUP-06 Supports It |
|-------|----------------------|
| **Guardrails** | This control directly protects guardrail integrity. A compromised guardrail that silently passes malicious content is worse than no guardrail at all. |
| **Judge** | Judge model integrity is equally critical. A compromised Judge that approves harmful outputs defeats the evaluation layer entirely. |
| **Human Oversight** | Version-controlled configurations and tamper detection ensure that human-approved safety settings remain in effect. |

---

## SUP-07 — Maintain AI Component Inventory (AI-BOM)

**Risk Tiers:** All

### Objective

Maintain a comprehensive, machine-readable inventory of all AI components in production — analogous to a software bill of materials (SBOM) but extended to cover models, datasets, guardrails, tools, and evaluation systems.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Component coverage** | The AI-BOM must include: foundation models, fine-tuned models, guardrail models/rules, Judge models/configurations, embedding models, RAG knowledge bases, tools and plugins, orchestration frameworks, and vector databases. |
| **Metadata per component** | Each entry includes: component type, name, version, publisher/source, hash, deployment location, risk tier, dependencies, approval status, and last assessment date. |
| **Machine-readable format** | The AI-BOM is maintained in a structured, machine-readable format (e.g., JSON, YAML) that can be consumed by automated tooling. |
| **Continuous update** | The AI-BOM is updated automatically when components are deployed, updated, or decommissioned. Manual-only maintenance is insufficient for production systems. |
| **Dependency mapping** | The AI-BOM captures dependencies between components: which guardrails protect which models, which tools are available to which agents, which knowledge bases serve which retrieval endpoints. |

### Relationship to Three Layers

| Layer | How SUP-07 Supports It |
|-------|----------------------|
| **Guardrails** | The AI-BOM identifies which guardrails are deployed for each model, enabling gap analysis and coverage verification. |
| **Judge** | The AI-BOM tracks Judge model versions and their associations with primary models, ensuring evaluation consistency. |
| **Human Oversight** | The AI-BOM gives human reviewers a single source of truth for what is deployed, enabling informed risk decisions and incident response. |

---

## SUP-08 — Monitor for Model and Dependency Vulnerabilities

**Risk Tiers:** All

### Objective

Continuously monitor for newly disclosed vulnerabilities, attacks, and safety issues affecting any component in the AI-BOM, and trigger assessment or remediation when relevant disclosures occur.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Vulnerability feed monitoring** | Subscribe to vulnerability feeds and advisories for: model providers (e.g., security bulletins from OpenAI, Anthropic, Meta, Google), framework providers (e.g., LangChain, LlamaIndex, Hugging Face), tool and plugin providers, and general CVE databases for software dependencies. |
| **AI-BOM correlation** | Correlate incoming vulnerability disclosures against the AI-BOM to determine which production deployments are affected. |
| **Impact assessment** | For each relevant vulnerability, assess: exploitability in the deployment context, data exposure risk, whether existing guardrails/Judge mitigate the issue, and urgency of remediation. |
| **Remediation tracking** | Track remediation actions to completion: model updates, guardrail rule additions, configuration changes, or compensating controls. |
| **Proactive testing** | When new attack techniques are published (e.g., novel prompt injection methods, jailbreak patterns), proactively test deployed models against these techniques rather than waiting for a vendor advisory. |

### Relationship to Three Layers

| Layer | How SUP-08 Supports It |
|-------|----------------------|
| **Guardrails** | Vulnerability monitoring may identify new attack patterns that require guardrail rule updates (e.g., new injection techniques). |
| **Judge** | New vulnerability disclosures may require Judge evaluation criteria updates to detect exploitation of newly discovered weaknesses. |
| **Human Oversight** | Vulnerability monitoring feeds human risk assessment and drives prioritised remediation decisions. |

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
