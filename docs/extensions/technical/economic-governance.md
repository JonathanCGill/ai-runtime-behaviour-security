# Economic Governance

> You can't govern what you don't meter. AI costs are non-deterministic — treat them like risk, not like infrastructure.

## The Problem

Traditional software costs are predictable: compute scales linearly, storage costs are forecastable, and API calls have fixed prices. AI systems break all of these assumptions.

LLM inference costs depend on input length, output length, model selection, and — increasingly — reasoning tokens that are invisible without instrumentation. Agentic systems compound the problem: autonomous agents retry, reformulate, and chain tool calls in patterns that make per-task costs unpredictable. A single agent loop can consume thousands of API calls before anyone notices.

The result is a new class of operational risk: **economic risk from uncontrolled AI runtime behaviour.**

This isn't hypothetical. IDC's 2025 survey found that 92% of decision-makers reported AI agent costs higher than expected. The Greyhound CIO Pulse 2025 found that 68% of digital leaders experienced major budget overruns during initial agent deployments, with nearly half attributing overruns to runaway tool loops and recursive logic. Gartner predicts that over 40% of agentic AI projects will fail to reach production by 2027, driven by cost and complexity.

The framework's [Cost & Latency](cost-and-latency.md) guide covers how to budget for security controls. This document covers a different problem: **how to govern AI economics at runtime** — monitoring spend, enforcing budgets, and preventing runaway costs before they become incidents.

---

## Why This Is a Security Problem

Economic governance is not just a finance concern. Uncontrolled AI spending creates security-relevant risks:

| Risk | How It Manifests | Security Impact |
|------|-----------------|-----------------|
| **Resource exhaustion** | Agent loops or prompt injection cause excessive API calls | Denial of service through cost, not traffic |
| **Budget-driven shortcuts** | Teams disable controls to reduce costs | Security controls bypassed to stay within budget |
| **Adversarial cost inflation** | Attacker crafts inputs that maximise token consumption | Financial denial-of-service (FDoS) |
| **Shadow AI spend** | Teams use unmonitored AI services to avoid governance | Ungoverned AI systems with no controls |
| **Model downgrade pressure** | Cost pressure forces use of cheaper, less capable models | Judge and guardrail effectiveness reduced |

Financial denial-of-service is an emerging threat class. An attacker who can trigger expensive model calls — through prompt injection that causes verbose output, or inputs that trigger agent retry loops — can inflict economic harm without exfiltrating data or compromising systems.

---

## The Economic Governance Model

Economic governance for AI runtime requires four capabilities:

```
Meter → Attribute → Enforce → Optimise
```

### 1. Meter: Know What You're Spending

You cannot govern what you cannot see. Every AI interaction must be instrumented for cost:

| Telemetry Point | What to Capture | Why It Matters |
|----------------|----------------|----------------|
| **Token usage** | Input tokens, output tokens, reasoning tokens (where applicable) | Basis for cost calculation |
| **Model selection** | Which model served each request | Different models have 50x cost differences |
| **Tool calls** | Number and type of external tool invocations | Agentic systems chain tool calls with compounding cost |
| **Retry count** | Number of retries per task | Retries are the primary driver of runaway spend |
| **Latency** | Time per request and total task duration | Correlates with cost; long-running tasks signal loops |
| **Cache hits** | Requests served from cache vs. fresh inference | Validates cost optimisation effectiveness |

**Integration with existing telemetry.** The framework's [Runtime Telemetry Reference](runtime-telemetry-reference.md) defines the observability baseline. Economic telemetry should be captured alongside security telemetry — same pipeline, same dashboards, same alerting infrastructure. Cost anomalies and security anomalies often share the same root cause.

### 2. Attribute: Know Who's Spending It

Visibility without attribution doesn't change behaviour. Every AI cost must be attributable to a specific dimension:

| Attribution Dimension | Purpose | Example |
|----------------------|---------|---------|
| **Application** | Which AI system incurred the cost | Customer service bot vs. fraud detection |
| **Team / business unit** | Who owns the spend | Engineering, operations, marketing |
| **User / session** | Which end-user or session triggered the cost | Per-user cost tracking for abuse detection |
| **Feature** | Which capability within an application | Search vs. summarisation vs. decision support |
| **Risk tier** | Cost segmented by risk classification | Tier 3 systems should cost more (they have more controls) |
| **Control layer** | Cost of security controls vs. primary inference | Generator cost vs. judge cost vs. guardrail cost |

