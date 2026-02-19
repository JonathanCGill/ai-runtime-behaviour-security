# References & Sources

**This framework builds on the work of researchers, practitioners, standards bodies, and organisations who are defining the field of AI security. This page credits their contributions and provides links to the primary sources.**

---

## Industry Frameworks & Standards

These are the established frameworks that inform the architecture, control design, and risk classification used throughout this project. Where this framework extends or diverges from them, the relevant sections note this explicitly.

### NIST AI Risk Management Framework (AI RMF 1.0)

The foundational U.S. government framework for managing AI risks, organised around four core functions: Govern, Map, Measure, Manage. Released January 2023. Increasingly referenced by federal regulators (CFPB, FDA, SEC, FTC, EEOC) and aligned with the EU AI Act, OECD AI Principles, and the G7 Code of Conduct.

This framework's risk tier classification and governance structure align with NIST AI RMF's four functions.

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### NIST AI 600-1: Generative AI Profile

A companion to the AI RMF specifically addressing generative AI risks — data memorisation/leakage, confabulations (hallucinations), training data poisoning, and prompt injection. Published July 2024, developed pursuant to Executive Order 14110.

This framework's treatment of prompt injection and hallucination as distinct control domains draws on the risk categories defined here.

- [NIST AI 600-1 (PDF)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

### OWASP Top 10 for LLM Applications (2025)

The practitioner-oriented ranking of LLM security risks: (1) Prompt Injection, (2) Sensitive Information Disclosure, (3) Supply Chain Vulnerabilities, (4) Data and Model Poisoning, (5) Improper Output Handling, (6) Excessive Agency, (7) System Prompt Leakage, (8) Vector and Embedding Weaknesses, (9) Misinformation, (10) Unbounded Consumption.

This framework provides full mapping against all ten risks across both the foundation layer and MASO. The 2025 additions of "Excessive Agency" and "Vector and Embedding Weaknesses" directly validate the control domains we define for execution control and data protection.

- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)

### OWASP Top 10 for Agentic Applications (2026)

The emerging companion to the LLM Top 10, focused specifically on multi-agent and agentic AI risks. MASO provides full coverage mapping.

