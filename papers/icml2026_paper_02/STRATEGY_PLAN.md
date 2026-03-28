# Strategy Plan

## Global themes

- Theme 1: Clarify the true scope of the paper. ASTRA targets the communication bottleneck in bandwidth-constrained multi-device inference and, for decoder models, accelerates the prompt-encoding / prefill stage rather than the decode phase.
- Theme 2: Defend practical value without overclaiming novelty. The contribution is system-level integration and deployment framing, but the empirical value in low-bandwidth settings is strong and reviewer-visible.
- Theme 3: Concede real limits precisely. The main safe concessions are zero-shot degradation, non-plug-and-play training cost, missing KV-cache-compression discussion, and theory assumptions that are qualitative / simplifying rather than tight practical characterizations.
- Theme 4: Keep positive reviewers positive. Three reviewers are already on the accept side; answer them fully, reinforce the paper’s value, and avoid introducing new friction while addressing their concerns concretely.

## Reviewer priorities

- yS5Y:
  - Highest priority. Answer every point fully and calmly.
  - Main goal: reduce concern around generative applicability, prefill-only scope, KV-cache comparison, and theory restrictions.
  - Avoid sounding defensive or dismissive.
- GzCs:
  - Preserve weak-accept stance by handling training asymmetry, theory/practice gap, KV-cache relation, and prefill-only scope cleanly.
  - Strongest lever is broad evaluation plus low-bandwidth latency benefit.
- 3uqF:
  - Focus on explicitness: prefill-only latency, network simulation setup, adaptation cost, and integration-level novelty.
  - Reviewer sounds open to persuasion if answers are concrete.
- PTaj:
  - Use a warmer but still technical tone.
  - Reinforce why a system-level integration contribution is meaningful here.
  - Keep reply concise but not perfunctory; try to encourage stronger support.

## Character budget

- yS5Y: 4700-4950
- GzCs: 4300-4700
- 3uqF: 4200-4600
- PTaj: 3000-3600
- Reserve: 300-500 if the codebook-size experiment finishes and is approved for use

## Blocked claims

- Do not claim ASTRA is plug-and-play or training-free.
- Do not claim ASTRA accelerates decode / TPOT for autoregressive generation.
- Do not claim the theorems quantitatively explain the empirical gains.
- Do not claim KV-cache compression methods directly solve the same bottleneck as ASTRA.
- Do not claim exact fine-tuning wall-clock or GPU-hours unless they are explicitly confirmed.
- Do not use unfinished codebook-size results as facts before they are finalized and approved.
- Do not claim retraining is unnecessary for device-count changes.

## Evidence gaps

- Exact fine-tuning wall-clock and GPU-hours for each model.
- Explicit end-to-end latency fraction for prefill vs full generation under realistic prompt/generation ratios.
- Finalized codebook-size sensitivity results.
- Cleaner wording on network simulation details, especially stack overhead and what is included in latency timing.
- Stronger related-work positioning against KV-cache compression literature.

## Concessions to make

- Zero-shot generalization is weaker than in-domain performance for GPT models.
- Decoder experiments currently accelerate prefill / prompt encoding only.
- The training requirement is real and should be made more prominent.
- Theorem 3.1 uses simplifying Gaussian / i.i.d. assumptions for analytical clarity.
- Related-work discussion on KV-cache compression should be expanded in the revision.
- The theory is best presented as qualitative support for the design, not as a tight quantitative predictor.

## Risks

- Overstating generative-task support beyond what the paper actually evaluates.
- Irritating yS5Y by sounding dismissive about mitigation, model scale, or related work.
- Sounding evasive on the prefill-only scope.
- Sounding dismissive about KV-cache compression instead of positioning it as related but not a strong direct baseline for the low-bandwidth communication setting.
- Promising unfinished experiments or unconfirmed training-cost numbers.
- Letting the novelty response slip into “only integration” defensiveness rather than explaining why the integration matters.
