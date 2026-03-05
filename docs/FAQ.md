---
description: Honest answers to the questions practitioners actually ask about AI runtime security - cost, resources, practicality, and scale.
---

# Frequently Asked Questions

Honest answers to the questions we hear most.

## "Do we actually need AI for this?"

Ask this question before anything else. Seriously.

If a process can be solved with RPA, a rules engine, or straightforward code, that's almost certainly the better option. It's cheaper to build, cheaper to run, and cheaper to secure. Every AI system you deploy brings runtime behaviour you need to monitor, guardrails you need to tune, and risks you need to manage. If you don't need a model making decisions, don't introduce one just because you can.

AI earns its place when the problem genuinely requires language understanding, reasoning over unstructured data, or handling inputs that can't be reduced to deterministic rules. If you're automating a form submission or routing tickets based on keywords, you don't need a large language model. You need a script.

Getting this decision right is the single most effective way to reduce your AI security workload. The safest AI system is the one you didn't need to build.

## "Can this framework tell me which model to use?"

No. And nothing can - reliably.

LLMs are built by specialist companies that retain the weights of their models. You cannot inspect a closed-weight model to determine what it's capable of. Open-weight models let you download the parameters, but billions of weights don't yield to human inspection either. In both cases, the model is a black box.

Worse, even the developers don't fully know what their models can do. Research has shown that frontier models can strategically underperform during safety evaluations - a behaviour called [sandbagging](insights/evaluation-integrity-risks.md) - and that there is essentially no correlation between model capability and safeguard robustness. The tools used to evaluate models are vulnerable to the very models being evaluated.

This framework accepts that opacity as a given. It cannot help you choose the right model - but it can monitor what the model actually does, constrain its actions to what your use case requires, and detect when behaviour drifts from baseline. That is why runtime monitoring exists: not because AI is dangerous by default, but because it is unpredictable by design. See [You Don't Know What You're Deploying](insights/you-dont-know-what-youre-deploying.md) for the full argument.

## "This feels expensive."

It can be. But it doesn't have to start that way.

Guardrails can be enabled in managed services like AWS Bedrock, Azure AI Content Safety, or Databricks with minimal configuration. You're not building from scratch - you're turning on capabilities that already exist in the platforms you're paying for. On Bedrock, for example, you can enable content filtering and PII detection without writing new code. These filters run inline with model invocations and generate logs you can route to CloudWatch automatically.

A Judge layer doesn't need to evaluate every interaction. Sample 5% of traffic on a medium-risk system and you've got meaningful oversight at a fraction of the cost of 100% coverage. Scale up only where the risk justifies it.

## "We don't have the resources."

You don't need a dedicated AI security team to start.

Turn on platform guardrails. That's configuration, not engineering. Enable logging through CloudTrail, CloudWatch, or your platform's equivalent - most of this telemetry is already being generated, you just need to look at it. Assign a system owner to review flagged interactions for 30 minutes a week.

That's a starting point, not the finish line. Over time, introduce sampled judge evaluations and human edge-case reviews as your adoption and risk appetite grow. You don't need full maturity on day one - you need a direction of travel.

The [Quick Start](QUICK_START.md) guide is designed to get you from zero to working controls in 30 minutes with what you already have.

## "Does this work in practice?"

The three-layer pattern - Guardrails, Judge, Human Oversight - is where the industry is converging. Guardrails block known-bad patterns in real time. Judges catch what guardrails miss through asynchronous evaluation. Humans decide the edge cases that machines shouldn't.

Does every layer work perfectly? No. Guardrails need tuning to reduce false positives. Judges need calibration against your specific use case. Humans need clear escalation paths or they become a bottleneck.

Concretely: a guardrail that blocks prompt injection patterns will catch the obvious attacks on day one. After a week of reviewing logs, you tune it to reduce false positives on legitimate queries that happen to contain code snippets. That iteration cycle is exactly how these controls mature in production.

## "Do we really need judges everywhere?"

No. You don't.

Judges add latency and cost. Put them where the **risk of errors outweighs the cost of evaluation** - not everywhere.

A low-risk internal FAQ bot? Guardrails and logging are probably enough. A system making credit decisions or generating customer-facing communications at scale? That's where judge evaluation earns its keep.

Match the control to the risk. The [Risk Tiers](core/risk-tiers.md) framework exists precisely to help you make this call.

## "When do we actually need humans in the loop?"

