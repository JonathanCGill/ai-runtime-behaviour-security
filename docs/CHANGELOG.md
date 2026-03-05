# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Cost model with production data
- Platform-specific implementation guides (detailed)
- Case studies from production deployments
- Judge accuracy benchmarks from real deployments
- Epistemic risk detection algorithm specifications

## [0.8.4] - 2026-03-01

### Added
- **Why Containment Beats Evaluation** - New position paper page articulating the constrain-regardless architecture for sandbagging-resistant AI governance. Covers closed-loop vs open-loop control, action-space vs reasoning-space constraints, compound defence by design, enterprise-owned Judge positioning, and honest acknowledgement of limits. Aligns the framework with the published position paper.

### Changed
- **Architecture Overview** - Added closed-loop control system framing, constrain-regardless language, and enterprise-owned Judge positioning.
- **Foundations README** - Added action-space constraint language, enterprise-owned Judge emphasis, and compound defence by design framing.
- **Evaluation Integrity Risks** - Reframed from "mitigate sandbagging" to "sandbagging is operationally irrelevant as a breakout vector" under the constrain-regardless architecture.
- **Containment Through Declared Intent** - Added constrain-regardless framing, action-space vs reasoning-space distinction, parental analogy, and closed-loop control system language.

## [0.8.3] - 2026-03-01

### Added
- **Containment Through Declared Intent** - New insights page articulating the framework's unified defence thesis. Declared intent is the organising principle that gives every layer (guardrails, Judge, monitoring, human oversight, PACE) its reference point. Covers how intent flows through the defence stack, downstream intent awareness between agents, the confinement model, and honest assessment of where the theory breaks down.

## [0.8.2] - 2026-03-01

### Added
- **CoSAI Principles Alignment** - Updated References with full alignment mapping to CoSAI's Principles for Secure-by-Design Agentic Systems (July 2025). Demonstrates how the framework's three-layer pattern, PACE resilience, and MASO controls operationalise CoSAI's three principles.
- **Producer/Implementer/Principal Accountability** - Added supply chain accountability model to the AI Governance Operating Model. Complements the three-lines governance model with a supply chain lens for distributing responsibility across technology producers, service implementers, and human principals. Credit to CoSAI.
- **SLSA-Style Supply Chain Provenance** - Added to ET-04 (MCP as Attack Surface). Recommends adapting SLSA for verifiable provenance of agent and model artifacts: signed build provenance, content hashes for tool definitions, and verifiable chain from source to deployment.

## [0.8.1] - 2026-03-01

### Added
- **E-Commerce 10K Stress Test** - New MASO stress test scenario: 6 agent types, 10,000 concurrent customers, 60,000 agent instances on EKS. Complements the 100-agent breadth test with a depth-and-volume test covering type-level observability, risk-tiered Judge sampling, exception-driven human oversight, Kubernetes-native identity, PCI scope containment, two-level PACE, graduated shutdown, and volume-based compound attacks.

### Changed
- **100-Agent Stress Test** - Added cross-reference to the new e-commerce stress test in the relationship table.

## [0.8.0] - 2026-03-01

### Added
- **Evaluation Integrity Risks** - New insights page covering sandbagging, evaluation evasion, and the AISI finding that black-box monitors lose accuracy on harder tasks. Includes mitigations: canary interactions, evaluation signature elimination, multi-model cross-validation, behavioural consistency monitoring.
- **AISI 5-Level MCP Autonomy Classification** - Added to The MCP Problem page. Maps MCP server autonomy levels (read-only through unbounded autonomous) to MASO implementation tiers, with specific guidance for financial services.
- **Self-Replication Capabilities (ET-09)** - New emerging threat in MASO threat intelligence. Documents RepliBench progression from 5% to 60% success rates (2023–2025) and implications for kill switch architecture.
- **Capability Acceleration (ET-10)** - New emerging threat documenting the ~8-month doubling time for autonomous task complexity, with implications for control framework evolution cadence.
- **Persuasion Scaling Risk** - Added to Emerging Trends. Documents AISI finding that persuasive capability increases with model scale while accuracy decreases, and post-training amplifies persuasion more than scaling.
- **Emotional Dependence Data** - Added to Emerging Trends. Documents AISI finding on 33% AI emotional support usage and 30x negative sentiment spikes during outages. PACE implications for service continuity.
- **AISI Reference** - Added UK AI Security Institute Frontier AI Trends Report (December 2025) to References & Sources page with full finding summary and cross-references to all updated pages. Added 6 new key statistics.

