# Strategy Plan

## Global themes
- FOREST is a structured state-transition model for sparse-snapshot robotic stow; the central claim should be framed around useful object-level foresight, not around solving full visual world modeling.
- The canonical new-item mask is a proof-of-concept proxy for the in-bin contact-surface view; acknowledge this clearly, then use the SAM3D experiment to show the method still outperforms heuristics under a weaker proxy.
- The evaluation is limited in baseline breadth and generalization scope; concede that directly, while emphasizing two things already in the paper: large gains over strong static heuristics and downstream usefulness in DLO and multi-stow reasoning.
- Clarify implementation details reviewers explicitly asked for: Claude-3.7 VQA audit, no manual verification, and the six item attributes coming from stow-relevant ARMBench metadata.

## Reviewer priorities
- Dwiz: robustness to noisy supervision, strength of assumptions, diffusion motivation, and missing implementation details.
- gfXd: world-model framing, privileged-input concern, deployment realism, and weak baseline criticism.
- oQeb: baseline breadth, robustness, generalization, and single-step scope.
- TAf5: canonical-mask prior, baseline weakness, and two clarification questions.

## Character budget
- Dwiz: 2600-3400 chars
- gfXd: 3300-4300 chars
- oQeb: 2500-3200 chars
- TAf5: 1800-2600 chars

## Blocked claims
- Do not claim that the SAM3D result closes the deployment gap.
- Do not claim any learned baseline comparison not present in the paper.
- Do not imply quantitative robustness, physical-plausibility, or cross-dataset generalization experiments that were not run.
- Do not promise new experiments or revised camera setups.

## Evidence gaps
- No quantitative segmentation-noise ablation.
- No learned baseline comparison.
- No cross-dataset or unseen-category generalization study.
- No explicit physics metric for overlap or stability.

## Concessions to make
- The single-step formulation and the canonical-mask proxy are real limitations.
- The evaluation breadth is limited, especially regarding learned baselines and generalization.
- The six attributes are useful but not claimed exhaustive.

## Risks
- Over-defending the “world model” terminology may backfire; keep it tied to structured future-state prediction.
- Overusing the SAM3D experiment could sound like a last-minute patch; present it as quantifying the proxy gap, not as solving it.
- Reviewer gfXd is most likely to react negatively to rhetorical pushback, so keep that response especially direct and technical.
