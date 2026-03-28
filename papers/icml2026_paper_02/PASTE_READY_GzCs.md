Thank you for the careful review and for recognizing the practical systems value of the low-bandwidth setting.

**W1:** Fine-tuning requirement and "plug-and-play" interpretation.  
**A1:** ASTRA is not training-free, and the paper should make that more explicit. The correct claim is architecture-agnosticity, not plug-and-play deployment. The same framework applies across ViT, GPT2, and Llama, but the VQ modules still need to be aligned with the pretrained model through fine-tuning.

That adaptation cost is real, but it is also bounded and should simply be reported more clearly. Appendix D already gives the training schedules: `32` epochs for ViT-Base on CIFAR-100, `4` epochs on ImageNet-1K, and `1` epoch for the NLP models on the datasets listed there. The missing information is wall-clock time and GPU-hours, which we agree should be added explicitly. We are preparing the reporting format below for the revision.

| Model | Fine-tuning dataset | Fine-tuning schedule | Hardware | Wall-clock time | GPU-hours |
|---|---|---|---|---:|---:|
| ViT-Base | CIFAR-100 | 32 epochs | L40S | [TBD] | [TBD] |
| ViT-Base | ImageNet-1K | 4 epochs | L40S | [TBD] | [TBD] |
| GPT2-S | Wikipedia / Wikitext-103 | 1 epoch | L40S | [TBD] | [TBD] |
| GPT2-M | Wikipedia / Wikitext-103 | 1 epoch | L40S | [TBD] | [TBD] |
| Llama-3-8B | Wikipedia | 1 epoch | L40S | [TBD] | [TBD] |

**W2 / W5:** NAVQ gain and the gap between theory and practice.  
**A2:** The paper should present the theory as qualitative justification for NAVQ, not as a tight quantitative account of the full empirical pipeline. The Gaussian and i.i.d. assumptions in Theorem 3.1 are idealized, and real token embeddings and quantization residuals are clearly more heterogeneous. We agree that this theory-practice gap should be acknowledged more directly.

At the same time, the empirical role of NAVQ is still meaningful. NAVQ is not introduced as a large standalone accuracy gain; it is introduced to make aggressive communication compression more stable by reducing overfitting to discrete codebook boundaries. Table 12 shows exactly that kind of effect: increasing the noise magnitude from `0.0` to `1.0` improves validation accuracy from `89.91` to `90.77` and reduces the train-validation gap from `10.07` to `9.21`. A `0.86`-point gain is not huge, but in this already compressed regime it is still a real and consistent improvement. Our view is therefore that the theorem motivates the design direction, while the ablation establishes that the mechanism is useful in practice.

**W3:** Relation to KV-cache compression methods.  
**A3:** We agree that this literature should be discussed more clearly. ASTRA and KV-cache compression are related because both compress attention-related state, but they target different bottlenecks. KV-cache compression primarily targets memory-limited or long-context serving, whereas ASTRA targets inter-device communication during multi-device inference under limited bandwidth.

That is why we do not think KV-cache compression methods are strong direct baselines for the exact setting studied here. They are better viewed as adjacent and potentially complementary methods. We will add this discussion explicitly in the revised paper and summarize the distinction in the following table.

| Method | Primary target | Communication reduction in ASTRA-style low-bandwidth inference | Memory reduction | Direct baseline for ASTRA's setting? |
|---|---|---:|---:|---|
| KVQuant | KV-cache memory | [TBD] | [TBD] | No |
| CacheGen | KV-cache streaming / serving | [TBD] | [TBD] | No |
| Eigen Attention | KV-cache compression | [TBD] | [TBD] | No |
| ASTRA (`G=32`) | inter-device communication | [TBD] | [TBD] | Yes |

**W4:** Prefill-only acceleration for decoder models.  
**A4:** For decoder models, ASTRA currently accelerates the prompt-encoding / prefill stage rather than autoregressive decoding. We agree that this should be made explicit around Table 7. In the current paper, the reported Llama-3-8B latency numbers should be interpreted as prefill latency.

This does not make the result unimportant. Under low bandwidth, prefill is exactly the stage where inter-device communication dominates and where ASTRA is designed to help. Reducing that stage improves time-to-first-token, which is an important user-facing latency metric in interactive systems. The right claim is therefore not full end-to-end decode acceleration, but practical low-bandwidth acceleration of multi-device prefill.