### Changed
- **Risk Tiers** - Added Domain-Specific Guardrail Tuning section with AISI evidence for uneven safeguard coverage across risk categories (R² = 0.097 capability-safety correlation, 40x jailbreak effort increase for targeted categories).
- **When the Judge Can Be Fooled** - Expanded sandbagging section with AISI empirical data on black-box monitor accuracy degradation. Added cross-reference to new Evaluation Integrity Risks page.
- **Open-Weight Models** - Added AISI confirmation that safeguards can be "quickly and cheaply removed" and 4–8 month open-to-closed source capability gap data. Strengthens case for runtime monitoring as primary control.
- **Emerging Threats** - Updated threat landscape summary table to include ET-09 and ET-10.

### Rationale
The UK AI Security Institute's Frontier AI Trends Report (December 2025) is the strongest empirical backing for runtime behavioural security from a government body. Its findings directly validate the framework's core thesis (runtime controls matter more than deployment-time security alone) and provide concrete data points that strengthen multiple framework sections. Credit given throughout via source attribution.

## [0.7.0] - 2026-02-15

### Added
- **MATURITY.md** - Honest assessment of framework validation status
  - Four-level validation model (production, incident, standards, pattern consistency)
  - Explicit documentation of known gaps
  - Call for pilot partners and peer review
- **VALIDATED-AGAINST.md** - Control-by-control incident validation
  - Controls mapped to known real-world incidents with confidence ratings
  - Evidence strength ratings (Strong: 3+ incidents, Moderate: 1–2, Threat-modelled: 0)
  - Validation coverage map by MASO domain
  - Top 5 most-validated controls identified
- **EVOLUTION.md** - Narrative history of framework development
  - Decision rationale for every major version
  - What drove each change (incidents, feedback, architectural shifts)
  - Timeline from v0.1.0 (Dec 2025) through current

### Changed
- Updated site navigation to include Credibility section (Maturity, Validated Against, Evolution)
- Changelog now links to narrative Evolution page for context

### Rationale
The framework is comprehensive but has no production deployments. Rather than ignoring this gap, these additions address it directly: honest status assessment, retroactive alignment against real incidents, and a living record of how the framework evolves in response to real-world events. Credibility comes from transparency, not claims.

## [0.6.0] - 2026-02-08

### Changed
- **Renamed: AI Security Blueprint → Enterprise AI Security Framework**
  - Better reflects the content scope (governance, compliance, org structure)
  - "Blueprint" implied buildable artifacts; "Framework" is accurate
  - Later renamed to **AI Runtime Behaviour Security** (February 2026)
  
### Added
- **IMPLEMENTATION_GUIDE.md** - New practical guide with working code
  - Input guardrails (regex + Bedrock + NeMo examples)
  - Output guardrails (PII, forbidden phrases, structured validation)
  - LLM-as-Judge (prompts, sampling strategies, async processing)
  - Human-in-the-loop queue (Redis implementation, FastAPI endpoints)
  - Telemetry and logging (structured logs, Prometheus metrics)
  - Complete request flow example
  - Test suite templates (unit tests, red team inputs)
  - ~1,500 lines of copy-paste-ready Python

### Rationale
Reality check revealed the framework was thought leadership, not a buildable blueprint. Now there are two clear paths:
- **Implementors**: Start with IMPLEMENTATION_GUIDE.md (code)
- **Architects/Governance**: Use the full Framework (strategy)

## [0.5.0] - 2026-02-07

### Changed
- **Major restructure: Core + Extensions model**
- New `/core/` folder with 5 essential documents:
  - README.md - Overview and quick start
  - risk-tiers.md - Classification and control selection
  - controls.md - Guardrails, Judge, HITL combined
  - agentic.md - Agent-specific controls
  - checklist.md - Implementation tracking
- New `/extensions/` folder for reference material:
  - regulatory/ - ISO 42001, EU AI Act, banking
  - technical/ - Bypass prevention, infrastructure, metrics
  - templates/ - Playbooks, assessments
  - examples/ - Worked examples
- Root README now serves as navigation hub
- Previous detailed documents preserved in extensions

### Rationale
Framework had grown to 48 files. Core + Extensions model provides clear "start here" path (5 docs) while preserving depth for those who need it.

## [0.4.1] - 2026-02-06

