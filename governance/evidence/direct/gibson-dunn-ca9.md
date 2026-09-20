Title: Ninth Circuit Clarifies Limits of DMCA Liability for AI-Generated Code

URL Source: https://www.gibsondunn.com/ninth-circuit-clarifies-limits-of-dmca-liability-for-ai-generated-code/

Published Time: 2026-09-18T23:32:05+00:00

Markdown Content:
Client Alert | September 18, 2026

* * *

**_The decision provides an important defense to claims that an AI tool violates the DMCA merely because it generates material resembling a plaintiff’s work without identifying the original author or including the accompanying copyright notices and licensing terms._**

On September 16, 2026, the Ninth Circuit upheld the dismissal of software programmers’ claims against GitHub, Microsoft, and OpenAI under the Digital Millennium Copyright Act (DMCA), for alleged unauthorized removal or alteration of “copyright management information” (CMI) from the plaintiffs’ source code._Doe v. GitHub, Inc._, No.24-7700, slip op. at 13–17 (9th Cir. Sept.16, 2026). The plaintiffs alleged that GitHub Copilot and OpenAI’s Codex violated the DMCA by reproducing their code without including its accompanying CMI—namely, the original authors or the accompanying copyright notices and licensing terms. But the Ninth Circuit concluded from the complaint’s allegations that Copilot and Codex simply generated new code that never contained CMI, rather than removing or altering CMI from copies of the plaintiffs’ existing code. The plaintiffs therefore had not alleged the removal or alteration of CMI necessary to state their claims under 17 U.S.C. §1202(b).

The decision also addresses an important distinction between two types of DMCA claims in AI litigation under Section 1202(b). Claims concerning a model’s _inputs_ challenge the removal of author or licensing information from source materials before those materials are used to train the model. Claims concerning a model’s _outputs_ challenge its reproduction of protected material without accompanying CMI. The court rejected the programmers’ output theory because they had not alleged facts showing removal or alteration of CMI from copies of their code, but it declined to consider the programmers’ input theory because they had failed to preserve it in the district court._Id._ at 9–11, 17. The court also rejected the argument that a copied work must be identical to the original to sustain a claim under Section 1202(b), explaining that minor cosmetic changes do not necessarily protect a defendant who substantially reproduces a protected work and removes its CMI._Id._ at 15–16._Doe_ highlights the significance of these DMCA claims in connection with AI-generated code, and the limits on using them as alternatives to traditional copyright-infringement claims.

**Background**

Section 1202 of the DMCA defines CMI to include authors’ names, copyright notices, and terms and conditions governing a work’s use when conveyed in connection with copies of the work. Section 1202(b)(1) prohibits intentionally removing or altering CMI without authority, while Section 1202(b)(3) prohibits distributing works or copies with knowledge that CMI has been removed or altered without authority. Both provisions also require knowledge, or reasonable grounds to know, that the conduct will “induce, enable, facilitate, or conceal” copyright infringement. 17 U.S.C. §1202(b)–(c). Section 1203 permits statutory damages of $2,500 to $25,000 for each violation of Section 1202. 17 U.S.C. §1203(c)(3)(B).

The plaintiffs in _Doe_ are programmers who published copyrighted code in public GitHub repositories under open-source licenses. They alleged that Copilot and Codex were trained on publicly available code and sometimes reproduced their code without identifying the original authors or including the accompanying copyright notices and licensing terms._Doe_, slip op. at 6–7.

The district court dismissed the DMCA claims finding Section 1202(b) required that the challenged copies be _identical_ to the plaintiffs’ original works, whereas the complaint’s examples included modified versions of the plaintiffs’ code. The court certified for interlocutory appeal the question of whether Sections 1202(b)(1) and (b)(3) require that the challenged copies be identical to the plaintiffs’ original works (the “identicality requirement.”)_Id._ at 8–9.

**The Ninth Circuit’s Decision**

**Generating Code Lacking Author Attribution Does Not Itself Establish Removal or Alteration of CMI.**The Ninth Circuit began with the statutory terms “remove” and “alter,” explaining that both contemplate an affirmative act directed at CMI connected to an existing work. Accordingly, merely alleging that a similar or derivative work lacks the original’s author or licensing information does not establish that the information was removed or altered under Section 1202(b)._Id._ at 14–15. The complaint alleged that Copilot learned statistical patterns from training materials and used a probabilistic process to generate code responsive to prompts. The court concluded that those allegations did not describe any action taken to remove or alter CMI attached to an existing work._Id._ The court contrasted that process with a traditional search engine’s retrieval and display of stored material, observing that a tool operating in that manner could present a stronger basis for alleging removal of CMI._Id._ at 17.

**Minor Changes to a Copied Work Do Not Necessarily Defeat a DMCA Claim.**The Ninth Circuit nevertheless rejected the district court’s view that a plaintiff can establish a violation of Section 1202(b) only if the challenged copy is identical to the original work, apart from the missing CMI._Id._ at 15. The court explained that where a defendant substantially reproduces a work but omits its CMI, that reproduction “will often be strong circumstantial evidence” that the information was removed._Id._ at 15–16. The court emphasized that minor cosmetic changes do not necessarily protect a defendant who substantially or entirely reproduces a protected work and removes its CMI._Id._ at 16.

