# Session & Scope for Agentic AI

> **Control Domain:** Agentic — Containment Controls  
> **Purpose:** Isolate agent sessions, limit blast radius, and prevent scope creep in autonomous AI operations.  
> **Extends:** IAM-06 (session-scoped credentials) and NET-01 (network zones) with agentic-specific depth.

---

## The Problem

An agent operating within a session accumulates context, credentials, data access, and decision history. Over time, a long-running agent session becomes a high-value target: it holds data from multiple tool calls, has active credentials, and has built a context window containing potentially sensitive information from across the session.

The longer a session runs, the greater the blast radius if compromised. Session isolation limits what an attacker can reach through any single compromised session.

---

## Control Objectives

| ID | Objective | Risk Tiers |
|----|-----------|------------|
| SESS-01 | Define and enforce session boundaries with automatic expiry | Tier 2+ (agentic) |
| SESS-02 | Isolate sessions from each other (no cross-session data leakage) | Tier 2+ (agentic) |
| SESS-03 | Limit the scope of each session to a declared task | Tier 2+ (agentic) |
| SESS-04 | Implement progressive trust within sessions | Tier 3+ (agentic) |
| SESS-05 | Clean up session state on termination | Tier 2+ (agentic) |

---

## SESS-01: Session Boundaries

Every agent session must have defined boundaries:

| Boundary | Enforcement |
|----------|-------------|
| **Time limit** | Maximum session duration (e.g., 30 minutes for Tier 3, 4 hours for Tier 2). Hard cutoff, not advisory. |
| **Token limit** | Maximum total tokens consumed across all model calls in the session. Prevents denial-of-wallet and runaway context accumulation. |
| **Action limit** | Maximum number of tool invocations per session. Prevents infinite loops and excessive automation. |
| **Scope boundary** | Session is scoped to a declared task. The agent cannot "pivot" to unrelated tasks within the same session. |
| **Credential expiry** | All session credentials expire with the session (IAM-06). No credential carry-over. |

When any boundary is reached, the session terminates gracefully: pending actions are cancelled (not auto-approved), the user is notified, and all session state is cleaned up (SESS-05).

---

## SESS-02: Session Isolation

Sessions must be isolated from each other. No data, credentials, context, or state from one session should be accessible to another.

### Isolation Requirements

- **Context isolation:** Agent A's session context (conversation history, tool results, intermediate reasoning) is not accessible to Agent B's session, even if they serve the same user.
- **Credential isolation:** Credentials issued for Session A cannot be used in Session B.
- **Memory isolation:** If the agent has persistent memory, session-specific data must be clearly separated from cross-session memory, and cross-session memory must not contain sensitive data from individual sessions.
- **Resource isolation:** For Tier 3+ systems, sessions run in separate compute contexts (containers, sandboxes) to prevent side-channel information leakage.

### What This Prevents

- A compromised session cannot pivot to access data from other sessions.
- An attacker who extracts context from one session cannot use it to authenticate in another.
- Cross-session data correlation attacks (where an attacker uses multiple sessions to reconstruct information that no single session should reveal).

---

## SESS-03: Scope Constraints

Each session should have a declared scope — the task it is permitted to accomplish.

### Scope Definition

| Element | Description |
|---------|-------------|
| **Task type** | What the session is doing (e.g., "answer customer query", "process expense report") |
| **Data domain** | What data the session can access (e.g., "customer record for user X only") |
| **Tool set** | Which tools are available in this session (subset of the agent's full manifest) |
| **Output type** | What the session can produce (e.g., "text response only", "response + database update") |
| **User context** | Who initiated the session and what permissions they carry |

### Scope Enforcement

The authorization gateway (IAM-04) enforces scope by:

- Restricting tool invocations to those relevant to the declared task.
- Filtering data queries to the declared data domain.
- Monitoring agent reasoning for scope drift (e.g., the agent starts discussing topics unrelated to the declared task).
- Terminating sessions that persistently attempt out-of-scope actions.

---

## SESS-04: Progressive Trust

For Tier 3+ systems, sessions should not start with full permissions. Instead, permissions increase as the session demonstrates expected behaviour.

### Trust Levels

| Level | Permissions | Triggers to Advance |
|-------|------------|---------------------|
| **Initial** | Read-only tool access, text response only | N successful interactions without guardrail flags |
| **Standard** | Full read access, reversible writes | No Judge flags, confirmed user identity |
| **Elevated** | Irreversible writes (with approval), external communications | Human reviewer approves elevation, explicit user request |

### Why Progressive Trust

- Limits the damage from injection attacks early in a session (before the agent has accumulated data or context).
- Forces attackers to maintain consistent benign behaviour before gaining access to destructive capabilities.
- Provides natural checkpoints where human oversight can intervene.

---

## SESS-05: Session Cleanup

When a session terminates (normally or abnormally), all session state must be cleaned up:

- **Credentials:** All session-scoped tokens revoked immediately.
- **Context:** Session context purged from memory (not just dereferenced — actively cleared).
- **Temporary data:** Any temporary files, cache entries, or intermediate results created during the session are deleted.
- **Tool connections:** Any open connections to backend tools are closed.
- **Audit record:** A session termination event is logged with: session duration, token consumption, tool invocation count, guardrail/Judge flags, and termination reason.

For abnormal termination (crash, timeout, forced kill), cleanup must still occur — design for crash-safe cleanup.

---

## Platform-Neutral Implementation Checklist

- [ ] Session boundaries defined (time, token, action, scope, credential expiry)
- [ ] Hard session termination on boundary breach (not advisory)
- [ ] Sessions isolated from each other (context, credentials, memory, resources)
- [ ] Session scope declared and enforced via authorization gateway
- [ ] Progressive trust implemented for Tier 3+ systems
- [ ] Session cleanup verified for normal and abnormal termination
- [ ] Session metadata logged for forensics and drift detection
- [ ] Cross-session data correlation attacks considered in threat model

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
