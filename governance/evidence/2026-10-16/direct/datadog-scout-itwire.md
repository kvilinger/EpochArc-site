Title: Introducing Scout 1.0: A new SRE model powering Bits AI with frontier performance at a fraction of the cost

URL Source: https://itwire.com/business-it-news/data/introducing-scout-1-0-a-new-sre-model-powering-bits-ai-with-frontier-performance-at-a-fraction-of-the-cost

Published Time: 2026-10-16T00:09:48.114Z

Markdown Content:
Datadog has introduced Scout 1.0, its first AI model specialised for investigating production issues. Scout powers Bits Investigation, Datadog’s AI site reliability engineer (SRE). The company trained Scout to reduce inference cost so that investigations are cheap enough to run an order of magnitude more often and earlier in an incident’s lifecycle.

Key highlights include:

*   Scout achieves a better price-performance curve on Datadog’s target scenarios when compared with general-purpose frontier models.Scout 1.0 medium matches GPT-6.1 Sol high and Claude Opus 5.5 high at 3-8× lower estimated inference cost, and performs comparably to Fable medium and Astra medium at 12× and 19× lower cost, respectively. With test-time scaling, Scout 1.0 xhigh matches Fable xhigh at 4× lower cost.

*   Datadog built Scout using its in-house distributed reinforcement learning infrastructure, and relied extensively on real historical incidents and telemetry data to build high-quality training simulations that don’t contain any customer data. For more technical details, [see our full report](https://web-assets.dd-static.net/42588/1792071077-datadog-scout_technical_report.pdf).

*   Datadog engineering teams and a small group of customers in a closed preview are already using Scout to investigate production alerts. [Sign up for the preview](https://forms.gle/Db3HaW78pRpvE59g6) to try it in your environment and provide feedback before general availability.

**[Bits as a first responder for every alert](https://www.datadoghq.com/blog/ai/introducing-scout-sre-specialized-model-bits-ai/#bits-as-a-first-responder-for-every-alert)**

Datadog’s goal is for Bits to serve as an always-on first responder, gathering evidence and identifying likely causes before an engineer steps in. Each Bits investigation involves forming hypotheses, querying telemetry, and deciding whether the evidence supports a conclusion. Those steps require repeated model calls. By reducing a model’s inference cost, Datadog can give teams more room to run investigations across their environments. Scout’s efficiency makes it practical to extend support to more alerts and investigate complex issues in greater depth, enabling greater breadth of coverage, reducing the burden of on-call work, and freeing more time for development.

Lower inference cost also makes it practical to spend additional computation on harder or higher-impact problems. For instance, Scout 1.0 xhigh uses more computation per incident to improve investigation quality, and this added investigative depth reduces engineering workload and pressure during even the highest-stakes incidents.

**[Training and evaluating Scout for SRE investigations](https://www.datadoghq.com/blog/ai/introducing-scout-sre-specialized-model-bits-ai/#training-and-evaluating-scout-for-sre-investigations)**

Advertisement

Datadog built Scout 1.0 on GLM-5.3 Flash and post-trained it using reinforcement learning in investigation simulations. It uses historical incidents and telemetry from real alerts to build realistic simulations with known causes. Scout practices using tools modelled on Bits Investigation to gather evidence and test competing explanations. Its training rewards finding the cause and supporting its conclusions with evidence.

Datadog also built its own training infrastructure on top of open source tools, with the simulation, evaluation, and model-training systems needed to run reinforcement learning at scale.

To test whether those skills transfer to real incidents, Datadog built AlertEval. The company’s engineers have curated thousands of evaluation points through its [incident-response workflow](https://www.datadoghq.com/blog/engineering/bits-ai-eval-platform/). AlertEval draws on that work, combining real alerts, archived telemetry, and root cause explanations written by engineers.

Datadog is building Scout and Bits Investigation together, training the model for the tools Bits uses and improving those tools based on what we learn from its investigations.

Datadog has also evaluated Scout on [SREGym](https://www.sregym.com/), a third-party benchmark, to test its performance outside AlertEval. The company again has found that Scout 1.0 medium significantly improves upon the base model, GLM-5.3-Flash, performance, surpassing GLM-5.3 at a more than 4× reduction in cost. Through additional test time scaling, Datadog found that Scout 1.0 high is competitive with the best models on this benchmark, while still maintaining at least 2× cost savings compared to all competitors (10× savings compared to Astra/Fable-class models).

Moving forward, Datadog plans to simulate a wider range of failures and keep improving investigation quality while lowering inference cost. It also plans to extend this approach beyond investigation to help teams autonomously remediate issues to restore service faster. Together, these advances move Bits beyond its role as a first responder and toward becoming the only responder during an incident, resolving issues faster and reducing on-call burden.

Advertisement
