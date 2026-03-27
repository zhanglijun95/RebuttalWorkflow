Thank you for the detailed review and for raising questions about formulation, realism, and evaluation. Many of these concerns relate to the same core issue, namely what the paper is intended to validate under realistic industrial data constraints, and what should be left to future system components [这里的what should be left to future system components不是很理解想表达什么].

**W1:** The problem formulation is unclear. [问题1应该首先是关于论文写作的structure的其中包括关于problem formulation的，the description of the proposed method and the data processing pipeline is scattered across multiple sections，我非常不同意他的这个问题，之前我也跟你说过，我们的结构非常整齐]
**A1:** [所以首先回答关于论文结构的，尤其是method和data processing是怎么按序组织的。]We would like to first clarify that the formal problem statement is already given in Section 2, where we define the pre-stow state, the new-item observation, the stow intent, and the post-stow target state, together with the transition model `F_theta: X x O x U -> X` [关于problem formulation的内容另起一段写]. The method is then presented in the same chronological order as the pipeline itself [这句话意义不明，看不懂，其实我们是想说Sec3是我们的framework的部分，然后写的很清楚每个subsection是干什么的]. Section 3.2 describes how raw production data is converted into slot-aligned supervision, Section 3.3 describes how these inputs are encoded into tokens and embeddings, and Section 3.4 describes the diffusion model. In that sense, the structure is already explicit [这句话有点aggresive，不这么写比较好]. At the same time, your comment is useful because the train/test inputs and supervision signals can be stated more prominently before the architecture, which would make the paper easier to parse on a first read [最后这句很没必要，为什么一定要同意他，我们的结构在3.1就是有明确写清楚的，应该point out to him].

**W2:** The “world model” characterization is questionable. [你仔细阅读第二个weakness就会发现，reviewer理解的world model和我们理解的是一样的，他之所以问这个问题是因为我们用了从GT post-stow extract的new item mask，他会质疑这个world model是否真的做到了，又或者是不是真的是world model，这和下面的W3 / W4 / W6 / Q2 / Q3是一脉相承的问题，因此我认为我们应该这么写：把这几个合并，然后总结出reviewer的concern来自于用了这个从GT post-stow extract的new item mask，从这个concern衍生出几个问题xxx/xxx/xxx，然后回答的时候我们还是要先回答为什么用了这个setting，也就是类似我们给Dwiz写的第二和第三段，但这一次的侧重点是我们要在real scenario没有这个信息的情况先做proof-of-concept，这在原文的line 657-661有提到，也就是你后面写的"This choice is meant to isolate the core modeling question: if a representation of the incoming item’s contact-side geometry is available, can a model predict how the bin will reconfigure after the stow?"。然后我们来逐一回答衍生的几个问题，包括这个model是否真的学习到了dynamics而不是简单的"a placement transform for a known silhouette"，然后是test time没有这样的mask怎么办，我们论文里line 661-665有提到一些解决办法包括加摄像头、用3D reconstruction等等，然后提出我们这里用SAM3D来替换new item mask的结果，最后是object silhouette是否多少泄露了一些信息，其实是肯定的，通过对比用SAM3D的结果和那个GT mask的结果就能看出来，当然这个IoU用SAM3D的时候变差了也有一部分原因是SAM3D也有误差。所以现在你应该知道这个问答和下一个问答怎么合并并且怎么组织了。] 
**A2:** We would like to clarify the intended meaning of “world model” in this paper. The claim is not that FOREST is a full RGB environment simulator. Rather, it is a model of future state transitions over a task-relevant object-centric representation of the bin. In other words, the paper studies structured future-state prediction for robotic stow under sparse snapshot supervision. That is the level at which we believe the term should be interpreted here. 

**W3 / W4 / W6 / Q2 / Q3:** The canonical new-item mask is privileged information, may reduce the task to placement, and raises deployment concerns.  
**A3:** This is the central weakness of the paper, and it is also where we think the paper still has value if interpreted correctly. The canonical new-item mask is used as a proxy for the in-bin contact-surface view because the production data does not provide such a view directly. This choice is explicitly stated in the paper and is meant to isolate the core modeling question: if a representation of the incoming item’s contact-side geometry is available, can a model predict how the bin will reconfigure after the stow? That proxy certainly gives the model useful information [我觉得用proxy这个词不对，因为首先new item mask本来就是input，这里用GT post-stow提取出来的本来就是一定的作弊，这也是为什么我们要用canonicalization去掉pose和location的信息], and we do not want to understate that.

However, the results do not support the interpretation that FOREST is merely learning a placement transform for a known silhouette. If that were the case, one would not expect substantial improvement on the motion of pre-existing items. Yet in sweep insert, O-IoU rises from 0.5287 for copy-paste(+gravity) to 0.6878/0.6906 for FOREST. This indicates that the model is learning part of the rearrangement dynamics of the existing items as well. The same conclusion is supported by the downstream evaluations, where DLO predictions driven by FOREST masks are much closer to those obtained from ground-truth masks than heuristic alternatives are.

To make this issue more concrete, we additionally tested a weaker proxy [其实不是weaker proxy而是real solution] in which the in-bin contact-surface view is estimated from the induct-view image using SAM3D rather than derived from the ground-truth post-stow mask:

