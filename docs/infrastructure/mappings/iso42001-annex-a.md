# ISO/IEC 42001 Annex A Mapping

> Maps infrastructure controls to ISO/IEC 42001:2023 Annex A — Controls for AI Management Systems.
>
> Part of the [AI Security Infrastructure Controls](../README.md) framework.
> Companion to [AI Runtime Behaviour Security](https://github.com/JonathanCGill/ai-runtime-behaviour-security).

---

## Scope and Limitations

This mapping covers the **technical infrastructure layer** of ISO 42001 Annex A compliance. ISO 42001 requires both organisational and technical controls. This repo addresses the technical controls; organisational controls (policies, governance structures, roles, training, third-party management) are addressed by the parent framework and by the implementing organisation's management system.

ISO 42001 Annex A sections A.2 through A.10 are mapped below. Each section lists the Annex A controls, the infrastructure controls that support them, and notes on coverage scope.

---

## A.2 — Policies for AI

| Annex A Control | Description | Infrastructure Controls | Notes |
|----------------|-------------|------------------------|-------|
| A.2.2 | AI policy | NET-06, IAM-03 | Control plane protection ensures AI policy configurations are tamper-proof. Technical controls enforce what policies declare. Organisational policy definition is out of scope for this repo. |
| A.2.3 | Internal use AI policy | IAM-01, IAM-02, DAT-01, DAT-02 | Authentication, least privilege, data classification, and minimisation enforce internal use policies at the technical layer. |
| A.2.4 | AI policy for third parties | SUP-01, SUP-02, SUP-05, SEC-07 | Model provenance, risk assessment, tool supply chain auditing, and endpoint credential protection govern third-party AI component usage. |

---

## A.3 — Internal Organisation

| Annex A Control | Description | Infrastructure Controls | Notes |
|----------------|-------------|------------------------|-------|
| A.3.2 | Roles and responsibilities for AI | IAM-01, IAM-02, IAM-03, IAM-08 | Authentication, least privilege, control/data plane separation, and access auditing enforce role-based access. Role definition is organisational. |
| A.3.3 | Reporting AI concerns | IR-01, IR-02, IR-06 | AI-specific incident categories, detection triggers, and communication protocols provide the technical infrastructure for concern reporting. |
| A.3.4 | AI governance | NET-06, IAM-03, LOG-07, SUP-07 | Control plane protection, plane separation, log integrity, and AI-BOM provide technical infrastructure for governance. Governance structure is organisational. |

---

## A.4 — Resources for AI Systems

| Annex A Control | Description | Infrastructure Controls | Notes |
|----------------|-------------|------------------------|-------|
| A.4.2 | Resources for AI system development | SUP-04, SAND-01, SAND-04 | Fine-tuning pipeline security, sandbox isolation, and resource limits govern AI development resource usage. |
| A.4.3 | AI system computational resources | SAND-04, SESS-01, TOOL-05 | Resource limits, session boundaries, and rate limiting ensure controlled resource consumption. |
| A.4.4 | Data resources for AI | DAT-01, DAT-02, DAT-04, SUP-03 | Data classification, minimisation, RAG access control, and data source integrity govern data resources. |
| A.4.5 | AI system tools and utilities | SUP-05, TOOL-01, TOOL-02, TOOL-03 | Tool supply chain, declared permissions, gateway enforcement, and parameter constraints govern tool resources. |
| A.4.6 | Data quality for AI | SUP-03, SUP-04, DAT-01 | RAG data integrity, fine-tuning pipeline security, and data classification address data quality at the infrastructure level. |

---

## A.5 — AI System Development

| Annex A Control | Description | Infrastructure Controls | Notes |
|----------------|-------------|------------------------|-------|
| A.5.2 | AI system impact assessment | SUP-02, IR-01, TOOL-04 | Model risk assessment, incident category definitions, and action classification by impact support impact assessment. Assessment methodology is organisational. |
| A.5.3 | AI system lifecycle | SUP-01, SUP-04, SUP-07, SUP-08, IR-04 | Provenance, fine-tuning security, AI-BOM, vulnerability monitoring, and rollback capability support lifecycle management. |
| A.5.4 | AI system design and development | NET-01, IAM-04, SEC-01, DAT-02 | Zone architecture, tool invocation constraints, credential isolation, and data minimisation are design-stage decisions. |
| A.5.5 | AI system testing | SUP-02, SUP-04, LOG-05, SAND-06 | Risk assessment, post-training evaluation, drift detection, and code scanning support testing processes. |
| A.5.6 | AI system deployment | SUP-01, SUP-06, TOOL-01, NET-02 | Provenance verification, safety model integrity, manifest validation, and bypass prevention support secure deployment. |
| A.5.7 | AI system operation | LOG-01 through LOG-10, NET-08, SESS-01 | Full logging suite, cross-zone monitoring, and session boundaries support operational monitoring. |
| A.5.8 | AI system maintenance | IR-04, SUP-08, SUP-06, SEC-05 | Rollback, vulnerability monitoring, integrity verification, and credential rotation support maintenance. |

---

## A.6 — Data for AI Systems

| Annex A Control | Description | Infrastructure Controls | Notes |
|----------------|-------------|------------------------|-------|
| A.6.2 | Data for AI acquisition | SUP-03, DAT-01, DAT-04 | RAG source integrity, data classification, and access-controlled retrieval govern data acquisition. |
| A.6.3 | Data quality management | SUP-03, SUP-04, LOG-05 | Source integrity verification, training data validation, and drift detection support data quality. |
| A.6.4 | Data provenance | SUP-01, SUP-03, DEL-02 | Model provenance, RAG source provenance, and delegation chain audit trails support data traceability. |
| A.6.5 | Data preparation | SUP-04, DAT-03, DAT-08 | Fine-tuning pipeline security, PII detection/redaction, and evaluation data tokenisation govern data preparation. |
| A.6.6 | Data annotation/labelling | SUP-04, IAM-01, LOG-07 | Pipeline security, authentication of annotators, and log integrity support labelling integrity. Note: annotation quality controls are organisational. |
| A.6.7 | Data for testing | SAND-01, DAT-08, DAT-05 | Sandbox isolation, evaluation data protection, and encryption protect test data. |

---

## A.7 — AI System Performance and Monitoring

| Annex A Control | Description | Infrastructure Controls | Notes |
|----------------|-------------|------------------------|-------|
| A.7.2 | AI system performance monitoring | LOG-01, LOG-02, LOG-03, LOG-05, LOG-10 | Model I/O logging, guardrail decision logging, Judge evaluation logging, drift detection, and SIEM correlation provide comprehensive performance monitoring. |
| A.7.3 | AI system performance evaluation | LOG-03, LOG-05, SUP-02 | Judge evaluation logs, drift detection, and model risk assessment support performance evaluation. Evaluation methodology is organisational. |
| A.7.4 | AI system monitoring | LOG-04, LOG-06, LOG-10, NET-08, IR-02 | Agent chain logging, injection detection, SIEM correlation, cross-zone monitoring, and detection triggers provide operational monitoring. |
| A.7.5 | Addressing performance issues | IR-03, IR-04, IR-07, LOG-05 | Containment procedures, rollback capability, post-incident review, and drift detection support performance issue response. |

---

## A.8 — AI System Transparency

| Annex A Control | Description | Infrastructure Controls | Notes |
|----------------|-------------|------------------------|-------|
| A.8.2 | AI system documentation | SUP-07, TOOL-01, REPO-STRUCTURE | AI-BOM, tool manifests, and the structured control documentation support system documentation. Document content is organisational. |
| A.8.3 | AI system explainability | LOG-01, LOG-04, DEL-02, TOOL-06 | Model I/O logs, agent chain reconstruction, delegation audit trails, and tool invocation logs provide the data needed for explainability. Explainability methods are organisational. |
| A.8.4 | Information about AI system interaction | LOG-01, LOG-02, DAT-07 | I/O logging, guardrail decision logging, and conversation history management support interaction transparency. User-facing disclosures are organisational. |

---

## A.9 — AI System Accountability

| Annex A Control | Description | Infrastructure Controls | Notes |
|----------------|-------------|------------------------|-------|
| A.9.2 | AI system record-keeping | LOG-07, LOG-08, DEL-02, TOOL-06, IAM-08 | Log integrity, retention policies, delegation audit trails, tool invocation logging, and access change auditing provide comprehensive record-keeping. |
| A.9.3 | AI system auditing | All LOG controls, all mapping documents, SUP-07 | Full logging suite, standards mappings, and AI-BOM support audit capability. Audit programme design is organisational. |
| A.9.4 | Responsibility for AI system decisions | IAM-01, IAM-05, DEL-05, TOOL-04 | Authentication, human approval routing, user identity propagation, and action classification by impact enable decision attribution. |
| A.9.5 | Reporting of AI incidents | IR-01 through IR-08 | Full incident response control suite supports incident reporting. Reporting obligations are organisational/regulatory. |

---

## A.10 — Third-Party and Customer Relationships

| Annex A Control | Description | Infrastructure Controls | Notes |
|----------------|-------------|------------------------|-------|
| A.10.2 | Third-party AI suppliers | SUP-01, SUP-02, SUP-05, SUP-08 | Provenance, risk assessment, tool/plugin supply chain, and vulnerability monitoring govern third-party AI components. Supplier management processes are organisational. |
| A.10.3 | Third-party AI customers | DAT-06, SEC-01, NET-07, LOG-09 | Response leakage prevention, credential isolation, gateway enforcement, and log redaction protect customer data in multi-tenant AI deployments. |
| A.10.4 | Interested parties for AI systems | IR-06, IR-07, LOG-10 | Communication protocols, post-incident review, and SIEM correlation support stakeholder engagement. Stakeholder identification is organisational. |

---

## Coverage Summary

| Annex A Section | Infrastructure Controls Mapped | Coverage Type |
|----------------|-------------------------------|---------------|
| A.2 Policies | 8 controls | Technical enforcement of policies; policy creation is organisational |
| A.3 Internal Organisation | 7 controls | Technical infrastructure for governance; organisational structure is out of scope |
| A.4 Resources | 11 controls | Resource usage controls at infrastructure level |
| A.5 Development | 16 controls | Lifecycle security from design through maintenance |
| A.6 Data | 12 controls | Data integrity, quality, and protection at infrastructure level |
| A.7 Performance | 10 controls | Monitoring, detection, and response infrastructure |
| A.8 Transparency | 7 controls | Data and logging infrastructure supporting transparency |
| A.9 Accountability | 10 controls | Record-keeping, auditing, and attribution infrastructure |
| A.10 Third Parties | 8 controls | Supply chain and multi-tenant protection |

**Note:** Full ISO 42001 compliance requires both the technical infrastructure controls in this repo and the organisational controls (policies, governance, training, roles, processes) addressed by the implementing organisation's AI management system. This mapping covers the technical layer only.

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
