# The Long-Horizon Problem

*Securing an agent for one task is solved. Securing it over weeks and months is not.*

Most security evaluations test a single session. A prompt goes in. An output comes out. The guardrails fire or they don't. The Judge scores. The human reviews.

This models a world where agents are stateless. That world is disappearing.

Production agents run for days, weeks, months. They accumulate memory. They adapt to user patterns. They build context that spans hundreds of sessions. They interact with other agents whose behaviour evolves independently.

The security properties you validated on day one may not hold on day thirty.

## What Changes Over Time

### Memory accumulates - and so do vulnerabilities

[The Memory Problem](the-memory-problem.md) describes how persistent memory creates attack surfaces. The long-horizon dimension makes it worse. A memory poisoning attack doesn't need to succeed immediately. It can deposit small, benign-looking fragments across multiple sessions, assembling into a harmful instruction only when the right query activates the accumulated context.

No individual memory write looks malicious. The pattern is only visible across time.

### Behavioural baselines drift

Agents learn from interaction. Not through fine-tuning (usually), but through accumulated context, retrieved examples, and reinforced patterns. An agent that handles customer queries will gradually shift its response patterns based on the queries it receives and the feedback it gets.

This is expected. But it means the baseline you calibrated your anomaly detection against is a moving target. Slow, steady drift evades short-window detection. The agent at week twelve behaves differently from the agent at week one - and both might be "normal." The question is whether the drift trajectory is benign or being steered.

### Compound errors accumulate silently

A single-session error is observable: wrong output, flagged by the Judge, caught in review. A compound error across sessions is harder to see. The agent makes a slightly wrong assumption on Tuesday. That assumption enters memory. On Thursday, it informs a recommendation. On the following Monday, the recommendation shapes a decision. Each step looks reasonable in isolation. The chain produces harm.

This is the AI equivalent of normalization of deviance - the slow, invisible process by which an organisation accepts gradually degrading standards because each individual deviation from the norm is small. In long-running agents, normalization of deviance is automated.

### The attack surface expands with time

A single-session agent has a bounded attack surface: the current prompt, the current tools, the current data. A long-running agent accumulates surface: every past interaction that influenced its memory, every tool it has ever called, every data source it has ever retrieved from. The adversary has a wider window to find and exploit a vulnerability.

Time itself is an attack vector. The longer the agent runs, the more opportunities for poisoning, drift manipulation, and slow-burn exploitation.

## Why Short-Window Detection Misses This

The framework's anomaly detection ([OB-2.3](../maso/controls/observability.md)) uses a 7-day rolling baseline. This catches sudden changes - an agent that starts behaving differently this week compared to last week will trigger an alert.

But consider an adversary who shifts agent behaviour by 0.5% per week. In any 7-day window, the change is within normal variance. Over six months, the agent has drifted 13% from its original baseline - and the 7-day window never saw a statistically significant deviation because it was comparing against a baseline that was itself drifting.

This is why [OB-3.1](../maso/controls/observability.md) (Long-window behavioural analysis) exists at Tier 3: 30-day and 90-day trend analysis in addition to the 7-day rolling window. The "behavioural slow drift" attack pattern is the specific threat it addresses.

But even long-window detection has limits. If the baseline itself is recalculated from drifted data, the long window inherits the drift. The detection requires an anchored reference point - a snapshot of the agent's behaviour at a known-good state - that is preserved independently of the rolling baseline.

## The Named Threat Patterns

Long-horizon security risks are not a single threat. They are a category that contains distinct patterns:

| Pattern | Mechanism | Detection Difficulty |
|---------|-----------|---------------------|
| **Slow memory poisoning** | Small, benign-looking memory fragments deposited across sessions that assemble into a harmful instruction | High - no individual write is malicious |
| **Baseline drift manipulation** | Adversary gradually shifts agent behaviour to evade rolling-window anomaly detection | High - each window shows normal variance |
| **Compound error chains** | Small errors accumulate across sessions, each one within tolerance, producing cumulative harm | High - each step passes individual evaluation |
| **Dormant payload activation** | Instruction injected early, activated by a specific trigger condition that may not occur for weeks | Very high - payload is invisible until activation |
| **Trust escalation over time** | Agent accumulates trust signals (successful interactions, positive feedback) that reduce oversight scrutiny, then exploits the reduced scrutiny | Medium - detectable if trust-level is monitored |
| **Cross-agent temporal coordination** | Multiple agents independently shift behaviour over time, converging on a coordinated malicious action | Very high - requires cross-agent temporal correlation |

## What the Framework Provides - and What's Missing

### Already covered

The framework addresses long-horizon risk across several controls:

