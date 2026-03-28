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
