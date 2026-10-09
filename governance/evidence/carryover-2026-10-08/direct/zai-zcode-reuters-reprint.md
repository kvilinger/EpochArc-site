Title: Chinese AI firm Z.ai disables coding assistant features; issues apology after security backlash

URL Source: https://www.thenews.com.pk/latest/1417148-chinese-ai-firm-zai-disables-coding-assistant-features-after-security-backlash

Published Time: 2026-09-22T11:00:00+05:00

Markdown Content:
![Image 1: Chinese AI firm Z.ai disables coding assistant features; issues apology after security backlash](https://www.thenews.com.pk/assets/uploads/updates/2026-09-22/1417148_9400073_Untitled-design---2026-09-22T105705_464_updates.jpg)

Chinese AI firm Z.ai disables coding assistant features; issues apology after security backlash

Chinese artificial intelligence firm Z.ai (also known as Zhipu AI) disabled certain features of its ZCode coding assistant after developers discovered the tool was silently packaging and uploading local project workspaces and Git histories to external cloud servers without explicit user consent.

## Key details of security incident:

Independent developers and tech bloggers revealed that ZCode was automatically packaging large local directories—including commercial project code and full Git histories containing sensitive metadata and attempting to upload them to Alibaba Cloud storage.

The behavior was traced back to the assistant's Codebase Indexing feature (used for session checkpoints, version rollbacks, and wiki generation), which was enabled by default upon launch and lacked a clear user toggle to turn it off.

Captured archives were heavily compressed and encrypted using private keys held exclusively on Z.ai's backend servers.

This prevented affected users from independently opening the files to verify what was transmitted, sparking widespread criticism and trust concerns within the developer community.

## Z.ai’s Response:

Beijing-based Z.ai, also known as Zhipu, apologized in a social media post after Chinese developers last week wrote on social media that its ZCode had uploaded their code data from open-source developer platform Git to Alibaba Cloud.

Z.ai issued a formal apology, admitted that the indexing feature caused the unintended data transmission, and stated that a patch has been rolled out to disable the problematic features.

The company claimed that an independent security assessment by an affiliated think tank and cybersecurity firm NSFOCUS verified that user data was deleted and not retained.

However, because the original data archives were encrypted by default, outside verification remains challenging.

In an effort to repair its reputation and rebuild trust, Z.ai pledged to open-source the ZCode codebase to allow third-party security audits and transparency.