**Why control-layer attribution matters.** Without it, security controls become the first target when cost pressure arrives. If leadership sees "AI costs are over budget" without understanding that 30% is security controls, the response is often to reduce controls rather than optimise inference. Separating generator costs from security costs protects the control framework from budget-driven erosion.

### 3. Enforce: Stop Spending Before It's a Problem

Monitoring alone is insufficient. Economic governance requires enforcement — automated mechanisms that prevent budget overruns before they occur.

#### Graduated Budget Responses

Do not jump straight to blocking requests when budgets are approached. Use graduated responses:

| Budget Threshold | Response | Example Action |
|-----------------|----------|---------------|
| **50%** of period budget | **Alert** | Notify cost owner via dashboard and email |
| **75%** of period budget | **Warn** | Alert escalation to team lead; increase monitoring frequency |
| **90%** of period budget | **Throttle** | Reduce sampling rates; route to cheaper models for non-critical requests |
| **95%** of period budget | **Degrade** | Disable non-essential features; queue non-urgent requests |
| **100%** of period budget | **Hard stop** | Block new requests; serve cached responses where possible |

#### Enforcement Mechanisms

| Mechanism | What It Does | When to Use |
|-----------|-------------|-------------|
| **Per-request token caps** | Limits `max_tokens` per individual request | Always — prevents single requests from consuming excessive budget |
| **Per-session budget** | Caps total spend within a single user session | Agentic systems where sessions can run for extended periods |
| **Per-user daily/monthly limits** | Prevents individual users from consuming disproportionate budget | Multi-tenant systems; abuse prevention |
| **Per-application budget** | Hard ceiling on total spend per application per period | Portfolio-level cost governance |
| **Agent loop detection** | Detects and terminates repetitive agent behaviour | Agentic systems — the primary runaway cost driver |
| **Circuit breaker** | Automatically halts AI processing when cost rate exceeds threshold | Emergency protection against cost spikes |

#### The Agent Loop Problem

Agentic AI introduces the most significant economic governance challenge. Unlike single-request systems, agents persist — retrying, reformulating, and chaining operations. A single poorly-constrained agent can generate hundreds of model calls for one task.

Runtime controls for agent economics:

| Control | Implementation |
|---------|---------------|
| **Maximum iterations per task** | Hard limit on agent retry/reformulation cycles (e.g., 10 iterations) |
| **Maximum tool calls per session** | Cap on external tool invocations per agent session |
| **Token budget per task** | Total token budget allocated to complete a single task |
| **Cost-per-step monitoring** | Track cost accumulation per agent step; alert on acceleration |
| **Diminishing returns detection** | Detect when additional iterations aren't improving outcomes; terminate early |
| **Recursive call depth limits** | Prevent agents from spawning unbounded sub-agent chains |

Google's Budget Tracker and BATS framework (2025) introduces budget awareness directly into the agent decision loop — giving agents real-time feedback about what they've spent, what's left, and what's worth doing next. This approach treats budget as a first-class input to agent reasoning, not an external constraint applied after the fact.

### 4. Optimise: Spend Effectively, Not Less

Cost optimisation is not cost reduction. The goal is maximum security and business value per unit of spend.

| Optimisation Strategy | How It Works | Typical Savings |
|----------------------|-------------|-----------------|
| **Tiered model routing** | Route simple requests to cheaper models; reserve expensive models for complex tasks | 40–60% |
| **Prompt optimisation** | Reduce input token count through concise prompting | 10–30% |
| **Response caching** | Cache identical or semantically similar responses (Tier 1 only — see [Cost & Latency](cost-and-latency.md)) | 5–30% |
| **Adaptive sampling** | Adjust judge evaluation frequency based on risk signals (see [Cost & Latency](cost-and-latency.md)) | 20–40% |
| **Batch processing** | Aggregate non-urgent requests for batch inference at lower cost | 30–50% |
| **Token-aware rate limiting** | Limit by tokens consumed, not requests made — prevents heavy prompts from consuming disproportionate budget | Variable |

**Critical principle: never optimise security controls to meet budget.** If the budget doesn't support the required control intensity for the risk tier, the correct response is to reduce the system's scope or autonomy (lowering the risk tier), not to weaken controls. This is a governance decision, not an engineering one.

---

## Budget Governance by Risk Tier

Economic governance intensity should match risk tier, just like security controls:

