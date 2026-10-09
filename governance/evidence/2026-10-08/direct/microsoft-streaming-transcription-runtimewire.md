Title: Microsoft adds streaming transcription and two voice models to its MAI lineup

URL Source: https://runtimewire.com/article/microsoft-mai-streaming-transcription-voice-models

Published Time: 2026-10-01T18:12:23.810Z

Markdown Content:
STORIES Handpicked by the editor
Released October 1st, the models target voice agents with incremental transcripts and two speech-generation options priced by usage.

**By Ryan Merket**Published Oct 1st, 2026, 1:12pm CT

![Image 1: Microsoft adds streaming transcription and two voice models to its MAI lineup](https://runtimewire.com/api/storage/uploads/source-images/microsoft-mai-streaming-transcription-voice-models-4f814fd0.png?w=1600&fmt=webp)

Source image: https://pbs.twimg.com/media/HTjspUrXcAAGhI8.png

Microsoft added streaming transcription and two text-to-speech models to its MAI lineup on October 1st, giving developers a set of Microsoft-built components for voice agents that need to listen and respond with less delay. The three models, announced in a [Microsoft AI post on X](https://x.com/MicrosoftAI/status/2105693024013467905), are MAI-Transcribe-2-Streaming, MAI-Voice-2.1 and MAI-Voice-2.1-Flash. Microsoft said they were available that day.

[Video 4](https://runtimewire.com/api/storage/public-objects/tweet-videos/microsoft-mai-streaming-transcription-voice-models-67ee4d9e.mp4)

_Video from the [original post on X](https://x.com/MicrosoftAI/status/2105693024013467905)._

Introducing 3 new models: MAI-Transcribe-2-Streaming, MAI-Voice-2.1 and MAI-Voice-2.1-Flash. Accurate streaming transcription. Natural speech and less waiting between turns. Build voice agents that keep the conversation moving!

The most consequential change is the streaming transcription model. Rather than wait for a speaker to finish an utterance before returning text, it accepts continuous audio over a WebSocket and sends incremental transcript updates before confirming a final segment, according to its [model listing on Vercel AI Gateway](https://vercel.com/ai-gateway/models/mai-transcribe-2-streaming). That lets an application display captions as someone speaks or begin processing a request before the sentence is complete. The listing names Azure as the provider and gives the model a price of $0.54 per audio hour.

Microsoft says the streaming model supports 60 languages with automatic language detection. Coverage of the launch reported that its first transcript hypotheses can arrive in the low hundreds of milliseconds, with words appearing as early as 320 milliseconds in most cases. Those figures describe Microsoft’s reported model performance; they are not a guarantee of end-to-end response time for a deployed voice agent, which also depends on network conditions, the application and the system generating the reply.

The other two releases generate speech from text. MAI-Voice-2.1 is positioned for higher-fidelity, expressive output, while the Flash version is aimed at applications where responsiveness and cost matter more. Vercel lists MAI-Voice-2.1 at $22 per million characters and Flash at $15 per million characters. The [MAI-Voice-2.1 listing](https://vercel.com/ai-gateway/models/mai-voice-2.1) describes support for 23 languages; Microsoft’s launch coverage says the model spans 23 languages and 26 locales. The [Flash listing on OpenRouter](https://openrouter.ai/microsoft/mai-voice-2.1-flash/) likewise describes it as a low-latency speech-generation model for interactive uses such as assistants and call centers.

The pricing makes the transcription model's intended use clearer. Microsoft launched batch-oriented MAI-Transcribe-2 in September at $0.10 per audio hour, a lower rate for audio processed without the same streaming behavior. The new model's $0.54 rate is 5.4 times that figure, though the comparison is between different workloads: continuous transcription has to return provisional results while audio is still arriving. Microsoft described the earlier $0.10 rate as a limited-time offer through the end of 2026, so it is not necessarily a permanent benchmark for the family.

For Microsoft AI chief executive Mustafa Suleyman, the release extends a product line built around bringing in-house models closer to Microsoft products and developer services. Suleyman co-founded DeepMind before Google acquired it, then co-founded Inflection AI, where the team built the Pi assistant. He joined Microsoft in 2024 to lead Microsoft AI, an organization formed with Inflection co-founder Karén Simonyan and several Inflection employees, according to [Microsoft's announcement at the time](https://blogs.microsoft.com/blog/2024/03/19/mustafa-suleyman-deepmind-and-inflection-co-founder-joins-microsoft-to-lead-copilot/). Microsoft's earlier model releases included transcription and speech systems; this launch adds an explicitly real-time transcription option alongside more differentiated speech-generation tiers.

That packaging addresses a practical development problem. A voice agent needs to recognize speech, decide what to do and produce an audible response. Separate models for transcription and speech generation give developers control over those pieces and let them choose different quality, latency and cost trade-offs. Microsoft is selling the components into a market that also includes specialist speech providers and other cloud platforms; the product announcement itself does not establish that its models outperform those alternatives in independent, like-for-like tests.

The commercial bet is straightforward: as developers build more spoken interfaces, Microsoft wants its models and cloud services in the request path, rather than serving only as the place where an application runs. For buyers, the useful test will be whether the incremental transcript and generated speech reduce pauses in real applications enough to justify per-character and per-hour costs. Microsoft's announcement sets out the components and pricing; actual agent response time will depend on how developers combine them with the rest of their systems.

Signal check

Noise Signal

Where does this story land? Drag the dial.2 readers have rated

[THE BRIEFING The deals, discoveries, and stories worth knowing before your next meeting. See what you’ve been missing. GET THE BRIEFING →](https://runtimewire.com/newsletter)

## Sources & references

1.   [Introducing 3 new models: MAI-Transcribe-2-Streaming, MAI-Voice-2.1 and MAI-Voice-2.1-Flash](https://x.com/MicrosoftAI/status/2105693024013467905) — Microsoft AI on X

Read online, with links to the original sources:
[https://runtimewire.com/article/microsoft-mai-streaming-transcription-voice-models](https://runtimewire.com/article/microsoft-mai-streaming-transcription-voice-models)

KEEP READING
