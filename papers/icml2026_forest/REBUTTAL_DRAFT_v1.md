# Rebuttal Draft v1

Readable markdown versions of the current per-review responses are in:

- `PASTE_READY_Dwiz.md`
- `PASTE_READY_gfXd.md`
- `PASTE_READY_oQeb.md`
- `PASTE_READY_TAf5.md`

## Reviewer Dwiz

Thank you for the thoughtful review. We agree the key concerns are noisy supervision, the single-step assumption, and whether diffusion is justified beyond heuristics. On robustness, the current pipeline has two safeguards that we did not explain clearly enough: (1) we discard events whose post-stow instance count is not exactly pre-stow count + 1, and (2) we audit the remaining one-to-one correspondences with Claude-3.7 in a VQA-style consistency check over the pre/post RGB images; there is no manual verification. We agree a dedicated quantitative noise-ablation would be valuable, but despite imperfect supervision FOREST still substantially improves N-IoU over heuristics (direct insert 0.7017 vs 0.3632; sweep insert 0.6166 vs 0.2167) while keeping O-IoU competitive.

You are also right that the current formulation is explicitly single-step: it assumes exactly one newly inserted item and uses the count change to identify it. We view this as the scope of the present problem rather than a claim to arbitrary rearrangement scenes. Similarly, our goal was not to claim diffusion is uniquely optimal, but to test whether a conditional generative model over structured object states can capture non-trivial rearrangements better than static placement heuristics. The strongest evidence we have is empirical: besides the large mask-IoU gains, using FOREST masks increases DLO MAE by only +0.0016 / +0.0025 over using ground-truth post-stow masks.

For your specific questions: the correspondence-auditing VLM is Claude-3.7 used in a visual QA consistency check over pre/post RGB images, with no manual verification. The six attributes (rigid, round, square, conveyable, foldable, fragile) come from ARMBench metadata and were chosen as compact stow-relevant cues about shape/material behavior; we do not claim they are exhaustive. Their utility is supported by the appendix ablation, where removing the property token lowers direct-insert N-IoU from 0.7017 to 0.6619.

## Reviewer gfXd

Thank you for the detailed critique. To make the setting explicit: the model predicts a structured future bin state, not a future RGB image. The inputs are the pre-stow slot-aligned mask state, pre-stow RGB, a new-item observation, and the stow intent; the target is the post-stow slot-aligned mask state. We chose mask layouts because the planning signals we study depend primarily on occupancy and geometry, and this avoids conflating dynamics with appearance synthesis.

We also agree that the “world model” claim should be interpreted narrowly. FOREST is a transition model over a task-relevant object-centric state space, not a full RGB environment simulator. The canonical new-item mask is indeed a privileged proxy, and we do not want to hide that limitation. The paper already states this assumption explicitly. To quantify the gap, we additionally tested a weaker proxy that recovers the in-bin contact-surface view from the induct-view image using SAM3D, then trains/evaluates with that synthetic condition. Performance drops, but remains clearly above heuristics: direct insert N-IoU/O-IoU = 0.5290/0.8443 and sweep insert = 0.4784/0.6678. We see this as evidence that the method is not solely exploiting the idealized canonical-mask input, while still leaving a real deployment gap.

Relatedly, we do not think the model is only learning a rigid placement transform for a known silhouette. If that were the case, it would be difficult to explain the improved handling of pre-existing-item motion and the downstream results; for example, in sweep insert O-IoU rises from 0.5287 for copy-paste(+gravity) to 0.6878/0.6906 for FOREST. We agree that stronger learned baselines would strengthen the paper. Our current evidence therefore supports FOREST as a useful first model for this sparse-snapshot setting, rather than as a definitive comparison against all learned alternatives.

## Reviewer oQeb

Thank you for the balanced review. We agree that stronger learned baselines would be valuable. Our current comparisons are limited to copy-paste heuristics because this setting is unusually constrained: sparse pre/post supervision, object-centric mask states, intent conditioning, and real warehouse data. To complement direct mask prediction, we therefore included downstream tasks: FOREST reduces the DLO error increase over ground-truth masks from +0.0057 / +0.0098 with copy-paste+gravity to only +0.0016 / +0.0025, and supports multi-stow rollouts over 1,581 chains.

On segmentation robustness, we did not provide a dedicated noise-ablation. The current pipeline removes events that violate the single-step count constraint and audits the remaining correspondences with Claude-3.7 in a VQA-style consistency check over pre/post RGB images. This does not replace a full robustness study, so we keep it as a limitation. We also agree that the present evaluation is ARMBench-specific and single-step; accordingly, we view the multi-stow results as evidence of useful compositionality rather than proof of a fully sequential model. We likewise did not run a dedicated physical-plausibility metric, and agree this would be a useful future evaluation axis.

## Reviewer TAf5

Thank you for the encouraging assessment and concrete suggestions. We agree that the canonical-mask prior, baseline strength, and generalization scope are the main limitations. To quantify the role of the canonical-mask input more directly, we additionally tested a weaker proxy that recovers the in-bin contact-surface view from the induct-view image using SAM3D, then trains/evaluates FOREST with that synthetic condition. The performance decreases, but remains above heuristics: direct insert N-IoU/O-IoU = 0.5290/0.8443 and sweep insert = 0.4784/0.6678. This suggests the canonical prior helps substantially, but the model is not entirely dependent on the idealized setting.

We also agree that stronger learned baselines and broader generalization tests would strengthen the paper; the current results should be read as establishing a promising first benchmark/model for sparse-snapshot stow rather than fully settling those questions. On your two clarification questions: our interpretation is that recent visual foresight work is relatively sparse partly because dense-video supervision is expensive in real manipulation systems and because many efforts shifted toward policy learning or large multimodal models; our setting is different because warehouse data naturally comes as sparse before/after snapshots. The blue sweep annotation is intended as a schematic indicator of the sweep action path/position rather than a precise swept-volume estimate, which is why it is drawn as a line.