| Setting | DI N | DI O | SW N | SW O |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D proxy | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

The expected drop confirms that the idealized proxy helps [这句话的分析就非常不好，显得好像没有ideal的mask效果就完全不行了]. At the same time, the model still substantially outperforms heuristics under the weaker, noisier pre-insertion proxy [the weaker, noisier pre-insertion proxy这种说法也是不对的]. Our interpretation [Our interpretation这种句式也不好，直接说分析或者结论就行了] is therefore not that the deployment problem is solved, but that the paper validates the core predictive component and shows that its value does not disappear once the proxy is weakened.

**W5:** Baselines are weak and there is no strong learned comparison.  
**A4:** This concern is fair, and we think the right way to frame it is through the structure of the problem [这个总起句看不懂，所以你到底同不同意review的说法？the right way to frame it是什么意思？]. The setting here is not standard video prediction, and it is not ordinary RGB generation [这句话就非常没有逻辑]. The supervision is temporally sparse, the prediction target is object-centric bin state rather than appearance, and the relevant signal for stow is geometry and occupancy rather than texture [这句话是具体的分析我们target的问题本身才对]. For that reason, off-the-shelf video or RGB generative baselines are not directly suitable without substantial redesign for this task [这句话才是重点，才是总起，那就是没有baselines能在不redesign的情况下能直接用或者有好结果(RGB的结果不好)]. This is why the paper compares against strong deterministic heuristics that are natural for this state-based setting, and then supplements that comparison with downstream evaluations of utility. We do not mean that this settles the learned-baseline question completely, but rather that the current comparisons are appropriate for a first study of this specific problem setting [这句话可以保留但是说法要换，现在这样说太模糊了，我们可以直接简单一点但是有礼貌]. [整个这个回答都要改，逻辑非常不好]

**Q1:** Why predict instance-mask layouts rather than final images?  
**A5:** The main reason is that texture is not the key variable governing stow dynamics. What matters most for post-stow prediction is occupancy, shape, contact, and the motion induced in neighboring items. The mask-based representation focuses the model on exactly those quantities, while avoiding the additional burden of synthesizing appearance that is less relevant to the downstream reasoning tasks considered in the paper [具体一点，什么downstream reasoning tasks].

---

## Revised Draft

**Thank you for the detailed review and for the thoughtful questions on formulation, realism, and evaluation.**

**W1:** The problem formulation is unclear, and the method/data-processing pipeline is scattered across multiple sections.  
**A1:** We would like to first clarify the paper structure, because this point seems to come from a different reading of how the method is organized. Section 2 gives the formal problem statement, including the pre-stow state, the new-item observation, the stow intent, the post-stow target state, and the transition model. Section 3 is then the framework section. Within Section 3, the subsections are organized in the same order as the actual pipeline described in Section 3.1. Section 3.2 explains how the raw production data is processed into supervised signals ["namely materialize the inputs introduced in Section 2 problem statement"我觉得应该加上类似这样的描述], Section 3.3 explains how these signals are encoded into tokens and embeddings, and Section 3.4 explains the diffusion model itself. In this sense, the data processing and the method are already presented in a structured and sequential way rather than being scattered. If anything should be improved, it is not the overall organization, but the prominence of the key train/test signals at the beginning of Section 3.1 so that the link between the formal problem statement and the framework is even easier to see [if anything should be...这句话太难理解了，你什么意思？到底要不要improve？].

**W2 / W3 / W4 / W6 / Q2 / Q3:** The use of a new-item mask extracted from the post-stow state raises questions about whether the model is truly a world model, whether it learns dynamics or only placement, and how it can be used at test time[太精简了，你还记得我在第一版的详细的comments吗？里面列出了三个问题，我们这里用bullet points列出来它们].  
**A2:** These concerns all stem from the same source, namely the use of the in-bin contact-surface view of the new item[是因为这个view来自于GT post-stow，不是用了这个view有什么问题啊]. We therefore answer them together. [从这里应该分段，然后每一段总分结构不能忘了]The paper intentionally studies a proof-of-concept setting in which this contact-surface view is assumed available. This is stated explicitly in the paper and in Appendix C[这句话有点aggresive，好像是指责reviewer没看到似的，直接说as stated in xx不行吗？]. The reason for introducing this setting is that in a real production scenario this information is not directly provided, but we still want to answer a more basic question first. If a representation of the incoming item’s contact-side geometry is available, can a model predict how the bin will reconfigure after the stow? This is the core modeling question that the paper isolates [这个单个的句子挺好的，但是和上文来来回回都在说一个意思].[所以就是第一段的结构非常差，我之前有说过，第一段的回答应该是“先回答为什么用了这个setting，也就是类似我们给Dwiz写的第二和第三段，但这一次的侧重点是我们要在real scenario没有这个信息的情况先做proof-of-concept，这在原文的line 657-661有提到，也就是你后面写的"This choice is meant to isolate the core modeling question: if a representation of the incoming item’s contact-side geometry is available, can a model predict how the bin will reconfigure after the stow?"”所以重点是我们还是要讲清楚这是real，real有什么特点，具体到我们想做的事是怎么回事，这一段的逻辑太差了。总分的结构不是让人说废话，而是更有条理]

