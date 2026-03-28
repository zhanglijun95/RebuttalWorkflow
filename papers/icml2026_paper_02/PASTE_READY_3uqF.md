Thank you for the thoughtful review and for recognizing both the practical importance of the problem and the breadth of the evaluation.

**W1 / Q1:** Prefill-only acceleration and the interpretation of Table 7.  
**A1:** Yes, Table 7 measures prefill latency for decoder models, and the paper should state that explicitly. In Section 3.1, prompt tokens are encoded in parallel across devices, while autoregressive decoding then proceeds on a single device. The current method therefore accelerates TTFT-side latency rather than the full decode process.

We nevertheless think this is a meaningful result. In low-bandwidth multi-device inference, prefill is exactly the stage where communication becomes dominant, and ASTRA is designed to remove that bottleneck. Reducing prefill latency improves time-to-first-token, which is important in interactive systems even when long-generation TPOT is still dominated by sequential decoding. A credible extension to the decode phase would require compressing and updating the incremental KV state in the same spirit as ASTRA's prefill communication. That is a natural next step, but it is not part of the current paper.

**W2:** Quality drop in zero-shot GPT evaluation and some Llama downstream tasks.  
**A2:** The main empirical picture is that ASTRA preserves useful in-domain quality under large communication compression, while zero-shot transfer is the clearest weakness. For GPT2-M at `G=32`, Wikitext-103 PPL changes from `14.80` to `16.84`, whereas zero-shot PPL rises from `43.22` to `62.29`. We think this gap reflects the same generalization boundary discussed in Appendix H: the discretized codebook representation retains the dominant in-domain structure well, but generalizes less well when the test distribution shifts.

At the same time, the method remains useful on the larger decoder setting in the paper. For Llama-3-8B, Table 10 shows that the downstream-task drop at `G=32` is still modest relative to the original model, while communication is reduced by at least `51.2x`. For example, CoLA / SST2 / AG News / QQP move from `0.7615 / 0.8426 / 0.8374 / 0.7970` to `0.7539 / 0.8314 / 0.8325 / 0.7803`. Our intended claim is therefore not "uniform quality preservation," but rather that ASTRA retains strong practical utility under severe communication compression, with zero-shot robustness remaining the main unresolved limitation.

**W3 / Q2:** Deployment and networking setup.  
**A3:** The latency experiments use simulated bandwidth-constrained communication rather than a full physical network deployment, and the paper should explain that more explicitly. Concretely, when data are exchanged, communication time is enforced according to the transmitted size and the specified bandwidth cap. This is the same implementation framework used for all compared methods, so the latency comparison is controlled and fair.

In the current setup, ASTRA timing includes the local codebook lookup and dequantization operations. What is not modeled separately is full network-stack overhead beyond the bandwidth-constrained transfer simulation. The correct interpretation is therefore algorithmic end-to-end latency under a controlled bandwidth-constrained setting, not a full deployment study of every systems overhead. We will make this distinction explicit in the revision.

**W4:** Originality is mainly at the integration level.  
**A4:** We think this is a fair characterization, and we also think that this is where the paper's value lies. The individual ingredients are not each new in isolation. The contribution is that they are assembled into a communication-efficient inference framework that makes multi-device Transformer inference useful in a low-bandwidth regime where prior baselines often fail to beat single-device inference.

That systems-level integration is meaningful because it changes the operating region of distributed inference. The paper is not claiming a fundamentally new Transformer primitive. It is showing that a carefully designed combination of known ingredients can make `10-100 Mbps` multi-device inference practical, which is the real deployment problem motivating the work.

**Q3:** Adaptation cost and retraining under deployment changes.  
**A5:** ASTRA does require adaptation, and we agree that this should be stated more explicitly. Appendix D gives the fine-tuning schedules, but not the wall-clock time or GPU-hours, and we are preparing those numbers for the revision. The adaptation cost is therefore real, but it should be reported directly rather than left implicit.

Regarding deployment changes, the current formulation does not require retraining when only the bandwidth changes. It does require retraining when the device count changes, because the partitioning structure changes with it. We summarize the reporting format below.

| Model | Fine-tuning dataset | Fine-tuning schedule | Hardware | Wall-clock time | GPU-hours | Retrain if device count changes? | Retrain if bandwidth changes? |
|---|---|---|---|---:|---:|---|---|
| ViT-Base | CIFAR-100 / ImageNet-1K | [TBD] | L40S | [TBD] | [TBD] | Yes | No |
| GPT2-S | Wikipedia / Wikitext-103 | 1 epoch | L40S | [TBD] | [TBD] | Yes | No |
| GPT2-M | Wikipedia / Wikitext-103 | 1 epoch | L40S | [TBD] | [TBD] | Yes | No |
| Llama-3-8B | Wikipedia | 1 epoch | L40S | [TBD] | [TBD] | Yes | No |