**The Court Did Not Decide Whether Removing CMI Before AI Training Violates the DMCA.**The court distinguished the programmers’ claim that defendants allegedly removed CMI from the programmers’ code _before_ supplying that code to Copilot as training data._Id._ at 9. The court declined to consider that training-stage theory because the plaintiffs had not corrected the district court’s express understanding that their case did not challenge training.[[1]](https://www.gibsondunn.com/ninth-circuit-clarifies-limits-of-dmca-liability-for-ai-generated-code/#_ftn1)

**What It Means.**_Doe_ provides an important defense to claims that an AI tool violates the DMCA merely because it generates material resembling a plaintiff’s work without identifying the original author or including the accompanying copyright notices and licensing terms. A plaintiff must allege facts supporting removal or alteration of that CMI from copies of an existing work to sustain a claim under Section 1202(b)—not simply its absence from an AI-generated response.

For companies developing or integrating AI systems, relevant questions include what CMI accompanies source materials, whether particular collection or processing steps remove it, whether removal is intentional, and what happens to the resulting copies. The rejection of strict identicality means that modest changes to copied material are not a categorical defense where the facts otherwise support removal of CMI._Id._ at 10–11, 15–16.

For rights holders,_Doe_ underscores the importance of identifying when and how author credits, copyright notices, or licensing terms allegedly were removed from their works. To survive Rule 12(b)(6), a DMCA claim based on a model’s output lacking CMI must allege facts supporting that the missing CMI was removed or altered from copies of existing works.

[[1]](https://www.gibsondunn.com/ninth-circuit-clarifies-limits-of-dmca-liability-for-ai-generated-code/#_ftnref1)The court also held that the plaintiffs had standing, finding the complaint sufficiently alleged a substantial risk that the Plaintiffs’ code would be reproduced without author attribution. The court highlighted the complaint’s examples of Copilot reproducing portions of the named plaintiffs’ code. The court emphasized that these allegations sufficed at the pleading stage without deciding whether the referenced evidence would establish standing at summary judgment._Id._ at 12–13

* * *

The following Gibson Dunn lawyers prepared this update: Ilissa Samplin and Doran Satanove.

Gibson Dunn’s lawyers are available to assist in addressing any questions you may have regarding these issues. Please contact the Gibson Dunn lawyer with whom you usually work, the authors, or any leader or member of the firm’s Intellectual Property,Artificial Intelligence, or Media, Entertainment, and Technology practice groups:

**Intellectual Property**:****Kate Dominguez– New York (+1 212.351.2338,[kdominguez@gibsondunn.com](mailto:kdominguez@gibsondunn.com))  
 Josh Krevitt– New York (+1 212.351.4000,[jkrevitt@gibsondunn.com](mailto:jkrevitt@gibsondunn.com))  
 Jane M. Love, Ph.D.– New York (+1 212.351.3922,[jlove@gibsondunn.com](mailto:jlove@gibsondunn.com))

**Artificial Intelligence**:  
 Cassandra L. Gaedt-Sheckter– Palo Alto (+1 650.849.5203,[cgaedt-sheckter@gibsondunn.com](mailto:cgaedt-sheckter@gibsondunn.com))  
 Vivek Mohan– Palo Alto (+1 650.849.5345,[vmohan@gibsondunn.com](mailto:vmohan@gibsondunn.com))  
 Eric D. Vandevelde– Los Angeles (+1 213.229.7186,[evandevelde@gibsondunn.com](mailto:evandevelde@gibsondunn.com))

**Media, Entertainment, and Technology**:  
 Kevin Masuda– Los Angeles (+1 213.229.7872,[kmasuda@gibsondunn.com](mailto:kmasuda@gibsondunn.com))  
 Benyamin S. Ross– Los Angeles (+1 213.229.7048,[bross@gibsondunn.com](mailto:bross@gibsondunn.com))  
 Brian C. Ascher– New York (+1 212.351.3989,[bascher@gibsondunn.com](mailto:bascher@gibsondunn.com))  
 Ilissa Samplin– Los Angeles (+1 213.229.7354,[isamplin@gibsondunn.com](mailto:isamplin@gibsondunn.com))  
 Doran J. Satanove– New York (+1 212.351.4098,[dsatanove@gibsondunn.com](mailto:dsatanove@gibsondunn.com))

© 2026 Gibson, Dunn & Crutcher LLP. All rights reserved. For contact and other information, please visit us at www.gibsondunn.com.

Attorney Advertising: These materials were prepared for general informational purposes only based on information available at the time of publication and are not intended as, do not constitute, and should not be relied upon as, legal advice or a legal opinion on any specific facts or circumstances. Gibson Dunn (and its affiliates, attorneys, and employees) shall not have any liability in connection with any use of these materials. The sharing of these materials does not establish an attorney-client relationship with the recipient and should not be relied upon as an alternative for advice from qualified counsel. Please note that facts and circumstances may vary, and prior results do not guarantee a similar outcome.
