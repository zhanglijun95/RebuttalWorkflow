# User Confirmed Evidence

Only place facts here that are safe to use in the rebuttal but are not already easy to recover from the submitted paper text.

## Approved additional results
- Approved for rebuttal use: yes.
- Additional experiment:
  Generate or recover the in-bin contact-surface view of the newly stowed item using SAM3D from the induct-view image in ARMBench, then train the proposed diffusion model using this synthetic condition instead of the ground-truth-derived canonical mask.
- Exact allowed results:
  - Direct Insert: N-IoU 0.5290, O-IoU 0.8443.
  - Sweep Insert: N-IoU 0.4784, O-IoU 0.6678.
- Safe interpretation:
  - Performance drops relative to the main setting that uses the ground-truth-derived canonical mask, but remains clearly above heuristic baselines.
  - This supports the claim that FOREST is not solely dependent on the idealized canonical-mask input, while still showing an honest gap to the proof-of-concept setting.

## Approved commitments
- No explicit new commitments approved yet.

## Explicitly blocked items
- Do not imply that the SAM3D-based condition fully closes the deployment gap.
- Do not claim stronger learned-baseline results that are not in the paper or user-confirmed evidence.
- Do not promise new experiments or revised architectures unless explicitly approved later.