## V1

Thank you for the thoughtful review and for recognizing both the practical importance of the problem and the breadth of the evaluation.

**W1 / Q1:** Prefill-only acceleration and the interpretation of Table 7.  
**A1:** Yes, Table 7 measures prefill latency for decoder models, and we should state that explicitly in the paper. In Section 3.1, prompt tokens are encoded in parallel across devices, while autoregressive decoding then proceeds on a single device. The current method therefore accelerates TTFT-side latency rather than the full decode process.

We nevertheless think this is a meaningful result. In low-bandwidth multi-device inference, prefill is exactly the stage where communication becomes dominant, and ASTRA is designed to remove that bottleneck. Reducing prefill latency improves time-to-first-token, which is important in interactive systems even when long-generation TPOT is still dominated by sequential decoding. A credible extension to the decode phase would require compressing and updating the incremental KV state in the same spirit as ASTRA's prefill communication. That is a natural direction, but it is not part of the current paper.

**W2:** Quality drop in zero-shot GPT evaluation and some Llama downstream tasks.  
**A2:** We agree that the zero-shot GPT results are weaker than the in-domain results, and this should be stated clearly. At the same time, the broader empirical picture is more positive than the zero-shot numbers alone suggest. For GPT2-M at `G=32`, Wikitext-103 PPL changes from `14.80` to `16.84`, whereas zero-shot PPL rises from `43.22` to `62.29`. We think this gap reflects the same generalization boundary discussed in Appendix H. The discretized codebook representation retains the dominant in-domain structure well, but generalizes less well when the test distribution shifts.

The method still remains useful on the larger decoder setting in the paper. For Llama-3-8B, Table 10 shows that the downstream-task drop at `G=32` is only `0.48%-1.67%` relative to the original model, while communication is reduced by at least `51.2x`. Our intended claim is therefore not uniform quality preservation in every setting. It is that ASTRA retains strong practical utility under severe communication compression, with zero-shot robustness remaining the clearest limitation.

**W3 / Q2:** Deployment and networking setup.  
**A3:** The latency experiments use simulated bandwidth-constrained communication rather than a full physical network deployment, and we should explain that more explicitly. Concretely, when data are exchanged, communication time is enforced according to the transmitted size and the specified bandwidth cap. This is the same implementation framework used for all compared methods, so the latency comparison is controlled and fair.

In the current setup, ASTRA timing includes the local codebook lookup and dequantization operations. What is not modeled separately is full network-stack overhead beyond the bandwidth-constrained transfer simulation. The correct interpretation is therefore algorithmic end-to-end latency under a controlled bandwidth-constrained setting, not a full deployment study of every systems overhead. We will make this distinction explicit in the revision.

**W4:** Originality is mainly at the integration level.  
**A4:** We think this is a fair characterization, and we also think that this is where the paper's value lies. The individual ingredients are not each new in isolation. The contribution is that they are assembled into a communication-efficient inference framework that makes multi-device Transformer inference useful in a low-bandwidth regime where prior baselines often fail to beat single-device inference.

That systems-level integration is meaningful because it changes the operating region of distributed inference. The paper is not claiming a fundamentally new Transformer primitive. It is showing that a carefully designed combination of known ingredients can make `10-100 Mbps` multi-device inference practical, which is the real deployment problem motivating the work.

**Q3:** Adaptation cost and retraining under deployment changes.  
**A5:** ASTRA does require adaptation, and we agree that this should be stated more explicitly. Appendix D gives the fine-tuning schedules, but not the wall-clock time or GPU-hours. Following your suggestion, we will report these numbers directly rather than leave them implicit.

Regarding deployment changes, the current formulation does not require retraining when only the bandwidth changes. It does require retraining when the device count changes, because the partitioning structure changes with it. We summarize the reporting format below.

| Model | Fine-tuning dataset | Fine-tuning schedule | GPU-hours | Retrain if device count changes? | Retrain if bandwidth changes? |
|---|---|---|---|---|---|
| ViT-Base | CIFAR-100 / ImageNet-1K | [TBD] | [TBD] | Yes | No |
| GPT2-S | Wikipedia / Wikitext-103 | 1 epoch | [TBD] | Yes | No |
| GPT2-M | Wikipedia / Wikitext-103 | 1 epoch | [TBD] | Yes | No |
| Llama-3-8B | Wikipedia | 1 epoch | [TBD] | Yes | No |
