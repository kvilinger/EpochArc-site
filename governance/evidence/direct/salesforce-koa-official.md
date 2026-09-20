Title: Announcing Koa: Salesforce’s First CRM Reasoning Model, Built on NVIDIA Nemotron

URL Source: https://www.salesforce.com/in/news/stories/koa-reasoning-model/

Published Time: 2026-09-16T00:51:26+00:00

Markdown Content:
_Koa is trained with 27 years of Salesforce CRM intelligence to enable agents to reason through the complex, multistep tasks required for enterprise work_

_The collaboration also brings NVIDIA open models and accelerated computing into Missionforce, giving government and regulated organizations control over their model, data, and deployment environment_

* * *

**SAN FRANCISCO, September 15, 2026 — Salesforce and NVIDIA** today announced [Koa](http://salesforce.com/koa), Salesforce’s first CRM reasoning model for [Agentforce](https://www.salesforce.com/agentforce/?d=cta-body-promo-8), built on NVIDIA Nemotron. Developed through deep technical collaboration with NVIDIA, Koa is purpose-built to help agents reason through complex, multistep workflows and use the right tools to get work done.

Koa was built by post-training NVIDIA Nemotron 3 Super with a proprietary synthetic dataset modeled on enterprise knowledge from nearly three decades of CRM deployments. The result is a reasoning model grounded in how businesses run — their processes, workflows, and operational policies. In [Salesforce’s CRM benchmark](https://www.salesforceairesearch.com/crm-benchmark), a model benchmark that includes a suite of real-world tasks like updating an opportunity, routing a case, or scheduling a follow-up, Koa already matches or exceeds leading model performance on CRM actions with [three times fewer errors](https://arxiv.org/abs/2609.15066). Salesforce controls the model weights and performs post-training and inference entirely within its own trust boundary, giving customers a specialized, Salesforce-hosted option to power their Agentforce use cases.

Salesforce and NVIDIA are also bringing Nemotron-based models and accelerated computing into [Missionforce](https://www.salesforce.com/government/?d=cta-body-promo-8), extending that same control over model, data, and deployment environment to government and regulated organizations. Together, the companies are bringing mission-specific AI to private clouds, air-gapped networks, and other secure environments.

“The most valuable thing Salesforce has built isn’t our platform — it’s the accumulated knowledge of how enterprise business actually works. With Koa, the knowledge is put inside the model itself. We trained a reasoning engine that understands the structure of a deal, the lifecycle of a service case, and the workflows that vary across industries. That’s a different kind of intelligence, and it runs entirely inside your trust boundary.” **_— Marc Benioff, Chair and CEO, Salesforce_**

“AI is creating a much larger opportunity for software. Every company needs useful AI, tailored to its knowledge, expertise, and work. NVIDIA Nemotron open models give Salesforce the foundation to turn decades of enterprise expertise into specialized AI with Koa, creating a CRM model that can reason and securely take action.”**_— Jensen Huang, founder and CEO of NVIDIA_**

## **What makes Koa different**

No customer data was used to train the Koa reasoning model. Its training corpus was built entirely from synthetic scenarios that reflect the reasoning, tool use, and decision-making skills Agentforce agents perform across CRM workflows: generating leads, qualifying opportunities, and resolving service cases across the customer lifecycle.

Rather than relying on generic content, these scenarios were built to simulate real-world enterprise workflows across more than 14 industries, including manufacturing, financial services, healthcare, and travel. Each scenario paired a persona with specific tasks then mapped the sequence of actions and tool calls an agent must take to complete them.

To post-train the model, Salesforce applied Supervised Fine-Tuning (SFT) and reinforcement learning with Group Relative Policy Optimization (GRPO) with NVIDIA NeMo RL, NeMo Gym, and NeMo AutoModel. By training on a targeted set of prioritized enterprise tasks, the model developed deeper expertise and learned not only to produce the right answer but to take the right action, step by step, to reach a goal.

NVIDIA Nemotron [open models](https://www.nvidia.com/en-us/glossary/open-models/) gave Salesforce the control to build CRM intelligence into the model itself. Salesforce controls the weights and runs Koa within its own infrastructure, ensuring that no customer data crosses the trust boundary during inference.

Koa is already in use inside Salesforce, including an agent in Slack that helps employees find information and complete everyday tasks in Slack, and is now moving into customer pilots with [1-800Accountant](https://www.salesforce.com/customer-stories/1800-accountant/), [Baxter Credit Union](https://www.salesforce.com/customer-stories/bcu/) (BCU), [Engine](https://www.salesforce.com/customer-stories/engine/), [Formula 1](https://www.salesforce.com/customer-stories/formula-one/), [UChicago Medicine](https://www.salesforce.com/customer-stories/uchicago-medicine/), and [Xero](https://www.salesforce.com/ap/customer-stories/xero/).

“Accounting requires navigating tax rules, financial data, documents, and the unique circumstances of every customer. Koa gives our agents the reasoning to work through that complexity step by step and use the right tools along the way. That means we can extend more of our accountants’ expertise across every customer interaction and help people get to the right outcome faster.” **_— Ryan Teeples, Chief Strategy Officer, 1-800Accountant_**

“Our members come to us with goals, whether that’s buying a home, managing their money, or planning for what’s next. Koa can help our Digital agents understand the full complexity and context behind those goals and reason across the information, tools, and policies needed to move them forward. It gives us a powerful way to make every interaction more intelligent, personal, and useful.” **_— John Sahagian, SVP and Chief Data Officer, Baxter Credit Union_**

“At Engine, we’re building the future of business travel, and that starts with equipping our teams to deliver exceptional service. Business travel has countless moving parts, and what we need from AI isn’t a model that sounds confident — it’s one that can reason precisely through complex, multi-step problems. Collaborating with Salesforce and NVIDIA on a reasoning model purpose-built for Agentforce lets us push that vision further, faster.” **_— Elia Wallen, Founder and CEO, Engine_**

“Some of the most important work in healthcare happens behind the scenes, coordinating information, navigating complex processes, and making sure the right next step happens at the right time. Koa can work across those longer, multi-step workflows and help our teams manage that complexity more effectively. That creates more time and capacity for what matters most, caring for patients.” **_— Andrew Chang, Chief Marketing Officer, UChicago Medicine_**

## **Mission-specific intelligence**

For many government and highly regulated organizations to deploy AI, they must control the model and training data and deploy in specialized environments — private clouds, classified networks, and fully air-gapped systems — that never touch public infrastructure.

Salesforce is bringing NVIDIA models and accelerated computing into Missionforce to enable customers in highly sensitive industries to train, tune, and deploy mission-specific models on their own critical data.

Post-trained NVIDIA models will power agents for Missionforce Operations, a product that digitizes and automates complex government workflows, including procurement, supplier management, and logistics. Trained on an organization’s operational data and terminology, these specialized models enable agents to reason through back-office processes and act within the customer’s environment, including air-gapped networks. The companies are also working to bring post-trained NVIDIA models into additional Missionforce capabilities to enable customers to build and run models on their own infrastructure for specialized workloads.

##### **Availability**

**Koa:** Available to select pilot customers now in Agentforce; general availability expected winter 2026 in U.S. regions.

**Missionforce Operations:** Product generally available now in U.S. regions. Post-trained NVIDIA models available to select customers in October 2026.

##### **About Salesforce**

Salesforce helps organizations of any size become [agentic enterprises](https://www.salesforce.com/welcome-to-the-agentic-enterprise/) — integrating humans, agents, apps, and data on a trusted, unified platform to unlock unprecedented growth and innovation. Visit [www.salesforce.com](http://www.salesforce.com/) for more information.
