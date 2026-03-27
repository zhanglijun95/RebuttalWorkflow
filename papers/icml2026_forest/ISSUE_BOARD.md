# Issue Board

| issue_id | reviewer | round | raw_anchor | issue_type | severity | reviewer_stance | response_mode | evidence_source | status | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | Dwiz | initial | robustness to segmentation / matching noise | empirical_support | major | swing | grounded_evidence | paper | answered | explain count filter + Claude-3.7 audit; acknowledge no full quantitative noise study |
| D2 | Dwiz | initial | strong single-step count assumption | assumptions | major | swing | narrow_concession | paper | answered | acknowledge single-step formulation and scope |
| D3 | Dwiz | initial | why diffusion vs alternatives | novelty | major | swing | narrow_concession | paper | answered | rely on object-centric state, strong gains over static heuristics, but avoid overclaiming uniqueness |
| D4 | Dwiz | initial | VLM filtering details unclear | clarity | minor | swing | direct_clarification | paper | answered | Claude-3.7 VQA, no manual verification |
| D5 | Dwiz | initial | rationale for six attributes | clarity | minor | swing | direct_clarification | paper | answered | chosen from ARMBench metadata for stow-relevant shape/material cues; not claimed exhaustive |
| G1 | gfXd | initial | problem formulation / clarity | clarity | major | negative | direct_clarification | paper | answered | state exact train/test inputs and target in first sentences |
| G2 | gfXd | initial | questionable world-model characterization | novelty | critical | negative | assumption_hierarchy | paper | answered | defend structured-state world model framing while narrowing claim |
| G3 | gfXd | initial | canonical mask from post-stow image is privileged information | assumptions | critical | negative | grounded_evidence | paper,user_confirmed_result | answered | acknowledge proxy; use SAM3D experiment to quantify gap |
| G4 | gfXd | initial | model may only predict placement transform for known silhouette | empirical_support | major | negative | grounded_evidence | paper | answered | point to movement of pre-existing items + downstream utility |
| G5 | gfXd | initial | weak baselines and lack of learned comparisons | baseline_comparison | major | negative | narrow_concession | paper | answered | acknowledge limitation; argue first-step setting and downstream tests |
| G6 | gfXd | initial | practical deployment unclear | practical_significance | critical | negative | grounded_evidence | paper,user_confirmed_result | answered | clarify proxy contact-surface assumption and SAM3D-based approximation |
| O1 | oQeb | initial | stronger learned baselines missing | baseline_comparison | major | swing | narrow_concession | paper | answered | same response as G5 |
| O2 | oQeb | initial | segmentation robustness not quantified | empirical_support | major | swing | grounded_evidence | paper | answered | same response as D1 |
| O3 | oQeb | initial | generalization beyond ARMBench unknown | practical_significance | major | swing | future_work_boundary | paper | answered | acknowledge dataset-specific scope |
| O4 | oQeb | initial | single-step formulation | assumptions | major | swing | narrow_concession | paper | answered | acknowledge limitation but cite multi-stow rollout utility |
| O5 | oQeb | initial | physical plausibility not explicitly measured | empirical_support | minor | swing | narrow_concession | paper | answered | answer with observed rearrangements / DLO utility, but no dedicated physics metric |
| T1 | TAf5 | initial | weak baselines | baseline_comparison | major | positive | narrow_concession | paper | answered | concise answer |
| T2 | TAf5 | initial | generalization / distribution shift not tested | practical_significance | major | positive | future_work_boundary | paper | answered | acknowledge scope |
| T3 | TAf5 | initial | canonical-mask prior may help too much | assumptions | major | positive | grounded_evidence | paper,user_confirmed_result | answered | use SAM3D experiment and honest gap |
| T4 | TAf5 | initial | why little recent visual foresight work | other | minor | positive | direct_clarification | inference | answered | sparse-snapshot real-world setting is hard and under-benchmarked |
| T5 | TAf5 | initial | why sweep shown as blue line | clarity | minor | positive | direct_clarification | paper | answered | explain it is a schematic indicator of sweep path/position |
