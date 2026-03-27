# Stress Test Notes

## Unsupported or weak claims
- Avoid claiming FOREST is better than learned baselines; that comparison was not run.
- Avoid claiming the SAM3D experiment solves deployment; it only quantifies the gap under a weaker proxy.
- Avoid implying a quantitative robustness study for segmentation/matching noise; only filtering and auditing were performed.

## Missing issue coverage
- All major reviewer concerns are covered: canonical-mask proxy, world-model framing, weak baselines, segmentation robustness, single-step scope, generalization, and figure/attribute clarifications.

## Risky promises
- Do not promise new experiments, new sensors, revised figures, or new baselines unless explicitly approved.

## Tone problems
- Reviewer gfXd should receive the most careful wording; do not sound dismissive about the privileged-input concern.
- Positive reviewers should still receive substantive technical answers, not only thanks.

## Minimal grounded fixes
- Frame FOREST as a structured future-state model over object-centric bin states.
- Use the SAM3D result only as evidence that the method is not entirely dependent on the idealized canonical mask.
- Concede limits on learned baselines, generalization, and physical-plausibility evaluation.

## Verdict
- safe to submit
