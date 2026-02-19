# Agentic AI Controls

Additional controls for AI systems that take autonomous actions.

---

## What Makes Agents Different

| Characteristic | Chatbot | Agent |
|---------------|---------|-------|
| Actions | Responds only | Takes real-world actions |
| Autonomy | Single turn | Multi-step, self-directed |
| Scope | Fixed | May expand based on goals |
| Failure mode | Bad answer | Bad action with consequences |

**Key risk:** Agents can cause harm at machine speed without human review.

---

## The Two Core Problems

Agentic AI security reduces to two problems:

![The Two Core Problems](../images/agentic-two-problems.svg)

| Problem | Question | Failure Mode |
|---------|----------|--------------|
| **1. System Access** | Does the agent access only the right systems? | Reaches data/APIs it shouldn't |
| **2. Request Integrity** | Does the action match the user's actual intent? | Manipulated or misinterpreted requests |

### Problem 1: System Access

The agent should only reach systems it needs, with minimum necessary permissions. For the governance model, lifecycle, and threat landscape behind these controls, see [IAM Governance for AI Systems](iam-governance.md).

| Control | Implementation |
|---------|----------------|
| **Least-privilege credentials** | Agent gets tokens scoped to specific resources |
| **Network allowlists** | Agent can only reach approved endpoints |
| **Data views** | Database exposes only permitted subset |
| **Action allowlists** | Only pre-approved action types permitted |
| **Blast radius limits** | Maximum records, funds, or scope per action |

**Test:** If the agent is fully compromised, what's the worst it can do? Reduce that.

### Problem 2: Request Integrity

The action the agent takes should match what the user actually wanted.

| Threat | Control |
|--------|---------|
| **Injection attacks** | Input guardrails, tool output sanitisation |
| **Instruction drift** | Anchor to original request, not intermediate reasoning |
| **Misinterpretation** | Intent confirmation before irreversible actions |
| **Manipulation via tools** | Treat tool outputs as untrusted data |

**Test:** Can you trace from the user's original request to the final action? Is the link intact?

### Why Both Problems Matter

| Scenario | Access OK? | Integrity OK? | Outcome |
|----------|------------|---------------|---------|
| Normal operation | ✓ | ✓ | Correct action |
| Over-privileged agent | ✗ | ✓ | Correct action, but breach waiting to happen |
| Injection attack | ✓ | ✗ | Wrong action on right systems |
| Compromised agent | ✗ | ✗ | Catastrophic — wrong action, broad access |

Both problems must be solved. Solving one doesn't help if the other fails.

---

## Core Principle

**Infrastructure beats instructions.**

Don't tell the agent "only access customer service data."  
Give it credentials that can only access customer service data.

| Bad (Instruction) | Good (Infrastructure) |
|-------------------|----------------------|
| "Only access CS data" | Database view exposes only CS data |
| "Don't send emails without approval" | Email API requires approval token |
| "Stay within budget" | Hard spending cap at API gateway |

---

## Control Categories

### 1. Scope Enforcement

Limit what the agent can access and do — technically, not via prompts.

| Control | Implementation |
|---------|----------------|
| **Network allowlist** | Agent can only reach approved endpoints |
| **Data views** | Agent sees only authorised data subset |
| **Action allowlist** | Only permitted actions can execute |
| **Resource caps** | Hard limits on compute, API calls, cost |
| **Time limits** | Maximum execution duration |

### 2. Action Validation

Validate every action independently. Don't trust agent reasoning.

**Validation flow:**

![Action Validator Flow](../images/action-validator-flow.svg)

### 3. Tool Output Sanitisation

Tool outputs are injection vectors. Treat as untrusted.

| Control | Purpose |
|---------|---------|
| Scan for instructions | Detect "ignore previous" patterns |
| Truncate length | Limit context pollution |
| Mark as data | Clear framing that this is data, not instructions |
| Flag suspicious | Human review before continuing |

### 4. Approval Workflows

Make approval meaningful, not rubber-stamp.

| Bad | Good |
|-----|------|
| "Approve?" | Show context, data, impact, expected outcome |
| Approve/Deny only | Approve / Deny / Modify / Escalate |
| Same approver for all | Different approvers by action type |
| No expiry | Approval expires, must re-request |

### 5. Circuit Breakers

Hard stops that trigger regardless of agent "reasoning."

| Threshold | Action |
|-----------|--------|
| >100 actions in one task | Pause |
| >$50 in API calls | Pause |
| >30 minutes execution | Pause |
| >10% error rate | Pause |
| Any scope violation | Terminate |
| Any irreversible action | Require approval |

---

## Agent Risk Tiers

Agents are typically HIGH or CRITICAL tier. LOW/MEDIUM agents are rare.

| Agent Type | Typical Tier | Key Controls |
|------------|--------------|--------------|
| Read-only research | HIGH | Scope limits, output review |
| Internal automation | HIGH | Action allowlist, circuit breakers |
| Customer-facing | CRITICAL | Full approval workflow |
| Financial actions | CRITICAL | All controls, human approval |

---

## Judge for Agents

Agent interactions need deeper evaluation.

| Additional Criteria | Question |
|--------------------|----------|
| Goal alignment | Did agent pursue stated goal? |
| Action appropriateness | Were actions proportionate? |
| Scope adherence | Did agent stay in bounds? |
| Reasoning quality | Was the reasoning sound? |
| Efficiency | Did agent take unnecessary steps? |

---

## Monitoring

| Signal | Concern |
|--------|---------|
| Action volume spike | Runaway agent |
| Error rate increase | Agent confused or attacking |
| Novel action patterns | Unexpected behaviour |
| Scope boundary probes | Attempted breakout |
| Cost anomalies | Resource abuse |

---

## Recovery and Rollback

When integrity is compromised, you need to undo the damage.

| Capability | Purpose |
|------------|---------|
| **Action logging** | Full audit trail of what agent did (not just said) |
| **Reversibility windows** | Delay irreversible actions to allow intervention |
| **Automated rollback** | Undo actions when integrity breach detected |
| **Blast radius tracking** | Know exactly what was affected |

Not all actions are reversible. For those that aren't, require human approval.

---

## Key Takeaways

1. **Solve both problems** — Access control AND integrity preservation
2. **Enforce via infrastructure** — Agents can ignore instructions
3. **Validate every action** — Independent of agent reasoning
4. **Sanitise tool outputs** — They're injection vectors
5. **Use circuit breakers** — Hard stops that can't be reasoned around
6. **Require approval for impact** — Irreversible actions need humans
7. **Enable rollback** — Assume integrity will sometimes fail
8. **Monitor aggressively** — Agents can cause harm fast

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
