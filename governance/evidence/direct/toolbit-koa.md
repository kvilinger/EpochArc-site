Title: Salesforce Koa: The First CRM Reasoning Model, Built on Nvidia Nemotron, Explained

URL Source: https://www.toolbit.ai/blog/salesforce-koa-crm-reasoning-model-explained

Published Time: 2026-09-17T08:16:23.048185+00:00

Markdown Content:
At Dreamforce on September 15, 2026, Salesforce announced [Koa](https://investor.salesforce.com/news/news-details/2026/Announcing-Koa-Salesforces-First-CRM-Reasoning-Model-Built-on-NVIDIA-Nemotron/default.aspx), its first-ever reasoning model - and the biggest surprise is not that Salesforce built a model, but what it built it on. Koa is a CRM reasoning model for Agentforce, created by post-training NVIDIA's open-weight Nemotron-3-Super-120B with a synthetic dataset modeled on nearly three decades of CRM deployments. No customer data went in. Salesforce controls the weights, and inference stays inside its trust boundary.

Why that matters takes a full article to unpack: it is a bet that enterprises would rather have a task-specialized model inside a vendor's trust boundary than a general frontier model outside it. And the headline performance claim - "matches or exceeds leading models with 3x fewer errors" - deserves a closer look, because the company's own technical paper tells a more modest story.

**In short:**

*   Koa is Salesforce's first reasoning model, built on NVIDIA's open-weight Nemotron-3-Super-120B and purpose-built for Agentforce workflows.
*   It was post-trained with SFT and GRPO on a fully synthetic dataset - zero customer data - spanning 14+ industries.
*   The PR claims "3x fewer errors" than leading models; the paper's own Table 1 places Koa at 0.86, below GPT-5.5 (0.90) and Claude Opus 4.8 (0.87) on Salesforce's own CRM Bench.
*   Pilots are live with 1-800Accountant, Baxter Credit Union, Engine, Formula 1, UChicago Medicine, and Xero; general availability is expected in winter 2026 (US).
*   The bigger signal: open-weight bases plus proprietary post-training is becoming the enterprise recipe, with Palantir also building on Nemotron.

* * *

## **What a "CRM reasoning model" actually does**

A reasoning model for CRM is not a chatbot wrapper with a new coat of paint. Koa is built to work through multi-step business workflows - generating leads, qualifying opportunities, resolving service cases - and to take the right tool actions, step by step, to reach a goal. Salesforce describes it as trained to "use the right tools to get work done" across the customer lifecycle.

The base is NVIDIA's Nemotron-3-Super-120B, an open-weight model, which matters for reasons we will get to. The announcement names it "Nemotron 3 Super"; the company's [technical paper](https://arxiv.org/abs/2609.15066) calls it Nemotron-3-Super-120B. Same model, two names.

Koa is already live inside Salesforce as "customer zero": an agent in Slack that helps employees find information and complete everyday tasks. The six pilot customers now testing it are 1-800Accountant, Baxter Credit Union, Engine, Formula 1, UChicago Medicine, and Xero.

* * *

## **Why build on open weights instead of renting frontier APIs?**

The short answer is control. Before Koa, when an Agentforce agent needed to reason through a long-running task, the request was routed through an AI gateway to a frontier model like Claude or GPT, as [TechCrunch reported](https://techcrunch.com/2026/09/15/salesforce-and-nvidias-new-reasoning-model-is-everything-the-ai-labs-should-fear) in an interview with Salesforce AI EVP Jayesh Govindarajan. "Reasoning has always been something that we've relied on the frontier model providers for. Until now."

Three reasons drove the choice:

**Trust boundary.** Salesforce controls Koa's weights and runs post-training and inference inside its own infrastructure. No customer data crosses the trust boundary during training or inference. For regulated industries, that is the whole ballgame.

**Data provenance.** Salesforce's AI leadership argued there was no sovereign, state-of-the-art American base model with clear data provenance to build on before Nemotron. With open weights, the provenance question is answered by construction.

**Token economics.** NVIDIA positions Nemotron as token-efficient, and Koa is billed by Salesforce as using fewer tokens for the same work - though the company has not published the numbers, so treat that as directional.

It is not either-or: Koa joins the model lineup in Agentforce's AI gateway alongside frontier models, and the deepened Anthropic partnership ("Claudeforce") was announced in the same week, per TechCrunch.

* * *

## **How was Koa trained - and why does "no customer data" matter?**

Koa's training recipe, per the [announcement](https://investor.salesforce.com/news/news-details/2026/Announcing-Koa-Salesforces-First-CRM-Reasoning-Model-Built-on-NVIDIA-Nemotron/default.aspx) and the paper: supervised fine-tuning (SFT) plus reinforcement learning with Group Relative Policy Optimization (GRPO), using NVIDIA NeMo RL, NeMo Gym, and NeMo AutoModel. The interesting part is the simulation-to-reward pipeline: workflow specifications written in Agent Script, Salesforce's declarative language for Agentforce agents, are expanded into persona-conditioned multi-turn tasks, with rewards grounded in successful tool use. A frozen Nano-30B helper model plays the customer simulator, the tool emulator, and the coverage judge. Training ran on clusters of NVIDIA B200 GPUs.

And the dataset itself? Built entirely from synthetic scenarios across 14+ industries, including manufacturing, financial services, healthcare, and travel. The "27 years" you will see in the marketing copy means the synthetic data was modeled on nearly three decades of CRM deployment patterns. It does not mean, and Salesforce is explicit about this, that any customer data went in. The paper states it plainly: Koa was "trained on public and synthetically generated data, with no customer data."

Two honest caveats come straight from the paper's authors. They found reinforcement learning contributed far more than SFT for multi-turn tool use, while SFT remained competitive on single-turn CRM tasks. And they flag that the Nemotron base they started from was itself already RL-post-trained, which limits how cleanly those SFT-versus-RL findings generalize to fresh, unpost-trained bases.

For an enterprise buyer, the compliance payoff is simple: nothing of yours went into the model, and inference stays inside the vendor's boundary.

* * *

## **Does Koa really "match or exceed leading models"? Auditing the claim**

Here is the claim, verbatim from the [announcement](https://investor.salesforce.com/news/news-details/2026/Announcing-Koa-Salesforces-First-CRM-Reasoning-Model-Built-on-NVIDIA-Nemotron/default.aspx): "In Salesforce's CRM Benchmark... Koa already matches or exceeds leading model performance on CRM actions with 3x fewer errors." Salesforce's own news story even hyperlinks "three times fewer errors" to the company's [technical paper](https://arxiv.org/abs/2609.15066).

Here is the problem: the phrase "3x fewer errors" appears nowhere in that paper. Not once. A full-text search turns up zero occurrences of "3x," "three times," "times fewer," or "fewer errors."

What the paper's Table 1 actually reports as CRM Bench overall scores: Koa at 0.86, versus GPT-5.5 at 0.90, Claude Opus 4.8 at 0.87, the Nemotron base at 0.84, and GPT-4.1 at 0.81. The authors' own summary is admirably candid: Koa "surpasses a strong proprietary baseline (GPT-4.1) while remaining below the strongest frontier models."

Two more things to weigh before you repeat the headline number. First, CRM Bench is Salesforce's own benchmark - a suite of real-world tasks like updating an opportunity, routing a case, or scheduling a follow-up, scored with human evaluations from Salesforce employees and customers. It is not a third-party evaluation, so its results are vendor-reported by definition. Second, the [Koa product page](https://www.salesforce.com/agentforce/koa/) adds separate stats - 11% better action precision, 2.1x better customer-context recall, 15% better context retention in long conversations - with no published methodology at all, so treat those as marketing rather than measurement.

The fair verdict? Koa genuinely beats a strong frontier baseline (GPT-4.1) on CRM-specific work, at what is presumably a far better token cost, and it was purpose-built for agentic tool use. That is a real achievement. But "matches or exceeds leading models" is a marketing characterization, not the paper's finding - the paper's own numbers place Koa below two frontier models on Salesforce's own benchmark. Attribute every number you read, and you will read this launch correctly.

![Image 1: Bar chart comparing CRM Bench overall scores from the Koa paper: GPT-5.5 at 0.90, Claude Opus 4.8 at 0.87, Koa at 0.86, Nemotron base at 0.84, GPT-4.1 at 0.81, with Koa highlighted](https://cdn.toolbit.ai/post-img/bodyclaimschart-1789632845455.webp)

* * *

## **When can you use it, and under what constraints**

Right now: pilots with 1-800Accountant, Baxter Credit Union, Engine, Formula 1, UChicago Medicine, and Xero. General availability is expected in winter 2026 in U.S. regions - that is the vendor's stated plan, not a shipped fact.

Deployment options, per the [product page](https://www.salesforce.com/agentforce/koa/): Koa can run as a managed LLM in the generative AI models catalogue, as an org-wide model provider in Agentforce, or as a per-agent or sub-agent choice in the Agentforce builder. It is Agentforce-only and Salesforce-hosted. There is no download, no self-hosting, and no API key to take elsewhere.

The government angle needs precision. What Salesforce announced for Missionforce, its offering for private clouds, classified networks, and fully air-gapped deployment, is that post-trained NVIDIA models will power Missionforce Operations agents covering procurement, supplier management, and logistics starting October 2026. Note the wording: "post-trained NVIDIA models," not Koa specifically.

Pricing and plan details are as published by the vendor around September 2026 and can change - confirm on the official site.

* * *

## **The bigger signal: open weights as the enterprise base**

Koa is not an isolated bet. [Constellation Research](https://www.constellationr.com/insights/news/salesforce-launches-koa-crm-reasoning-model-built-nvidias-nemotron) notes that Palantir was among the first software providers to bet big on Nemotron, and frames Koa as part of enterprises "coalescing around Nvidia's Nemotron family and open models" to keep AI costs in check while getting better accuracy. The timing helps: NVIDIA's $12.93 billion Hugging Face acquisition, announced days before Dreamforce, which analysts such as Constellation Research read as open weights getting their institutional validation.

Zoom out and the recipe is now legible: take an open-weight base, add proprietary post-training on task-specific synthetic data, run it inside your own trust boundary, and ship it as part of your platform. The vendor absorbs the model instead of renting it forever. Analysts already expect [AI agents to keep rewriting enterprise software economics](https://www.toolbit.ai/blog/ai-agents-reshaping-234-billion-enterprise), and the SaaS vendors that own their models will be positioned very differently from those that do not.

If you are rethinking which models and agents deserve a spot in your stack, the toolbit.ai directory lets you search and compare AI tools side by side before committing.

* * *

## **Salesforce Koa: frequently asked questions**

### **Is Salesforce Koa open-source, and can you download its weights?**

No. Koa's base model, Nemotron-3-Super-120B, is open-weight, but Koa itself is proprietary: Salesforce controls Koa's weights and performs post-training and inference entirely within its own trust boundary. You can only use Koa as a Salesforce-hosted model inside Agentforce; there is no download and no self-hosting.

### **Is "3x fewer errors" a finding from the research paper?**

No. "3x fewer errors" appears nowhere in the Koa technical paper (arXiv 2609.15066); the phrase is Salesforce's marketing characterization of its own CRM Benchmark results. The paper's Table 1 puts Koa at 0.86 overall, below GPT-5.5 (0.90) and Claude Opus 4.8 (0.87), and the authors themselves describe Koa as "below the strongest frontier models."

### **What is CRM Bench, and is it independent?**

CRM Bench is Salesforce's own benchmark for evaluating models on CRM tasks such as updating an opportunity, routing a case, or scheduling a follow-up, and it relies on human evaluations by Salesforce employees and customers. It is not a third-party evaluation, so its results should be treated as vendor-reported.

### **Does Koa replace Claude, GPT, or Gemini inside Agentforce?**

No. Koa is a new selectable model routed through Agentforce's AI gateway alongside frontier models, and Salesforce announced a deepened Anthropic partnership ("Claudeforce") in the same week, per TechCrunch. Koa is positioned as a task-specialized, trust-boundary option, not a wholesale replacement for the frontier labs' models.

### **Can enterprises fine-tune Koa on their own CRM data?**

Not as announced. Salesforce controls Koa's post-training, and Koa's training corpus was built entirely from synthetic scenarios with no customer data. Enterprises consume Koa through Agentforce - as a catalogue model, an org-wide provider, or a per-agent choice - rather than fine-tuning it themselves.

### **Does Koa work in air-gapped government environments?**

Koa itself was not announced for air-gapped deployment. What Salesforce announced is that post-trained NVIDIA models will reach Missionforce Operations, its offering for private clouds, classified networks, and fully air-gapped government use, starting October 2026. The announcement says "post-trained NVIDIA models," not Koa specifically.