### Added
- Bypass Prevention document - comprehensive guide to preventing and detecting control circumvention across 5 bypass categories (guardrails, intent, agentic, architectural, process)
- Technical Controls document - network, firewall, WAF, AI gateway, DLP, proxy, endpoint, cloud, and IAM controls for infrastructure-level enforcement
- 14 new SVG diagrams:
  - bypass-taxonomy.svg - 5 bypass categories visual
  - defence-in-depth.svg - 8-layer control stack
  - technical-controls-architecture.svg - infrastructure overview
  - ai-gateway-architecture.svg - gateway internals
  - network-zones.svg - network segmentation
  - agent-sandbox.svg - infrastructure constraints
  - action-validator-flow.svg - action validation pipeline
  - tool-output-sanitiser.svg - tool output handling
  - canary-testing.svg - control verification programme
  - dlp-inspection-points.svg - 4 DLP layers
  - casb-ai-classification.svg - sanctioned/tolerated/blocked apps
  - bypass-learning-loop.svg - continuous improvement cycle
  - infra-vs-instruction.svg - enforcement comparison
  - multi-layer-input-validation.svg - input processing pipeline

### Changed
- Updated bypass-prevention.md and technical-controls.md to reference SVG diagrams instead of ASCII art
- Clarified lifecycle scope in README - framework is operationally focused (deployment → operation → incident response), not full AI/ML lifecycle

## [0.4.0] - 2026-02-05

### Added
- AI Incident Response Playbook - 10 playbooks for AI-specific incidents
- Vendor Assessment Questionnaire - comprehensive due diligence template
- Operational Metrics document - KPIs, dashboards, alerting thresholds
- Data Retention Guidance - requirements by tier and jurisdiction
- Templates README - index of all templates
- Standard repo files: CODE_OF_CONDUCT.md, GOVERNANCE.md, LICENSE (MIT), SECURITY.md

### Changed
- Updated README with Templates section and new document links
- Moved "Threats" section to "Threats and Risks" with expanded content

## [0.3.0] - 2026-02-05

### Added
- Novel AI Risks document - 12 risks unique to AI systems
- Support Systems Risk document - operational risks that matter most
- Banking Cyber Risks document - top 10 banking risks through AI lens
- Feeder systems analysis with diagram
- 10 new controls: AI.3.4, AI.5.4, AI.6.4, AI.6.5, AI.7.4, AI.8.5, AI.9.5, AI.10.6, AI.13.4
- Support systems risk heat map SVG
- Banking AI feeder systems diagram SVG
- Model card template
- Reference materials (glossary, bibliography)
- Future work roadmap

### Changed
- Strengthened AI.4.2 (Testing) with statistical testing for non-determinism
- Strengthened AI.6.2 (Model Validation) with bias testing and continuous validation
- Strengthened AI.6.3 (Model Monitoring) with degradation detection
- Strengthened AI.7.1 (Input Guardrails) with semantic analysis and RAG filtering
- Strengthened AI.7.2 (Output Guardrails) with grounding checks
- Strengthened AI.7.3 (Guardrail Maintenance) with semantic adversarial testing
- Strengthened AI.8.1 (Judge Evaluation) with hallucination and override detection
- Strengthened AI.8.2 (Sampling Strategy) with baseline integration
- Strengthened AI.9.1 (HITL) with automation bias mitigation
- Strengthened AI.11.1 (Logging) with full context capture
- Strengthened AI.13.1 (Vendor Assessment) with training data practices
- Strengthened AI.14.1 (Training) with cognitive bias training
- Strengthened AG.2.3 (Scope Enforcement) with outcome boundaries
- Updated README with new documentation links

### Fixed
- XML entity escaping in SVG files (ampersand encoding)

## [0.2.0] - 2026-01-15

### Added
- Agentic Controls (AG.1-AG.4) for autonomous AI systems
- AG.2.5 Tool Protocol Security for MCP, function calling
- ISO 42001 alignment document
- EU AI Act crosswalk
- Platform integration guide (Bedrock, Databricks, Foundry)
- Control selection guide
- Tube map visualisation
- Multiple architecture diagrams

### Changed
- Expanded risk tier definitions
- Enhanced HITL model documentation
- Improved Judge model selection guidance

## [0.1.0] - 2025-12-01

### Added
- Initial framework release
- Three-layer control model (Guardrails, Judge, HITL)
- AI control families AI.1-AI.16
- Risk tiering framework (CRITICAL/HIGH/MEDIUM/LOW)
- LLM-as-Judge pattern and operating model
- HITL operating model
- ISO 27001 alignment
- OWASP LLM Top 10 threat mapping
- Implementation guide
- Maturity model
- Example implementations (customer service, document assistant, credit decision)

## Categories

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes

