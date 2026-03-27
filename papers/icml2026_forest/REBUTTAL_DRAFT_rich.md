# Rebuttal Draft Rich

## Reviewer Dwiz

Thank you for the thoughtful review and for recognizing the practical relevance of visual foresight for stow. We agree that the most important caveats concern noisy supervision, the single-step assumption, and whether diffusion is justified beyond heuristics.

On robustness to segmentation and matching noise: the current paper does include two safeguards, although we did not explain them clearly enough. First, we discard events whose post-stow instance count is not exactly pre-stow count + 1, which removes obvious segmentation failures for the single-step setting. Second, for the remaining events we audit the one-to-one correspondence with a large vision-language model, specifically Claude-3.7 in a visual-question-answering setup over the pre/post RGB images; there is no manual verification in this step. We agree that a dedicated quantitative noise-ablation would be valuable. At present, our evidence is indirect: despite imperfect supervision, FOREST still achieves much higher N-IoU than the heuristic baselines (direct insert 0.7017 vs 0.3632; sweep insert 0.6166 vs 0.2167), while keeping O-IoU competitive.

Regarding the single-step assumption, you are right that the current formulation assumes exactly one newly inserted item and uses the count change to identify it. We view this as the scope of the present problem rather than a general solution to arbitrary rearrangement scenes. The multi-stow rollout results suggest the learned transition is still useful when chained over longer horizons, but they do not remove the fact that training is single-step.

On why diffusion: our goal was not to claim diffusion is uniquely optimal for this task, but to test whether a conditional generative model over structured object states can capture non-trivial post-stow rearrangements better than static placement heuristics. The strongest evidence we have is empirical: beyond large gains on the new-item mask, the model improves downstream DLO prediction error to within +0.0016 / +0.0025 MAE of using ground-truth post-stow masks, and supports multi-stow reasoning. We agree that comparisons to stronger learned baselines would further sharpen the case for diffusion specifically.

For the two clarification questions: the VLM used for correspondence auditing is Claude-3.7 in a VQA-style consistency check over pre- and post-stow RGB images, with no manual verification. The six item attributes (rigid, round, square, conveyable, foldable, fragile) come from ARMBench metadata and were selected as compact stow-relevant cues about geometry/material behavior; we do not claim they are exhaustive. Their contribution is supported by the appendix ablation, where removing the property token lowers direct-insert N-IoU from 0.7017 to 0.6619.

## Reviewer gfXd

Thank you for the detailed critique. Your concerns are centered on the exact problem formulation, the “world model” terminology, and the realism of using a canonical mask derived from the post-stow view. These are the most important issues to address directly.

First, to make the setting explicit: the model predicts a structured future bin state, not a future RGB image. The training/test inputs are (i) the pre-stow slot-aligned mask state, (ii) the pre-stow RGB image, (iii) a new-item observation, and (iv) the stow intent; the target is the post-stow slot-aligned mask state. We chose instance-mask layouts rather than full-image prediction because the downstream planning signals we study (object rearrangement, DLO, and multi-stow reasoning) depend primarily on object occupancy and geometry rather than texture synthesis. This also lets us focus modeling capacity on object interactions instead of appearance reconstruction.

Second, on the “world model” framing: we use the term in the restricted sense of a transition model over a task-relevant state space X, where X is an object-centric bin-state representation. We agree this is narrower than a full visual environment model over RGB trajectories, and our claim should be read that way. The paper’s contribution is therefore not “complete visual simulation” but a structured future-state model for sparse-snapshot stow.

Third, the canonical new-item mask is indeed a privileged proxy, and we do not want to obscure that limitation. The paper already states that this mask is derived from the ground-truth post-stow view to isolate the quality of post-stow prediction under the assumption that an in-bin contact-surface view is available. To quantify how much this prior matters, we ran an additional experiment using a weaker proxy: recovering the in-bin contact-surface view from the induct-view image with SAM3D, then training/evaluating with that synthetic condition. Performance drops, as expected, but remains clearly above heuristics: for direct insert, N-IoU/O-IoU = 0.5290/0.8443; for sweep insert, 0.4784/0.6678. We view this as evidence that the method is not solely exploiting the idealized canonical-mask input, while also honestly showing a deployment gap.

