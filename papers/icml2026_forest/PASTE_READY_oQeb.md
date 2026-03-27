Thank you for the balanced review and for highlighting both the practical motivation and the downstream evaluations. Your comments mainly ask what the current experiments establish, and what they do not yet establish, which is exactly the right question for this paper.

**W1 / Q1:** Stronger learned baselines are missing.  
**A1:** The key reason is that this setting does not align well with standard learned baselines from video prediction or RGB generation. The supervision is temporally sparse, the state is object-centric, and the prediction target is a structured post-stow layout rather than future appearance. For that reason, heuristic baselines are the most natural deterministic reference point in this problem setup. At the same time, the paper does not rely only on mask overlap to validate the model. It also asks whether the predicted states remain useful in downstream reasoning tasks. In Table 2, FOREST reduces the extra DLO error over ground-truth masks from +0.0057 / +0.0098 with copy-paste+gravity to only +0.0016 / +0.0025, and it also supports multi-stow rollouts over 1,581 chains. Our interpretation is that this provides evidence of practical utility beyond direct IoU comparison.

**W2 / Q2:** Segmentation robustness is not thoroughly analyzed.  
**A2:** The current study does not provide a full controlled robustness benchmark, because ARMBench does not come with the ground-truth segmentation and matching annotations required for that kind of analysis. Instead, the pipeline is designed to reduce noise automatically. It first filters for single-step cases via the instance-count condition, and then uses Claude-3.7 as a consistency checker over pre/post RGB images to reject clearly unreliable matches. This should be interpreted as a practical automatic curation strategy for noisy industrial data, rather than as a complete robustness analysis.

**W3 / Q3:** Generalization beyond ARMBench is unclear.  
**A3:** We would like to clarify the target of generalization in this paper. The goal is not broad out-of-environment transfer, but strong performance within the deployment distribution that matters for production stow. ARMBench captures large diversity in objects and bins within that warehouse environment, and it is the only public production-scale dataset we found for this domain. For this reason, the paper is best read as a first study of real-world sparse-snapshot stow within its target environment, rather than a claim of broad cross-domain generalization.

**W4 / Q4:** The formulation is single-step rather than sequential.  
**A4:** The single-step formulation is chosen deliberately because it mirrors the execution policy in production. Each stow is a discrete transit conditioned on the current bin state, the incoming item, and the selected intent. The multi-step rollout experiments are therefore meant to answer a narrower question: whether a model trained on single-step transitions remains useful when composed over longer chains. In that sense, they demonstrate compositional robustness of the learned single-step model rather than explicit sequential training.

**W5 / Q5:** Physical plausibility is not explicitly evaluated.  
**A5:** The current paper does not include a dedicated overlap or stability metric. Instead, physical plausibility is evaluated indirectly through the behaviors that matter most in this application, namely better prediction of rearranged items, stronger DLO prediction fidelity, and stable behavior in multi-stow rollouts. Since the model is trained from real post-stow outcomes rather than explicit physics labels, these downstream evaluations are the most relevant validation we can provide in the current setting.

---

## Revised Draft

Thank you for the balanced review and for highlighting both the practical motivation and the downstream evaluations.

**W1 / Q1:** Stronger learned baselines are missing.  
**A1:**
[我觉得回复得不好，因为你写的this is什么样的问题是我们自己定义的，从problem statement来看并不是非要这样定义，因为你这样定义问题然后去说已有方法不能用是不合理的，请参照gfXd的A3重新写一版。]
We would like to first clarify the structure of the task, because that is the main reason the baselines look unusual here. This is a sparse-snapshot, object-centric post-stow state prediction problem conditioned on the current bin state, the incoming item, and the stow intent. The target is not a future RGB frame but a future instance-mask layout, and the signal that matters for this problem is geometry, occupancy, and contact rather than texture. **For this reason, off-the-shelf video prediction or RGB generation methods are not directly applicable without redesigning the representation, the conditioning interface, and the learning objective for this setting.** Once such changes are introduced, the result is no longer a direct baseline but a newly adapted task-specific method.

For this first study, the paper therefore compares against deterministic heuristics that are natural for this state-based setting and then asks a second question, namely whether the predicted states are useful in downstream tasks. Table 2 shows that FOREST reduces the extra DLO error over ground-truth masks from +0.0057 / +0.0098 with copy-paste(+gravity) to +0.0016 / +0.0025, and it also supports multi-stow rollouts over 1,581 chains. In our view, this is the key evidence that the model captures actionable post-stow structure rather than only improving mask overlap in isolation.