[在讲完大背景，也就是为什么要用这个mask之后，我们逐一回答列的三个问题，可以用A2-1这样的格式。包括这个model是否真的学习到了dynamics而不是简单的"a placement transform for a known silhouette"，这个你之前回答过呀，怎么不用了呢？然后是test time没有这样的mask怎么办，我们论文里line 661-665有提到一些解决办法包括加摄像头、用3D reconstruction等等，然后提出我们这里用SAM3D来替换new item mask的结果，最后是object silhouette是否多少泄露了一些信息，其实是肯定的，通过对比用SAM3D的结果和那个GT mask的结果就能看出来，当然这个IoU用SAM3D的时候变差了也有一部分原因是SAM3D也有误差。所以现在你应该知道这个问答和下一个问答怎么合并并且怎么组织了。]
At the same time, the concern about information leakage is valid [这是最后一个问题，而且这种xxx is valid的句子非常没有意义，回答问题就行了]. The new-item mask used in the main setting is extracted from the post-stow state and then canonicalized to remove pose and location. This does not remove all privileged information, and we should be explicit about that. However, the resulting model is not merely learning a placement transform for a known silhouette [这是第一个问题才对，怎么混到一起了]. If that were the case, one would not expect substantial gains on the motion of pre-existing items. Yet in sweep insert, O-IoU rises from 0.5287 for copy-paste(+gravity) to 0.6878/0.6906 for FOREST. This indicates that the model is also capturing how existing items are displaced and rearranged, not only where the new item should go. The same conclusion is supported by the downstream evaluations, where DLO predictions driven by FOREST masks are much closer to those obtained from ground-truth masks than heuristic alternatives are.

The test-time question is also important. The paper already discusses possible solutions in lines 661-665, including additional cameras or deriving the needed view through a separate 3D reasoning module. To make this issue more concrete, we additionally replace the ground-truth-derived new-item mask with a practical pre-insertion solution [什么叫做pre-insertion solution？] based on SAM3D, which generates the in-bin contact-surface view from the induct-view image by first constructing the 3D map for the new item ["then retrain the FOREST diffusion model with this mask to see performance"应该有类似这样的话]:

| Setting | DI N | DI O | SW N | SW O |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

The gap between the SAM3D results and the main results confirms that the ground-truth-derived mask provides an advantage[这个话太模糊了，该承认的就应该承认，那就是GT提取的mask应该还是leak了一些post-stow shape上的信息所以IoU更高，但是这句话应该是和回答最后一个问题放在一起，而且放在最后A2-3]. At the same time, the SAM3D-based setting remains substantially stronger than heuristics, which means the predictive value of the model does not disappear [用still preserve就好，不要用does not disappear] once the idealized input is replaced by a more realistic pre-insertion estimate. Our conclusion is therefore not that the deployment problem is fully solved, but that the paper validates the core predictive component and shows that it continues to help under a more practical substitute for the new-item input [这个conclusion太啰嗦了，把观点说清楚就可以了].

**W5:** Baselines are weak and there is no strong learned comparison.  
**A3:** The key issue here is the structure of the task itself. This problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the target is an object-centric bin state rather than future appearance, and the relevant signal for stow is geometry and occupancy rather than texture. For that reason, off-the-shelf video or RGB generative baselines are not directly suitable without substantial redesign, and in our own experience simple RGB-conditioned generation performs poorly for exactly this reason. This is why the paper compares against deterministic heuristics that are natural for this state-based setting, and then supplements that comparison with downstream evaluations. We do not mean that this fully settles the learned-baseline question. Rather, the current comparisons should be read as an appropriate first evaluation for this specific sparse-snapshot stow problem. [还是写的非常非常的差，你有仔细看我之前一版的comment吗？我们要先关键的总起句，然后抽丝剥茧一点一点把该讲的东西按逻辑顺序讲清楚，重新组织]

**Q1:** Why predict instance-mask layouts rather than final images?  
**A4:** The main reason is that texture is not the key variable governing stow dynamics. What matters most for post-stow prediction is occupancy, shape, contact, and the motion induced in neighboring items. The mask-based representation focuses the model on exactly those quantities. It is also more aligned with the downstream tasks considered in the paper, DLO prediction and multi-stow reasoning, both of which depend primarily on geometry and object arrangement rather than appearance synthesis.

---

## Revised Draft V2

Thank you for questions on formulation, realism, and evaluation.

**W1:** The problem formulation is unclear, and the method/data-processing pipeline is scattered across multiple sections.  
**A1:** We would like to first clarify the organization of the paper, because we do not think the method and data processing are actually scattered [你怎么这么写啊，we do not think...这么写是不对的，你在写academic paper rebuttal呀，你这么写太冒犯了]. Section 2 gives the formal problem statement, including the pre-stow state, the new-item observation, the stow intent, the post-stow target state, and the transition model. Section 3 is then the framework section. Within Section 3, the subsections are ordered according to the actual pipeline [你怎么把我加的内容删掉了啊？我明明还写了section 3.1]. Section 3.2 explains how raw production data is processed into supervised signals, namely how the inputs introduced in the formal problem statement are materialized from the dataset. Section 3.3 explains how these signals are encoded into tokens and embeddings. Section 3.4 explains the diffusion model itself. In this sense, the method is presented in a structured and sequential manner. If anything can be improved, it is simply to make the connection between the formal problem statement and the three framework stages even more explicit at the beginning of Section 3.1 [我说了多少遍了，if anything should be...这句话太难理解了，你到底什么意思？到底要不要improve？你要是想说we will revise xx 就直说。].