Relatedly, we do not believe the model is only learning a rigid placement transform for a known silhouette. If that were the case, it would be difficult to explain the improved handling of rearrangements of pre-existing items and the downstream DLO/multi-stow results. For example, in sweep insert O-IoU rises from 0.5287 for copy-paste(+gravity) to 0.6878/0.6906 for FOREST, indicating better prediction of how existing items move as space is created.

We agree that stronger learned baselines would strengthen the paper. The current comparison is to static heuristics because, to our knowledge, there is no prior method for this sparse-snapshot, object-centric stow setting. We therefore tried to compensate with two downstream evaluations that test whether the predicted states are actually useful, not only higher-IoU masks. We will keep the claim conservative: the current evidence supports FOREST as a useful first model for this setting, not as a definitive win over all learned alternatives.

## Reviewer oQeb

Thank you for the balanced review and for highlighting the usefulness of the downstream evaluations. We agree with the main weaknesses you identified.

On baselines: stronger learned comparisons would certainly be valuable. Our current comparisons are limited to copy-paste heuristics because this exact setting is unusually constrained: sparse pre/post supervision, object-centric mask states, intent conditioning, and real warehouse data. We therefore used downstream tasks to complement direct mask prediction. In particular, FOREST reduces the DLO error increase over ground-truth masks from +0.0057 / +0.0098 with copy-paste+gravity to only +0.0016 / +0.0025, and supports multi-stow rollouts over 1,581 chains.

On segmentation robustness: you are right that we did not provide a dedicated noise-ablation. The current pipeline mitigates obvious failures by discarding events that violate the single-step count constraint and auditing the remaining correspondences with Claude-3.7 in a VQA-style consistency check over pre/post RGB images. This does not replace a full robustness study, so we treat residual errors as label noise and keep this limitation explicit.

On generalization and single-step scope: the current evaluation is indeed ARMBench-specific and the training objective is single-step. We therefore view the multi-stow experiments as evidence of useful compositionality rather than as proof of a fully sequential world model. Likewise, we do not claim cross-geometry or unseen-category generalization beyond what ARMBench already contains.

On physical plausibility: we did not run a dedicated overlap/stability metric. Our evidence is instead task-driven: the model improves both direct mask fidelity and downstream signals that depend on bin geometry. We agree that explicit physical-constraint metrics would be a useful next evaluation axis.

## Reviewer TAf5

Thank you for the encouraging assessment and for the concrete suggestions. We agree with the three main limitations you raised: baseline strength, generalization scope, and the idealized canonical-mask prior.

On the canonical-mask prior, this is an important concern and we tried to quantify it more directly. The main paper uses a ground-truth-derived canonical mask to isolate the structured post-stow prediction problem under an assumed contact-surface view. We additionally tested a weaker proxy that recovers the in-bin contact-surface view from the induct-view image using SAM3D, then trains/evaluates FOREST with that synthetic condition. The performance decreases, but remains well above heuristic baselines: direct insert N-IoU/O-IoU = 0.5290/0.8443 and sweep insert = 0.4784/0.6678. This suggests the canonical prior helps substantially, but the model is not entirely dependent on the idealized setting.

We also agree that stronger learned baselines and broader generalization tests would strengthen the paper; the current evidence should be read as establishing a promising first benchmark/model for sparse-snapshot stow, rather than fully settling those questions.

For your two clarification questions: we suspect recent visual foresight work has become relatively sparse partly because dense-video supervision is expensive in real manipulation systems and because many recent efforts shifted toward action policies or large multimodal models. Our setting is different in that warehouse data naturally comes as sparse before/after snapshots, which makes structured future-state prediction both practical and underexplored. For the figure, the blue sweep annotation is intended as a schematic indicator of the sweep action path/position rather than a precise swept-volume estimate, which is why it is drawn as a line.
