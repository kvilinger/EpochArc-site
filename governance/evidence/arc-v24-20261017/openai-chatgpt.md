Title: Introducing ChatGPT

URL Source: https://openai.com/index/chatgpt/

Markdown Content:
We’ve trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer followup questions, admit its mistakes, challenge incorrect premises, and reject inappropriate requests.

ChatGPT is a sibling model to[InstructGPT⁠](https://openai.com/index/instruction-following/), which is trained to follow an instruction in a prompt and provide a detailed response.

We are excited to introduce ChatGPT to get users’ feedback and learn about its strengths and weaknesses. During the research preview, usage of ChatGPT is free. Try it now at[chatgpt.com⁠(opens in a new window)](https://chatgpt.com/).

### Samples

## Methods

We trained this model using Reinforcement Learning from Human Feedback (RLHF), using the same methods as[InstructGPT⁠](https://openai.com/index/instruction-following/), but with slight differences in the data collection setup. We trained an initial model using supervised fine-tuning: human AI trainers provided conversations in which they played both sides—the user and an AI assistant. We gave the trainers access to model-written suggestions to help them compose their responses. We mixed this new dialogue dataset with the InstructGPT dataset, which we transformed into a dialogue format.

To create a reward model for reinforcement learning, we needed to collect comparison data, which consisted of two or more model responses ranked by quality. To collect this data, we took conversations that AI trainers had with the chatbot. We randomly selected a model-written message, sampled several alternative completions, and had AI trainers rank them. Using these reward models, we can fine-tune the model using[Proximal Policy Optimization⁠](https://openai.com/index/openai-baselines-ppo/). We performed several iterations of this process.

ChatGPT is fine-tuned from a model in the GPT‑3.5 series, which finished training in early 2022. You can learn more about the 3.5 series[here⁠(opens in a new window)](https://beta.openai.com/docs/model-index-for-researchers). ChatGPT and GPT‑3.5 were trained on an Azure AI supercomputing infrastructure.

## Limitations

*   ChatGPT sometimes writes plausible-sounding but incorrect or nonsensical answers. Fixing this issue is challenging, as: (1) during RL training, there’s currently no source of truth; (2) training the model to be more cautious causes it to decline questions that it can answer correctly; and (3) supervised training misleads the model because the ideal answer[depends on what the model knows⁠(opens in a new window)](https://www.alignmentforum.org/posts/BgoKdAzogxmgkuuAt/behavior-cloning-is-miscalibrated), rather than what the human demonstrator knows.

*   ChatGPT is sensitive to tweaks to the input phrasing or attempting the same prompt multiple times. For example, given one phrasing of a question, the model can claim to not know the answer, but given a slight rephrase, can answer correctly.

*   The model is often excessively verbose and overuses certain phrases, such as restating that it’s a language model trained by OpenAI. These issues arise from biases in the training data (trainers prefer longer answers that look more comprehensive) and well-known over-optimization issues.[1](https://openai.com/index/chatgpt/#citation-bottom-1), [2](https://openai.com/index/chatgpt/#citation-bottom-2)

*   Ideally, the model would ask clarifying questions when the user provided an ambiguous query. Instead, our current models usually guess what the user intended.

*   While we’ve made efforts to make the model refuse inappropriate requests, it will sometimes respond to harmful instructions or exhibit biased behavior. We’re using the[Moderation API⁠](https://openai.com/index/new-and-improved-content-moderation-tooling/)to warn or block certain types of unsafe content, but we expect it to have some false negatives and positives for now. We’re eager to collect user feedback to aid our ongoing work to improve this system.

## Iterative deployment

Today’s research release of ChatGPT is the latest step in OpenAI’s[iterative deployment⁠](https://openai.com/index/language-model-safety-and-misuse/)of increasingly safe and useful AI systems. Many lessons from deployment of earlier models like GPT‑3 and Codex have informed the safety mitigations in place for this release, including substantial reductions in harmful and untruthful outputs achieved by the use of reinforcement learning from human feedback(RLHF).

We know that many limitations remain as discussed above and we plan to make regular model updates to improve in such areas. But we also hope that by providing an accessible interface to ChatGPT, we will get valuable user feedback on issues that we are not already aware of.

Users are encouraged to provide feedback on problematic model outputs through the UI, as well as on false positives/negatives from the external content filter which is also part of the interface. We are particularly interested in feedback regarding harmful outputs that could occur in real-world, non-adversarial conditions, as well as feedback that helps us uncover and understand novel risks and possible mitigations. You can choose to enter the[ChatGPT Feedback Contest⁠(opens in a new window)](https://cdn.openai.com/chatgpt/chatgpt-feedback-contest.pdf)[3](https://openai.com/index/chatgpt/#citation-bottom-3)for a chance to win up to$500 in API credits.[A](https://openai.com/index/chatgpt/#citation-bottom-A) Entries can be submitted via the feedback form that is linked in the ChatGPT interface.

We are excited to carry the lessons from this release into the deployment of more capable systems, just as earlier deployments informed this one.

*   [ChatGPT](https://openai.com/news/?tags=chatgpt)
*   [2022](https://openai.com/news/?tags=2022)

## Footnotes

1.   A

## References

1.   1
2.   2
3.   3
The inspiration for this contest comes in part from work by Kenway, Josh, Camille François, Sasha Costanza-Chock, Inioluwa Deborah Raji, and Joy Buolamwini._Bug Bounties For Algorithmic Harms? Lessons from Cybersecurity Vulnerability Disclosure for Algorithmic Harms Discovery, Disclosure, and Redress_. Washington, DC: Algorithmic Justice League. January 2022. Available at[https://ajl.org/bugs⁠(opens in a new window)](https://ajl.org/bugs). See also work by Brundage, Miles, Avin, Shahar, Wang, Jasmine, Belfield, Haydn, and Gretchen Krueger et al. “Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims,” April 2020. Available at[https://arxiv.org/abs/2004.07213⁠(opens in a new window)](https://arxiv.org/abs/2004.07213). See an earlier instance of such a competition at HackerOne. 2021b. “Twitter Algorithmic Bias.” HackerOne.[https://hackerone.com/twitter-algorithmic-bias?type=team⁠(opens in a new window)](https://hackerone.com/twitter-algorithmic-bias?type=team). Finally, see early published work on this topic from Rubinovitz, JB, “Bias Bounty Programs as a Method of Combatting Bias in AI,” August 2018. Available at[https://rubinovitz.com/2018/08/01/bias-bounty-programs-as-a-method-of-combatting⁠(opens in a new window)](https://rubinovitz.com/2018/08/01/bias-bounty-programs-as-a-method-of-combatting). [](https://openai.com/index/chatgpt/#citation-top-3)

## Author

OpenAI

## Acknowledgments

John Schulman, Barret Zoph, Christina Kim, Jacob Hilton, Jacob Menick, Jiayi Weng, Juan Felipe Ceron Uribe, Liam Fedus, Luke Metz, Michael Pokorny, Rapha Gontijo Lopes, Shengjia Zhao, Arun Vijayvergiya, Eric Sigler, Adam Perelman, Chelsea Voss, Mike Heaton, Joel Parish, Dave Cummings, Rajeev Nayak, Valerie Balcom, David Schnurr, Tomer Kaftan, Chris Hallacy, Nicholas Turley, Noah Deutsch, Vik Goel, Jonathan Ward, Aris Konstantinidis, Wojciech Zaremba, Long Ouyang, Leonard Bogdonoff, Joshua Gross, David Medina, Sarah Yoo, Teddy Lee, Ryan Lowe, Dan Mossing, Joost Huizinga, Roger Jiang, Carroll Wainwright, Diogo Almeida, Steph Lin, Marvin Zhang, Kai Xiao, Katarina Slama, Steven Bills, Alex Gray, Jan Leike, Jakub Pachocki, Phil Tillet, Shantanu Jain, Greg Brockman, Nick Ryder, Alex Paino, Qiming Yuan, Clemens Winter, Ben Wang, Mo Bavarian, Igor Babuschkin, Szymon Sidor, Ingmar Kanitscheider, Mikhail Pavlov, Matthias Plappert, Nik Tezak, Heewoo Jun, William Zhuk, Vitchyr Pong, Lukasz Kaiser, Jerry Tworek, Andrew Carr, Lilian Weng, Sandhini Agarwal, Karl Cobbe, Vineet Kosaraju, Alethea Power, Stanislas Polu, Jesse Han, Raul Puri, Shawn Jain, Benjamin Chess, Christian Gibson, Oleg Boiko, Emy Parparita, Amin Tootoonchian, Kyle Kosic, Christopher Hesse