**W2 / W3 / W4 / W6 / Q2 / Q3:** The use of a new-item mask extracted from the GT post-stow state raises questions about whether the model is truly a world model, whether it learns dynamics or only placement, and how it could be used at test time [我让你按照bullet points列我在第一版的时候就提的几个问题你为什么不做？我说的三个问题是这个model是否真的学习到了dynamics，然后是test time没有这样的mask怎么办，最后是object silhouette是否多少泄露了一些信息，你为什么不听我的？].  
**A2:** These concerns are tightly connected, and they all stem from the same design choice, namely that the new-item input in the main setting is derived from the GT post-stow state [这句话太长了，你的语言要formal要to-the-point]. [这里加上一个过渡句，说我们会首先解释为什么用这个mask，然后逐一回答上面列的三个问题]

The reason for introducing this setting is not that such information is directly available in a real deployment [我很困惑，你的意思是我们用GT提取的mask不是real deployment里这个信息是available？什么意思？意思是原因是这个信息在real deployment不available？怎么会是这个原因啊，你认真理解了吗？你理解了我在和Dwiz解释"Our goal is not to study stow under fully curated academic supervision, but to study production-style robotic stow, where the available data is large-scale yet inherently incomplete."这件事的意义和重要性了吗？我们在这里要解释为什么用这个mask是一样的道理啊，你要说清楚啊]. Rather, the paper first studies a proof-of-concept scenario in order to isolate the core predictive question. In a real production setting, the in-bin contact-surface view of the new item is not directly given [你的这句话是及其不负责的，为什么real production里这个view是not directly given？明明加个摄像头就能解决的事]. Before solving that perception problem, we first want to know whether a model can predict how the bin will reconfigure if a representation of that contact-side geometry is available. This is the motivation behind the setting described in the paper around lines 657-661. [我看你根本没理解我一直以来要解释类似于和Dwiz的第二和第三段解释的原因是不是？我们要解释受限于这个ARMBench没有啊，逻辑是我们要做production-style robotic stow -> ARMBench是我们能找到的唯一的production的stow，它不仅production，还有一个非常real的特点是不是你想要什么数据就能有的，它只有最常有的"In a real warehouse system, what one commonly has is a large number of executed stows together with before/after observations and operational metadata." -> 因此为了绕开数据收集，在这种数据不全的情况下，我们还是想先proof-of-concept，因此使用了一个get-around的方案，这种proof-of-concept也十分real，因为在production我们要先确定方案有用，再去架设额外的摄像头收集更多的数据]

From that design choice, three natural follow-up questions arise. The first is whether the model truly learns dynamics or merely a placement transform for a known silhouette. The second is what can be done at test time when such a mask is not available. The third is whether the GT-derived mask leaks information about the final post-stow shape. We address these three questions separately below. [错误，不是这三个问题，是我在question的comments里写的那三个问题。在question部分写的清楚的前提下，这一段根本不需要。]

**A2-1:** On whether the model learns dynamics rather than only placement, the empirical evidence is inconsistent with a pure placement-transform explanation [直接给结论，不要说什么和pure placement-transform explanation inconsistent，太委婉了]. If FOREST were only learning where to place the new item, one would not expect substantial gains on the motion of pre-existing items. Yet in sweep insert, O-IoU rises from 0.5287 for copy-paste(+gravity) to 0.6878/0.6906 for FOREST. This indicates that the model is also capturing how existing items are displaced and rearranged. The same conclusion is supported by the downstream evaluations, where DLO predictions driven by FOREST masks are substantially closer to those obtained from ground-truth masks than heuristic alternatives are.

**A2-2:** On the test-time question, the paper already discusses possible practical solutions in lines 661-665, including adding cameras or deriving the needed view through a separate 3D reasoning module. To make this more concrete, we additionally replace the GT-derived new-item mask with a practical alternative based on SAM3D. Specifically, we first estimate the in-bin contact-surface view from the induct-view image through 3D reconstruction, and then retrain FOREST with this estimated mask:

| Setting | DI N | DI O | SW N | SW O |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

These results are lower than the main setting, but they remain substantially stronger than heuristics. This means the predictive value of the model is still preserved once the idealized new-item input is replaced by a more realistic one. [这部分对新结果的分析写的不好，其实我们就想说换了SAM3D还是比简单的placement好，然后再去说去main差了，这是因为SAM3D自己有误差，且来到下一个问题-关于leak的。]

**A2-3:** On whether the GT-derived mask leaks information, the answer is yes, to some extent it does. This is also exactly why the main-setting IoU is higher than the SAM3D-setting IoU [不是exactly why，只是one of the reason]. The GT-derived mask still carries post-stow shape information, even after canonicalization removes pose and location. At the same time, part of the performance gap also comes from the fact that SAM3D itself is imperfect [这个应该放在A2-2写]. The right conclusion, therefore, is not that the whole method depends only on that idealized input, but that the GT-derived mask gives an advantage while the model still retains clear predictive value when a practical substitute is used [这个结论没问题，写作要formal，to-the-point].

