Title: Google Releases Gemini 3.8 Flash TTS and Flash-Lite TTS With Prompt-Based Voice Design

URL Source: https://www.marktechpost.com/2026/09/23/google-releases-gemini-3-8-flash-tts-and-flash-lite-tts-with-prompt-based-voice-design/

Published Time: 2026-09-23T20:20:12+00:00

Markdown Content:
Google has released [Gemini 3.8 Flash TTS and Gemini 3.8 Flash-Lite TTS](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/), 2 new text-to-speech models in its Gemini Audio family. Google calls them its most expressive audio generation models yet. Flash TTS targets creative direction and character voices. Flash-Lite TTS targets high-volume, cost-efficient production. Both let developers direct delivery line by line using natural language.

**Is it deployable?** Yes, both models are rolling out now through the [Gemini API](https://aistudio.google.com/docs/speech-generation) and [Google AI Studio](https://aistudio.google.com/generate-speech?model=gemini-3.8-flash-tts). Access is API-only, with no open weights for self-hosting. Enterprise API access via [Gemini Enterprise](https://docs.cloud.google.com/gemini-enterprise-agent-platform) is listed as coming soon.

## **What Google Shipped**

**The release splits TTS into 2 tiers with shared direction controls**:

*   **Gemini 3.8 Flash TTS** is built for deep creative direction and character design. Target uses include gaming, immersive audiobooks, podcasts and interactive media. It offers granular control over acting cues, pacing, dialect shifts and backchanneling.
*   **Gemini 3.8 Flash-Lite TTS** is built for high-volume, cost-efficient scale. Google positions it for dubbing, audio content creation and expressive voice agents. It offers fine-grained control over tone, pacing and expressive nuance.

In AI Studio, the playground links use the model identifiers `gemini-3.8-flash-tts` and [`gemini-3.8-flash-lite-tts`](https://aistudio.google.com/generate-speech?model=gemini-3.8-flash-lite-tts).

## **Voice Design From a Text Prompt**

Previous Gemini TTS offered 30 original voices. The 3.8 release moves to a much larger voice system.

*   **Generative voice design:** Flash TTS creates new voices from prompts describing role, accent and voice characteristics. This works across more than 100 languages and dialects. Google’s demos include a Melbourne DJ, a monotone robot and a Japanese dragon.
*   **Voice library:** Developers get 2,000+ production-ready voices. Coverage includes regional varieties like Mexican Spanish, Quebec French and Scots English.
*   **Save and scale:** Custom voices can be saved and reused, with minimal drift across projects.
*   **Voice remixing (coming soon):** Users will adjust a library voice’s timbre, pitch, pace and accent through prompts.

## **Directing the Performance**

Both models accept stage directions written in the script. Gemini can also steer delivery from natural script cues.

*   **Long-form generation:** Voice quality, pacing and timbre hold across hours of continuous audio.
*   **Native 2-speaker staging:** A single script drives a multi-turn conversation with distinct, separated voices.
*   **Vocal bursts:** Non-verbal cues like `<laughs>`, `<sigh>` and `<gasp>` add conversational texture.
*   **Backchanneling:** Active-listening interjections like `|mhm|` and `|yeah|` control reaction beats and comedic timing.

## **Voice Replication and Safety Controls**

Voice replication builds a consistent vocal profile from a 30-second audio sample. The sample must be your voice or one you have rights to use. Replication requires a verbal consent recording from the voice owner, matched against the reference speaker.

Every clip from Gemini Audio models carries a [SynthID](https://deepmind.google/models/synthid/) watermark. This imperceptible mark is embedded directly in the audio output. Replicated voices also carry C2PA content credentials. Google points to the [Gemini 3.8 Audio model card](https://deepmind.google/models/model-cards/gemini-3-8-audio/) for its broader safety approach.

## **Benchmark Results**

**Google reports these results for the new models:**

*   **Hume AI Voice Design Benchmark:** Flash TTS ranks #1 overall with a score of 71.4, per [Hume AI](https://www.hume.ai/rw-voice-eq).
*   **Accent modeling:** Flash TTS leads with a score of 60.8.
*   **Hume AI Overall Quality Index:** Flash TTS ranks #1 and Flash-Lite TTS ranks #2.
*   **[Voice Arena](https://voicearena.com/tts-leaderboard/us-english) blind preference:** Both models take top positions in Japanese, Brazilian Portuguese, Vietnamese, Modern Standard Arabic, Mexican Spanish and Hindi.

## **Key Takeaways**

*   Google launched Gemini 3.8 Flash TTS for creative work and Flash-Lite TTS for scale.
*   Flash TTS designs new voices from prompts across 100+ languages and dialects.
*   Developers get 2,000+ production voices, up from 30 originals.
*   Voice replication needs a 30-second sample plus a matching consent recording.
*   Flash TTS ranks #1 on Hume AI’s Voice Design Benchmark with 71.4.

## **FAQ**

1.   **What is Gemini 3.8 Flash TTS?** It is Google’s text-to-speech model for creative voice design and line-by-line performance direction. It is available through the Gemini API and Google AI Studio.
2.   **How is Flash-Lite TTS different?** Flash-Lite TTS is optimized for high-volume, cost-efficient workloads like dubbing and voice agents. It ranks #2 on Hume AI’s Overall Quality Index.
3.   **Can I clone my own voice?** Yes, with a 30-second sample and a verbal consent recording. It is unavailable in AI Studio in several regions, including the UK, EEA and India.

* * *

Check out the [**Technical Blog**](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/). All credit goes to the researcher of this project. Also,feel free to follow us on**[Twitter](https://x.com/intent/follow?screen_name=marktechpost)**and don’t forget to join our**[150k+ML SubReddit](https://www.reddit.com/r/machinelearningnews/)**and Subscribe to**[our Newsletter](https://magic.beehiiv.com/v1/f5e63dd4-5653-4f09-83e2-321a8b1ba526?email={{email}})**. Wait! are you on telegram?**[now you can join us on telegram as well.](https://t.me/machinelearningresearchnews)**

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.?**[Connect with us](https://forms.gle/MJjjVDPS7whH8Ngs6)**

[![Image 1](https://www.marktechpost.com/wp-content/uploads/2019/06/Screen-Shot-2021-09-14-at-9.02.24-AM-150x150.png)](https://www.marktechpost.com/)

##### [Asif Razzaq](https://www.marktechpost.com/author/6flvq/)

Asif Razzaq is the CEO of Marktechpost AI Media Inc.. As a visionary entrepreneur and engineer, Asif is committed to harnessing the potential of Artificial Intelligence for social good. His most recent endeavor is the launch of an Artificial Intelligence Media Platform, Marktechpost, which stands out for its in-depth coverage of machine learning and deep learning news that is both technically sound and easily understandable by a wide audience. The platform boasts of over 2 million monthly views, illustrating its popularity among audiences.
