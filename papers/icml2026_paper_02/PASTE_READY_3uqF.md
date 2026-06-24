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

| Model | Fine-tuning dataset | Fine-tuning schedule | GPU-hours | Retrain if device count changes? | Retrain if bandwidth changes? |
|---|---|---|---|---|---|
| ViT-Base | CIFAR-100 / ImageNet-1K | [TBD] | [TBD] | Yes | No |
| GPT2-S | Wikipedia / Wikitext-103 | 1 epoch | [TBD] | Yes | No |
| GPT2-M | Wikipedia / Wikitext-103 | 1 epoch | [TBD] | Yes | No |
| Llama-3-8B | Wikipedia | 1 epoch | [TBD] | Yes | No |

## V4

Only **A2** is updated below. The rest follows **V3**.

**W2:** Quality drop in zero-shot GPT evaluation and some Llama downstream tasks.  
**A2:** We agree that the zero-shot results are weaker than the in-domain results. Our understanding is that the discretized codebook representation limits representation diversity and therefore makes the model more likely to learn patterns specific to the training distribution, which hurts generalization when the evaluation distribution shifts, as discussed in Appendix H.

The broader empirical picture should be interpreted in the context of low-bandwidth inference, which is the target setting of ASTRA. The goal is to reduce inter-device communication aggressively while preserving useful language-model quality. For GPT2-M at `G=32`, Wikitext-103 PPL changes from `14.80` to `16.84`, which corresponds to only a `4.4%` increase in loss under `102.4x` communication compression. For Llama-3-8B, the downstream-task drop in Table 10 remains within `0.48%-1.67%` while communication is reduced by at least `51.2x`. These results indicate that ASTRA remains practically useful on in-domain and downstream tasks even under severe bandwidth constraints. In this setting, the communication reduction is itself important because it directly improves the latency bottleneck that motivates the paper.

## V3

Thank you for the thoughtful review. Below we provide one-to-one responses to the raised weaknesses and questions.

**W1 / Q1:** Prefill-only acceleration and the interpretation of Table 7.  
**A1:** Table 7 reports prefill latency rather than full end-to-end generation latency. We agree that this should be stated explicitly in the paper. Section 3.1 already states that prompt tokens are encoded in parallel across devices, while autoregressive decoding proceeds on a single device. The current latency result should therefore be interpreted as TTFT-side speedup.

This result is still meaningful for the setting studied here. Prefill is exactly the stage where inter-device communication dominates under low bandwidth, and ASTRA is designed to reduce that cost. Reducing prefill latency therefore improves time-to-first-token, which is an important practical metric in interactive use. A credible path to the decode phase would require extending the same communication-efficient representation to the incremental KV-state updates used during autoregressive decoding. This is a reasonable direction, but it is outside the scope of the current paper.

**W2:** Quality drop in zero-shot GPT evaluation and some Llama downstream tasks.  
**A2:** The zero-shot GPT result is the clearest limitation of the current paper, but it is not the full picture of the language results. For GPT2-M at `G=32`, Wikitext-103 PPL changes from `14.80` to `16.84`, while zero-shot PPL rises from `43.22` to `62.29`. Our reading is that the discretized codebook representation preserves the dominant patterns needed for in-domain modeling, but reduces representation diversity and therefore generalizes less well when the evaluation distribution shifts. This point is also discussed in Appendix H.

The Llama-3-8B results remain encouraging under the same compression setting. Table 10 shows that, at `G=32`, the downstream-task drop is only `0.48%-1.67%` relative to the original model, while communication is reduced by at least `51.2x`. We therefore do not interpret the zero-shot result as overturning the main value of the paper. The more accurate conclusion is that ASTRA preserves strong in-domain and downstream utility under severe communication compression, while zero-shot robustness remains an important future direction.

**W3 / Q2:** Deployment and networking setup.  
**A3:** The latency experiments use a simulated bandwidth-constrained setting rather than a full physical network deployment. We agree that the paper should explain this more explicitly. Concretely, when data are exchanged, the communication time is enforced according to the transmitted size and the specified bandwidth cap. All compared methods share the same implementation stack, so the latency comparison is controlled and fair.

The reported ASTRA latency includes the local codebook lookup and dequantization operations. What is not modeled separately is additional network-stack overhead beyond the bandwidth-constrained transfer simulation. The correct interpretation is therefore algorithmic end-to-end latency under a controlled low-bandwidth setting, not a full deployment study of every systems overhead. We will revise the paper to state this distinction directly.

**W4:** Originality is mainly at the integration level.  
**A4:** We think this is a fair characterization of the novelty. The individual ingredients are not each new in isolation. The contribution is that they are assembled into a communication-efficient inference framework that makes multi-device Transformer inference useful in a low-bandwidth regime where prior baselines often fail to beat single-device inference.

This systems-level integration is meaningful because it changes the operating region of distributed inference. The paper is not claiming a fundamentally new Transformer primitive. It is showing that a carefully designed combination of known ingredients can make `10-100 Mbps` multi-device inference practical, which is the deployment problem motivating the work.