**W5:** Baselines are weak and there is no strong learned comparison.  
**A3:** The most important point here is the nature of the task itself [把task具体一点]. This problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture. Once that is made explicit, the baseline issue becomes easier to understand. 

Off-the-shelf video or RGB generative baselines are not directly suitable without substantial redesign, and in our own experience simple RGB-conditioned generation performs poorly for exactly this reason [你这里exactly this reason指的是什么？]. This is why the paper uses heuristics that are natural for a state-based setting as the direct baselines, and then supplements them with downstream evaluations. In that sense, the current comparison should be read not as a complete resolution of the learned-baseline question, but as an appropriate first evaluation for this specific sparse-snapshot stow problem [最后一句话看不懂，你什么意思？我其实想说现有方法不改不能用，那改了不是相当于我又提出一个method了吗].

**Q1:** Why predict instance-mask layouts rather than final images?  
**A4:** The main reason is that texture is not the key variable governing stow dynamics. What matters most for post-stow prediction is occupancy, shape, contact, and the motion induced in neighboring items. The mask-based representation focuses the model on exactly those quantities. It is also more aligned with the downstream tasks considered in the paper, especially DLO prediction and multi-stow reasoning, both of which depend primarily on geometry and object arrangement rather than appearance synthesis.

---

## Revised Draft V3

Thank you for the detailed review and for the thoughtful questions on formulation, realism, and evaluation.

**W1:** The problem formulation is unclear, and the method/data-processing pipeline is scattered across multiple sections.  
**A1:** We would like to clarify the paper organization first. Section 2 gives the formal problem statement, including the pre-stow state, the new-item observation, the stow intent, the post-stow target state, and the transition model. Section 3 is the framework section with Section 3.1 showing the overall pipeline. Section 3.2 explains how the raw production logs are processed so that the inputs and targets introduced in Section 2 are materialized from the dataset. Section 3.3 explains how these signals are encoded into tokens and embeddings. Section 3.4 then presents the diffusion model itself. The method and the data processing are therefore organized as one sequential pipeline rather than scattered pieces. In the revision, we will make the train/test signals more prominent at the beginning of Section 3.1.

**W2 / W3 / W4 / W6 / Q2 / Q3:** The new-item mask derived from the ground-truth post-stow state raises several concerns.  
- whether FOREST truly learns stow dynamics or mainly performs placement for a known silhouette  
- how the method can be used at test time if this mask is not directly available  
- whether the GT-derived mask leaks post-stow shape information  

**A2:** These concerns all originate from the same design choice, namely the new-item input derived from the post-stow annotation. We therefore answer them together.

We would like to first clarify the scenario targeted by the paper for better understaning the design choice. Our goal is not to study robotic stow under fully curated academic supervision. Our goal is to study production-style robotic stow, where the available data is large-scale but inherently incomplete [这两句our goal分开写非常不formal，而且前一句给人感觉莫名其妙，为啥要提fully curated academic supervision，逻辑可能需要再想想]. In a real warehouse system, what one commonly has is a large number of executed stows together with before/after observations and operational metadata. This means the practical challenge is to build an automated pipeline that can extract usable supervision, minimize human intervention, and then test whether a useful prediction model can be learned under those constraints.

ARMBench is the only public production-scale stow dataset we found, and it reflects this reality. In ARMBench, before/after bin observations, induct-view images of the incoming item, and operational metadata are provided, but not every intermediate signal that would be ideal for learning. Instead of waiting for a richer sensor setup first, the paper studies a proof-of-concept setting that isolates the core predictive question described around lines 657-661. Namely, if a representation of the incoming item's contact-side geometry is available, can a model predict how the bin will reconfigure after the stow? This lets us evaluate the value of the transition model itself under realistic data constraints before introducing additional hardware or reconstruction modules.

**A2-1:** We believe that FOREST learns more than placement. If the model were only placing a known silhouette, it should not produce large gains on the motion of pre-existing items. However, on sweep insert, O-IoU rises from 0.5287 for copy-paste(+gravity) to 0.6878/0.6906 for FOREST. The downstream results also point in the same direction. Specicially, DLO predictions driven by FOREST masks are substantially closer to those obtained from ground-truth masks than heuristic alternatives are. These results indicate that the model is capturing how existing items are displaced and rearranged, not only where the new item should appear.

**A2-2:** At test time, the paper discusses practical ways to obtain this input in lines 661-665, including adding cameras or deriving the needed view through 3D reconstruction. To make this point concrete, we additionally replace the GT-derived new-item mask with a practical estimate produced from the induct-view image using SAM3D, and then retrain FOREST with this estimated input:

| Setting | DI N | DI O | SW N | SW O |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

With SAM3D, FOREST still remains clearly above the simple placement heuristic across all four metrics. Once the GT-derived input is replaced by a realistic acquisition route, the model should be able to preserve a substantial advantage over copy-paste(+gravity).

