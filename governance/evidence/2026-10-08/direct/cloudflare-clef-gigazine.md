Title: Cloudflare has released 'Clef,' a decision-making model similar to Jev, which now supports image input and surpasses Jev in benchmarks, but the creator of Jev is skeptical of the benchmark itself.

URL Source: https://gigazine.net/gsc_news/en/20261005-clef-cloudflare-decision-model/

Markdown Content:
Oct 05, 2026 13:05:00

[![Image 1](https://i.gzn.jp/img/2026/10/05/clef-cloudflare-decision-model/00_m.png)](https://i.gzn.jp/img/2026/10/05/clef-cloudflare-decision-model/00.png)

This article, originally posted in **[Japanese](http://gigazine.net/news/20261005-clef-cloudflare-decision-model/)** on 13:05 Oct 05, 2026, may contains some machine-translated parts.
If you would like to suggest a corrected translation, please click **here**.

Cloudflare has released its decision-making model 'Clef' as an open model. Unlike

**[Jev](https://gigazine.net/news/20260916-system-one-jev/)** , which sparked the popularity of decision-making models, Clef is characterized by its support for image input.

**Introducing Clef: our open-source decision models, and new RL fine-tuning platform | Cloudflare Blog**
**[https://blog.cloudflare.com/clef-decision-models/](https://blog.cloudflare.com/clef-decision-models/)**

Following the release of Jev on September 15, 2026, numerous decision-making models with similar functionality have emerged. Decision-making models process tasks using a different approach than LLMs and can output judgments for given inputs. The processing results output a score for each of the many choices, and when used appropriately, they can process tasks significantly faster and at a lower cost than LLMs.

One such decision-making model developed by Cloudflare is Clef. The name 'Clef' is derived from the ' **[clef' (musical clef)](https://sakikomasuda.com/music-theory/basic/clef/)** used in musical notation to determine pitch.

While Jev only supports text input, Clef also supports image input. There are two versions of Clef: the standard 'Clef' and the lightweight 'Clef-flash.' Clef has achieved higher scores than Jev in benchmark tests. The graph below shows the time taken to produce output on the horizontal axis and the score of the decision model benchmark test ' **[Decision Index 0.2.1](https://huggingface.co/spaces/multimodalart/jev-decision-index)** ' on the vertical axis, demonstrating that Clef is faster and scores higher than Jev.
[![Image 2](https://i.gzn.jp/img/2026/10/05/clef-cloudflare-decision-model/01_m.png)](https://i.gzn.jp/img/2026/10/05/clef-cloudflare-decision-model/01.png)

Cloudflare's threat intelligence team is already using Clef to classify websites. Clef can categorize websites under review, such as '95% likely to be a fashion site,' '85% likely to be an online store,' or 'less than 1% likely to be a scam site.' While the classification process takes 4.7 seconds with gpt-oss-120b, Clef can complete it in 2.2 seconds. Another strength of Clef is its ability to handle multiple options.

Clef and Clef-flash are released as open models and can be downloaded from the following link. The license is the Apache License 2.0.

**Cloudflare/clef · Hugging Face**
**[https://huggingface.co/Cloudflare/clef](https://huggingface.co/Cloudflare/clef)**

**Cloudflare/clef-flash · Hugging Face**
**[https://huggingface.co/Cloudflare/clef-flash](https://huggingface.co/Cloudflare/clef-flash)**

Ollama already supports running Clef series.

> . [@Cloudflare](https://x.com/Cloudflare?ref_src=twsrc%5Etfw) 's decision models are available on Ollama!
>
>
> Decision models allow you to classify an image, label a bug report or route a support ticket to the right team.
>
>
> Clef (27B):
>  Ollama pull clef
>
>
> Clef Flash (9B):
>  ollama pull clef-flash [pic.twitter.com/hxohKeomvT](https://t.co/hxohKeomvT)
>
> — ollama (@ollama) [October 3, 2026](https://x.com/ollama/status/2106186667543666841?ref_src=twsrc%5Etfw)

As more and more decision-making models surpass Jev in benchmark scores, Diogo Almeida, the developer of Jev, has questioned the validity of benchmark testing. For example, on October 5, 2026 (Japan time), he posted, 'There is a crucial difference between a model optimized for benchmark testing and a model that prioritizes true reliability, and that difference does not show up in benchmark scores. (I learned this phenomenon in LLM...)'

> there's a critical difference between benchmaxxed models and ones made by people who truly care about reliability that, by definition, doesn't show up on benchmarks
>
>
> (we've somewhat learned this for string LLMs...) [https://t.co/u808vG8Eap](https://t.co/u808vG8Eap)
>
> — Diogo Almeida (@CompleteSkeptic) [October 4, 2026](https://x.com/CompleteSkeptic/status/2106883012856336539?ref_src=twsrc%5Etfw)

Furthermore, on October 2, 2026, Jev's market entry strategist stated that 'a quarter of Fortune 500 companies are already adopting Jev,' highlighting Jev's advantages.

> me to our GTM guy: do enterprises want benchmarks
>
>
> him: no, the fast ones have already benchmarked their internal use cases. the slow ones are copying the fast ones.
>
>
> he's onboarded a quarter of the fortune 500 already 🥵
>
> — Diogo Almeida (@CompleteSkeptic) [October 1, 2026](https://x.com/CompleteSkeptic/status/2105764336522424779?ref_src=twsrc%5Etfw)