| Dimension | Tier 1 (Low) | Tier 2 (Medium) | Tier 3 (High) | Tier 4 (Critical) |
|-----------|-------------|-----------------|---------------|-------------------|
| **Budget monitoring** | Monthly review | Weekly review | Daily review | Real-time |
| **Cost attribution** | Per-application | Per-application, per-team | Per-application, per-team, per-feature | Per-request |
| **Budget enforcement** | Soft alerts only | Graduated responses | Hard limits with circuit breakers | Hard limits, circuit breakers, automatic degradation |
| **Anomaly detection** | Manual review | Threshold-based alerts | Statistical anomaly detection | ML-based anomaly detection with automated response |
| **Reporting** | Monthly cost report | Weekly cost report with variance analysis | Daily cost report with forecasting | Real-time dashboard with predictive alerts |
| **Governance approval** | Annual budget | Quarterly review | Monthly review with variance justification | Weekly review; real-time escalation for overruns |

---

## FinOps for AI: What's Different

The FinOps Foundation's 2026 State of FinOps report found that 98% of respondents now manage AI spend (up from 63% in 2025 and 31% in 2024). AI cost governance has moved from emerging concern to mainstream operational requirement in two years.

However, AI FinOps is not cloud FinOps. Traditional cloud cost management assumptions break down:

| Cloud FinOps Assumption | Why AI Breaks It |
|------------------------|-----------------|
| **Costs scale linearly with usage** | Agent retry loops and reasoning tokens create non-linear cost curves |
| **Resource usage is predictable** | Same prompt can cost 10x more depending on model reasoning path |
| **Idle resources are the main waste** | Active AI systems waste through inefficient prompting, unnecessary retries, and over-provisioned model selection |
| **Cost allocation maps to infrastructure** | AI costs map to business outcomes — cost per resolved ticket, not cost per GPU hour |
| **Monthly billing cycles are sufficient** | AI cost spikes happen in minutes, not months |

### Cost-Per-Outcome Thinking

Mature AI economic governance tracks cost per business outcome, not cost per API call:

| Metric | What It Measures | Why It Matters |
|--------|-----------------|----------------|
| **Cost per resolved interaction** | Total AI cost to resolve one customer query | Enables comparison with human-only cost |
| **Cost per decision** | AI cost to produce one actionable recommendation | Determines whether AI adds value vs. alternatives |
| **Security cost ratio** | Control cost as percentage of total AI cost | Tracks whether security overhead is proportionate |
| **Cost per risk tier** | Average interaction cost segmented by tier | Validates that higher-risk systems cost more (they should) |
| **Cost variance coefficient** | Standard deviation of per-interaction cost | Measures predictability — high variance signals governance gaps |

---

## The Financial Denial-of-Service Threat

Financial denial-of-service (FDoS) deserves specific attention as an emerging threat class:

### Attack Vectors

| Vector | Mechanism | Impact |
|--------|-----------|--------|
| **Verbose prompt injection** | Crafted input that causes model to generate maximum-length output | Maximises output token cost per request |
| **Agent loop triggering** | Input designed to cause repeated agent retries without resolution | Multiplies cost through iteration |
| **Complex reasoning provocation** | Prompts that trigger extended chain-of-thought in reasoning models | Reasoning tokens consumed without producing useful output |
| **Distributed low-rate attacks** | Many users each triggering slightly-above-normal costs | Bypasses per-user limits while exceeding aggregate budget |
| **Tool call amplification** | Input that causes agent to invoke expensive external tools repeatedly | Compounds cost across multiple services |

### Defences

| Defence | Mechanism |
|---------|-----------|
| **Per-request cost ceiling** | Hard `max_tokens` limit on every request |
| **Per-user cost rate limiting** | Token-aware rate limits (not just request count) |
| **Agent iteration caps** | Maximum retry/reformulation cycles per task |
| **Cost anomaly detection** | Statistical detection of cost patterns deviating from baseline |
| **Circuit breaker** | Automatic halt when cost rate exceeds threshold |
| **Input complexity analysis** | Pre-screening inputs for characteristics associated with high-cost responses |

---

## Integration with Existing Controls

Economic governance is not a standalone function. It integrates with existing framework controls:

| Framework Component | Economic Governance Integration |
|--------------------|-------------------------------|
| **Guardrails** | Input guardrails can reject inputs likely to trigger high-cost responses (complexity screening) |
| **Judge** | Judge evaluation costs must be tracked separately; judge sampling rates are an economic governance lever |
| **Circuit Breaker** | Extend circuit breaker criteria to include cost thresholds, not just safety thresholds |
| **Observability** | Economic telemetry uses the same pipeline as security observability |
| **Risk Tiers** | Economic governance intensity scales with risk tier |
| **PACE Resilience** | Budget exhaustion is a failure mode requiring PACE-style resilience planning |
| **Incident Response** | Cost overruns may require incident response procedures — especially if caused by adversarial action |