**A2-3:** The GT-derived mask does leak some post-stow shape information, even after canonicalization removes pose and location, and this is one reason the main-setting IoU is higher than the SAM3D-setting IoU. Another reason is that SAM3D itself is imperfect, so the gap should not be attributed to leakage alone [我说过，这个应该放在A2-2最后，A2-2最后应该起到一个承上启下的作用，既点出SAM3D结果没有main的好，一方面是因为SAM3D imperfect，一方面提到main的leak作用]. The comparison is therefore best read in two parts. The main setting shows the predictive potential of the dynamics model when the contact-side geometry is accurately available. The SAM3D setting shows that a large part of this value is still preserved when that input is replaced by a practical estimate [我觉得这两个read in two parts还挺好的，但是应该放在A2-2后面].

**W5:** Baselines are weak and there is no strong learned comparison.  
**A3:** The most important point here is the nature of the task [把task具体一点] itself. This problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture. Once that is made explicit, the baseline issue becomes easier to understand. 

Off-the-shelf video or RGB generative baselines are not directly suitable without substantial redesign, and in our own experience simple RGB-conditioned generation performs poorly for exactly this reason [你这里exactly this reason指的是什么？]. This is why the paper uses heuristics that are natural for a state-based setting as the direct baselines, and then supplements them with downstream evaluations. In that sense, the current comparison should be read not as a complete resolution of the learned-baseline question, but as an appropriate first evaluation for this specific sparse-snapshot stow problem [最后一句话看不懂，你什么意思？我其实想说现有方法不改不能用，那改了不是相当于我又提出一个method了吗].

**Q1:** Why predict instance-mask layouts rather than final images?  
**A4:** We predict instance-mask layouts because the downstream value in this post-stow state prediction task comes from geometry and arrangement, not from appearance synthesis. For stow prediction, the key quantities are occupancy, contact, shape, and the induced motion of neighboring items. A full RGB target would force the model to spend capacity on texture and rendering details that are not essential for the decision-making tasks considered here. The mask-based state is also the more appropriate interface for the downstream evaluations in the paper, especially DLO prediction and multi-stow reasoning, both of which depend primarily on object layout rather than photorealistic image generation.

## Revised Draft V4

Thank you for the detailed review and for the thoughtful questions on formulation, realism, and evaluation.

**W1:** The problem formulation is unclear, and the method/data-processing pipeline is scattered across multiple sections.  
**A1:** We would like to first clarify the paper organization. Section 2 gives the formal problem statement, including the pre-stow state, the new-item observation, the stow intent, the post-stow target state, and the transition model. Section 3 is the framework section, with Section 3.1 summarizing the overall pipeline. Section 3.2 explains how raw production data are processed so that the inputs and targets introduced in Section 2 are materialized from the dataset. Section 3.3 explains how these signals are encoded into tokens and embeddings. Section 3.4 then presents the diffusion model itself. The paper is therefore organized as one sequential pipeline from problem statement, to data processing, to representation, to model. 

**W2 / W3 / W4 / W6 / Q2 / Q3:** The new-item mask derived from the ground-truth post-stow state raises several concerns.  
- whether FOREST truly learns stow dynamics or mainly performs placement for a known silhouette?
- how the method can be used at test time if this mask is not directly available? 
- whether the GT-derived mask leaks post-stow shape information? 

**A2:** These concerns all originate from the same design choice, namely the use of a canonical new-item mask derived from the post-stow annotation. We therefore answer them together.

We would like to first clarify the scenario targeted by the paper for better understaning the design choice. Our goal is not to study robotic stow under fully curated academic supervision. Our goal is to study production-style robotic stow, where the available data is large-scale but inherently incomplete [这两句our goal分开写非常不formal，而且前一句给人感觉莫名其妙，为啥要提fully curated academic supervision，逻辑可能需要再想想]. In a real warehouse system, what one commonly has is a large number of executed stows together with before/after observations and operational metadata. This means the practical challenge is to build an automated pipeline that can extract usable supervision, minimize human intervention, and then test whether a useful prediction model can be learned under those constraints.

ARMBench is the only public production-scale stow dataset we found, and it reflects this reality. In ARMBench, before/after bin observations, induct-view images of the incoming item, and operational metadata are provided, but not every intermediate signal that would be ideal for learning. Instead of waiting for a richer sensor setup first, the paper studies a proof-of-concept setting that isolates the core predictive question described around lines 657-661. Namely, if a representation of the incoming item's contact-side geometry is available, can a model predict how the bin will reconfigure after the stow? This lets us evaluate the value of the transition model itself under realistic data constraints before introducing additional hardware or reconstruction modules.

**A2-1:** We believe that FOREST learns more than placement. If the model were only placing a known silhouette, it should not produce large gains on the motion of pre-existing items. However, on sweep insert, O-IoU rises from 0.5287 for copy-paste(+gravity) to 0.6878/0.6906 for FOREST. The downstream results also point in the same direction. Specicially, DLO predictions driven by FOREST masks are substantially closer to those obtained from ground-truth masks than heuristic alternatives are. These results indicate that the model is capturing how existing items are displaced and rearranged, not only where the new item should appear.

**A2-2:** At test time, the paper discusses practical ways to obtain this input in lines 661-665, including adding cameras or deriving the needed view through 3D reconstruction. To make this point concrete, we additionally replace the GT-derived new-item mask with a practical estimate produced from the induct-view image using SAM3D, and then retrain FOREST with this estimated input:

| Setting | DI N | DI O | SW N | SW O |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