**W2 / Q4:** The formulation is single-step rather than sequential.  
**A4:** The single-step formulation is chosen deliberately because it mirrors the execution policy in production. Each stow is a discrete transit conditioned on the current bin state, the incoming item, and the chosen intent. The corresponding prediction problem is therefore to estimate the immediate post-stow state for that one candidate action. **In this sense, the single-step formulation is aligned with the operational unit of decision and execution in the warehouse setting.** The multi-step rollout evaluation are included to test whether a model trained on single-step transitions remains stable and useful when composed over longer chains.
[这个回答写的挺好的，不过reviewer还有一个问题是“Would training the model explicitly on multi-step transitions improve long-horizon prediction performance compared to the current single-step training formulation”，也需要回答一下。]


**W3 / Q2:** Sensitve analysis to errors in segmentation and item matching.  
**A2:** We would like to clarify the data regime [不要用regime这个词] targeted by the paper. Our goal is to study production-style robotic stow, where the available data is large-scale but inherently incomplete. In a real warehouse system, what one commonly has is a large number of executed stows together with before/after observations and operational metadata, rather than dense ground-truth labels for every intermediate step. ARMBench reflects exactly this setting. As a result, a fully controlled robustness benchmark is not possible here because ARMBench does not provide the ground-truth segmentation and matching annotations that would be required for such an analysis.

Instead, the pipeline is designed to reduce noise automatically and test whether useful learning is still possible under these constraints. Concretely, we filter for likely single-step transitions, construct matches algorithmically, and then use Claude-3.7 as an automated consistency checker over the pre/post RGB images to remove clearly unreliable cases. **This should be interpreted as a practical automatic curation strategy for noisy industrial data, rather than as a complete segmentation robustness benchmark.**

**W4 / Q5:** Physical plausibility is not explicitly evaluated.  
**A5:** [我觉得这个回答的内容基本没有问题，但是可以委婉一点，先说我们做dowonstream evaluation的目的（算是总起句），做了什么用来evaluate prediction performance，然后承认我们确实没做physical plausibility相关的evaluation，这需要人工的GT或者合理的自动化benchmark的设计，是可以做的future，不过最后再强调一下我们并不需要预测的post-stow完全符合物理定理，因为不是在真的做simulation，只要预测的未来能够用于downstream就行了（什么样的downstream可以简单说一下）]
The current paper does not include a dedicated overlap, penetration, or stability metric. Instead, physical plausibility is evaluated through the downstream behaviors that matter most in this application, namely more accurate prediction of rearranged items, stronger DLO prediction fidelity, and stable behavior in multi-stow rollouts. Since the model is trained from real post-stow outcomes rather than explicit physics labels, **these downstream evaluations are the most relevant validation available in the current setting for whether the predicted states remain physically useful.**

**W5 / Q3:** Generalization beyond ARMBench is unclear.  
**A3:** [我觉得这个回答也是内容上问题不大，但是要委婉一点，先说明我们做实验的ARMBench有什么特点，确实是包含不同的object\item\bin的，然后说明我们的目的确实是做这个target env的study，generalization to new env/OOD需要更多的设计，最后加上我们的一点思考，那就是其实给production的warehouse做learning model往往要的是stable，而且这样的工业环境往往是standard的]
We would like to clarify the target of generalization in this paper. The goal is not broad out-of-environment transfer, but strong performance within the deployment distribution that matters for production stow. ARMBench is the only public production-scale stow dataset we found, and it already contains substantial diversity in object categories, item instances, and storage bins within that warehouse environment. **For this reason, the paper is best read as a first study of real-world sparse-snapshot stow within its target environment, rather than as a claim of broad cross-domain generalization.** 

---

## Revised Draft V2

Thank you for the balanced review and for highlighting both the practical motivation and the downstream evaluations.

