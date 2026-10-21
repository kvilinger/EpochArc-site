Title: Beam is now available — Reflection

URL Source: https://reflection.ai/blog/beam-is-available

Markdown Content:
Beam is our first open-weight model, built for advanced coding, reasoning, and long-horizon agentic workloads with frontier reasoning efficiency. Today, we have released Beam’s model weights [on Hugging Face](https://huggingface.co/reflection/) under an Apache 2.0 license. Our [model card](http://reflection.ai/beam-model-card) includes final benchmarks, and the [Beam Safety Technical Report](http://reflection.ai/beam-safety-report) shares the model’s complete safety methodology and evaluations.

In addition to releasing Beam’s weights and documentation, we’re launching with an ecosystem of over 40 partners and integrations to create what we are calling an open operating system for agents. The model is the kernel, and everything above the infrastructure layer is open: reference agentic integrations, deployment containers, inference integrations, and customization pipelines.

Developers can download and self-host the model, evaluate it, customize it for their own domains, connect it to agentic systems, and access it through Reflection and our partners.

## Building with Beam

Beam is a sparse Mixture-of-Experts model with 501 billion total parameters, 23 billion active, built for coding, reasoning, and agentic workloads. Since opening up access to Beam, we’ve seen some interesting use cases from early developers.

## Partnering to create the open operating system for agents

Our vision is to build an open intelligence stack that gives developers, enterprises, and governments control over how AI is deployed in their environments. A model is only one layer of a working system; making it useful takes more than releasing weights. It also requires reliable inference, evaluation, safety tooling, customization workflows, agent runtimes, and deployment paths.

We have worked with partners across the open ecosystem to support inference, quantization, fine-tuning, reinforcement learning, agent harnesses, evaluation, and observability. Partners are making Beam available through managed endpoints, cloud platforms, on-premises systems, and sovereign infrastructure.

We are building and releasing our own open-source tools while collaborating with the projects developers already use. Together, these efforts expand a single model release into a usable system with many paths to adoption.

## Deploy Beam Efficiently

We are releasing Beam’s model weights in BF16, FP8, and NVFP4 precision formats, along with a speculative decoding drafter model. We have also worked with partners to optimize serving configurations and develop fused kernels for lower latency and higher throughput. Together, these reduce memory requirements and accelerate token generation out of the box.

Beam has native, day-zero support across the ecosystem including: Transformers (**Hugging Face**), vLLM (**Inferact**), SGLang (**RadixArk**), **Unsloth**, **Axolotl**, TokenSpeed (**LightSeek Foundation**), and Dynamo (**NVIDIA**) so you can go from weights to a production-scale endpoint without writing custom plumbing.

## Agentic development with Mirror CLI

Beam and [Mirror CLI](https://developers.reflection.ai/mirror-overview) are both open-source friendly. We trained Beam along with the Mirror CLI harness to offer best performance, while also integrating with other popular [open source harnesses](https://developers.reflection.ai/coding-agents-quickstart) to give developers optionality.

Mirror lets developers run Beam from a terminal, point it at different checkpoints or endpoints, and use it as a daily coding and agent harness. Developers can inspect the agent’s activity, approve tool calls, and steer it as it works. Mirror supports resumable conversations and parallel agents in separate worktrees, while project instructions, skills, MCP connections, and Python extensions let developers adapt it to their workflows.

Mirror’s architecture reflects this design. A Python frontend handles the product layer: prompts, skills, and developer tooling. It talks to a Rust agent core over a local connection, and that core is what actually drives the model. Keeping the core minimal lets it double as a clean evaluation surface, so results produced through Mirror are reliable.

We initially built Mirror for internal use at Reflection to help our engineers move faster – with isolated workspaces, background sessions, and integrations into Slack, Linear, and GitHub. Agents could keep working after we closed our laptops, and we saw substantial productivity gains, especially in tasks like code review. Those experiences helped us train Beam to work better with different coding harnesses. We then evolved Mirror into a tool we could open source to bring these benefits to developers.

Beam has also been tested with Pi (**Earendil**), OpenCode (**Anomaly**), and Hermes (**Nous Research**) across coding and knowledge work, including tasks that involve reading repositories, editing files, and running commands.

All of these harnesses work with Beam today through [Reflection’s first-party API](https://developers.reflection.ai/quickstart), other hosted third-party inference providers, or by self-hosting the model. We’ll keep adding harness support over time.

## Customize Beam

Developers can post-train Beam, including with large scale reinforcement learning, to customize the model. Because model customization is an iterative process that depends heavily on your evaluations, we are providing recipes and integrations from Reflection and the open-source ecosystem, as well as the tools to measure both capabilities and safety at every step.

When we did our largest RL runs when training Beam, for example, we ran roughly 1.3 billion sandboxes across RL training, evaluation, and ablations. We are upstreaming lessons from training Beam into the open-source ecosystem we’re building, including [OpenEnv](https://github.com/huggingface/OpenEnv), an open environment standard we’ll adopt for future runs.

We partnered with **NVIDIA** (NeMo RL, AutoModel, Megatron), **RadixArk** (Miles), **Hugging Face** (TRL), **Anyscale** (SkyRL) and **Axolotl** to build fine-tuning and RL workflows, so developers can deeply customize Beam for their own use cases.

## Beam Self-Distillation

Developers can also leverage novel approaches like self-distillation to customize Beam for additional domains and increase accuracy and token efficiency on your tasks. We plan to release recipes for developers to do this in the coming days.

## Start Using Beam

Beam is available on a broad set of platforms. Beyond the open weights and Reflection’s API, we’ve partnered with hyperscalers, inference providers, and open-source projects so Beam is available on various platforms at launch including: **Amazon Web Services, Nscale, Applied Compute, Baseten, Cloudflare, CoreWeave, Databricks, Fireworks AI, Google Cloud, Hermes, LM Studio, Microsoft Foundry, Modal, Nebius, Nvidia NIMs, Ollama, OpenCode, OpenRouter, Oracle**, **Together AI, Vercel,** and **Weights & Biases.**

For on-premises, sovereign, and air-gapped environments, **Dell** and **HPE** deliver Beam behind the firewall. It’s the same open stack a developer runs on a laptop, deployed at enterprise scale with no retooling or rebuilding for a different environment.

*   **Try Beam at [platform.reflection.ai](http://platform.reflection.ai/).**It’s free to start. Sign up for the public beta to test Beam on Reflection’s first party API.
*   **Get the weights**. Pull the weights from [Hugging Face](https://huggingface.co/reflection), read the model card, or hit a hosted endpoint on one of our partner offerings.
*   **Access developer documentation** at [developers.reflection.ai](https://developers.reflection.ai/) for API references, deployment guides, agentic tooling, customization recipes, and demos.
*   **Join the community.** Join us on [Discord](https://discord.gg/vUmV8ayxy4) to discuss open models, find collaborators, and build with us.

Thank you again to all our partners, including those who worked closely with us to test Beam’s capabilities and safety ahead of release: **Andon Labs, Artificial Analysis, Arena, Gray Swan, Irregular, Nemesys, Perimeter Bio, SecureBio, Snorkel AI, Transfyr.ai, Handshake**, and **Mercor**.