With SAM3D, FOREST still remains clearly above copy-paste(+gravity) across all four metrics. This means the predictive value is still preserved when the GT-derived input is replaced by a practical acquisition route. Besides, the SAM3D results are lower than the main-setting results partly because SAM3D itself is imperfect, which also leads to the final question on information leakage.

**A2-3:** The GT-derived mask does retain some post-stow shape information even after canonicalization removes pose and location, so it gives the main setting an advantagem which contributes to the gap between the main setting and the SAM3D setting. 
The comparison is therefore best read in two parts. The main setting shows the predictive potential of the dynamics model when the contact-side geometry is accurately available. The SAM3D setting shows that a large part of this value is still preserved when that input is replaced by a practical estimate.

**W5:** Baselines are weak and there is no strong learned comparison.  
**A3:** The most important point here is the nature of the task itself. This problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture.

For these reasons, off-the-shelf video prediction or RGB generation models are not directly applicable without redesigning the representation, the conditioning interface, and the learning objective for this setting. In our own trials, simple RGB-conditioned generation performs poorly for exactly this reason. Once such changes are introduced, the result is no longer a direct baseline but a newly adapted task-specific method. For this first study, we therefore compare against deterministic heuristics that are natural for this state-based problem and then validate utility through downstream tasks.

**Q1:** Why predict instance-mask layouts rather than final images?  
**A4:** We predict instance-mask layouts because the downstream value in this post-stow state prediction task comes from geometry and arrangement, not from appearance synthesis. For stow prediction, the key quantities are occupancy, contact, shape, and the induced motion of neighboring items. A full RGB target would force the model to spend capacity on texture and rendering details that are not essential for the decision-making tasks considered here. The mask-based state is also the more appropriate interface for the downstream evaluations in the paper, especially DLO prediction and multi-stow reasoning, both of which depend primarily on object layout rather than photorealistic image generation.

---

## Revised Draft V5

Thank you for the detailed review and for the thoughtful questions on formulation, realism, and evaluation.

**W1:** The problem formulation is unclear, and the method/data-processing pipeline is scattered across multiple sections.  
**A1:** We would like to first clarify the paper organization. Section 2 gives the formal problem statement, including the pre-stow state, the new-item observation, the stow intent, the post-stow target state, and the transition model. Section 3 is the framework section, with Section 3.1 summarizing the overall pipeline. Section 3.2 explains how raw production data are processed so that the inputs and targets introduced in Section 2 are materialized from the dataset. Section 3.3 explains how these signals are encoded into tokens and embeddings. Section 3.4 then presents the diffusion model itself. **The paper is therefore organized as one sequential pipeline from problem statement, to data processing, to representation, to model.**

**W2 / W3 / W4 / W6 / Q2 / Q3:** The new-item mask derived from the ground-truth post-stow state raises several concerns.  
- whether FOREST truly learns stow dynamics or mainly performs placement for a known silhouette?
- how the method can be used at test time if this mask is not directly available? 
- whether the GT-derived mask leaks post-stow shape information? 

**A2:** These concerns all originate from the same design choice, namely the use of a canonical new-item mask derived from the post-stow annotation. We therefore answer them together.

We would like to first clarify the scenario targeted by the paper for better understanding the design choice. Our goal is to study production-style robotic stow, where the available data is large-scale but inherently sparse. In a real warehouse system, what one commonly has is a large number of executed stows together with before/after observations and operational metadata. This means the practical challenge is to build an automated pipeline that can extract usable supervision, minimize human intervention, and then test whether a useful prediction model can be learned under those constraints. 

ARMBench is the only public production-scale stow dataset we found, and it reflects exactly this reality while additionally providing induct-view images of the incoming item. It still does not provide every intermediate signal that would ideally be available for learning. **For this reason, the paper first studies a proof-of-concept setting as described around lines 657-661: if a representation of the incoming item's contact-side geometry is available, can a model predict how the bin will reconfigure after the stow?** This allows us to validate the predictive component first under realistic data constraints before introducing extra hardware or separate reconstruction modules.

**A2-1:** We believe that FOREST learns more than placement. If the model were only placing a known silhouette, it should not produce large gains on the motion of pre-existing items. However, on sweep insert, O-IoU rises from 0.5287 for copy-paste(+gravity) to 0.6878/0.6906 for FOREST. The downstream results also point in the same direction. Specifically, DLO predictions driven by FOREST masks are substantially closer to those obtained from ground-truth masks than heuristic alternatives are. These results indicate that the model is capturing how existing items are displaced and rearranged, not only where the new item should appear.

**A2-2:** At test time, the paper discusses practical ways to obtain this input in lines 661-665, including adding cameras or deriving the needed view through 3D reconstruction. To make this point concrete, we additionally replace the GT-derived new-item mask with a practical estimate produced from the induct-view image using SAM3D, and then retrain FOREST with this estimated input:

| Setting | DI N | DI O | SW N | SW O |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

With SAM3D, FOREST still remains clearly above copy-paste(+gravity) across all four metrics. **This means the predictive value is still preserved when the GT-derived input is replaced by a practical acquisition route.** Besides, the SAM3D results are lower than the main-setting results partly because SAM3D itself is imperfect, and partly because the main setting still benefits from information retained in the GT-derived mask. The comparison is therefore best read in two parts. The main setting shows the predictive potential of the dynamics model when the contact-side geometry is accurately available. While the SAM3D setting shows that a large part of this value is still preserved when that input is replaced by a practical estimate.

