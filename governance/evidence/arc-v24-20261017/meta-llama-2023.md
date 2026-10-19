Title: Introducing LLaMA: A foundational, 65-billion-parameter language model

URL Source: https://ai.meta.com/blog/large-language-model-llama-meta-ai/

Markdown Content:
[](https://ai.meta.com/blog/large-language-model-llama-meta-ai/# "Go up one level")[![Image 1: Meta](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/252294889_575082167077436_6034106545912333281_n.svg/meta-logo-primary_standardsize.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=3pOt4aPU_ysQ7kNvwGP1DL0&_nc_oc=AdqWeIYBWMY7x9ygWT4HoYVaZuDpeMhvF7IJtIRDkExkxKQZWmfiOSlOHgnzhfPV7ck&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQMatkINPiLJ_04CyjmUWUi9vyLkR9DozLy9L08n7cuIkw&oe=6AD8B4B9)](https://ai.meta.com/)
*   [Products](https://ai.meta.com/blog/large-language-model-llama-meta-ai/#) 
*   [AI Research](https://ai.meta.com/blog/large-language-model-llama-meta-ai/#) 
*   [Resources](https://ai.meta.com/blog/large-language-model-llama-meta-ai/#) 
*   [About](https://ai.meta.com/blog/large-language-model-llama-meta-ai/#) 
*   [AI Developers](https://developer.meta.com/ai/?utm_source=ai_meta_site&utm_medium=web&utm_campaign=nav_AI-developers_07242026&utm_content=nav_AI-developers) 

*   [Try Muse](https://applink.muse.ai/?pt=10684&pid=ai_meta_site&utm_source=ai_meta_site&utm_medium=web&utm_campaign=nav_try-muse_09082026&utm_content=nav_try-muse_09082026&ct=nav_try-muse_09082026&referrer=utm_source%3Dai_meta_site%26utm_medium%3Dweb%26utm_campaign%3Dnav_try-muse_09082026%26utm_content%3Dnav_try-muse_09082026)
*   [](https://ai.meta.com/blog/large-language-model-llama-meta-ai/# "Toggle site search") 

[](https://ai.meta.com/blog/large-language-model-llama-meta-ai/# "Close submenu")

[](https://ai.meta.com/blog/large-language-model-llama-meta-ai/# "Main menu")

[BACK](https://ai.meta.com/blog/large-language-model-llama-meta-ai/# "Go up one level")

*   [Muse](https://ai.meta.com/muse/)
*   [Meta AI](https://ai.meta.com/meta-ai/assistant/)
*   [Media Generation](https://ai.meta.com/meta-ai/media-generation/)
*   [Vibes](https://ai.meta.com/meta-ai/vibes/)

*   [Overview](https://ai.meta.com/research/)
*   [Projects](https://ai.meta.com/research/#projects)
*   [Resources & Tools](https://ai.meta.com/resources/)
*   [Publications](https://ai.meta.com/results/?content_types[0]=publication)
*   [GitHub](https://github.com/facebookresearch/)

*   [Blog](https://ai.meta.com/blog/)
*   [Learning Hub](https://ai.meta.com/learn/)
*   [Demos](https://aidemos.meta.com/)

*   [Overview](https://ai.meta.com/about/)
*   [Open Source](https://ai.meta.com/opensourceai/)
*   [Careers](https://www.metacareers.com/)

Clear

*   Clear   
*   [Products >](https://ai.meta.com/blog/large-language-model-llama-meta-ai/#) 
*   [AI Research >](https://ai.meta.com/blog/large-language-model-llama-meta-ai/#) 
*   [Resources >](https://ai.meta.com/blog/large-language-model-llama-meta-ai/#) 
*   [About >](https://ai.meta.com/blog/large-language-model-llama-meta-ai/#) 
*   [AI Developers](https://developer.meta.com/ai/?utm_source=ai_meta_site&utm_medium=web&utm_campaign=nav_AI-developers_07242026&utm_content=nav_AI-developers)

[Try Muse](https://applink.muse.ai/?pt=10684&pid=ai_meta_site&utm_source=ai_meta_site&utm_medium=web&utm_campaign=nav_try-muse_09082026&utm_content=nav_try-muse_09082026&ct=nav_try-muse_09082026&referrer=utm_source%3Dai_meta_site%26utm_medium%3Dweb%26utm_campaign%3Dnav_try-muse_09082026%26utm_content%3Dnav_try-muse_09082026)

#### Research

# Introducing LLaMA: A foundational, 65-billion-parameter large language model

February 24, 2023

[Share on Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fai.meta.com%2Fblog%2Flarge-language-model-llama-meta-ai%2F)[Share on Twitter](https://twitter.com/intent/tweet?text=Introducing+LLaMA%3A+A+foundational%2C+65-billion-parameter+large+language+model+https%3A%2F%2Fai.meta.com%2Fblog%2Flarge-language-model-llama-meta-ai%2F)

**UPDATE:** We just launched [Llama 2](https://ai.meta.com/llama/) - for more information on the latest see our [blog post on Llama 2](https://ai.meta.com/blog/llama-2/).

As part of Meta’s commitment to open science, today we are publicly releasing LLaMA (Large Language Model Meta AI), a state-of-the-art foundational [large language model](https://ai.facebook.com/blog/democratizing-access-to-large-scale-language-models-with-opt-175b/) designed to help researchers advance their work in this subfield of AI. Smaller, more performant models such as LLaMA enable others in the research community who don’t have access to large amounts of infrastructure to study these models, further democratizing access in this important, fast-changing field.

Training smaller foundation models like LLaMA is desirable in the large language model space because it requires far less computing power and resources to test new approaches, validate others’ work, and explore new use cases. Foundation models train on a large set of unlabeled data, which makes them ideal for fine-tuning for a variety of tasks. We are making LLaMA available at several sizes (7B, 13B, 33B, and 65B parameters) and also sharing a LLaMA model card that details how we built the model in keeping with our approach to [Responsible AI practices](https://ai.facebook.com/blog/responsible-ai-progress-meta-2022/).

Over the last year, large language models — natural language processing (NLP) systems with billions of parameters — have shown new capabilities to generate creative text, [solve mathematical theorems](https://ai.facebook.com/blog/ai-math-theorem-proving/), [predict protein structures](https://ai.facebook.com/blog/protein-folding-esmfold-metagenomics/), answer reading comprehension questions, and more. They are one of the clearest cases of the substantial potential benefits AI can offer at scale to billions of people.

Even with all the recent advancements in large language models, full research access to them remains limited because of the resources that are required to train and run such large models. This restricted access has limited researchers’ ability to understand how and why these large language models work, hindering progress on efforts to improve their robustness and mitigate known issues, such as bias, toxicity, and the potential for generating misinformation.

Smaller models trained on more tokens — which are pieces of words — are easier to retrain and fine-tune for specific potential product use cases. We trained LLaMA 65B and LLaMA 33B on 1.4 trillion tokens. Our smallest model, LLaMA 7B, is trained on one trillion tokens.

Like other large language models, LLaMA works by taking a sequence of words as an input and predicts a next word to recursively generate text. To train our model, we chose text from the 20 languages with the most speakers, focusing on those with Latin and Cyrillic alphabets.

There is still more research that needs to be done to [address the risks of bias](https://ai.facebook.com/blog/measure-fairness-and-mitigate-ai-bias/), toxic comments, and hallucinations in large language models. Like other models, LLaMA shares these challenges. As a foundation model, LLaMA is designed to be versatile and can be applied to many different use cases, versus a fine-tuned model that is designed for a specific task. By sharing the code for LLaMA, other researchers can more easily test new approaches to limiting or eliminating these problems in large language models. We also provide in the paper a set of evaluations on benchmarks evaluating model biases and toxicity to show the model’s limitations and to support further research in this crucial area.

To maintain integrity and prevent misuse, we are releasing our model under a noncommercial license focused on research use cases. Access to the model will be granted on a case-by-case basis to academic researchers; those affiliated with organizations in government, civil society, and academia; and industry research laboratories around the world. People interested in applying for access can find the link to the application in our research paper.

We believe that the entire AI community — academic researchers, civil society, policymakers, and industry — must work together to develop clear guidelines around responsible AI in general and responsible large language models in particular. We look forward to seeing what the community can learn — and eventually build — using LLaMA.

[Read the paper](https://arxiv.org/abs/2302.13971)

[Read the model card](https://github.com/facebookresearch/llama/blob/main/MODEL_CARD.md)

[Apply for access to LLaMA](https://docs.google.com/forms/d/e/1FAIpQLSfqNECQnMkycAp2jP4Z9TFX0cGR4uf7b_fBxjY_OjhJILlKGA/viewform)

[Share on Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fai.meta.com%2Fblog%2Flarge-language-model-llama-meta-ai%2F)[Share on Twitter](https://twitter.com/intent/tweet?text=Introducing+LLaMA%3A+A+foundational%2C+65-billion-parameter+large+language+model+https%3A%2F%2Fai.meta.com%2Fblog%2Flarge-language-model-llama-meta-ai%2F)

### Research Areas

[Research](https://ai.meta.com/research/)

[Meta AI](https://ai.meta.com/meta-ai/assistant/)

[Assistant](https://ai.meta.com/meta-ai/assistant/)

[Media Generation](https://ai.meta.com/meta-ai/media-generation/)

[Vibes](https://ai.meta.com/meta-ai/vibes/)

[Muse](https://ai.meta.com/muse/)

[Agent](https://ai.meta.com/muse/)

[AI agents explained](https://ai.meta.com/learn/agentic-ai/what-are-ai-agents/)

[What is agentic AI](https://ai.meta.com/learn/agentic-ai/what-is-agentic-ai/)

[Agentic AI examples](https://ai.meta.com/learn/agentic-ai/agentic-ai-examples/)

[AI Research](https://ai.meta.com/research)

[Overview](https://ai.meta.com/research/)

[Projects](https://ai.meta.com/research/#projects)

[Resources & tools](https://ai.meta.com/resources/)

[Publications](https://ai.meta.com/results/?content_types%5B0%5D=publication)

[GitHub](https://github.com/facebookresearch/)

Resources

[Blog](https://ai.meta.com/blog/)

[Learning Hub](https://ai.meta.com/learn/)

[Demos](https://aidemos.meta.com/)

[About](https://ai.meta.com/about)

[Overview](https://ai.meta.com/about/)

[Open Source](https://ai.meta.com/opensourceai/)

[Careers](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams[0]=Artificial%20Intelligence&is_in_page=0)

![Image 2](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/87524316_2677189655726266_6338721200264445952_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Pnoc7Ktn2h4Q7kNvwE_5iDu&_nc_oc=AdoMfcRcbNps2eWZyXU2fBr_iYY7-4qRo6_JQpZGtfEzTmUIW0_9GVrBfxhHjPD2zBg&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQPd9kmZUputVMyRBGi9_yUYI5BRar2Oo4gJ3h89cJolxw&oe=6AED1E78)

![Image 3](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/85559716_2814260008668824_1992323131183726592_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=wK_rV7pwcvQQ7kNvwEElx4G&_nc_oc=AdoACasqF9gSTjRPU__EnJ_qfbW3E8N8Vl5IpNHwHXeJKjbDoX29f8F_gDoc9yvBt0I&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQPDtGyiBWJk4AT4LiWeOugAx1JqN72xXGg8g3eAJeehWA&oe=6AED234F)

[![Image 4](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=8GK7Nca9GDEQ7kNvwEnCE_g&_nc_oc=AdqcTKKWMRLsKFLNm2pPpu8fEPtyx7WtDVFmBlc6nSxM-fqP91uS3rLQK9X8i7QRUqQ&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQMGHMpCAPN6R0UEIqYzCS_C9yqClSZ2nWlz2TmIKcYVMg&oe=6AD8A4E7) ![Image 5](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=8GK7Nca9GDEQ7kNvwEnCE_g&_nc_oc=AdqcTKKWMRLsKFLNm2pPpu8fEPtyx7WtDVFmBlc6nSxM-fqP91uS3rLQK9X8i7QRUqQ&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQMGHMpCAPN6R0UEIqYzCS_C9yqClSZ2nWlz2TmIKcYVMg&oe=6AD8A4E7)](https://www.facebook.com/aiatmeta/)

[![Image 6](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=EOxnus0Vys8Q7kNvwFxdDfx&_nc_oc=AdpjsTP9j3jXrA0EER2byUFvj4ufdPM2XXsxColGFpvrrYOdMlmgLb775HBLV6XmzfA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQN_mac_H2U2bJg9elz7ty4iLKX4viSSeNsI0ZuFHSi0xg&oe=6AD89D22) ![Image 7](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=EOxnus0Vys8Q7kNvwFxdDfx&_nc_oc=AdpjsTP9j3jXrA0EER2byUFvj4ufdPM2XXsxColGFpvrrYOdMlmgLb775HBLV6XmzfA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQN_mac_H2U2bJg9elz7ty4iLKX4viSSeNsI0ZuFHSi0xg&oe=6AD89D22)](https://twitter.com/aiatmeta/)

[![Image 8](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=q7YsnXDxOwMQ7kNvwEXQF2b&_nc_oc=Adq9flbwbW5-qW7JyFoZRGvXwCqBvfNYO2cNKsqKOHiLXyIcfNoWJilpdjPSmOVY3HI&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNBelmqOGJ-YTZYIweSUcefpZUABPe27CQkUBPgJFT-tQ&oe=6AD8C8FB) ![Image 9](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=q7YsnXDxOwMQ7kNvwEXQF2b&_nc_oc=Adq9flbwbW5-qW7JyFoZRGvXwCqBvfNYO2cNKsqKOHiLXyIcfNoWJilpdjPSmOVY3HI&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNBelmqOGJ-YTZYIweSUcefpZUABPe27CQkUBPgJFT-tQ&oe=6AD8C8FB)](https://www.linkedin.com/showcase/aiatmeta)

[![Image 10](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=YfCiH5z29_MQ7kNvwEY1niA&_nc_oc=Adre_-mJvG01K19KIQO3ZRgQ4OKmGc-ehdyK5jBvtYk5MhRptzXsm4y1WO64OfUs2LA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNvMpu9Wg56RpB-XMutf_Rbd96PIuQcFxsoPDM8ajtMdQ&oe=6AD8AA2E) ![Image 11](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=YfCiH5z29_MQ7kNvwEY1niA&_nc_oc=Adre_-mJvG01K19KIQO3ZRgQ4OKmGc-ehdyK5jBvtYk5MhRptzXsm4y1WO64OfUs2LA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNvMpu9Wg56RpB-XMutf_Rbd96PIuQcFxsoPDM8ajtMdQ&oe=6AD8AA2E)](https://www.youtube.com/@aiatmeta)

Meta AI

[Meta AI](https://ai.meta.com/meta-ai/assistant/)[Assistant](https://ai.meta.com/meta-ai/assistant/)[Media Generation](https://ai.meta.com/meta-ai/media-generation/)[Vibes](https://ai.meta.com/meta-ai/vibes/)

Muse

[Muse](https://ai.meta.com/muse/)[Agent](https://ai.meta.com/muse/)[AI agents explained](https://ai.meta.com/learn/agentic-ai/what-are-ai-agents/)[What is agentic AI](https://ai.meta.com/learn/agentic-ai/what-is-agentic-ai/)[Agentic AI examples](https://ai.meta.com/learn/agentic-ai/agentic-ai-examples/)

AI Research

[AI Research](https://ai.meta.com/research)[Overview](https://ai.meta.com/research/)[Projects](https://ai.meta.com/research/#projects)[Resources & tools](https://ai.meta.com/resources/)[Publications](https://ai.meta.com/results/?content_types%5B0%5D=publication)[GitHub](https://github.com/facebookresearch/)

Resources

[Blog](https://ai.meta.com/blog/)[Learning Hub](https://ai.meta.com/learn/)[Demos](https://aidemos.meta.com/)

About

[About](https://ai.meta.com/about)[Overview](https://ai.meta.com/about/)[Open Source](https://ai.meta.com/opensourceai/)[Careers](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams[0]=Artificial%20Intelligence&is_in_page=0)

[![Image 12](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=8GK7Nca9GDEQ7kNvwEnCE_g&_nc_oc=AdqcTKKWMRLsKFLNm2pPpu8fEPtyx7WtDVFmBlc6nSxM-fqP91uS3rLQK9X8i7QRUqQ&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQMGHMpCAPN6R0UEIqYzCS_C9yqClSZ2nWlz2TmIKcYVMg&oe=6AD8A4E7) ![Image 13](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=8GK7Nca9GDEQ7kNvwEnCE_g&_nc_oc=AdqcTKKWMRLsKFLNm2pPpu8fEPtyx7WtDVFmBlc6nSxM-fqP91uS3rLQK9X8i7QRUqQ&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQMGHMpCAPN6R0UEIqYzCS_C9yqClSZ2nWlz2TmIKcYVMg&oe=6AD8A4E7)](https://www.facebook.com/aiatmeta/)

[![Image 14](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=EOxnus0Vys8Q7kNvwFxdDfx&_nc_oc=AdpjsTP9j3jXrA0EER2byUFvj4ufdPM2XXsxColGFpvrrYOdMlmgLb775HBLV6XmzfA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQN_mac_H2U2bJg9elz7ty4iLKX4viSSeNsI0ZuFHSi0xg&oe=6AD89D22) ![Image 15](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=EOxnus0Vys8Q7kNvwFxdDfx&_nc_oc=AdpjsTP9j3jXrA0EER2byUFvj4ufdPM2XXsxColGFpvrrYOdMlmgLb775HBLV6XmzfA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQN_mac_H2U2bJg9elz7ty4iLKX4viSSeNsI0ZuFHSi0xg&oe=6AD89D22)](https://twitter.com/aiatmeta/)

[![Image 16](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=q7YsnXDxOwMQ7kNvwEXQF2b&_nc_oc=Adq9flbwbW5-qW7JyFoZRGvXwCqBvfNYO2cNKsqKOHiLXyIcfNoWJilpdjPSmOVY3HI&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNBelmqOGJ-YTZYIweSUcefpZUABPe27CQkUBPgJFT-tQ&oe=6AD8C8FB) ![Image 17](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=q7YsnXDxOwMQ7kNvwEXQF2b&_nc_oc=Adq9flbwbW5-qW7JyFoZRGvXwCqBvfNYO2cNKsqKOHiLXyIcfNoWJilpdjPSmOVY3HI&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNBelmqOGJ-YTZYIweSUcefpZUABPe27CQkUBPgJFT-tQ&oe=6AD8C8FB)](https://www.linkedin.com/showcase/aiatmeta)

[![Image 18](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=YfCiH5z29_MQ7kNvwEY1niA&_nc_oc=Adre_-mJvG01K19KIQO3ZRgQ4OKmGc-ehdyK5jBvtYk5MhRptzXsm4y1WO64OfUs2LA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNvMpu9Wg56RpB-XMutf_Rbd96PIuQcFxsoPDM8ajtMdQ&oe=6AD8AA2E) ![Image 19](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=YfCiH5z29_MQ7kNvwEY1niA&_nc_oc=Adre_-mJvG01K19KIQO3ZRgQ4OKmGc-ehdyK5jBvtYk5MhRptzXsm4y1WO64OfUs2LA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNvMpu9Wg56RpB-XMutf_Rbd96PIuQcFxsoPDM8ajtMdQ&oe=6AD8AA2E)](https://www.youtube.com/@aiatmeta)

[Privacy Policy](https://www.facebook.com/about/privacy/)

[Terms](https://www.facebook.com/policies/)

[Cookies](https://www.facebook.com/policies/cookies/)

Meta © 2026

[![Image 20](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=8GK7Nca9GDEQ7kNvwEnCE_g&_nc_oc=AdqcTKKWMRLsKFLNm2pPpu8fEPtyx7WtDVFmBlc6nSxM-fqP91uS3rLQK9X8i7QRUqQ&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQMGHMpCAPN6R0UEIqYzCS_C9yqClSZ2nWlz2TmIKcYVMg&oe=6AD8A4E7) ![Image 21](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=8GK7Nca9GDEQ7kNvwEnCE_g&_nc_oc=AdqcTKKWMRLsKFLNm2pPpu8fEPtyx7WtDVFmBlc6nSxM-fqP91uS3rLQK9X8i7QRUqQ&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQMGHMpCAPN6R0UEIqYzCS_C9yqClSZ2nWlz2TmIKcYVMg&oe=6AD8A4E7)](https://www.facebook.com/aiatmeta/)

[![Image 22](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=EOxnus0Vys8Q7kNvwFxdDfx&_nc_oc=AdpjsTP9j3jXrA0EER2byUFvj4ufdPM2XXsxColGFpvrrYOdMlmgLb775HBLV6XmzfA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQN_mac_H2U2bJg9elz7ty4iLKX4viSSeNsI0ZuFHSi0xg&oe=6AD89D22) ![Image 23](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=EOxnus0Vys8Q7kNvwFxdDfx&_nc_oc=AdpjsTP9j3jXrA0EER2byUFvj4ufdPM2XXsxColGFpvrrYOdMlmgLb775HBLV6XmzfA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQN_mac_H2U2bJg9elz7ty4iLKX4viSSeNsI0ZuFHSi0xg&oe=6AD89D22)](https://twitter.com/aiatmeta/)

[![Image 24](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=q7YsnXDxOwMQ7kNvwEXQF2b&_nc_oc=Adq9flbwbW5-qW7JyFoZRGvXwCqBvfNYO2cNKsqKOHiLXyIcfNoWJilpdjPSmOVY3HI&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNBelmqOGJ-YTZYIweSUcefpZUABPe27CQkUBPgJFT-tQ&oe=6AD8C8FB) ![Image 25](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=q7YsnXDxOwMQ7kNvwEXQF2b&_nc_oc=Adq9flbwbW5-qW7JyFoZRGvXwCqBvfNYO2cNKsqKOHiLXyIcfNoWJilpdjPSmOVY3HI&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNBelmqOGJ-YTZYIweSUcefpZUABPe27CQkUBPgJFT-tQ&oe=6AD8C8FB)](https://www.linkedin.com/showcase/aiatmeta)

[![Image 26](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=YfCiH5z29_MQ7kNvwEY1niA&_nc_oc=Adre_-mJvG01K19KIQO3ZRgQ4OKmGc-ehdyK5jBvtYk5MhRptzXsm4y1WO64OfUs2LA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNvMpu9Wg56RpB-XMutf_Rbd96PIuQcFxsoPDM8ajtMdQ&oe=6AD8AA2E) ![Image 27](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=YfCiH5z29_MQ7kNvwEY1niA&_nc_oc=Adre_-mJvG01K19KIQO3ZRgQ4OKmGc-ehdyK5jBvtYk5MhRptzXsm4y1WO64OfUs2LA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=V7xkjfTWKn3MpZSImC85jA&_nc_ss=7b289&oh=00_AQNvMpu9Wg56RpB-XMutf_Rbd96PIuQcFxsoPDM8ajtMdQ&oe=6AD8AA2E)](https://www.youtube.com/@aiatmeta)
