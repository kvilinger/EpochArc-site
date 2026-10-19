Title: Commerce Department Extends Export Controls to Advanced AI Models; Authorizes Release to Specific Trusted Partners

URL Source: https://www.mayerbrown.com/en/insights/publications/2026/06/commerce-department-extends-export-controls-to-advanced-ai-models-authorizes-release-to-specific-trusted-partners

Published Time: 6/30/2026

Markdown Content:
Through targeted, company-specific actions, the US government has taken the unprecedented step of extending export controls to both artificial intelligence (“AI”) models and the provision of access to such models, raising uncertainty for the cloud-computing and AI industry.

#### Background

On June 12, 2026, the US Commerce Department, under Secretary Howard Lutnick’s signature, issued an Is-Informed Letter (“IIL”) export control directive to Anthropic, requiring the company to obtain a license before any export, reexport, or transfer (in-country) of its Mythos and Fable models, including to any foreign person worldwide (including if employed by Anthropic in the United States). According to [public reporting](https://www.wsj.com/tech/ai/amazon-ceos-talks-with-u-s-officials-triggered-crackdown-on-anthropic-models-dcc90578), the [Anthropic IIL](https://www.bloomberg.com/news/articles/2026-06-16/read-the-lutnick-letter-that-led-anthropic-to-disable-mythos) followed outreach to senior government officials by a US company raising concerns that researchers had identified a method of bypassing safety guardrails, enabling access to the unrestricted cybersecurity capabilities such as identifying previously unknown “zero-day” vulnerabilities and generating working exploit code. Anthropic announced in response it was not technically feasible to block access only by foreign persons on short notice, and therefore that it had disabled the models for all users worldwide.

These actions followed the June 2, 2026, release of an Executive Order on promoting advanced AI innovation and security (see our recent [Legal Update](https://www.mayerbrown.com/en/insights/publications/2026/06/president-trump-signs-executive-order-on-advanced-ai-innovation-and-security)), which created a mechanism for voluntary collaboration between the AI industry and government on frontier model deployment.

One week after issuing the Anthropic IIL, Secretary Lutnick on June 26, 2026, issued a second letter, exempting “certain trusted partners” and their foreign national employees, along with Anthropic’s own foreign national employees, from the license requirement applicable to Mythos 5.The letter did not address exemptions related to the license requirement applicable to Fable 5. In a parallel announcement, Anthropic confirmed that the U.S. government approved deployment of Mythos 5 to a “set of U.S. organizations that operate and defend critical infrastructure.” On the same date, another AI model developer [announced](https://openai.com/index/previewing-gpt-5-6-sol/) that, as part of its next generation AI model launch it previewed the models’ capabilities to the government, and, at the government’s request, was releasing the AI models first to a “small group of trusted partners whose participation has been shared with the government.” The company asserted that this “short-term step” is “the strongest path to broader availability [of the AI models] in the coming weeks, while we work with the Administration to develop the cyber Executive Order framework and a repeatable process for future model releases.”

#### Legal Considerations

The Anthropic IIL asserts two substantive grounds for Commerce authority:

1.   Section 4817(b)(1) of the [Export Control Reform Act of 2018](https://www.govinfo.gov/content/pkg/PLAW-115publ232/pdf/PLAW-115publ232.pdf) (“ECRA”), which authorizes the Commerce Department to establish interim controls on emerging or foundational technologies essential to national security.
2.   Section 744.22(b) of the [Export Administration Regulations](https://www.bis.gov/regulations/ear) (“EAR”), which authorizes Commerce’s Bureau of Industry and Security (“BIS”)to inform a person that a license is required for specific exports, reexports, or transfers (in-country) of any item subject to the EAR when there is an unacceptable risk of diversion to a “military-intelligence end use” or “military-intelligence end user” in countries of concern, including China and Russia.

Commerce’s exercise of jurisdiction over an AI model as an item subject to ECRA and the EAR is novel, as is BIS’s assertion that provision of access to a model is an export, reexport, or in-country transfer.

##### Controls on AI Models

Under ECRA and the EAR, the Commerce Department identifies commodities, software, and technologies that are subject to its jurisdiction. If the AI models themselves are the controlled item, this would be the first time Commerce has treated an AI model itself,rather than its weights or source code, as controlled technology under the EAR.[1](https://www.mayerbrown.com/en/insights/publications/2026/06/commerce-department-extends-export-controls-to-advanced-ai-models-authorizes-release-to-specific-trusted-partners#_edn1) The January 2025 AI Diffusion Rule, for which the Trump Administration established a [non-enforcement policy](https://www.mayerbrown.com/en/insights/publications/2025/05/us-commerce-department-announces-new-export-compliance-expectations-related-to-artificial-intelligence), extended controls over model weights, not models (while remaining silent as to whether models constitute technology). Under statutory authority, “technology” is defined to include “information, in tangible or intangible form, necessary for the development, production or use” of a commodity, software, or other technology. The EAR use the term “required” instead of “necessary.” The IIL does not identify for which items under Commerce jurisdiction these AI models are necessary/required for development, production, or use.

##### Controls on API-based Access to an AI Model

The IIL treats remote, API-based access to a model as a “release” controlled under ECRA and the EAR. Yet Commerce’s consistent approach to this issue in the past has been that remote access to cloud-based software, without the transfer of technology or source code, is not an export (including intangible transfers of technology or “deemed exports”). Specifically, three BIS advisory opinions (2009, 2011, and 2014) have been widely relied upon across industry and remain posted on the BIS website. The assessment that remote access currently falls outside export-control jurisdiction is reinforced by pending legislation in Congress: the Remote Access Security Act would amend ECRA to authorize BIS to regulate remote access to items subject to the EAR. The existence of that bill reflects a legislative judgment that additional authority would be needed for BIS to reach remote access, which the IIL appears to assume it already has.

The IIL’s reliance on the EAR’s military-intelligence end use/end user provisions (tied directly in the Regulations to specific countries including China and Russia) for an access control is also notable. Given the reported offensive capabilities of these models, BIS’s determination of an unacceptable risk to foreign military-intelligence services has a factual basis in public record.

But identifying these grounds for a worldwide license requirement reaching every foreign person, regardless of country or end use, is without precedent.

##### Legal Challenge

The Commerce Department is already facing legal action over its Anthropic IIL: an Anthropic customer that used the Fable 5 model and has employees in Canada is seeking to vacate and enjoin the directive, including on grounds that it exceeds the government’s statutory authority.[2](https://www.mayerbrown.com/en/insights/publications/2026/06/commerce-department-extends-export-controls-to-advanced-ai-models-authorizes-release-to-specific-trusted-partners#_edn2)

#### [](https://www.mayerbrown.com/en/insights/publications/2026/06/commerce-department-extends-export-controls-to-advanced-ai-models-authorizes-release-to-specific-trusted-partners#_edn2)Implications for the AI Industry

If BIS now treats AI models themselves as controlled technology (whether through interim orders or industry-wide directives that have the weight of regulations) that precedent could reach far beyond one or two developers’ models. Similarly, if BIS has concluded that it can regulate remote access under its current legal authority, it could extend jurisdiction over a wide range of activity involving foreign persons that has historically fallen outside the reach of dual-use export-controls. Any company that offers AI-driven cloud products, particularly dual-use cybersecurity tools that identify software vulnerabilities or could be repurposed for offensive operations, could face the same treatment if BIS extends the IIL’s reasoning.

Under a broad reading of the IIL, customer-facing AIaaS, in which foreign persons access AI outputs remotely, and internal operations, where foreign-person employees develop or maintain AI infrastructure (whether inside or outside the United States) could trigger license obligations. A narrower reading is that BIS is seeking to address the offensive output capabilities of the AI models, rather than to assert jurisdiction over AI models generally.

Faced with what the US government views as a significant national security threat, Commerce activated the tools at its disposal (directives and negotiations), which do not preclude more-tailored controls in the future (e.g., the “repeatable process”). For example, once it has identified the technical parameters across AI models of concern, BIS could publish a control in the Export Control Classification Number 0Y521 holding category to create a common understanding across AI model developers regarding what thresholds engender US government concern.

#### How We Can Help

Please reach out to our Mayer Brown team if you have questions about how the US government is interpreting the ECRA and EAR and utilizing the voluntary process identified in the June 2026 AI Executive Order. We can help clients engage proactively with the US government and map their exposure to potential future controls.

* * *

[](https://www.mayerbrown.com/en/insights/publications/2026/06/commerce-department-extends-export-controls-to-advanced-ai-models-authorizes-release-to-specific-trusted-partners#_ednref1)1 While the EAR’s technology definition includes the word models, that reference dates at least to 1996, well before AI models existed.

[](https://www.mayerbrown.com/en/insights/publications/2026/06/commerce-department-extends-export-controls-to-advanced-ai-models-authorizes-release-to-specific-trusted-partners#_ednref2)2 _Legion LegalTech, Corp. v. United States_, No. 1:26-cv-02225

## Stay Up To Date With Our Insights

See how we use a multidisciplinary, integrated approach to meet our clients' needs.

[Subscribe](https://www.mayerbrown.com/en/subscribe)