**A2-3:** The GT-derived mask does retain some post-stow shape information even after canonicalization removes pose and location, so it gives the main setting an advantage and contributes to the gap between the main setting and the SAM3D setting as mentioned in A2-2.

**W5:** Baselines are weak and there is no strong learned comparison.  
**A3:** The most important point here is the nature of the task itself. This problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture.

**For these reasons, off-the-shelf video prediction or RGB generation models are not directly applicable without redesigning the representation, the conditioning interface, and the learning objective.** For example, in our own trials, simple RGB-conditioned generation performs poorly because it is built to model appearance, while this task is governed primarily by object geometry and arrangement. Therefore once changes to existing methods are introduced, the result is no longer a direct baseline but a newly adapted task-specific method.  For this first study, we therefore compare against heuristic baselines that are natural for this problem and then validate utility through downstream tasks.

**Q1:** Why predict instance-mask layouts rather than final images?  
**A4:** **We predict instance-mask layouts because the downstream value in this post-stow state prediction task comes from geometry and arrangement, not from appearance synthesis.** For stow prediction, the key quantities are occupancy, contact, shape, and the induced motion of neighboring items. A full RGB target would force the model to spend capacity on texture and rendering details that are not essential for the decision-making tasks considered here. The mask-based state is also the more appropriate interface for the downstream evaluations in the paper, i.e., DLO prediction and multi-stow reasoning, both of which depend primarily on object layout rather than photorealistic image generation.

## Final

Thank you for the detailed review and for thoughtful questions.

**W1:** The problem formulation is unclear, and the method/data-processing pipeline is scattered across multiple sections.  
**A1:** We would like to first clarify the paper organization. Section 2 gives the formal problem statement. Section 3 is the framework section: Section 3.1 summarizes the overall pipeline, Section 3.2 materializes the inputs and targets from raw production data, Section 3.3 encodes them into tokens and embeddings, and Section 3.4 presents the diffusion model. **The paper is therefore organized as one sequential pipeline from problem statement, to data processing, to representation, to model.**

**W2 / W3 / W4 / W6 / Q2 / Q3:** The new-item mask derived from the ground-truth post-stow state raises several concerns.  
- whether the model truly learns stow dynamics or mainly performs placement for a known silhouette?
- how can the method be used at test time if this mask is not directly available? 
- whether the GT-derived mask leaks post-stow shape information? 

**A2:** We would like to first clarify the scenario targeted by the paper to better understanding this design choice. We study production-style robotic stow, where large-scale logs provide before/after observations and operational metadata, but not every intermediate signal that would ideally be available for learning. ARMBench is the representative public production-scale stow dataset and reflects exactly this reality. **This means a practical challenge is to build an automated pipeline that can extract usable supervision, minimize human intervention, and then test whether a useful prediction model can be learned under those constraints.** 

**A2-1:** We believe that FOREST learns more than placement. If the model were only placing a known silhouette, it should not produce large gains on the motion of pre-existing items. However, on sweep insert, O-IoU rises from 0.5287 for copy-paste(+gravity) to 0.6878/0.6906 for FOREST. DLO predictions driven by FOREST masks are also substantially closer to those obtained from ground-truth masks than heuristic alternatives are. These results indicate that the model is capturing how existing items are displaced and rearranged, not only where the new item should appear.

**A2-2:** At test time, the paper discusses practical ways to obtain this new item mask in lines 661-665, including additional cameras or 3D reconstruction. We additionally replace the GT-derived new-item mask with a SAM3D estimate from the induct-view image and retrain FOREST with this input:

| Setting | DI N | DI O | SW N | SW O |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

With SAM3D, FOREST still remains clearly above copy-paste(+gravity) across all four metrics. **This means the predictive capability is still preserved when the GT-derived input is replaced by a practical estimate.**

**A2-3:** The GT-derived mask does retain post-stow shape information even after canonicalization removes pose and location, so it contributes to the gap between the main setting and the SAM3D setting as shown in A2-2.

**W5:** Baselines are weak and there is no strong learned comparison.  
**A3:** We agree that the current baselines are weak. However, stronger learned baselines are nontrivial here because this problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture.

**For these reasons, off-the-shelf video prediction or RGB generation models are not directly applicable without redesigning the representation, the conditioning interface, and the learning objective.** In our own trials, simple RGB-conditioned generation performs poorly because it is built to model appearance, while this task is governed primarily by object geometry and arrangement. For this first study, we therefore compare against deterministic heuristics that are natural for this state-based problem and then validate utility through downstream tasks.

**Q1:** Why predict instance-mask layouts rather than final images?  
**A4:** **We predict instance-mask layouts because the downstream value of the post-stow state prediction comes from geometry and arrangement, not from appearance synthesis.** A full RGB target would force the model to spend capacity on texture and rendering details that are not essential for the decision-making tasks considered here. The mask-based state is also the more appropriate interface for the downstream evaluations, i.e., DLO prediction and multi-stow reasoning, both of which depend primarily on object layout rather than photorealistic image generation.

