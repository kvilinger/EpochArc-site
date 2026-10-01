Title: Holo4 Computer-Use AI: Run GUI Agents Locally on Windows, Benchmarks and License Limits

URL Source: https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/

Published Time: 2026-09-28T14:52:55-04:00

Markdown Content:
M ost AI models are good at conversation and bad at finding the right button in a cluttered Windows dialog. Paris-based H Company is trying to fix that. On Monday it released Holo4, a family of "computer-use" models built to point, click, scroll and type through graphical interfaces. The same models can also write code and call APIs when that's the quicker route.

For Windows admins and developers, this matters more than another chatbot launch. A lot of real business software still has no usable API. It has a GUI, a fixed set of menus, and maybe a macro language. An agent that can switch between clicking and scripting is aimed right at that software.

## [](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/) What H actually shipped​[](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/#-what-h-actually-shipped "Permanent link")

According to H Company's Hugging Face announcement, Holo4 comes in two sizes: 27B dense and 35B-A3B Mixture of Experts. Both are available on the H Models API. H is also releasing an updated version of Holotron 3: Holotron4 Nano.

The model cards show how the lineage splits:

| Model | Architecture | Base model | Weight formats (per H) |
| --- | --- | --- | --- |
| Holo4-27B | 27B dense | Alibaba Qwen3.8-27B | BF16, FP8, NVFP4, Q4 GGUF |
| Holo4-35B-A3B | 35B mixture-of-experts, ~3B active | Alibaba Qwen3.6-35B-A3B | BF16, FP8, NVFP4, Q4 GGUF |
| Holotron4 Nano | NemotronH Nano Omni | Nvidia Nemotron 3 Nano Omni | BF16, FP8 |

This clears up an ambiguity in The Register's coverage, which said Holo4 sits "atop" both Qwen models. In fact each Holo4 model has one base: the 27B uses Qwen3.8 and the 35B-A3B uses Qwen3.6. The Holo4-27B model card lists a maximum configured context length of 262,144 tokens.

As AlphaSignal pointed out, the 35B-A3B label describes total and active parameters rather than a capability ranking. The bigger number doesn't mean the better model, and the benchmarks below show why.

**Summary:** two Qwen-based Holo4 models, one updated Nemotron-based Holotron, and weights in formats that suit both datacenter GPUs and local hobbyist setups.

## [](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/)One model for every interface​[](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/#-one-model-for-every-interface "Permanent link")

H's main pitch is versatility. In its words, Holo4 clicks and types on a screen, writes and runs its own code, and calls MCP or API tools. It uses whichever fits the task. The company says the usual alternative is fragmented: GUI-focused models are blind without a screen, while models that prefer tool calling are stuck in front of an application that has no API.

H also says the model runs identically on desktops, the web, Android, code sandboxes, and against business APIs, called the same way in every case. That's a company claim, not an independent compatibility audit. The design goal still makes sense: a single business task often needs a spreadsheet, a web portal and a legacy desktop app.

The FreeCAD demos show the approach in practice. In one, Holo4-27B used FreeCAD's macro capability to build a dimensioned Eiffel Tower programmatically instead of assembling primitives by hand. The spec was detailed: a square plan at every height, four tapering legs, three platforms at set heights, and a mast. In the other demo, the model went the other way and used extruded shapes to recreate H's logo.

H's own numbers for these runs are mixed:

*   **Eiffel Tower:** Holo4 27B (84 calls, 1.3M tokens) Qwen3.8 27B (60 calls, 1.0M tokens). The fine-tuned model used _more_ calls and tokens than its base.
*   **H logo:** Holo4 used 94 calls and 1.5 million tokens, versus 118 calls and 1.9 million tokens for the base model.
*   **Pac-Man-style game in Godot:** Holo4 used 68 calls and 2.4 million tokens, versus 197 calls and 11.4 million tokens for Qwen.

These are single runs chosen by the vendor. They're useful illustrations, not guarantees. Note, too, that one CAD job took more than a million tokens. Agentic GUI work uses a lot of context.

## [](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/)The benchmarks and the cost argument​[](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/#-the-benchmarks-and-the-cost-argument "Permanent link")

The headline number: on OSWorld 2.0, Holo4 27B scores 61.7% against 81.8% for Opus 5.5, and Holo4 35B-A3B reaches 30.9%. That means the dense 27B checkpoint lands well ahead of the larger MoE checkpoint on this desktop benchmark, and still about 20 points behind the best closed-model result H cites.

H's model card puts per-task costs on OSWorld 2.0 at $1.22 for Holo4-27B and $0.61 for Holo4-35B-A3B. On AutomationBench v1.0.6 the card lists 45.4% at $0.05 per task for the 27B and 34.5% at $0.02 for the 35B-A3B. The card also reports 85.2% at $0.08 per task on the original OSWorld. Don't mix that figure up with the OSWorld 2.0 results.

Sources disagree on cost. H says Holo4 competes with frontier models at a much lower cost per task. The Register read the same charts and said that in many cases the models cost _more_ per task. It suggested Holo4 spends far more "thinking" tokens than something like GPT 6 Luna, which scores lower on OSWorld 2.0 but costs much less.