---

## Governance Operating Model

Economic governance requires clear roles and responsibilities:

| Role | Responsibility |
|------|---------------|
| **AI Product Owner** | Sets budget for their AI system; accountable for cost-per-outcome |
| **AI Engineering** | Implements cost metering, attribution, and enforcement mechanisms |
| **FinOps / Finance** | Provides budget allocation, forecasting, and variance analysis |
| **Security** | Monitors for FDoS, ensures cost pressure doesn't degrade security controls |
| **AI Governance Committee** | Approves budget exceptions; reviews cost-vs-risk tradeoffs |

### Decision Rights

| Decision | Who Decides |
|----------|------------|
| Total AI budget allocation | Finance + Leadership |
| Budget per application | AI Product Owner + Finance |
| Model selection (cost/capability tradeoff) | AI Engineering + Product Owner |
| Security control budget (non-negotiable by tier) | AI Governance Committee |
| Budget exception requests | AI Governance Committee |
| Emergency cost circuit breaker threshold | Security + AI Engineering |

---

## Implementation Checklist

### Phase 1: Visibility (Weeks 1–4)

- [ ] Instrument all AI API calls for token usage and cost capture
- [ ] Implement cost attribution by application and team
- [ ] Create a cost dashboard with daily aggregation
- [ ] Establish baseline cost patterns for each AI system
- [ ] Separate security control costs from primary inference costs

### Phase 2: Governance (Weeks 5–8)

- [ ] Define budget allocations per application and risk tier
- [ ] Implement graduated budget alerts (50%, 75%, 90% thresholds)
- [ ] Establish cost reporting cadence (aligned to risk tier)
- [ ] Define cost escalation procedures
- [ ] Document cost-per-outcome metrics for each AI system

### Phase 3: Enforcement (Weeks 9–12)

- [ ] Implement per-request token caps
- [ ] Deploy agent loop detection and iteration limits
- [ ] Configure circuit breakers for cost rate spikes
- [ ] Implement per-user and per-session budget limits
- [ ] Test graduated response mechanisms (alert → throttle → degrade → stop)

### Phase 4: Optimisation (Ongoing)

- [ ] Implement tiered model routing based on request complexity
- [ ] Deploy response caching where risk-appropriate
- [ ] Optimise prompts for token efficiency
- [ ] Review cost-per-outcome trends monthly
- [ ] Conduct quarterly cost-vs-risk tier alignment reviews

---

## Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| **Cost variance vs. budget** | ±10% | >25% |
| **Cost per interaction (by tier)** | Within budget | >120% of budget |
| **Security cost ratio** | 15–40% (Tier 2), 40–100% (Tier 3) | Dropping below expected range (may indicate control erosion) |
| **Agent cost predictability** | CV < 0.3 | CV > 0.5 |
| **Budget utilisation** | 70–90% | <50% (underutilised) or >95% (at risk) |
| **FDoS incidents** | 0 | Any |
| **Cost-driven control exceptions** | 0 | Any |

---

## What This Doesn't Cover

- **Procurement and licensing costs.** This document covers runtime economics, not vendor selection or contract negotiation.
- **Infrastructure capacity planning.** See platform-specific guidance in [Platform Patterns](../../infrastructure/reference/platform-patterns/aws-bedrock.md).
- **Build-phase costs.** Development, training, and fine-tuning costs are project costs, not runtime governance. The framework's [Business Alignment](../../strategy/business-alignment.md) covers build-vs-run cost analysis.
- **Cost modelling for the security control layers.** See [Cost & Latency](cost-and-latency.md) for detailed control cost analysis.

---

## References

- FinOps Foundation, "FinOps for AI Overview" (2025) — [finops.org/wg/finops-for-ai-overview](https://www.finops.org/wg/finops-for-ai-overview/)
- FinOps Foundation, "State of FinOps 2026" — [data.finops.org](https://data.finops.org/)
- Google, "Budget Tracker and BATS Framework" (2025) — budget-aware agent cost governance
- IDC FutureScape 2026 — AI infrastructure cost underestimation projections
- NIST AI Risk Management Framework (AI RMF 1.0) — economic harm categories and continuous monitoring — [nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)
- OECD, "Governing with Artificial Intelligence" (2025) — [oecd.org](https://www.oecd.org/en/publications/2025/06/governing-with-artificial-intelligence_398fa287/full-report.html)
- Gartner — AI agent production failure predictions; AI strategy ROI findings

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
