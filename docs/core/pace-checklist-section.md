# PACE Resilience Checklist

*Verification items for PACE resilience, organised by risk tier. Complete these before go-live and revalidate at the cadence specified for your tier.*

> *This document uses the simplified three-tier system (Tier 1/2/3). See [Risk Tiers — Simplified Tier Mapping](risk-tiers.md#simplified-tier-mapping) for the mapping to LOW/MEDIUM/HIGH/CRITICAL.*

---

## All Tiers — Pre-Deployment

These items apply to every AI system, regardless of risk tier.

### Fail Posture

- [ ] Fail posture (open or closed) defined for each control layer (Guardrails, Judge, Human Oversight)
- [ ] Fail posture documented in system runbook
- [ ] Fail posture decision reviewed and approved by system owner

### Fallback Path

- [ ] Non-AI fallback path identified (the process that continues the business function without AI)
- [ ] Fallback path documented (who does what, using what tools)
- [ ] Fallback path tested at least once before go-live
- [ ] Team aware that fallback path exists and how to activate it

### Recovery

- [ ] Recovery criteria defined for each control layer (what must be true before returning to normal)
- [ ] Recovery procedure documented in runbook

---

## Tier 1 — Low Risk

*Internal tools, content generation, employee productivity.*

### PACE Plan

- [ ] P (Primary) and A (Alternate) behaviour defined for each control layer (one sentence each)
- [ ] C (Contingency) and E (Emergency) combined statement: "Disable feature via [mechanism], revert to [manual process], contact [name]"
- [ ] PACE plan documented as paragraph in system runbook

### Testing (Annual)

- [ ] Fallback path still works (manual process can be executed)
- [ ] Feature disable mechanism works (feature flag, deployment rollback, or equivalent)
- [ ] At least one team member knows how to activate fallback
- [ ] Runbook entry reviewed and still accurate

---

## Tier 2 — Medium Risk

*Customer-facing content, decision support, document processing.*

### PACE Plan

- [ ] Full P/A/C/E defined for each control layer with specific behaviours at each level
- [ ] Transition triggers defined (measurable conditions for each state change)
- [ ] Automated transition mechanisms configured where possible (circuit breaker, health checks)
- [ ] Escalation contact list documented (primary and alternate for each control layer)
- [ ] Customer communication template pre-drafted for degraded service notification
- [ ] PACE plan documented as dedicated runbook section

### Fail-Closed Verification

- [ ] Guardrail failure results in traffic blocked (not passed)
- [ ] Judge failure results in outputs held for human review
- [ ] Human oversight unavailability results in conservative automated thresholds
- [ ] Circuit breaker health check is independent of AI system components

### Non-AI Fallback Path

- [ ] Rule-based or templated fallback system operational
- [ ] Fallback handles 100% of AI traffic at degraded quality
- [ ] Fallback does not depend on any AI infrastructure component
- [ ] Fallback activation is automated (circuit breaker)

### Testing (Quarterly)

- [ ] Guardrail failure simulation: system fails-closed correctly
- [ ] Judge failure simulation: outputs held or handled per PACE plan
- [ ] Human escalation exercise: flagged items reach reviewers within SLA
- [ ] Circuit breaker activation: non-AI fallback activates cleanly
- [ ] Fallback path operated with production-equivalent traffic
- [ ] Recovery procedure validated: step back up from fallback to normal
- [ ] Runbook entries reviewed and updated

### Testing (Semi-Annual)

- [ ] Full degradation walkthrough: P → A → C → E and recovery for at least one control layer
- [ ] Exercise involves same personnel and tools as real incident

---

## Tier 3 — High Risk

*Regulated decisions, autonomous agents with write access, financial/medical/legal domains.*

### PACE Plan

- [ ] Full P/A/C/E defined for each control layer with quantitative trigger criteria
- [ ] All transition triggers have automated monitoring and alerting
- [ ] Standalone operational resilience document created and reviewed by risk function
- [ ] Regulatory notification templates prepared and reviewed by legal
- [ ] Forensic evidence preservation automated (audit logs immutable, state snapshots configured)
- [ ] Recovery governance defined: sign-off chain for each step-back-up

### Fail-Closed Verification

- [ ] No AI traffic can pass a degraded control under any condition
- [ ] Circuit breaker activates automatically when triggered
- [ ] Circuit breaker cannot be overridden without documented authorisation
- [ ] Two or more layers at Emergency simultaneously triggers immediate circuit breaker

### Non-AI Fallback Path

- [ ] Staffed parallel process operational with trained operators
- [ ] Fallback handles critical subset of AI functions at production quality
- [ ] Fallback shares no infrastructure with AI system
- [ ] Fallback staffing model defined (who, how many, availability)

### Agentic Systems (if applicable)

- [ ] All five degradation phases defined (Normal, Constrained, Supervised, Bypassed, Full Stop)
- [ ] Trigger criteria defined for each phase transition
- [ ] Transaction resolution matrix completed for every tool in agent's permission set
- [ ] Multi-agent cascade prevention designed and tested (if multi-agent)
- [ ] State preservation automation validated (memory, context, plans, tool calls, Judge state)
- [ ] Agent cannot modify its own logs during phase transition
- [ ] Recovery step-back-up procedure defined with authorisation gates at each phase

### Testing (Monthly)

- [ ] Guardrail failure simulation: system fails-closed, no AI traffic passes
- [ ] Judge failure simulation: all traffic paused or held
- [ ] Circuit breaker activation: non-AI fallback activates within seconds
- [ ] Fallback path operated with production-equivalent traffic
- [ ] Recovery procedure validated
- [ ] Monitoring and alerting thresholds validated against current baselines

### Testing (Quarterly)

- [ ] Full degradation walkthrough: all five phases for agentic systems (or P → A → C → E for non-agentic)
- [ ] Exercise involves same personnel, tools, and communication channels as real incident
- [ ] Human escalation exercise with domain expert reviewers
- [ ] Transaction resolution matrix validated against current tool set
- [ ] Post-exercise review documented with lessons learned and plan updates

### Testing (Semi-Annual)

- [ ] Degradation walkthrough with regulator observation (where required)
- [ ] Full operational resilience document reviewed and updated
- [ ] Fallback staffing model reviewed against current team composition
- [ ] PACE plan alignment reviewed against regulatory changes

---

## Ongoing Maintenance — All Tiers

These items prevent PACE plan decay over time:

- [ ] PACE plan reviewed when any control layer is modified (guardrail rules updated, Judge model changed, reviewer pool changed)
- [ ] PACE plan reviewed when agent tool permissions change (agentic systems)
- [ ] Fallback path validated after any infrastructure change that could affect it
- [ ] New team members briefed on PACE plan and their role in it
- [ ] Departing team members' PACE responsibilities reassigned
- [ ] Lessons from any real degradation events incorporated into PACE plan

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