H's footnotes explain why both readings are possible:

1.   Costs are estimated from the input and output tokens of each agentic run. Holo4 is priced at H Models API rates (single run).
2.   H's OSWorld notes say closed-model points come from vendor launch data and the official leaderboard, and that releases, harnesses and task subsets differ.
3.   For AutomationBench, H measured Holo4 in its own internal harness. The competitor scores come from public-set README figures and a leaderboard that runs on a private set. H says it will report Holo4 on the private set once that evaluation is done.

In other words, some of these points were measured differently. H does publish every trajectory behind its public-benchmark scores, so anyone can replay the runs, which is more than many vendors offer. AlphaSignal notes that independent replication remains necessary because computer-use benchmarks are sensitive to environment versions, step limits, and execution settings.

**Summary:** the 27B model is strong for its size, but "small" doesn't mean "cheap per task." Treat the cost comparisons as H's claims until someone replicates them.

## [](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/)How it was trained​[](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/#-how-it-was-trained "Permanent link")

H says its internal "Agentic Task Factory" builds interactive environments and verifiable tasks from documentation, including screenshots of real websites and open-source software. So far it has produced about 10,000 tasks across web apps, MCP servers and desktop environments. Some are hybrid environments where the same state is reachable through both a GUI and MCP.

The company also rebuilt its agent harness based on OSWorld 2.0 failures. The biggest changes were a memory that can track hundreds of steps and a shell on the desktop machine itself. Nobody has independently checked the size or effect of this training setup.

## [](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/)Running it locally on your PC​[](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/#-running-it-locally-on-your-pc "Permanent link")

This is the part hobbyists will care about. Weights are on Hugging Face in BF16, FP8, NVFP4 and 4-bit GGUF, so Llama.cpp, LM Studio and Ollama users have a way in. Community quantizations are already appearing. One GGUF repack notes that for image input, use the included F16 vision projector (mmproj-Holo4-27B-f16.gguf) and advises using a current llama.cpp build with the included chat template. Skip the projector file and your computer-use model can't see screenshots, which defeats the point.

On hardware, The Register estimated that a 24 GB RTX 3090 should comfortably run these models at 4-bit precision. H's model card doesn't confirm that. Treat it as an informed estimate, not a requirement. With a 262K-token context window and CAD runs that burn over a million tokens, your KV cache will use a lot of memory. Your mileage depends on the quantization, the runtime, and how much context you actually allocate.

H also says it will release DSpark drafter checkpoints "in the coming days" for speculative decoding. A small draft model guesses the larger model's tokens. When the guesses are right you get faster output, and when they're wrong the main model's output is used, so quality doesn't drop.

## [](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/)A model is not an agent​[](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/#-a-model-is-not-an-agent "Permanent link")

The weights on their own do nothing. The Holo4-27B card describes the harness loop: it sends screenshots and tool results to the model, carries out the clicks, typing, code and tool calls the model asks for, and sends the results back. H's open-source HAI-Agents harness is on its GitHub, and The Register says third-party computer-use harnesses should work in theory.

For enterprise IT, this is where the risk sits. H's rebuilt harness gives the agent a shell on the desktop machine. The Register's joke about escaping a sandbox by "pushing a button" has a serious side. An agent that can click through Windows and run shell commands has roughly the same power as a junior admin who never sleeps and occasionally misreads a screen. Before you let it near production:

*   **Isolate it:** run agents in a VM or Windows Sandbox-style environment, not on a daily-driver workstation logged into your tenant.
*   **Limit credentials:** give it a dedicated low-privilege account, never your Global Admin session.
*   **Log everything:** review the trajectories, which is exactly the kind of record H publishes for its benchmarks.
*   **Route by risk:** AlphaSignal suggests sending routine work to the 35B-A3B, harder visual tasks to the 27B, and escalating low-confidence or high-impact cases to a stronger model or human reviewer.

## [](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/)The licensing catch​[](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/#-the-licensing-catch "Permanent link")

Businesses should check this before anything else. The Holo4-27B model card lists **CC BY-NC 4.0**, a noncommercial license, even though its Qwen3.8-27B base is Apache 2.0. Downloadable weights don't mean free commercial use. The 27B is the stronger model, and its weights carry the noncommercial restriction. Read the 35B-A3B and Holotron cards separately before you build anything commercial. Paying for H's Models API is a separate route with its own terms.

## [](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/)The bigger picture​[](https://windowsforum.com/news/holo4-computer-use-ai-run-gui-agents-locally-on-windows-benchmarks-and-license-limits.446345/#-the-bigger-picture "Permanent link")

H isn't alone here. The Register notes that AWS announced its own computer-use models at re:Invent last year, and OpenAI, Google and Anthropic are all working on the same capability. What sets H apart is the combination of open weights, sizes that fit on a single workstation, and published trajectories.

Can a 27B model match the frontier labs on a Windows desktop? Not yet: it's still about 20 points behind the top closed model on H's own chart. For a model you can download and inspect, and for noncommercial use run on a single GPU, it's a solid showing. Test it on your own workflows before you trust the benchmark charts.