**W1 / Q1:** Stronger learned baselines are missing.  
**A1:** 
[这个第一段还是需要重新写，你认真看看gfXd的A3我们是怎么写的，主要问题是就在于你说是因为built for different prediction setting，这个prediction setting怎么不一样了？为什么不能统一？其实是因为问题本身的特质，不是我们不想统一，如果强行用已有model放在这个问题上，就需要adjustment了]We agree that learned baselines are important but would like to first clarify why it is a difficulty in this problem. The issue is that existing learned baselines are built for a different prediction setting. Our task is post-stow state prediction from sparse snapshots, conditioned on the current bin state, the incoming item, and the stow intent, while off-the-shelf video prediction and RGB generation methods are designed around dense visual prediction and appearance synthesis. **For this reason, they are not directly applicable here without redesigning the representation, the conditioning interface, and the learning objective.** Once such changes are introduced, the result is no longer a direct baseline but a newly adapted task-specific method.

For this first study, the paper therefore compares against heuristics that are natural for this state-based setting and then asks whether the predicted states are useful in downstream tasks. Table 2 shows that FOREST reduces the extra DLO error over ground-truth masks from +0.0057 / +0.0098 with copy-paste(+gravity) to +0.0016 / +0.0025, and it also supports multi-stow rollouts. In our view, this is the key evidence that the model captures actionable post-stow structure.

**W2 / Q4:** The formulation is single-step rather than sequential.  
**A4:** The single-step formulation is chosen deliberately because it mirrors the execution policy in production. Each stow is a discrete transit conditioned on the current bin state, the incoming item, and the chosen intent. The corresponding prediction problem is therefore to estimate the immediate post-stow state for that one candidate action. **In this sense, the single-step formulation is aligned with the operational unit of decision and execution in the warehouse setting.** The multi-step rollout evaluation is then used to test whether a model trained on single-step transitions remains stable and useful when composed over longer chains.

Training explicitly on multi-step transitions could improve long-horizon performance, and we view that as a meaningful future direction. At the same time, such a formulation would require additional modeling and supervision design, whereas the current paper focuses first on whether a strong single-step model already provides value. The rollout results suggest that it does, which is why we present the current work as a first step rather than a complete treatment of long-horizon sequential prediction [最后一句话太口语了，我们在写academic paper的rebuttal呀，整段的语言和用词还是要professional].

**W3 / Q2:** Sensitive analysis to errors in segmentation and item matching.  
**A2:** We would like to clarify the data setting targeted by the paper [我觉得不能说是data setting吧，用setting这个词感觉是我们故意用这种比较奇怪的数据集的，其实不是啊，是因为我们要做的问题是production-style robotic stow，所以才用的]. Our goal is to study production-style robotic stow, where the available data is large-scale but inherently incomplete. In a real warehouse system, what one commonly has is a large number of executed stows together with before/after observations and operational metadata, rather than dense ground-truth labels for every intermediate step. ARMBench reflects exactly this setting. As a result, a fully controlled robustness benchmark is not possible here because ARMBench does not provide the ground-truth segmentation and matching annotations that would be required for such an analysis.

Instead, the pipeline is designed to reduce noise automatically and test whether useful learning is still possible under these constraints. Concretely, we filter for likely single-step transitions, construct matches algorithmically, and then use Claude-3.7 as an automated consistency checker over the pre/post RGB images to remove clearly unreliable cases. **This should be interpreted as a practical automatic curation strategy for noisy industrial data, rather than as a complete sensitivity benchmark.**

**W4 / Q5:** Physical plausibility is not explicitly evaluated.  
**A5:** The purpose of the downstream evaluation in this paper is to test whether the predicted post-stow states are useful for subsequent reasoning. Therefore we evaluate prediction quality through DLO prediction fidelity and stable behavior in multi-stow rollouts. These are the downstream uses that matter most in the warehouse setting.

We agree that the paper does not include a dedicated physical-plausibility benchmark such as penetration, stability, or overlap violations. Such an evaluation would likely require either additional human annotation or a carefully designed automatic benchmark, and we view that as a valuable future direction. [这个转折也太生硬了，什么叫At the same time啊，明明是我们想再委婉地强调一下我们并不需要预测的post-stow完全符合物理定理，因为不是在真的做simulation，只要预测的未来能够用于downstream就行了]At the same time, the goal here is not full physical simulation. **The practical requirement is that the predicted future state remains useful for downstream tasks such as DLO prediction and multi-step planning support, and the current evaluations are designed to test exactly that.**