## V1

Thank you for the careful review and for highlighting both the systems value of the paper and the points that need clearer exposition.

**W1:** Fine-tuning requirement and "plug-and-play" interpretation.  
**A1:** ASTRA is not a plug-and-play method, and we should state that more explicitly. The contribution is architecture-agnosticity rather than training-free deployment. The same ASTRA design is used across ViT, GPT2, and Llama, but the VQ modules must still be aligned with the pretrained model through fine-tuning.

This adaptation cost is real, but it should be reported clearly rather than left implicit. Appendix D already specifies the training schedules: `32` epochs for ViT-Base on CIFAR-100, `4` epochs on ImageNet-1K, and `1` epoch for the NLP models on the corresponding datasets. Following your suggestion, we report the detailed training time in GPU hours using L40S in the table below.

| Model | Fine-tuning dataset | Fine-tuning schedule | GPU-hours |
|---|---|---|---|
| ViT-Base | CIFAR-100 | 32 epochs | [TBD] |
| ViT-Base | ImageNet-1K | 4 epochs | [TBD] |
| GPT2-S | Wikipedia | 1 epoch | [TBD] |
| GPT2-M | Wikipedia | 1 epoch | [TBD] |
| Llama-3-8B | Wikipedia | 1 epoch | [TBD] |

**W2:** NAVQ gain appears small, and the gap between theory and practice should be acknowledged.  
**A2:** We agree that the theory should be interpreted carefully. Theorem 3.1 uses Gaussian and i.i.d. assumptions for analytical clarity, while real token embeddings and quantization residuals are more heterogeneous. Therefore, the theorem should not be read as a tight quantitative predictor of the empirical gain.

At the same time, we do think the empirical gain from NAVQ is meaningful in this setting. NAVQ is not introduced as a large standalone accuracy gain. Its role is to make aggressive communication compression more stable by reducing overfitting to hard codebook boundaries. Table 12 shows exactly that effect. Increasing the noise magnitude from `0.0` to `1.0` improves validation accuracy from `89.91` to `90.77` and reduces the train-validation gap from `10.07` to `9.21`. In our view, this is not an accidental gain. Rather, it is a practical validation of the mechanism that the theorem motivates qualitatively.

**W3:** Relation to KV-cache compression methods.  
**A3:** We agree that this literature should be discussed more explicitly. The key distinction is that KV-cache compression mainly targets memory-limited or long-context serving, whereas ASTRA targets inter-device communication under limited bandwidth. These directions are related, but they are not solving the same deployment bottleneck.

For that reason, we do not think KV-cache compression methods are strong direct baselines for the exact setting studied in our paper. They are better understood as adjacent and potentially complementary methods. We will add this discussion explicitly in the revised paper and summarize the distinction in the following table.

| Method | Primary target | KV compression ratio (x) |
|---|---|---|
| KVQuant [1] | KV-cache memory | 10.7 |
| CacheGen [2] | KV-cache streaming / serving | 3.5-4.3 |
| Eigen Attention [3] | KV-cache compression | 1.6 |
| ASTRA (`G=32`) | inter-device communication | 51.2-192.4 |

**W4:** Prefill-only acceleration for decoder models.  
**A4:** For decoder models, ASTRA currently accelerates only the prompt-encoding / prefill stage. We agree that this should be made explicit around Table 7. In the current paper, the reported Llama-3-8B latency numbers should be interpreted as TTFT-side speedup rather than full end-to-end generation speedup.

This does not make the result unimportant. Under low bandwidth, prefill is exactly the stage where inter-device communication dominates, and ASTRA is designed to reduce that cost. The compared baselines are evaluated under the same decoder assumption, so the comparison remains fair. The right claim is therefore practical low-bandwidth acceleration of multi-device prefill, not decode acceleration.

**W5:** How tightly the theory maps to the practical pipeline.  
**A5:** The theory and the practical pipeline should be connected more explicitly in the paper. Our intended use of the theorems is to justify why the design choices are meaningful, not to claim that they quantitatively explain every empirical improvement.

More concretely, Theorem 3.1 supports the idea that adding noise to quantized embeddings can smooth the embedding space and reduce overfitting. The empirical NAVQ ablation then shows that this mechanism is useful in practice. The same logic applies to the distributed class-token analysis. We will make this theory-to-practice relationship clearer in the revised paper.
