Title: Holo4’s higher-scoring 27B model has a non-commercial license

URL Source: https://opentools.ai/news/holo4-27b-35b-license-benchmark-guide

Published Time: 2026-09-29T14:16:57.832Z

Markdown Content:
[OpenTools![Image 2: logo](https://opentools.ai/opentools-logo-red-light.svg)](https://opentools.ai/)

Open main menu

[Tools](https://opentools.ai/tools)[Experts](https://opentools.ai/experts)[Newsletter](https://newsletter.opentools.ai/)[Submit a Tool](https://opentools.ai/friends/launch-tool)

Knowledge Hub

Industry Hub

[Advertise](https://marshy-teller-328.notion.site/Advertise-With-OpenTools-37cb46049ad8809cb84bc22cb6fb03ed?pvs=74)[Learn AI](https://opentools.ai/ai-edge)

Get started

1.   [Home](https://opentools.ai/)
2.   /
3.   [News](https://opentools.ai/news)
4.   /
5.   Holo4’s higher-scoring 27B model has a non-commercial license

Updated 13 hours ago

![Image 3: Holo4’s higher-scoring 27B model has a non-commercial license](https://imagedelivery.net/FCiXvK7dG4mSm_W_033WNA/editorial-news-761e512051200977eea4e7ed24c5a1e0a31b20224b38cbeb6c2452e5b77bd801/editorialhero)

Source: H Company and Hugging Face. Figure: OpenTools Team. Holo4 checkpoint and evidence split; no third-party expressive material used. · [Source image](https://huggingface.co/blog/Hcompany/holo4)

AI News

# Holo4’s higher-scoring 27B model has a non-commercial license

By OpenTools Team · September 29, 2026

H Company released two open‑weight computer‑use agents, but their scores and licenses point builders in different directions. Here is what the public record supports.

## One release, two different deployment choices

H Company released Holo4 on September 28 as a family of vision‑language models that can work through graphical interfaces, code, MCP tools and APIs. The launch includes a dense 27‑billion‑parameter checkpoint and a mixture‑of‑experts checkpoint with 35 billion total parameters and about 3 billion active at a time. Both are available through H’s hosted Models API, and downloadable versions are listed in BF16, FP8, NVFP4 and 4‑bit GGUF formats.

The practical choice is less simple than the family name suggests. H’s [Holo4‑27B model card](https://huggingface.co/Hcompany/Holo4-27B) labels those weights CC BY‑NC 4.0, which permits reuse only for non‑commercial purposes under the licence’s conditions. The [Holo4‑35B‑A3B card](https://huggingface.co/Hcompany/Holo4-35B-A3B) labels its weights Apache 2.0, a permissive licence that allows commercial use subject to its notice and other terms. A team choosing a checkpoint therefore has to consider the exact repository, not just whether “Holo4” is described as open weight.

Both cards list a maximum configured context of 262,144 tokens. That is a configuration limit, not evidence that either model remains reliable for every task across that entire window. The stronger evidence concerns specific agent evaluations—and those results also split the family.

### Don’t fall behind.

Join 150,000+ builders staying up to date with AI. Daily digest, every business day. 5 minutes, you’re caught up.

### Save the AI tools you want to try.

Create your free OpenTools account to keep your favourites in one place.

Continue with Google[Sign up with email](https://opentools.ai/signin?callbackUrl=%2Fnews%2Fholo4-27b-35b-license-benchmark-guide)

## The 27B checkpoint is much stronger on H’s long‑workflow run

On OSWorld 2.0, H reports a 61.7% partial‑reward score for Holo4‑27B at a mean model cost of $1.22 per task. Holo4‑35B‑A3B scores 30.9% at $0.61 per task. On those vendor‑run figures, the dense model buys 30.8 additional percentage points of partial reward for twice the reported mean model cost per attempted task.

That comparison is useful within H’s own two runs. It does not establish that either checkpoint will deliver the same completion rate or cost on a company’s workflow. [OSWorld 2.0](https://osworld-v2.xlang.ai/) contains 108 long, stateful professional tasks; its site says the median task takes a skilled person about 1.6 hours and distinguishes partial reward from strict binary completion. H’s public trajectory card lists 106 OSWorld 2.0 runs for each checkpoint, two fewer than the benchmark’s 108 tasks; the retained sources do not establish whether those two were excluded from scoring or only omitted from the released traces. A partial score can credit pieces of an unfinished workflow, so it should not be read as a 61.7% end‑to‑end success rate.

H’s [launch post](https://huggingface.co/blog/Hcompany/holo4) also warns that releases, harnesses and task subsets differ across the comparison chart. Its Holo4 scores came from H’s harness, while several frontier‑model points came from vendors or the official leaderboard. Independent coverage from [The Register](https://assets.theregister.com/2026/09/28/202620/) likewise cautions that a smaller or lower‑priced model is not automatically cheaper per job when long agent runs consume more reasoning tokens. The launch numbers are a reason to test the 27B model, not a substitute for measuring completed work on the target queue.

## AutomationBench’s public score needs its held‑out footnote

H reports strict public‑set pass rates of 45.4% for Holo4‑27B and 34.5% for Holo4‑35B‑A3B on AutomationBench v1.0.6, at $0.05 and $0.02 per task respectively. AutomationBench counts a public task as passed only when every assertion passes; the average across the 600 scored public tasks is the public pass rate. H produced these figures with its internal harness and says 480 of the 600 tasks belong to the split from which it collected training data.

The cleaner comparison is the 120‑task subset H says it held out from that collection. There, H reports 49.3% for Holo4‑27B and 31.7% for Holo4‑35B‑A3B, compared with 40.3% for Qwen3.8‑27B and 13.1% for Qwen3.6‑35B‑A3B in the same harness. The held‑out results still favour both post‑trained models over their stated bases, but they are company‑run measurements rather than an independent replication.

The distinction between public and official scores matters. The [AutomationBench repository](https://github.com/zapier/AutomationBench) says its public set and the private set behind the official leaderboard are separate, and that local public‑set scores may not match the private leaderboard one‑for‑one. H says it has not yet reported Holo4 on that private set. Until it does, Holo4’s numbers should not be placed directly beside private‑set leaderboard results as if they shared one test population.

## The released traces improve auditability, not independence

H did publish substantially more evidence than a benchmark screenshot. Its [Holo4 trajectories dataset](https://huggingface.co/datasets/Hcompany/trajectories) lists 7,366 agent runs across OSWorld, OSWorld 2.0, AndroidWorld, AutomationBench, PinchBench and Agents’ Last Exam. Each trajectory record can include the task, steps, reasoning, actions, tool results, screenshots, token use and verifier outcome. The dataset is Apache 2.0, while upstream task content retains its original licence.

That lets researchers inspect failure paths, recalculate summaries and compare the two checkpoints at the run level. It also exposes a useful limitation: the dataset says credentials, internal hosts and personal data are masked, screenshots containing them are replaced, and a few tasks are omitted. Public traces make the launch more auditable; they do not turn H’s evaluation into an independent one.

A meaningful next check would rerun the downloadable checkpoint, pinned harness and benchmark environment under a separate operator, then report both partial credit and strict completion. For deployment decisions, teams should add recovery time, damaged‑state cleanup and human intervention to model‑token cost. A computer‑use agent that leaves a workflow half‑finished can be more expensive than a higher‑priced run that completes cleanly.

## Which Holo4 checkpoint fits which job

For non‑commercial research and evaluation, Holo4‑27B is the stronger starting point supported by H’s published long‑workflow result. For a commercial self‑hosting review, Holo4‑35B‑A3B has the clearer permissive weight licence, but its lower OSWorld 2.0 result makes workload‑specific testing essential. Hosted API use is a separate contract question; a repository’s weight licence does not by itself define the service terms.

Before choosing either model, freeze a small test set that mirrors the intended work. Record strict completions, partial outcomes, retries, human rescue minutes, latency and total inference spend. Pin the checkpoint, quantization, harness, step limit and application versions so a later rerun measures model or system changes instead of a moving environment. Run computer‑control tests in isolated accounts with least‑privilege tools and reviewable logs.

The release is still notable: two relatively compact checkpoints can move between screens, code and structured tools, and H has made the public evaluation traces inspectable. The evidence supports a narrower conclusion than “open Holo4 beats frontier agents.” It supports testing the non‑commercial 27B model when completion quality is the priority, and testing the Apache‑licensed 35B‑A3B model when permissive self‑hosting rights are a requirement.

_Figure: Holo4 checkpoint and evidence split. Sources: [H Company launch post](https://huggingface.co/blog/Hcompany/holo4), [Holo4‑27B model card](https://huggingface.co/Hcompany/Holo4-27B) and [Holo4‑35B‑A3B model card](https://huggingface.co/Hcompany/Holo4-35B-A3B), accessed September 29, 2026. Figure by OpenTools Team; no third‑party expressive material used._

## Sources

1.   1.[The Register](https://assets.theregister.com/2026/09/28/202620/)(assets.theregister.com)
2.   2.[H Company launch post](https://huggingface.co/blog/Hcompany/holo4)(huggingface.co)
3.   3.[Holo4-35B-A3B model card](https://huggingface.co/Hcompany/Holo4-35B-A3B)(huggingface.co)
4.   4.[huggingface.co](https://huggingface.co/Hcompany/Holo4-27B)(huggingface.co)
5.   5.[huggingface.co](https://huggingface.co/datasets/Hcompany/trajectories)(huggingface.co)
6.   6.[osworld-v2.xlang.ai](https://osworld-v2.xlang.ai/)(osworld-v2.xlang.ai)
7.   7.[github.com](https://github.com/zapier/AutomationBench)(github.com)

## Tags

H Company Holo4 computer-use agents open-weight AI AI model licenses

### Share this article

[Post](https://twitter.com/intent/tweet?url=https%3A%2F%2Fopentools.ai%2Fnews%2Fholo4-27b-35b-license-benchmark-guide&text=Holo4%E2%80%99s%20higher-scoring%2027B%20model%20has%20a%20non-commercial%20license)[Share](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fopentools.ai%2Fnews%2Fholo4-27b-35b-license-benchmark-guide)Copy Link

### In This Article

*   [One release, two different deployment choices](https://opentools.ai/news/holo4-27b-35b-license-benchmark-guide#section0)
*   [The 27B checkpoint is much stronger on H’s long-workflow run](https://opentools.ai/news/holo4-27b-35b-license-benchmark-guide#section1)
*   [AutomationBench’s public score needs its held-out footnote](https://opentools.ai/news/holo4-27b-35b-license-benchmark-guide#section2)
*   [The released traces improve auditability, not independence](https://opentools.ai/news/holo4-27b-35b-license-benchmark-guide#section3)
*   [Which Holo4 checkpoint fits which job](https://opentools.ai/news/holo4-27b-35b-license-benchmark-guide#section4)

### Topics

H Company Holo4 computer-use agents open-weight AI AI model licenses

### AI news in your inbox

Weekly updates on tools, models, and the companies building them.

[Subscribe](https://newsletter.opentools.ai/upgrade?offer_id=2b8eeb73-4d02-4137-a782-2a706cd1d187&utm_medium=sidebar&utm_source=article)

## Footer

[![Image 4: Company name](https://opentools.ai/opentools-logo-red.svg)](https://opentools.ai/)
The right AI tool is out there. We'll help you find it.

[LinkedIn](https://www.linkedin.com/company/opentools/)[X](https://twitter.com/opentoolsai)

### Knowledge Hub

*   [News](https://opentools.ai/news)
*   [Resources](https://opentools.ai/resources)
*   [Newsletter](https://newsletter.opentools.ai/)
*   [Blog](https://opentools.ai/blog)
*   [AI Tool Reviews](https://opentools.ai/reviews)
*   [YouTube Summary](https://opentools.ai/youtube-summary)
*   [YouTube Transcript Generator](https://opentools.ai/youtube-transcript-generator)

### Industry Hub

*   [AI Companies](https://opentools.ai/organizations)
*   [AI Tools](https://opentools.ai/tools)
*   [AI Models](https://opentools.ai/llms)
*   [MCP Servers](https://opentools.ai/mcp)
*   [Muse Connectors](https://opentools.ai/muse-connectors)
*   [AI Tool Categories](https://opentools.ai/categories)
*   [Top AI Use Cases](https://opentools.ai/use-cases)

### For Builders

*   [Submit a Tool](https://opentools.ai/friends/launch-tool)
*   [Experts & Agencies](https://opentools.ai/experts)
*   [Advertise](https://marshy-teller-328.notion.site/Advertise-With-OpenTools-37cb46049ad8809cb84bc22cb6fb03ed?pvs=74)
*   [Compare Tools](https://opentools.ai/compare)
*   [Favourites](https://opentools.ai/favourites)

### Legal

*   [Privacy Policy](https://opentools.ai/privacy-policy)
*   [Terms of Service](https://opentools.ai/tos)

© 2026 OpenTools - All rights reserved.

![Image 5](https://t.co/1/i/adsct?bci=4&dv=UTC%26en-US%2Cen%26Google%20Inc.%26Linux%20x86_64%26255%261280%261280%2610%2624%261280%261280%260%26na&eci=3&event=%7B%7D&event_id=eca09e41-bc3b-4949-8393-1c73525f246f&integration=advertiser&p_id=Twitter&p_user_id=0&pl_id=0b843b4c-6031-4e08-aa68-bb08bc98c7e2&tw_ch_fvl=Chromium%2F154.0.8037.57%2CGoogle%20Chrome%2F154.0.8037.57%2CNot%20A(Brand%2F99.0.0.0&tw_document_href=https%3A%2F%2Fopentools.ai%2Fnews%2Fholo4-27b-35b-license-benchmark-guide&tw_engaged_ms=2&tw_iframe_status=0&tw_pid_src=1&tw_session_count=1&tw_session_id=1790760132303-22752805&tw_session_start=1&twpid=tw.1790760132303.237286741818038507&txn_id=ofdjk&type=javascript&version=2.4.11)![Image 6](https://analytics.twitter.com/1/i/adsct?bci=4&dv=UTC%26en-US%2Cen%26Google%20Inc.%26Linux%20x86_64%26255%261280%261280%2610%2624%261280%261280%260%26na&eci=3&event=%7B%7D&event_id=eca09e41-bc3b-4949-8393-1c73525f246f&integration=advertiser&p_id=Twitter&p_user_id=0&pl_id=0b843b4c-6031-4e08-aa68-bb08bc98c7e2&tw_ch_fvl=Chromium%2F154.0.8037.57%2CGoogle%20Chrome%2F154.0.8037.57%2CNot%20A(Brand%2F99.0.0.0&tw_document_href=https%3A%2F%2Fopentools.ai%2Fnews%2Fholo4-27b-35b-license-benchmark-guide&tw_engaged_ms=2&tw_iframe_status=0&tw_pid_src=1&tw_session_count=1&tw_session_id=1790760132303-22752805&tw_session_start=1&twpid=tw.1790760132303.237286741818038507&txn_id=ofdjk&type=javascript&version=2.4.11)
