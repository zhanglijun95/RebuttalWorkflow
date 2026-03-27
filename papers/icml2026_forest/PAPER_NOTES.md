# Paper Notes

## One-paragraph summary
FOREST is a stow-intent-conditioned visual foresight model for robotic warehouse stow. Given a pre-stow bin observation, a new-item observation, and the intended stow action, it predicts the post-stow bin layout as a slot-aligned instance-mask state. The method converts sparse pre/post RGB snapshots from ARMBench into item-aligned supervision via MaskDINO instance masks and DINOv2-based item matching with placement and order priors, then uses a transformer-based latent diffusion model to predict the future bin state. The paper evaluates both direct post-stow mask prediction and downstream usefulness through DLO prediction and multi-stow reasoning.

## Main claims
- C1: FOREST is claimed to be the first learned world model for real robotic stow trained from sparse snapshot supervision rather than dense videos.
- C2: FOREST substantially improves prediction of the newly inserted item's post-stow mask over heuristic baselines in both direct-insert and sweep-insert settings.
- C3: FOREST predictions remain useful for downstream planning-style tasks: replacing ground-truth post-stow masks with FOREST predictions causes only modest degradation in DLO prediction and supports multi-stow rollouts.
- C4: The object-centric, slot-aligned state plus stow-intent conditioning lets the model capture rearrangements beyond static copy-paste placement.

## Key evidence already in the paper
- E1: Direct evaluation shows much higher N-IoU than copy-paste and copy-paste-with-gravity, while keeping O-IoU competitive.
- E2: DLO prediction with FOREST masks incurs only small MAE increases over ground-truth post-stow masks: +0.0016 for direct insert and +0.0025 for sweep insert.
- E3: Multi-stow experiments on 1,581 chains with length up to four show better long-horizon behavior than the heuristic baseline.
- E4: Conditioning ablations show both pre-stow RGB and item-property conditioning improve performance, especially for small and difficult stows.

## Important quantitative results
- Table 1:
  - What it shows: direct post-stow prediction quality in instance-mask space.
  - Exact numbers:
    - Direct insert overall N-IoU: copy-paste 0.2846, copy-paste+gravity 0.3632, FOREST-DI 0.7017, FOREST-J 0.7021.
    - Direct insert overall O-IoU: copy-paste 0.8563, copy-paste+gravity 0.8563, FOREST-DI 0.8550, FOREST-J 0.8536.
    - Direct-insert small / medium / large N-IoU for FOREST-DI: 0.5771 / 0.7263 / 0.8021.
    - Direct-insert surprise / non-obvious / obvious N-IoU for FOREST-DI: 0.5623 / 0.7354 / 0.7920.
    - Sweep insert overall N-IoU: copy-paste 0.1214, copy-paste+gravity 0.2167, FOREST-SI 0.6166, FOREST-J 0.6422.
    - Sweep insert overall O-IoU: copy-paste 0.5287, copy-paste+gravity 0.5287, FOREST-SI 0.6878, FOREST-J 0.6906.
    - Sweep-insert small / medium / large N-IoU for FOREST-SI: 0.4791 / 0.6276 / 0.7434.
    - Sweep-insert surprise / non-obvious / obvious N-IoU for FOREST-SI: 0.5855 / 0.6483 / 0.6394.
- Table 2:
  - What it shows: downstream DLO prediction quality when synthetic post-stow masks replace ground-truth masks.
  - Exact numbers:
    - Direct insert DLO MAE: GT 0.0168, copy-paste+gravity 0.0225, FOREST 0.0184.
    - Direct insert MAE increase over GT: copy-paste+gravity +0.0057, FOREST +0.0016.
    - Sweep insert DLO MAE: GT 0.0255, copy-paste+gravity 0.0353, FOREST 0.0280.
    - Sweep insert MAE increase over GT: copy-paste+gravity +0.0098, FOREST +0.0025.
- Table 3:
  - What it shows: dataset statistics.
  - Exact numbers:
    - Direct insert train/test: 26,531 / 6,558.
    - Sweep insert train/test: 20,678 / 5,350.
- Appendix F Table 5:
  - What it shows: ablation on conditioning signals for direct-insert FOREST.
  - Exact numbers:
    - Overall N-IoU: full 0.7017, w/o RGB 0.5799, w/o property 0.6619, w/o RGB + property 0.5089.
    - Overall O-IoU: full 0.8550, w/o RGB 0.8232, w/o property 0.8321, w/o RGB + property 0.7675.
    - The largest drops are on small and difficult stows.

## Baselines / comparisons already covered
- Copy-paste baseline: paste the new-item mask into the intended insertion region without modeling interactions.
- Copy-paste with gravity baseline: same as above, then vertically settle the pasted item until it hits the bin ground.
- The paper explicitly says there is no prior learned baseline for this exact sparse-snapshot stow setting, which is why it uses heuristic baselines plus downstream evaluations.

## Limitations we can acknowledge safely
- The current formulation is single-step and trained on sparse pre/post snapshots rather than explicit multi-step transitions.
- The new-item representation uses a canonical mask derived from the ground-truth post-stow mask; this is a proof-of-concept proxy for the in-bin contact-surface view, not the final deployment input.
- The method depends on instance segmentation and item matching quality, and residual label noise may remain after filtering.
- Evaluation is on ARMBench only, so broader domain-shift and cross-dataset generalization remain future work.
- The state is mask-based rather than a richer physical or visual world representation.

## Review-sensitive facts
- novelty anchors
- The paper claims this is the first learned world model for real stow with only snapshot supervision.
- The novelty is in the setting, state construction, and conditioning design, not in claiming diffusion itself is new.
- theoretical assumptions
- Single-step stow events only, with exactly one new item, so the matching setup assumes post-stow instance count equals pre-stow count plus one.
- The model uses a latent diffusion transformer conditioned on pre-stow state, canonical new-item mask, pre-stow RGB, item properties, and stow intent.
- runtime / complexity
- FOREST has 50M parameters and is evaluated with 50 denoising steps.
- ablations
- Appendix F shows both pre-stow RGB and the six-attribute property token matter; removing both causes the largest degradation.
- Direct-vs-joint variants are evaluated: FOREST-DI, FOREST-SI, and FOREST-J.
- dataset / setup details
- Dataset is ARMBench with pre-stow RGB, post-stow RGB, induct-view new-item image, item physical properties, and stow intent metadata.
- Only successful stow events are used; direct insert and sweep insert are split 8:2 into train/test.
- Item masks come from MaskDINO.
- Item matching uses DINOv2 visual embeddings plus placement and order priors, solved with the Hungarian algorithm.
- Matching failures are filtered by count checks and then audited with Claude-3.7 in a visual-question-answering consistency check.
- The six item properties are rigid, round, square, conveyable, foldable, and fragile.