- **Memory controls** ([Memory and Context](../core/memory-and-context.md)): Session isolation, context hygiene, memory expiration, periodic full-context evaluation.
- **Drift detection** ([OB-2.3](../maso/controls/observability.md)): 7-day rolling baseline with >2σ alerting.
- **Long-window analysis** ([OB-3.1](../maso/controls/observability.md)): 30-day and 90-day trend analysis at Tier 3.
- **Cross-agent correlation** ([OB-3.4](../maso/controls/observability.md)): Coordinated anomaly detection across agents at Tier 3.
- **Independent observability** ([OB-3.3](../maso/controls/observability.md)): Separate monitoring agent on separate infrastructure.

### The gap: anchored baselines and insider risk monitoring

The controls assume the baseline is trustworthy. If the baseline drifts, the anomaly detection drifts with it. And the current signals - while comprehensive for short-window detection - miss temporal and peer-group patterns that insider risk programs have been catching for over a decade. An agent that starts operating at weekends when it has no weekend triggers, or one agent in a fleet that diverges while its peers remain stable, should generate alerts through the same UEBA (User and Entity Behavior Analytics) mechanisms that flag compromised human accounts. See [The Insider Risk Parallel](behavioral-anomaly-detection.md#the-insider-risk-parallel) for the full mapping.

Long-horizon security requires:

**Anchored reference points.** Capture a behavioural snapshot at a known-good state (post-deployment validation, post-audit). Preserve it independently. Compare not just against the rolling baseline but against the anchor. If the rolling baseline has diverged significantly from the anchor, that itself is an alert - even if week-over-week change is within tolerance.

**Periodic re-validation against original acceptance criteria.** The tests that validated the agent for deployment should be re-run periodically - not just when the model changes, but on a calendar schedule. An agent that passed acceptance testing six months ago should still pass those same tests today. If it doesn't, something has changed.

**Memory state auditing.** Beyond monitoring memory writes, periodically audit the *accumulated* memory state. Does the current memory contain instructions, beliefs, or patterns that weren't present at deployment? Is the memory internally consistent? Does it contain content that, if injected as a prompt, would trigger guardrails?

## Research Context

Long-horizon security is identified as a distinct challenge across recent agentic AI security research.

[Datta, Nahin, Chhabra, and Mohapatra (2025)](https://arxiv.org/abs/2510.23883) explicitly name it as an open problem: "Securing an agent during a single task is one thing. Securing it over weeks or months as it learns and adapts is another challenge entirely." Their survey documents memory poisoning as a stealthy long-term attack vector and identifies the adversarial arms race - where defenders face adaptive, evolving attacks - as a challenge that intensifies with time. They also note that current evaluation benchmarks (AgentDojo, InjectAgent, ASB) test short trajectories with an average length of only three steps, leaving long-horizon defence effectiveness unmeasured.

[Arora and Hastings (2025)](https://arxiv.org/abs/2512.18043) address the lifecycle dimension through their MAAIS framework, which structures security across development, deployment, operations, and governance phases. Their lifecycle-aware approach implicitly acknowledges that security properties established at deployment must be maintained through operations - though their framework focuses more on the structural layers than on temporal degradation patterns.

[Dal Cin, Kendzior, Seedat, and Marinho (2025)](https://www.proquest.com/openview/d82e8ca1463253c1aeaf55c6dde38841/1?pq-origsite=gscholar&cbl=6831990) document runtime protections as one of their three essentials, noting that continuous monitoring and anomaly detection are necessary complements to pre-deployment testing. Their healthcare case study - where AI agents operate across OCR, LLMs, cloud APIs, and billing systems - illustrates the kind of long-running, multi-system workflow where temporal security degradation is most likely to occur.

## The Uncomfortable Implication

Long-horizon security means that "the system passed testing" has an expiry date. The confidence you have in the agent's security posture degrades over time unless you actively maintain it.

This is not unique to AI. It's how every complex system works. Aircraft don't stay airworthy because they passed certification once - they stay airworthy because they're inspected, tested, and maintained on recurring schedules. The certification establishes the baseline. Continuous maintenance preserves it.

For AI agents, the maintenance model is less mature. We test before deployment. We monitor in real-time. But the systematic, scheduled re-validation of long-running agents against their original security posture is not yet standard practice.

It should be.

## Related

- [The Memory Problem](the-memory-problem.md) - Long context and persistent memory as attack surfaces
- [Behavioral Anomaly Detection](behavioral-anomaly-detection.md) - Aggregating signals to detect drift
- [Observability Controls](../maso/controls/observability.md) - Drift detection, long-window analysis, cross-agent correlation
- [Memory and Context Controls](../core/memory-and-context.md) - Session isolation, context hygiene, memory governance
- [Process-Aware Evaluation](process-aware-evaluation.md) - Evaluating the trace, not just the output