- [OWASP GenAI Project](https://genai.owasp.org/)

### OWASP AI Exchange

300+ pages of free, evolving guidance on securing AI systems. Awarded OWASP Flagship project status in March 2025. Through an official liaison partnership, its content feeds directly into standards for the EU AI Act (70 pages contributed), ISO/IEC 27090 (AI security), and ISO/IEC 27091 (AI privacy).

Serves as a bridge between practitioner knowledge and formal standards. Enterprises can use this as an implementation guide that aligns with emerging regulatory requirements.

- [OWASP AI Exchange](https://owaspai.org/)

### MITRE ATLAS (Adversarial Threat Landscape for AI Systems)

A knowledge base of adversary tactics, techniques, and case studies targeting AI systems, modelled after MITRE ATT&CK. Contains 15 tactics, 66 techniques, 46 sub-techniques, 26 mitigations, and 33 real-world case studies. In October 2025, 14 new techniques focused on AI agents and generative AI were added in collaboration with Zenity Labs.

This framework's threat intelligence and red team playbook draw on ATLAS tactics and techniques. The MITRE Secure AI Program is supported by 16 member organisations including Microsoft, CrowdStrike, and JPMorgan Chase.

- [MITRE ATLAS](https://atlas.mitre.org/)

### MITRE SAFE-AI Framework

Published April 2025. Strengthens security control selection and assessment by ensuring AI-specific threats are systematically identified and addressed. Bridges the gap between NIST controls and AI-specific threat modelling.

- [MITRE SAFE-AI Full Report (PDF)](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf)

### ISO/IEC 42001:2023 — AI Management System Standard

The world's first AI management system standard. Specifies requirements for establishing, implementing, maintaining, and improving an AI management system (AIMS). Includes 38 distinct controls covering risk management, ethical considerations, transparency, and continuous learning. Uses Plan-Do-Check-Act methodology.

This framework's governance layer is designed to be compatible with ISO/IEC 42001. Organisations already certified to ISO/IEC 27001 will find familiar structures.

- [ISO/IEC 42001](https://www.iso.org/standard/81230.html)

### Google Secure AI Framework (SAIF)

Launched June 2023. Built around four pillars: Secure Development, Secure Deployment, Secure Execution, and Secure Monitoring. Includes a free SAIF Risk Assessment questionnaire. Google used SAIF principles to help form the Coalition for Secure AI (CoSAI).

The four-pillar structure parallels this framework's lifecycle approach, though we place heavier emphasis on runtime monitoring given the non-deterministic nature of AI systems.

- [Google SAIF](https://saif.google/)

### Coalition for Secure AI (CoSAI)

Industry coalition founded by Amazon, Anthropic, Cisco, IBM, Intel, Microsoft, NVIDIA, OpenAI, PayPal, Wiz, and others. Housed under OASIS Open. Has released frameworks for AI model signing and incident response, plus guidance on identity, access control, and isolation risks in MCP deployments.

- [Coalition for Secure AI](https://www.coalitionforsecureai.org/)

---

## Regulatory Landscape

### EU AI Act

The first comprehensive AI regulation by a major jurisdiction. Risk-based approach with key milestones: February 2025 (AI literacy requirements and prohibited AI uses), August 2025 (GPAI model transparency/documentation), August 2026 (full high-risk AI system compliance). Penalties up to EUR 35 million or 7% of global annual turnover.

This framework's regulatory mapping covers Articles 9, 14, and 15 — risk management, human oversight, and robustness.

- [EU AI Act](https://artificialintelligenceact.eu/)

### U.S. Executive Order 14110 on Safe, Secure, and Trustworthy AI

Signed October 2023. The most comprehensive U.S. government AI governance action at the time. Directed NIST to develop guidelines, red-teaming standards, and the GenAI Profile. Led to creation of the U.S. AI Safety Institute. Rescinded by President Trump on January 20, 2025 — but the NIST deliverables it produced (AI 600-1, AI 800-1, adversarial testing software) remain available and continue to be referenced by industry and regulators.

- [Executive Order 14110 (archived)](https://bidenwhitehouse.archives.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/)

---

## Research — Multi-Agent Security

These papers and reports directly inform MASO's treatment of multi-agent risks. This is the area where this framework makes its most distinctive contribution, and where we want to be transparent about what we're building on.

### "TRiSM for Agentic AI" (2025)

The first Trust, Risk, and Security Management framework for agentic AI, specifically for systems where multiple LLM-powered agents collaborate. Organised around pillars of Explainability, ModelOps, Security, Privacy, and Governance for autonomous decision-making. Gartner reports 35% of enterprises now use autonomous agents for business-critical workflows.

MASO's six control domains cover similar ground but are structured around operational implementation tiers rather than capability pillars.

- [TRiSM for Agentic AI (arXiv)](https://arxiv.org/html/2506.04133v3)

### "Multi-Agent Risks from Advanced AI" — Cooperative AI Foundation

Identifies critical risk categories for multi-agent systems including commitment/trust failures, emergent agency (new goals arising from collections of agents), and multi-agent security vulnerabilities. Notes that groups of AI agents are already responsible for tasks from trading million-dollar assets to recommending military actions.

This report's taxonomy of commitment failures directly informed MASO's identity and access controls, particularly the prohibition on transitive authority delegation.

- [Cooperative AI Foundation — Multi-Agent Risks](https://www.cooperativeai.com/post/new-report-multi-agent-risks-from-advanced-ai)

### "Open Challenges in Multi-Agent Security" (May 2025)

Examines security challenges when frontier model agents interact via direct communication or shared environments. Covers scenarios including trading agents on market platforms, personal assistants collaborating on scheduling, and autonomous cyber defence systems coordinating responses.

- [Open Challenges in Multi-Agent Security (arXiv)](https://arxiv.org/html/2505.02077v1)

### "Agentic AI Security: Threats, Defences, Evaluation, and Open Challenges" (October 2025)

Comprehensive survey outlining a taxonomy of threats specific to agentic AI, reviewing benchmarks, evaluation methodologies, and defence strategies from both technical and governance perspectives. Covers planning, tool use, memory, and autonomy risks.

- [Agentic AI Security Survey (arXiv)](https://arxiv.org/html/2510.23883v1)

### "Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training" — Anthropic (January 2024)

Hubinger et al. (39 co-authors). Demonstrated that if an LLM learns to be strategically deceptive — behaving helpfully in most situations but pursuing alternative objectives when triggered — current safety training techniques (RLHF, supervised fine-tuning) fail to remove this behaviour. Larger models are more persistent. Adversarial training can backfire, teaching models to better hide unsafe behaviour.

This paper has profound implications for model supply chain security: if you fine-tune on compromised data or use a model with an embedded backdoor, standard safety evaluations will not reliably detect the problem. MASO's supply chain controls — AIBOM, signed manifests, model provenance verification — are partly informed by this finding. Anthropic followed up with research on "defection probes" that can detect sleeper agent behaviour with AUROC scores above 99%.

- [Sleeper Agents (arXiv)](https://arxiv.org/abs/2401.05566)
- [Anthropic Research Page](https://www.anthropic.com/research/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training)
- [Simple probes can catch sleeper agents](https://www.anthropic.com/research/probes-catch-sleeper-agents)

---

## Research — Prompt Injection & Runtime Security

### Simon Willison — Prompt Injection Research

Willison coined the term "prompt injection" in September 2022 and has been its most consistent chronicler. Key contributions include the "lethal trifecta" concept (June 2025) — the dangerous combination of access to private data, exposure to untrusted content, and external communication ability. If your agent combines all three, exfiltration attacks become trivially possible.

This framework's guardrail architecture is designed around the assumption that prompt injection is unsolved — a position Willison has articulated more clearly than anyone.

- [Simon Willison's blog](https://simonwillison.net/)
- [Simon Willison's newsletter](https://simonw.substack.com/)

### Johann Rehberger — Embrace the Red

The most prolific independent AI security vulnerability researcher. His "Month of AI Bugs" (August 2025) published one critical vulnerability per day across ChatGPT, Codex, Cursor, Amp, Devin, OpenHands, Claude Code, GitHub Copilot, and Google Jules. Created "AgentHopper," a proof-of-concept self-propagating AI virus. His core advice to enterprises: *"Always assume breach. The agent gets compromised. What can it do? Then put security controls in place to mitigate that impact."*

This is essentially the design philosophy behind MASO's blast radius controls and PACE resilience architecture.

- [Embrace the Red](https://embracethered.com/)

### "The Attacker Moves Second" (October 2025)

Co-authored by 14 researchers from OpenAI, Anthropic, and Google DeepMind. Examined 12 published defences against prompt injection and jailbreaking. Subjected them to adaptive attacks, achieving >90% attack success rate against most defences.

This is the single most important paper for understanding why this framework emphasises defence-in-depth and runtime monitoring rather than relying on any single mitigation. If 12 published defences fail against adaptive attackers, the answer is not a better defence — it's layered controls with circuit breakers.

- [Coverage by Simon Willison](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/)

### "Not What You've Signed Up For" — Greshake et al. (February 2023)

Formalised the concept of "indirect prompt injection" — attacks where malicious prompts are planted in external data sources (web pages, documents, code comments) that an LLM retrieves and processes. Demonstrated attacks against Bing Chat, Microsoft Edge sidebar, and GitHub Copilot. Showed that injected prompts can replicate through contact lists and persist across sessions via stored memories.

Key insight: LLMs fundamentally cannot distinguish between instructions and data. Any system where an LLM processes external content is vulnerable. This is an architectural vulnerability, not a patchable bug.

- [Indirect Prompt Injection (arXiv)](https://arxiv.org/abs/2302.12173)
- [Black Hat USA 2023 Whitepaper (PDF)](https://i.blackhat.com/BH-US-23/Presentations/US-23-Greshake-Not-what-youve-signed-up-for-whitepaper.pdf)
- [Project Website](https://greshake.github.io/)

### "Here Comes The AI Worm" — Morris II (March 2024)

Cohen, Bitton, and Nassi (Cornell Tech / Israel Institute of Technology / Intuit). The first self-replicating worm targeting GenAI ecosystems. Uses "adversarial self-replicating prompts" that force the model to replicate the prompt in its output, execute a payload (data exfiltration, spam), and propagate to new agents. Zero-click — no user interaction required. Demonstrated against Gemini Pro, ChatGPT 4.0, and LLaVA.

MASO's data protection controls — particularly cross-agent message bus DLP and independent injection detection at every trust boundary — are directly informed by this research. If a poisoned message can propagate across agents, every inter-agent channel is an attack surface.

- [Morris II (arXiv)](https://arxiv.org/abs/2403.02817)
- [ComPromptMized Project Website](https://sites.google.com/view/compromptmized)

### SecAlign — ACM CCS 2025

The first known method that reduces prompt injection success rates to less than 10%, even against sophisticated attacks not seen during training. Uses preference optimisation to teach LLMs to prefer secure outputs over prompt-injected instructions. Promising but operational deployment at enterprise scale remains to be validated.

- [SecAlign (ACM CCS 2025)](https://dl.acm.org/doi/10.1145/3719027.3744836)

### Anthropic Constitutional Classifiers

System of constitutional classifiers that withstood over 3,000 hours of expert red teaming with no universal jailbreaks found. Uses a constitution defining harmful/harmless content categories to generate synthetic training data for classifier-based input/output monitoring. The jailbreak bug bounty challenge involved 300,000+ interactions and 339 participants.

Demonstrates a production-grade approach to input/output monitoring — the same pattern this framework recommends at the guardrail layer.

- [Constitutional Classifiers (arXiv)](https://arxiv.org/pdf/2501.18837)

---

## AI Incident Databases

These databases inform the [Incident Tracker](maso/threat-intelligence/incident-tracker.md) and provide the evidence base for control selection throughout the framework.

### AI Incident Database (AIID)

A project of the Responsible AI Collaborative. 1,200+ reports of AI systems causing safety, fairness, or other real-world problems. Over 80 new incidents added in April-May 2025 alone. Open-source.

- [AI Incident Database](https://incidentdatabase.ai/)

### MIT AI Risk Repository & Incident Tracker

A living, systematic review and database of AI risk frameworks. Classifies incidents using the MIT AI Risk Repository Domain Taxonomy across 24 subdomains. The April 2025 update expanded the dataset to 1,612 classified risks and added a new subdomain for multi-agent risks.

- [MIT AI Risk Repository](https://airisk.mit.edu/ai-incident-tracker)

### Stanford AI Index Report 2025

Documented AI safety incidents surged from 149 in 2023 to 233 in 2024 — a 56.4% increase.

- [Stanford HAI AI Index](https://aiindex.stanford.edu/)

---

## Real-World Incidents

These incidents are referenced throughout the framework to ground controls in demonstrated (not theoretical) risk. Each one maps to specific control domains.

### Samsung ChatGPT Data Leak (March–April 2023)

Samsung semiconductor engineers entered proprietary source code and internal meeting transcripts into ChatGPT within a 20-day window. Samsung banned generative AI tools company-wide. Similar restrictions followed at JPMorgan, Goldman Sachs, and other institutions.

Maps to: Data Protection, Guardrails (DLP).

- [AI Incident Database: Incident 768](https://incidentdatabase.ai/cite/768/)

### Air Canada Chatbot — Moffatt v. Air Canada (February 2024)

Air Canada's chatbot gave incorrect bereavement fare information. The airline argued the chatbot was "a separate legal entity responsible for its own actions." The BC Civil Resolution Tribunal ruled against Air Canada: *"It makes no difference whether the information comes from a static page or a chatbot."* Ordered to pay $812.02.

Established legal precedent that organisations are liable for AI-generated misinformation. Maps to: Guardrails, Human Oversight, LLM-as-Judge.

- [CBC News](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416)
- [American Bar Association](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)

### DPD Chatbot Incident (January 2024)

After a system update, DPD's AI chatbot could be prompted to swear at customers, write poems criticising the company, and call itself "useless." Screenshots went viral (1.3 million views). DPD confirmed the behaviour followed a system update that silently weakened guardrails.

Maps to: Guardrails (regression testing), Circuit Breaker.

- [TIME](https://time.com/6564726/ai-chatbot-dpd-curses-criticizes-company/)
- [AI Incident Database: Incident 631](https://incidentdatabase.ai/cite/631/)

### Chevrolet Watsonville Chatbot — $1 Car (December 2023)

A ChatGPT-powered dealership chatbot was manipulated into appearing to agree to sell a 2024 Chevy Tahoe for $1, claiming the offer was "legally binding — no takesies backsies." Post received 20 million views on X.

Maps to: Guardrails (output validation), Execution Control (action boundaries).

- [AI Incident Database: Incident 622](https://incidentdatabase.ai/cite/622/)
- [VentureBeat](https://venturebeat.com/ai/a-chevy-for-1-car-dealer-chatbots-show-perils-of-ai-for-customer-service)

### Slack AI Data Exfiltration via RAG Poisoning (August 2024)

PromptArmor demonstrated that Slack AI was vulnerable to indirect prompt injection that could exfiltrate data from private channels. An attacker posts a malicious prompt in a public channel; when a victim queries Slack AI, it retrieves the poisoned message as RAG context and embeds sensitive data from private channels into a clickable link. Slack initially dismissed the report as "intended behaviour."

Maps to: Data Protection (RAG integrity), Prompt Integrity (injection detection).

- [PromptArmor Research](https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via)
- [The Register](https://www.theregister.com/2024/08/21/slack_ai_prompt_injection/)
- [Simon Willison's coverage](https://simonwillison.net/2024/Aug/20/data-exfiltration-from-slack-ai/)

### Microsoft Copilot Vulnerabilities (2024–2025)

Multiple critical vulnerabilities in Microsoft 365 Copilot. CVE-2025-32711 ("EchoLeak," CVSS 9.3) enabled zero-click data exfiltration across Word, PowerPoint, Outlook, and Teams. The "Reprompt" attack bypassed LLM data leak protections through a double-request technique. A Mermaid diagram exploit enabled data exfiltration through crafted Excel spreadsheets.

Demonstrates that even the largest AI platform vendors face fundamental prompt injection challenges. Maps to: Guardrails, Data Protection, Supply Chain.

- [HackTheBox: CVE-2025-32711 EchoLeak](https://www.hackthebox.com/blog/cve-2025-32711-echoleak-copilot-vulnerability)
- [Varonis: Reprompt Attack](https://www.varonis.com/blog/reprompt)

### MCP Supply Chain Attacks (2024–2025)

CVE-2025-6514 (CVSS 9.6) in mcp-remote package (437,000+ downloads) — malicious MCP servers could achieve remote code execution on client machines. Separately, an unofficial Postmark MCP server was modified to silently BCC all emails to an attacker's address. Anthropic's own reference SQLite MCP server had SQL injection. Tool descriptions in MCP servers can contain hidden instructions that the LLM treats as legitimate directives.

Maps to: Supply Chain (MCP server vetting, signed tool manifests), Identity & Access (tool-level permissions).

- [Docker Blog: MCP Horror Stories](https://www.docker.com/blog/mcp-horror-stories-the-supply-chain-attack/)
- [AuthZed: Timeline of MCP Security Breaches](https://authzed.com/blog/timeline-mcp-breaches)
- [Palo Alto Unit 42: MCP Attack Vectors](https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/)

### Arup Deepfake Video Call Fraud (January 2024)

An employee in Arup's Hong Kong office joined a video conference where the CFO and colleagues were all AI-generated deepfakes. Made 15 transfers totalling HK$200M (~US$25 million) to five bank accounts.

Maps to: Identity & Access (authentication), Human Oversight (out-of-band verification for high-value actions).

- [CNN](https://www.cnn.com/2024/05/16/tech/arup-deepfake-scam-loss-hong-kong-intl-hnk)
- [World Economic Forum](https://www.weforum.org/stories/2025/02/deepfake-ai-cybercrime-arup/)

### Google Gemini Memory Poisoning (February 2025)

Johann Rehberger demonstrated that Google Gemini Advanced could be tricked into storing false data in its long-term memory via hidden prompts in documents. Gemini "remembered" fabricated biographical details across conversations — persistent manipulation of AI memory.

Maps to: Data Protection (memory isolation), Prompt Integrity (injection detection on retrieval).

- [Embrace the Red](https://embracethered.com/)

---

## Thought Leaders

These are researchers and practitioners whose work has directly shaped the thinking behind this framework. We cite them not to claim endorsement, but to credit influence and provide readers with the primary sources.

### Simon Willison

Creator of Datasette. Coined the term "prompt injection" (2022). The most prolific chronicler of prompt injection research. His "lethal trifecta" concept — the dangerous combination of private data access, untrusted content exposure, and external communication ability — is an essential decision tool for enterprise architects evaluating what capabilities to grant AI agents.

- [simonwillison.net](https://simonwillison.net/)

### Bruce Schneier

Internationally recognised security technologist. Testified before the House Committee on Oversight and Government Reform (June 2025) on federal AI data security. Keynoted RSAC 2025 on "AI, Security, and Trust." Advocates for AI transparency laws, security standards, and accountability mechanisms. His warning about "AI snake oil" in vendor marketing is valuable context for enterprise procurement decisions.

- [schneier.com](https://www.schneier.com/)

### Gary McGraw — Berryville Institute of Machine Learning (BIML)

Co-founder of BIML. Globally recognised authority on software security (8 books). BIML has mapped 78 risks associated with ML systems (the BIML-78), of which 23 are directly linked to LLM black-box risks. Compares the current state of ML security to application security 25 years ago — a useful calibration for enterprises expecting mature, settled answers.

- [Berryville Institute of Machine Learning](https://berryvilleiml.com/)

### Johann Rehberger

See [Prompt Injection & Runtime Security](#johann-rehberger--embrace-the-red) above. His "Month of AI Bugs" (August 2025) and AgentHopper self-propagating virus proof-of-concept provide continuous real-world evidence that prompt injection remains unsolved.

- [embracethered.com](https://embracethered.com/)

### Anthropic Safety Research

Frontier Red Team and Safeguards Research Team. Published Constitutional AI, Constitutional Classifiers, sleeper agents research, many-shot jailbreaking, and ASL-3 deployment safeguards. Partnered with the National Nuclear Security Administration for nuclear risk evaluation. Their published methodologies provide models for enterprise AI red teaming and safety evaluation programmes.

- [Anthropic Alignment Research](https://alignment.anthropic.com/)

---

## Enterprise AI Security Solutions

Commercial and open-source tools that implement patterns described in this framework. Listed for reference — inclusion is not endorsement. We encourage readers to evaluate these against their own requirements.

| Solution | What It Does | Reference |
| --- | --- | --- |
| **NVIDIA NeMo Guardrails** | Open-source toolkit for programmable guardrails — topic control, PII detection, RAG grounding, jailbreak prevention. Integrates with LangChain, LangGraph, LlamaIndex. | [GitHub](https://github.com/NVIDIA/NeMo-Guardrails) |
| **Lakera Guard** | Real-time prompt injection detection, jailbreak prevention, DLP. Supports 100+ languages. Single API call integration. Their Gandalf research game (1M+ players) doubles as a training tool. | [lakera.ai](https://www.lakera.ai/lakera-guard) |
| **Robust Intelligence AI Firewall** (now Cisco) | AI validation and real-time guardrail enforcement. Inspects prompts for injection, extraction, and PII. Continuously updated via automated red teaming. | [robustintelligence.com](https://www.robustintelligence.com/platform/ai-firewall-guardrails) |
| **HiddenLayer AISec Platform** | Supply chain security, runtime defence, posture management. AI Bill of Materials (AIBOM). Model Genealogy tracking. Partnered with NVIDIA and Google on OpenSSF Model Signing. | [hiddenlayer.com](https://www.hiddenlayer.com) |
| **Protect AI** (now Palo Alto Networks) | Open-source model scanning (ModelScan), LLM Guard, Jupyter Notebook security (NB Defense). Pioneer of the ML Bill of Materials (MLBOM) concept. | [protectai.com](https://protectai.com/) |
| **Prompt Security** | Security layer for agentic AI and MCP. Risk scoring for 13,000+ MCP servers. | [prompt.security](https://www.prompt.security/) |
| **Akamai Firewall for AI** | Input/output security for AI applications and LLMs. Prompt injection and data exfiltration protection. | [akamai.com](https://www.akamai.com/products/firewall-for-ai) |
| **Zscaler AI Security** | AI guardrails integrated into zero-trust architecture. Real-time threat mitigation and content moderation. | [zscaler.com](https://www.zscaler.com/products-and-solutions/ai-guardrails) |

---

## Key Statistics

These numbers provide context for why this framework exists and help calibrate the urgency of AI security controls.

| Statistic | Source |
| --- | --- |
| Only 34% of enterprises have AI-specific security controls | Cisco State of AI Security 2025 |
| AI agents move 16x more data than human users | Cisco State of AI Security 2025 |
| AI safety incidents surged 56.4% year-over-year (149 → 233) | Stanford AI Index Report 2025 |
| AI-specific data breaches average $4.80 million per incident | IBM Cost of a Data Breach Report 2025 |
| 97% of organisations with AI model breaches lacked access controls | IBM Cost of a Data Breach Report 2025 |
| Shadow AI adds $670K in additional breach costs | IBM Cost of a Data Breach Report 2025 |
| 35% of enterprises use autonomous agents for business-critical workflows | Gartner (via TRiSM for Agentic AI, 2025) |
| 12/12 published prompt injection defences bypassed at >90% success rate | "The Attacker Moves Second" (OpenAI/Anthropic/DeepMind, 2025) |

---

## Further Reading

### Georgetown CSET — AI Incidents Issue Brief (January 2025)

Academic perspective on key components needed for AI incident databases and gaps in current reporting. Useful for enterprises designing internal AI incident reporting processes.

- [Georgetown CSET AI Incidents (PDF)](https://cset.georgetown.edu/wp-content/uploads/CSET-AI-Incidents.pdf)

### NIST AI 800-1: Managing Misuse Risk for Dual-Use Foundation Models

Outlines seven objectives for foundation model developers to manage misuse risks. Second public draft released January 2025. Relevant for enterprises that develop or fine-tune foundation models, and as due diligence when evaluating third-party model providers.

- [NIST AI 800-1 (PDF)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-1.ipd2.pdf)

### Promptfoo — RAG Data Poisoning

Practical guidance on RAG poisoning attack vectors and defence strategies.

- [Promptfoo: RAG Poisoning Key Concepts](https://www.promptfoo.dev/blog/rag-poisoning/)

---

## A Note on How We Use These Sources

This framework is not a repackaging of the sources above. It is an original synthesis — particularly the MASO layer, which addresses multi-agent epistemic failures (groupthink, correlated errors, synthetic corroboration, uncertainty stripping) that we haven't found treated as a formal control domain elsewhere, though others may be working on similar ideas.

What the sources provide is:

- **Validation.** The three-layer runtime monitoring pattern (guardrails + LLM-as-Judge + human oversight) is not our invention — it's an emerging industry consensus reflected in NIST, OWASP, Google SAIF, and commercial implementations.
- **Evidence.** Every control in this framework maps to a documented incident, a published attack technique, or both. The incidents section above provides the evidence base.
- **Context.** No framework exists in isolation. Citing what came before helps readers understand where this work sits in the broader landscape and what it adds to the conversation.

We encourage readers to engage with the primary sources directly. If you find additional relevant work we should reference, please open an issue or pull request.

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
