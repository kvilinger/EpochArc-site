Title: GPT-2: 1.5B release

URL Source: https://openai.com/index/gpt-2-1-5b-release/

Markdown Content:
[Skip to main content](https://openai.com/index/gpt-2-1-5b-release/#main)

[](https://openai.com/)

*   [Research](https://openai.com/research/index/)
*   Products
*   [Business](https://openai.com/business/)
*   [Developers](https://openai.com/api/)
*   [Company](https://openai.com/about/)
*   [Foundation(opens in a new window)](https://openaifoundation.org/)

Log in[Try ChatGPT(opens in a new window)](https://chatgpt.com/?openaicom-did=ca1f27c8-1652-4b8e-a689-5272a777a42f&openaicom_referred=true)

*   Research
*   Products
*   Business
*   Developers
*   Company
*   [Foundation(opens in a new window)](https://openaifoundation.org/)

GPT-2: 1.5B release | OpenAI

November 5, 2019

[Release](https://openai.com/research/index/release/)

# GPT‑2: 1.5B release

[Read paper(opens in a new window)](https://arxiv.org/abs/1908.09203)[GPT-2 model(opens in a new window)](https://github.com/openai/gpt-2)[Detector model(opens in a new window)](https://github.com/openai/gpt-2-output-dataset/tree/master/detector)

![Image 1: GPT-2 1.5B Release](https://images.ctfassets.net/kftzwdyauwt9/5ca4df8a-bd0c-47e0-7efe1b15187a/f891c43eaec1e52760e3cf7c9902a819/gpt-2-1-5b-release.jpg?w=3840&q=90&fm=webp)

Illustration:Ben Barry

More Resources

[Model card(opens in a new window)](https://github.com/openai/gpt-2/blob/master/model_card.md)

Listen to article 4:59

[Audio 2](https://openai.com/index/gpt-2-1-5b-release/)

Share

Our findings

*   [Our findings](https://openai.com/index/gpt-2-1-5b-release/#our-findings)
*   [Next steps](https://openai.com/index/gpt-2-1-5b-release/#next-steps)

*   [Our findings](https://openai.com/index/gpt-2-1-5b-release/#our-findings)
*   [Next steps](https://openai.com/index/gpt-2-1-5b-release/#next-steps)

As the final model release of[GPT‑2⁠](https://openai.com/index/better-language-models/)’s[staged release⁠](https://openai.com/index/gpt-2-6-month-follow-up/), we’re releasing the largest version (1.5B parameters) of GPT‑2 along with[code and model weights⁠(opens in a new window)](https://github.com/openai/gpt-2-output-dataset)to facilitate detection of outputs of GPT‑2 models. While there have been larger language models released since August, we’ve continued with our original staged release plan in order to provide the community with a test case of a full staged release process. We hope that this test case will be useful to developers of future powerful models, and we’re actively continuing the conversation with the AI community on responsible publication.

While there have been larger language models released since August, we’ve continued with our original staged release plan in order to provide the community with a test case of a full staged release process. We hope that this test case will be useful to developers of future powerful models, and we’re actively continuing the conversation with the AI community on responsible publication.

## Our findings

**1. Humans find GPT‑2 outputs convincing**.Our partners at Cornell University surveyed people to assign GPT‑2 text a credibility score across model sizes. People gave the 1.5B model a “credibility score” of 6.91 out of 10. This is marginally greater than outputs from the 774M model (6.72) and significantly above the medium 355M model (6.07). These results make us more inclined to release the 1.5B model, as the incremental increase in human-perceived credibility relative to 774M seems low.

**2. GPT‑2 can be fine-tuned for misuse**.Our partners at the Middlebury Institute of International Studies’ Center on Terrorism, Extremism, and Counterterrorism (CTEC) found that extremist groups can use GPT‑2 for misuse, specifically by fine-tuning GPT‑2 models on four ideological positions: white supremacy, Marxism, jihadist Islamism, and anarchism. CTEC demonstrated that it’s possible to create models that can generate synthetic propaganda for these ideologies. They also show that, despite having low detection accuracy on synthetic outputs, ML-based detection methods can give experts reasonable suspicion that an actor is generating synthetic text.

**3. Detection is challenging**.We expect that content-based detection of synthetic text is a long-term challenge. To test whether machine learning approaches may help today, we conducted in-house detection research and developed a[detection model⁠(opens in a new window)](https://github.com/openai/gpt-2-output-dataset)that has detection rates of ~95% for detecting 1.5B GPT‑2‑generated text.[A](https://openai.com/index/gpt-2-1-5b-release/#citation-bottom-A) We believe this is not high enough accuracy for standalone detection and needs to be paired with metadata-based approaches, human judgment, and public education to be more effective. We are releasing this model to aid the study of research into the detection of synthetic text, although this does let adversaries with access better evade detection.

While we found detection accuracy depends heavily on the sampling methods used in training and testing, we also found detection to be more reliable when training across a range of sampling techniques. As seen in the figure below, we observed that larger models’ outputs are more difficult to classify, but training on larger models’ outputs makes detection results more accurate and robust. We expect this trend to continue and that detection will be more challenging with increased model size.

# Transferred model accuracy (nucleus samples)

| Trained on | Tested on Small (124M) | Medium (355M) | Large (774M) | XL (1.5B) |
| --- | --- | --- | --- | --- |
| Small (124M) | 99.3% | 96.6% | 90.9% | 79.3% |
| Medium (355M) | 99.0% | 98.5% | 96.9% | 91.8% |
| Large (774M) | 98.4% | 97.9% | 97.9% | 95.7% |
| XL (1.5B) | 96.9% | 96.7% | 96.6% | 96.0% |

**4. We’ve seen no strong evidence of misuse so far**.While we’ve seen some discussion around GPT‑2’s potential to augment high-volume/low-yield operations like spam and phishing, we haven’t seen evidence of writing code, documentation, or instances of misuse. We think synthetic text generators have a higher chance of being misused if their outputs become more reliable and coherent. We acknowledge that we cannot be aware of all threats, and that motivated actors can replicate language models without model release.

**5. We need standards for studying bias**.Language models have biases. Working out how to study these biases, discuss them, and address them, is a challenge for the AI research community. We’ve approached the challenge of bias in two ways:

*   Publishing a[model card⁠(opens in a new window)](https://github.com/openai/gpt-2/blob/master/model_card.md)[B](https://openai.com/index/gpt-2-1-5b-release/#citation-bottom-B) alongside our models on GitHub to give people a sense of the issues inherent to language models such as GPT‑2.

*   Performing a qualitative, in-house evaluation of some of the biases in GPT‑2: We probed GPT‑2 for some gender, race, and religious biases, using those findings to inform our model card. These probes are not comprehensive and raise the need for collaboration on bias analysis frameworks.

## Next steps

Our experience with GPT‑2 over the past 9 months has given us valuable insight into the challenges and opportunities for creating responsible publication norms in AI. We’re continuing our work on this issue via participation in the Partnership on AI’s “Responsible Publication Norms for Machine Learning” project and discussions with our colleagues in the research community.

_If you’d like to develop large-scale AI systems and think about their implications,_[_we’re hiring_⁠](https://openai.com/careers/)_._

*   [GPT](https://openai.com/research/index/?tags=gpt)
*   [Ethics & Safety](https://openai.com/research/index/?tags=ethics-safety)
*   [Generative Models](https://openai.com/research/index/?tags=generative-models)
*   [Language](https://openai.com/research/index/?tags=language)
*   [Transformers](https://openai.com/research/index/?tags=transformers)

## Footnotes

1.   A Specifically, we based a sequence classifier on RoBERTaBASE(125 million parameters) and RoBERTaLARGE(355 million parameters) and fine-tuned it to classify the outputs from the 1.5B GPT-2 model versus WebText, the dataset we used to train the GPT-2 model. [](https://openai.com/index/gpt-2-1-5b-release/#citation-top-A) 
2.   B Which we’ve based on “[Model Cards for Model Reporting⁠(opens in a new window)](https://arxiv.org/abs/1810.03993)” by Mitchell et al. [](https://openai.com/index/gpt-2-1-5b-release/#citation-top-B) 

## Related articles

[View all](https://openai.com/news/)

![Image 2: Abstract floral pattern with vibrant purple blooms on a green backdrop](https://images.ctfassets.net/kftzwdyauwt9/f50ce1d2-4f61-4ed2-e560c624d631/6f4dd4542898a35d0a91b137f85c9834/Democratic_inputs_to_AI_grant_program_lessons_learned_and_implementation_plans.jpg?w=3840&q=90&fm=webp)

[Democratic inputs to AI grant program: lessons learned and implementation plans Safety Jan 16, 2024](https://openai.com/index/democratic-inputs-to-ai-grant-program-update/)

![Image 3: White Digital Green logo on a green background.](https://images.ctfassets.net/kftzwdyauwt9/7b26cc3b-46d8-45b0-f67f6de0c8f8/8bc94d083a5a147609cddad159243ef7/digital_green.png?w=3840&q=90&fm=webp)

[Building agricultural database for farmers Jan 12, 2024](https://openai.com/index/digital-green/)

![Image 4: White Wix logo on a background of blue and green paint swathes](https://images.ctfassets.net/kftzwdyauwt9/6E3QyNLzuWwK3EGBHPw7nQ/fbd0c5a34cc4f4ba096028adbdda8934/oai_Wix_1x1.png?w=3840&q=90&fm=webp)

[Creating websites in minutes with AI Website Builder May 29, 2025](https://openai.com/index/wix/)

Research
*   [Research Index](https://openai.com/research/index/)
*   [Research Overview](https://openai.com/research/)
*   [Economic Research](https://openai.com/signals/)

Latest Advancements
*   [GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/)
*   [GPT-6 Astra](https://openai.com/index/gpt-6-astra/)
*   [GPT-5.6](https://openai.com/index/gpt-5-6/)
*   [GPT-5.5](https://openai.com/index/introducing-gpt-5-5/)

Safety
*   [Safety Approach](https://openai.com/safety/)
*   [Deployment Safety(opens in a new window)](https://deploymentsafety.openai.com/)
*   [Security & Privacy](https://openai.com/security-and-privacy/)
*   [Trust & Transparency](https://openai.com/trust-and-transparency/)

Products
*   [ChatGPT(opens in a new window)](https://chatgpt.com/?openaicom-did=ca1f27c8-1652-4b8e-a689-5272a777a42f&openaicom_referred=true)
*   [ChatGPT Business(opens in a new window)](https://chatgpt.com/business/?openaicom-did=ca1f27c8-1652-4b8e-a689-5272a777a42f&openaicom_referred=true)
*   [ChatGPT Enterprise(opens in a new window)](https://chatgpt.com/business/enterprise/?openaicom-did=ca1f27c8-1652-4b8e-a689-5272a777a42f&openaicom_referred=true)
*   [ChatGPT for Education(opens in a new window)](https://chatgpt.com/business/education/?openaicom-did=ca1f27c8-1652-4b8e-a689-5272a777a42f&openaicom_referred=true)
*   [Codex](https://chatgpt.com/codex/?openaicom-did=ca1f27c8-1652-4b8e-a689-5272a777a42f&openaicom_referred=true)
*   [Dots(opens in a new window)](https://chatgpt.com/features/dots?openaicom-did=ca1f27c8-1652-4b8e-a689-5272a777a42f&openaicom_referred=true)
*   [Release Notes](https://openai.com/products/release-notes/)

API Platform
*   [Overview](https://openai.com/api/)
*   [API Log In(opens in a new window)](https://platform.openai.com/login)
*   [Docs(opens in a new window)](https://developers.openai.com/api/docs)

Business
*   [Overview](https://openai.com/business/)
*   [Solutions](https://openai.com/solutions/)
*   [Resources](https://openai.com/business/learn/)
*   [Plugins](https://openai.com/business/plugins/)
*   [Customer Stories](https://openai.com/business/customer-stories/)
*   [Partner Network](https://openai.com/business/partners/)
*   [Contact Sales](https://openai.com/contact-sales/)

Developers
*   [Apps SDK(opens in a new window)](https://developers.openai.com/apps-sdk)
*   [Open Models](https://openai.com/open-models/)
*   [Docs(opens in a new window)](https://developers.openai.com/)
*   [Resources(opens in a new window)](https://developers.openai.com/learn)
*   [Developer Forum(opens in a new window)](https://community.openai.com/)

Company
*   [About Us](https://openai.com/about/)
*   [Our Charter](https://openai.com/charter/)
*   [Careers](https://openai.com/careers/)
*   [News](https://openai.com/news/)

Support
*   [Help Center(opens in a new window)](https://help.openai.com/)
*   [OpenAI Status(opens in a new window)](https://status.openai.com/)

More
*   [Stories](https://openai.com/stories/)
*   [Academy](https://openai.com/academy/)
*   [Supply Co.](https://openai.com/supply/)
*   [Livestreams](https://openai.com/live/)
*   [Podcast](https://openai.com/podcast/)
*   [RSS](https://openai.com/news/rss.xml)

Terms & Policies
*   [Terms of Use](https://openai.com/policies/terms-of-use/)
*   [Privacy Policy](https://openai.com/policies/privacy-policy/)
*   [Other Policies](https://openai.com/policies/)

[(opens in a new window)](https://x.com/OpenAI)[(opens in a new window)](https://www.youtube.com/OpenAI)[(opens in a new window)](https://www.linkedin.com/company/openai)[(opens in a new window)](https://github.com/openai)[(opens in a new window)](https://www.instagram.com/openai/)[(opens in a new window)](https://www.tiktok.com/@openai)[(opens in a new window)](https://discord.gg/openai)

OpenAI © 2015–2026 Your privacy choices

English United States