**Q3:** Adaptation cost and retraining under deployment changes.  
**A5:** ASTRA does require adaptation, and we agree that this should be reported more explicitly. Appendix D gives the fine-tuning schedules, but not the wall-clock time or GPU-hours. Following your suggestion, we will report the detailed adaptation cost directly in the revised paper.

The current formulation does not require retraining when only the bandwidth changes. It does require retraining when the device count changes, because the partitioning structure changes with it. We summarize the reporting format below.

| Model | Fine-tuning dataset | Fine-tuning schedule | GPU-hours | Retrain if device count changes? | Retrain if bandwidth changes? |
|---|---|---|---|---|---|
| ViT-Base | CIFAR-100 / ImageNet-1K | [TBD] | [TBD] | Yes | No |
| GPT2-S | Wikipedia / Wikitext-103 | 1 epoch | [TBD] | Yes | No |
| GPT2-M | Wikipedia / Wikitext-103 | 1 epoch | [TBD] | Yes | No |
| Llama-3-8B | Wikipedia | 1 epoch | [TBD] | Yes | No |

## V2

Thank you for the thoughtful review. Below we provide one-to-one responses to the raised weaknesses and questions.

**W1 / Q1:** Prefill-only acceleration and the interpretation of Table 7.  
**A1:** Yes, Table 7 measures prefill latency for decoder models, and we will make this explicit in the revised paper. Section 3.1 already states that prompt tokens are encoded in parallel across devices, while autoregressive decoding then proceeds on a single device. The reported speedup should therefore be interpreted as TTFT-side speedup rather than full end-to-end generation speedup.

This scope is narrower than full decode acceleration. It is still meaningful because prefill is exactly the stage where inter-device communication dominates in the low-bandwidth setting studied here. Reducing that stage improves time-to-first-token, which is an important practical latency metric in interactive systems. A credible path to the decode phase would require extending the same communication-efficient representation to incremental KV-state updates during autoregressive decoding. This is a natural direction, but it is outside the scope of the current paper.

**W2:** Quality drop in zero-shot GPT evaluation and some Llama downstream tasks.  
**A2:** We agree that the zero-shot GPT results are weaker than the in-domain results, and this should be stated clearly. For GPT2-M at `G=32`, Wikitext-103 PPL changes from `14.80` to `16.84`, while zero-shot PPL rises from `43.22` to `62.29`. Our understanding is that the discretized codebook representation preserves the dominant patterns needed for in-domain modeling, but reduces representation diversity and therefore generalizes less well when the evaluation distribution shifts. This point is also discussed in Appendix H.

The broader empirical picture remains positive. For Llama-3-8B, Table 10 shows that the downstream-task drop at `G=32` is only `0.48%-1.67%` relative to the original model, while communication is reduced by at least `51.2x`. We therefore do not view the zero-shot result as overturning the main value of the paper. The main takeaway is that ASTRA preserves strong practical utility under severe communication compression, while zero-shot robustness remains an important future direction.

**W3 / Q2:** Deployment and networking setup.  
**A3:** The latency experiments use simulated bandwidth-constrained communication rather than a full physical network deployment. We agree that the paper should explain this more explicitly. Concretely, when devices exchange data, the communication time is enforced according to the transmitted size and the specified bandwidth cap. All methods share the same implementation stack, so the latency comparison is controlled and fair.

The reported ASTRA latency includes the local codebook lookup and dequantization operations. What is not modeled separately is additional network-stack overhead beyond the bandwidth-constrained transfer simulation. The correct interpretation is therefore algorithmic end-to-end latency under a controlled low-bandwidth setting, not a full deployment study of every systems overhead. We will revise the paper to make this distinction explicit.

**W4:** Originality is mainly at the integration level.  
**A4:** We think this is a fair characterization. The individual ingredients are not each new in isolation. The contribution is that they are assembled into a communication-efficient inference framework that makes multi-device Transformer inference useful in a low-bandwidth regime where prior baselines often fail to beat single-device inference.

This systems-level integration is meaningful because it changes the operating region of distributed inference. The paper is not claiming a fundamentally new Transformer primitive. It is showing that a carefully designed combination of known ingredients can make `10-100 Mbps` multi-device inference practical, which is the deployment problem motivating the work.

**Q3:** Adaptation cost and retraining under deployment changes.  
**A5:** ASTRA does require adaptation, and we agree that this should be reported more explicitly. Appendix D gives the fine-tuning schedules, but not the wall-clock time or GPU-hours. Following your suggestion, we will report the detailed adaptation cost directly in the revised paper.

Regarding deployment changes, the current formulation does not require retraining when only the bandwidth changes. It does require retraining when the device count changes, because the partitioning structure changes with it. We summarize the reporting format below.

| Model | Fine-tuning dataset | Fine-tuning schedule | GPU-hours | Retrain if device count changes? | Retrain if bandwidth changes? |
|---|---|---|---|---|---|
| ViT-Base | CIFAR-100 / ImageNet-1K | [TBD] | [TBD] | Yes | No |
| GPT2-S | Wikipedia / Wikitext-103 | 1 epoch | [TBD] | Yes | No |
| GPT2-M | Wikipedia / Wikitext-103 | 1 epoch | [TBD] | Yes | No |
| Llama-3-8B | Wikipedia | 1 epoch | [TBD] | Yes | No |

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