At minimum, where regulations require it. The EU AI Act, financial services regulations, and sector-specific rules increasingly mandate human oversight for high-risk AI systems. That's your compliance baseline.

Beyond that, humans are needed where the consequences of errors are serious and irreversible - decisions affecting people's rights, health, or finances. Humans don't scale, so use them where they matter most: reviewing edge cases, calibrating controls, and making decisions that carry accountability.

The framework's [Human Factors](strategy/human-factors.md) page goes deeper on where human oversight adds genuine value versus where it becomes theatre.

## "Is this a compliance checklist?"

No. This framework is designed to **provoke thought** about AI runtime risks, not prescribe a rigid set of mandatory controls.

Realistically, only the most high-risk AI use cases need a full set of controls. A low-risk internal tool doesn't need the same governance as an autonomous agent making financial decisions. Treating everything the same wastes resources and creates compliance fatigue.

Adopt a **risk-aligned approach**. Look at your use cases, assess the risks, and enable what's needed and practical for your organisation. The controls exist as a menu, not a mandate.

## "What about normal security controls?"

This framework focuses on AI-specific runtime behaviour. It doesn't replace your existing information security foundations - it depends on them.

Access controls, network segmentation, firewalls, zero-trust architecture, identity management, encryption at rest and in transit - all of these still apply to AI systems, and arguably matter more. A model endpoint without proper authentication is a bigger problem than one without a judge layer. A RAG pipeline pulling from a data store with weak access controls has a data quality and data security problem before it has an AI behaviour problem.

The same risk-aligned approach applies here. Not every AI deployment needs the same level of infrastructure hardening, but every one needs the basics. Get these right and you reduce the workload on your AI-specific controls significantly. Get them wrong and no amount of guardrails or judges will save you.

## "How do we know what's actually happening in our AI systems?"

Use the data your AI systems already provide.

CloudTrail logs API calls. CloudWatch captures metrics and operational data. Bedrock provides invocation logging. Azure AI has diagnostic logs. Databricks has audit logs and model serving metrics. Your platform is generating telemetry - the question is whether anyone is looking at it.

Start by turning on what's available. Establish baselines. Look for anomalies. You don't need a custom observability platform on day one. You need eyes on the data your systems are already producing.

The [Logging & Observability](infrastructure/controls/logging-and-observability.md) controls and [Runtime Telemetry Reference](extensions/technical/runtime-telemetry-reference.md) provide practical starting points.

## "Does this scale?"

Honestly? I don't know yet. I believe it can.

The patterns - guardrails as automated first-line defence, sampling-based judge evaluation, risk-tiered human oversight - are designed to scale. Guardrails operate at the request level with minimal latency. Judges can be asynchronous and sampled. Human review focuses on the long tail of edge cases, not every interaction.

But the evidence base for AI runtime security at true enterprise scale is still emerging. We're all learning.

## "Is this framework finished?"

No. And it may never be in the traditional sense.

The threat landscape for AI systems is evolving rapidly. New model capabilities, new attack patterns, and new regulatory requirements emerge regularly. A finished framework would be an outdated one.

What exists today is a working structure for thinking about and implementing AI runtime controls. It's actively developed and designed to evolve as the field matures.

## "I've solved some of these problems. Should I share?"

Yes. Please.

This framework doesn't have all the answers. If you've found practical solutions to AI runtime security challenges, the community benefits from your experience.

- **Raise an issue** when something doesn't make sense or doesn't match your reality
- **Submit a PR** with a correction, a new pattern, or a better idea
- **Point out where this doesn't match reality** - that's how the framework improves

See the [Contributing](CONTRIBUTING.md) guide or open an issue on [GitHub](https://github.com/JonathanCGill/ai-runtime-behaviour-security).

## "Can I use this for my own work?"

Absolutely. This framework is [MIT licensed](https://github.com/JonathanCGill/ai-runtime-behaviour-security). Copy it, fork it, adapt it, build on it, or disagree with the entire approach and publish something better. No permission needed.

AI security is too important to gatekeep.

## Where to Go Next

| Question | Start Here |
|----------|-----------|
| How do I get started quickly? | [Quick Start](QUICK_START.md) |
| What controls do I actually need? | [Risk Tiers](core/risk-tiers.md) |
| What does implementation look like? | [Worked Examples](extensions/examples/README.md) |
| How do guardrails work in practice? | [Practical Guardrails](insights/practical-guardrails.md) |
| What about multi-agent systems? | [MASO Framework](maso/README.md) |