**W5 / Q3:** Generalization beyond ARMBench is unclear.  
**A3:** We would like to clarify the target of generalization in this paper [这个总起句也太差了，什么叫做the target of generalization in this paper，我们根本就没在做generalization啊，你是不是误解了]. ARMBench is the public production-scale stow dataset we found, and it contains substantial diversity in object categories, item instances, and storage bins within that warehouse environment. The paper therefore studies within this particular production environment rather than transfer to unrelated environments. **For this reason, the current work is best read as a study of sparse-snapshot stow prediction in its target deployment setting, rather than as a claim of broad out-of-distribution generalization.**

Generalization to new environments or stronger out-of-distribution settings would require additional data and modeling design, and we view that as an important next step. At the same time, production warehouse systems are often highly standardized, and what matters most in practice is stable performance within that standardized operating environment. That is why strong within-environment generalization on ARMBench is already meaningful for the application considered here.

---

## Revised Draft V3

Thank you for the balanced review and for highlighting both the practical motivation and the downstream evaluations.

**W1 / Q1:** Stronger learned baselines are missing.  
**A1:** Learned baselines are certainly important. The difficulty here comes from the nature of the problem rather than from an arbitrary modeling choice [我不是很理解你这里说的an arbitrary modeling choice是什么意思？你说difficulty不是from an arbitrary modeling choice是什么意思？]. Post-stow prediction in this paper is driven primarily by geometry, occupancy, and contact, while the available supervision is temporally sparse [这句话也像是不负责的claim，我们的论文里一点没提到"driven primarily by geometry, occupancy, and contact"，而且driven by它们为什么已有方法就用不了了？你为什么不看看gfXd的A3我们是怎么写的？“The most important point here is the nature of the task itself. This problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture.”这是给gfXd写的你为什么不用？你写的和这个表达的完全不是一回事啊]. Off-the-shelf video prediction and RGB generation models are designed for dense visual prediction and appearance synthesis, so they cannot be applied directly to this problem without adjusting the representation, conditioning, and objective. [simple RGB diffusion doesn't work为什么不提？] Once those adjustments are introduced, the result is no longer a direct baseline, but a newly adapted method for this task.

The current paper therefore compares against heuristics that are natural for this state-based setting and then evaluates whether the predicted states remain useful in downstream tasks. Table 2 shows that FOREST reduces the extra DLO error over ground-truth masks from +0.0057 / +0.0098 with copy-paste(+gravity) to +0.0016 / +0.0025, and it also supports multi-stow rollouts. These results show that the model improves not only direct prediction quality but also downstream utility.

**W2 / Q4:** The formulation is single-step rather than sequential.  
**A4:** The single-step formulation is chosen deliberately because it mirrors the execution policy in production. Each stow is a discrete transit conditioned on the current bin state, the incoming item, and the chosen intent. The corresponding prediction problem is therefore to estimate the immediate post-stow state for that action. **The single-step formulation is thus aligned with how transitions are defined and executed in the warehouse setting.**

Training explicitly on multi-step transitions could always improve long-horizon performance. However, that would require a different supervision and modeling setup. Whereas the present paper focuses on whether a strong single-step model already yields useful composed behavior and our rollout results indicate the sequential prediction capability of our method.

**W3 / Q2:** Sensitive analysis to errors in segmentation and item matching.  
**A2:** [总起句呢？我们要先回答审稿人的问题啊，一句话定调呢] The paper studies production-style robotic stow, where the available data is large-scale but inherently incomplete. Specifically in a real warehouse system, what one commonly has is a large number of executed stows together with before/after observations and operational metadata, rather than dense ground-truth labels for every intermediate step. ARMBench reflects exactly this situation. A fully controlled sensitivity analysis is therefore not possible here, because ARMBench does not provide the ground-truth segmentation and matching annotations required for such an analysis.

Instead, the pipeline is designed to reduce noise automatically and then evaluate whether useful learning remains possible under these constraints. Concretely, we filter for likely single-step transitions, construct matches algorithmically, and use Claude-3.7 as an automated consistency checker over the pre/post RGB images to remove clearly unreliable cases. They form a practical automatic curation process for noisy industrial data.

**W4 / Q5:** Physical plausibility is not explicitly evaluated.  
**A5:** 
[整个回答的结构我认为都不好，我认为我们一定要再第一段第一句就让人知道我们的观点。现在我看半天都不知道所以为什么没做Physical plausibility]
The downstream evaluations are included to test whether the predicted post-stow states are useful for subsequent reasoning, rather than only whether they score well under overlap-based metrics. In the current paper, this is assessed through DLO prediction fidelity and stable behavior in multi-stow rollouts. These are the downstream uses that matter most in the warehouse setting considered here.

The paper does not include a dedicated physical-plausibility benchmark such as penetration, stability, or overlap violations. Such an evaluation would require either additional annotation or a carefully designed automatic benchmark. At the same time, the objective here is not full physical simulation [这个转折也太生硬了，什么叫At the same time啊，明明是我们想再委婉地强调一下我们并不需要预测的post-stow完全符合物理定理，因为不是在真的做simulation，只要预测的未来能够用于downstream就行了]. **The practical requirement is that the predicted future state remain useful for downstream tasks such as DLO prediction and multi-stow planning support, and the current evaluations are designed to test exactly that.**


**W5 / Q3:** Generalization beyond ARMBench is unclear.  
**A3:** We do agree that generalization to new environments or stronger out-of-distribution settings is an important next step and would require additional data and modeling design. However, at this point, ARMBench is the only public production-scale stow dataset we found, and it already contains substantial diversity in object categories, item instances, and storage bins within that warehouse environment. The experiments therefore evaluate performance within a realistic production environment rather than transfer across unrelated environments. This work does not claim broad out-of-distribution generalization [你不觉得你这句话攻击性太强了吗？就直愣愣地说我们没claim，那审稿人就想知道真么办，我们要说的是我们没有这方面的focus啊，你太笨了]. It studies sparse-snapshot stow prediction for the target deployment environment represented by ARMBench.

This emphasis is also consistent with the application. Production warehouse systems are typically highly standardized, and what matters most in practice is stable performance within that standardized operating environment. Strong within-environment performance on ARMBench is therefore meaningful for the use case considered here.

---

## Revised Draft V4

Thank you for the balanced review and for highlighting both the practical motivation and the downstream evaluations.

**W1 / Q1:** Stronger learned baselines are missing.  
**A1:** Learned baselines are certainly relevant. The main issue here is the nature of the task itself. This problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric post-stow bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture. Accordingly, **off-the-shelf video prediction or RGB generation models are not directly suitable without redesigning the representation, conditioning interface, and learning objective**. In our own trials, simple RGB-conditioned diffusion performs poorly for exactly this reason. Once such changes are introduced, the result is no longer a direct baseline, but a newly adapted method for this task.

The current paper therefore compares against heuristic baselines that are natural for this problem and then evaluates whether the predicted states remain useful in downstream tasks. Table 2 shows that FOREST reduces the extra DLO error over ground-truth masks from +0.0057 / +0.0098 with copy-paste(+gravity) to +0.0016 / +0.0025, and it also supports multi-stow rollouts. These results show that the model improves not only direct prediction quality but also downstream utility.

**W2 / Q4:** The formulation is single-step rather than sequential.  
**A4:** The single-step formulation is chosen deliberately because it mirrors the execution policy in production. Each stow is a discrete transit conditioned on the current bin state, the incoming item, and the chosen intent. The corresponding prediction problem is therefore to estimate the immediate post-stow state for that action. **The single-step formulation is thus aligned with how transitions are defined and executed in the warehouse setting.**

Training explicitly on multi-step transitions may improve long-horizon performance. However, that would constitute a different supervision and modeling problem from the one studied here. The present paper addresses the question of whether a strong single-step model already yields useful composed behavior over longer chains. And our rollout results indicate the sequential prediction capability of our method

**W3 / Q2:** Sensitive analysis to errors in segmentation and item matching.  
**A2:** A error-sensitivity analysis would certainly be informative, but it is difficult in the current study because the paper addresses production-style robotic stow with inherently incomplete data. Specifically, in a real warehouse system, what one commonly has is a large number of executed stows together with before/after observations and operational metadata, rather than dense ground-truth labels for every intermediate step. ARMBench reflects exactly this situation. It does not provide the ground-truth segmentation and matching annotations required for a controlled error analysis.

It also explains that our pipeline is designed to reduce noise automatically and then evaluate whether useful learning remains possible under these constraints. Concretely, we filter for likely single-step transitions, construct matches algorithmically, and use Claude-3.7 as an automated consistency checker over the pre/post RGB images to remove clearly unreliable cases. They form a practical automatic curation process for noisy industrial data.

**W4 / Q5:** Physical plausibility is not explicitly evaluated.  
**A5:** Metrics such as penetration, stability, or overlap violations would certainly be informative, but they would require additional annotation or a carefully designed automatic benchmark. The present paper instead evaluates the criterion most relevant to the application, namely useful post-stow prediction for downstream reasoning (i.e., DLO prediction and multi-stow rollouts) rather than full physical simulation. These are the downstream uses that matter most in the warehouse setting considered here.


**W5 / Q3:** Generalization beyond ARMBench is unclear.  
**A3:** The present study is focused on the production environment represented by ARMBench rather than on broad cross-environment transfer. ARMBench is the only public production-scale stow dataset we found, and it contains substantial diversity in object categories, item instances, and storage bins within that warehouse environment. The experiments therefore evaluate performance within this realistic target environment rather than across different environments.

This emphasis is also consistent with the application. Production warehouse systems are typically highly standardized, and what matters most in practice is stable performance within that standardized operating environment. Therefore for the use case studied here, strong within-environment performance on ARMBench is already meaningful.

## Final

Thank you for the review and for highlighting both the practical motivation and the downstream evaluations.

**W1 / Q1:** Stronger learned baselines are missing.  
**A1:** Learned baselines are certainly valuable. However, stronger learned baselines are nontrivial here because this problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric post-stow bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture. Accordingly, **off-the-shelf video prediction or RGB generation models are not directly suitable without redesigning the representation, conditioning interface, and learning objective**. In our own trials, simple RGB-conditioned diffusion performs poorly for exactly this reason. Once such changes are introduced, the result is no longer a direct baseline, but a newly adapted method for this task.

The current paper therefore compares against heuristics that are natural for this problem and then evaluates whether the predicted states remain useful in downstream tasks. For example, our results show that FOREST reduces the extra DLO error over ground-truth masks from +0.0057 / +0.0098 with copy-paste(+gravity) to +0.0016 / +0.0025. 

**W2 / Q4:** The formulation is single-step rather than sequential.  
**A4:** The single-step formulation is chosen deliberately because it mirrors the execution policy in production. Each stow is a discrete transit conditioned on the current bin state, the incoming item, and the chosen intent. The corresponding prediction problem is therefore to estimate the immediate post-stow state for that action. **The single-step formulation is thus aligned with how transitions are defined and executed in the warehouse setting.**

Training explicitly on multi-step transitions may improve long-horizon performance. However, that would constitute a different supervision and modeling problem from the one studied here. The present paper addresses the question of whether a strong single-step model already yields useful composed behavior over longer chains. And our rollout results indicate the sequential prediction capability of our method.

**W3 / Q2:** Sensitive analysis to errors in segmentation and item matching.  
**A2:** An error-sensitivity analysis would certainly be informative, but it is difficult in the current study because the paper addresses production-style robotic stow with inherently incomplete data. Specifically, in a real warehouse system, what one commonly has is a large number of executed stows together with before/after observations and operational metadata, rather than dense ground-truth labels for every intermediate step. ARMBench reflects exactly this situation. It does not provide the ground-truth segmentation and matching annotations required for a controlled error analysis.

We would like to also explain that our pipeline is designed to reduce noise automatically and then evaluate whether useful learning remains possible under these constraints. Concretely, we filter for likely single-step transitions, construct matches algorithmically, and use Claude-3.7 as an automated consistency checker to remove clearly unreliable cases. They form a practical automatic curation process for noisy industrial data.

**W4 / Q5:** Physical plausibility is not explicitly evaluated.  
**A5:** Metrics such as penetration, stability, or overlap violations would be useful to identify physical alignment, but they would require additional annotation or a carefully designed automatic benchmark. The present paper instead evaluates the criterion most relevant to the real application, namely useful post-stow prediction for downstream reasoning (i.e., DLO prediction and multi-stow rollouts). These are the downstream uses that matter most in the warehouse setting considered here.

**W5 / Q3:** Generalization beyond ARMBench is unclear.  
**A3:** The present study is focused on the production environment represented by ARMBench rather than on broad cross-environment transfer. ARMBench is the representative public production-scale stow dataset, and it contains substantial diversity in object categories, item instances, and storage bins within that warehouse environment. The experiments therefore evaluate performance within this realistic target environment rather than across different environments.

This emphasis is also consistent with the real application. Production warehouse systems are typically highly standardized, and what matters most in practice is stable performance within that standardized operating environment. Therefore for the use case studied here, strong within-environment performance on ARMBench is already meaningful.
