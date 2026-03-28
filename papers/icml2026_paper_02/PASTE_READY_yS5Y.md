Thank you for the detailed and constructive review.

**W1:** Concern about the accuracy degradation in generative / zero-shot settings.  
**A1:** [开头总起写我们understand审稿人关于这方面的concern，但是我们要说明我们在NLP tasks的结果还是不错的] The language results are stronger than the zero-shot numbers alone suggest [看不懂你想表达什么，为什么一开始就是什么比什么stronger，就直接说我们在NLP tasks的结果不错不行吗？alone suggest是什么意思，不要用这种不formal的表达]. On the core in-domain evaluations, ASTRA preserves useful model quality under very large communication reduction: [永远不要用冒号，用句号然后for example] for GPT2-M at `G=32`, Wikitext-103 PPL changes from `14.80` to `16.84`, and for Llama-3-8B, Table 10 shows that the downstream-task drop remains modest [modest具体到数值] while communication is reduced by at least `51.2x`. We think this is the main empirical message of the paper: [不要冒号] ASTRA can compress inter-device communication very aggressively while keeping practical language-model utility.

We agree that the main weakness appears in zero-shot transfer. For GPT2-M at `G=32`, zero-shot PPL rises from `43.22` to `62.29`. This is primarily a generalization issue introduced by the discretized codebook representation. It preserves the dominant patterns needed for in-domain modeling, but it reduces representation diversity and therefore generalizes less well when the train and test distributions differ (as discussed in Appendix H). We do not want to overstate it as solved in the current submission. Rather, the current paper shows strong in-domain and downstream utility under large communication compression, while zero-shot robustness remains the clearest remaining limitation [最后半句改掉，确实是future work].

**W2 / Q3:** Comparisons to KV cache compression literature.  
**A2:** KV-cache compression is mainly reducing KV-cache size for memory-limited or long-context serving, whereas ASTRA targets inter-device communication in low-bandwidth multi-device inference. That difference matters because a method can be strong for cache-memory reduction and still be a weak direct baseline when the dominant cost is transmitting representations across devices at low bandwidth.

We therefore agree that this literature should be added and discussed explicitly in the revised paper. At the same time, we do not think these methods are strong direct baselines for the low-bandwidth setting we studied. 
In particular, the methods [1-3] report substantially smaller compression ratios than ASTRA as shown in the table below, which means their communication time in our low-bandwidth setting would still be much higher.

| Method | Primary target | KV compression ratio (x) |
|---|---|---|
| KVQuant [1] | KV-cache memory | 10.7 |
| CacheGen [2] | KV-cache streaming / serving | 3.5-4.3 |
| Eigen Attention [3] | KV-cache compression | 1.6 | 
| ASTRA (`G=32`) | inter-device communication | 51.2-192.4 | 

**W3 / Q1:** Adaptation/training cost of ASTRA.  
**A3:** ASTRA does require fine-tuning to align the VQ modules with the pretrained Transformer as described in the training protocol in Appendix D. Following your suggestion, we report the detailed training time in GPU hours using L40S in the table below.

| Model | Fine-tuning dataset | Fine-tuning schedule | GPU-hours |
|---|---|---|---|
| ViT-Base | CIFAR-100 | 32 epochs | [TBD] |
| ViT-Base | ImageNet-1K | 4 epochs | [TBD] |
| GPT2-S | Wikipedia | 1 epoch | [TBD] |
| GPT2-M | Wikipedia | 1 epoch | [TBD] |
| Llama-3-8B | Wikipedia | 1 epoch | [TBD] |

**W4:** Support for generative-task claims at larger scale.  
**A4:** We agree that broader model coverage would strengthen the paper further. [说明由于时间原因我们没办法在rebuttal阶段提供更多大模型的结果了，但是我们想强调我们的方法 goes beyond small GPT2 models by including Llama-3-8B to show the scalability of ASTRA]. In Table 6, Llama-3-8B PPL changes from `5.8118` to `7.4360` at `G=32` with `51.2x` communication reduction, and Table 10 shows that the downstream-task drop remains moderate. 

**W5:** Theorem 3.1's sensitivity to its assumptions.  
**A5:** We agree that the Gaussian and i.i.d. assumptions in Appendix B are idealized. [“Some explanation on the sensitivity of this theoretical guarantee when this assumption does not hold”需要你来帮我想想怎么分析]

Besides, the theorem provides the design logic behind NAVQ. The purpose of adding noise is to smooth the quantized embedding space so that the model does not overfit to hard codebook boundaries. That is also the effect we observe empirically. In Table 12, increasing the noise magnitude from `0.0` to `1.0` improves validation accuracy from `89.91` to `90.77` and reduces the train-validation gap from `10.07` to `9.21`. Our view is therefore that the theory explains why this design should help in principle, and the ablation shows that it is indeed useful in practice.

**Q2:** Concern about ASTRA only accelerates prefill phase for generative models.
**A6:** For decoder models, ASTRA currently only accelerates the prompt-encoding / prefill stage as stated in Section 3.1. We agree that for long generations, decoding can dominate total latency. Yet, we also would to emphasize that reducing prefill latency is still useful because it directly improves time-to-first-token and interactive responsiveness. 
Therefore, [考虑到我们的论文和baselines都是只在encoding阶段加速], the speedup reported is effectively TTFT(Time to First Token)-side speedup rather than overall speedup for easy and fair comparison.

**Q4:** Sensitivity to codebook size.  
**A7:** We fix the codebook size at `1024`, which corresponds to `10` bits per transmitted token index, and study the main communication-accuracy tradeoff by varying the number of groups `G`. 
Following your suggestion, we provide additional codebook-size evaluations in the table below.
We observe that [].

| Codebook size `K` | Total bits per token | Compression ratio | ImageNet accuracy of ViT-Base |
|---|---|---|---|
| 256 | [TBD] | [TBD] | [TBD] |
| 512 | [TBD] | [TBD] | [TBD] |
| 1024 | [TBD] | [TBD] | [TBD] |
| 2048 | [TBD] | [TBD] | [TBD] |

## V1

Thank you for the detailed and constructive review. Below we provide one-to-one responses to the raised weaknesses and questions.

**W1:** Concern about the accuracy degradation in generative / zero-shot settings.  
**A1:** We understand the concern regarding zero-shot generation. At the same time, we would like to clarify that the overall NLP results in the paper remain strong under severe communication compression. For GPT2-M at `G=32`, Wikitext-103 PPL changes from `14.80` to `16.84`. For Llama-3-8B, the downstream-task drop in Table 10 is only `0.48%-1.67%` while communication is reduced by at least `51.2x`. These results show that ASTRA preserves practical language-model utility on in-domain and downstream tasks.

The larger degradation appears mainly in zero-shot transfer. For GPT2-M at `G=32`, zero-shot PPL rises from `43.22` to `62.29`. Our understanding is that the discretized codebook representation limits representation diversity and therefore makes the model more likely to learn patterns specific to the training distribution, which hurts generalization when the evaluation distribution shifts. This point is already discussed in Appendix H. We do not want to claim that this issue is already solved in the current paper. Rather, we view it as the main future direction, while the present submission already demonstrates strong practical value for the matched and near-matched settings that motivate ASTRA.

**W2 / Q3:** Comparisons to KV cache compression literature.  
**A2:** KV-cache compression is related to ASTRA, and we agree that this literature should be discussed explicitly in the revised paper. The key distinction is that these methods mainly reduce KV-cache size for memory-limited or long-context serving, whereas ASTRA targets inter-device communication in low-bandwidth multi-device inference. For the setting studied in our paper, this difference is fundamental because the dominant bottleneck is communication time rather than cache-memory footprint.

We therefore do not think these methods are strong direct baselines for the exact setting studied here. In particular, the methods cited in `[1-3]` report substantially smaller compression ratios than ASTRA, as summarized in the table below. This means their communication time in our low-bandwidth setting would still be much higher. We will add this discussion to the related-work section and clarify that these methods are related and potentially complementary, but they do not directly address the same bottleneck as ASTRA.

| Method | Primary target | KV compression ratio (x) |
|---|---|---|
| KVQuant [1] | KV-cache memory | 10.7 |
| CacheGen [2] | KV-cache streaming / serving | 3.5-4.3 |
| Eigen Attention [3] | KV-cache compression | 1.6 |
| ASTRA (`G=32`) | inter-device communication | 51.2-192.4 |

**W3 / Q1:** Adaptation/training cost of ASTRA.  
**A3:** ASTRA does require fine-tuning to align the VQ modules with the pretrained Transformer, as described in Appendix D. This is a real adaptation cost, and we agree that it should be reported more explicitly. At the same time, the paper does not claim to be plug-and-play. The intended claim is architecture-agnosticity, namely that the same ASTRA design applies across ViT, GPT2, and Llama.

Following your suggestion, we report the detailed training time in GPU hours using L40S in the table below.

| Model | Fine-tuning dataset | Fine-tuning schedule | GPU-hours |
|---|---|---|---|
| ViT-Base | CIFAR-100 | 32 epochs | [TBD] |
| ViT-Base | ImageNet-1K | 4 epochs | [TBD] |
| GPT2-S | Wikipedia | 1 epoch | [TBD] |
| GPT2-M | Wikipedia | 1 epoch | [TBD] |
| Llama-3-8B | Wikipedia | 1 epoch | [TBD] |

**W4:** Support for generative-task claims at larger scale.  
**A4:** We agree that broader model coverage would strengthen the paper further. Due to the rebuttal-stage time limit, we cannot add a broader large-model sweep here. At the same time, the current submission already goes beyond small GPT2 models by including Llama-3-8B, which is exactly meant to demonstrate the scalability of ASTRA.

In Table 6, Llama-3-8B PPL changes from `5.8118` to `7.4360` at `G=32` with `51.2x` communication reduction. In Table 10, the downstream-task drop also remains moderate. We therefore think the present paper already supports applicability beyond small decoder models, even though broader coverage would further strengthen the empirical case.

**W5:** Theorem 3.1's sensitivity to its assumptions.  
**A5:** We agree that the Gaussian and i.i.d. assumptions in Appendix B are idealized. When these assumptions do not hold exactly, the quantitative guarantee in Theorem 3.1 can weaken because the Wasserstein-distance reduction no longer decomposes as cleanly across dimensions. In that sense, the theorem should not be interpreted as a precise predictive model of the practical gain.

At the same time, the theorem still explains the design logic behind NAVQ. The purpose of adding noise is to smooth the quantized embedding space so that the model does not overfit to hard codebook boundaries. That is also the effect we observe empirically. In Table 12, increasing the noise magnitude from `0.0` to `1.0` improves validation accuracy from `89.91` to `90.77` and reduces the train-validation gap from `10.07` to `9.21`. Our view is therefore that the theorem provides qualitative justification for the design, while the ablation shows that NAVQ is useful in practice.

**Q2:** Concern about ASTRA only accelerating the prefill phase for generative models.  
**A6:** For decoder models, ASTRA currently accelerates only the prompt-encoding / prefill stage, as stated in Section 3.1. We agree that for long generations, decoding can dominate total latency. The reported latency speedup is therefore TTFT-side speedup rather than full end-to-end generation speedup.

At the same time, reducing prefill latency is still useful because it directly improves time-to-first-token and interactive responsiveness. The comparison in Table 7 is also fair because our paper and the compared baselines are evaluated under the same decoder assumption, so the table isolates the stage where ASTRA actually reduces communication cost. We will revise the paper to make this TTFT interpretation explicit.

**Q4:** Sensitivity to codebook size.  
**A7:** We fix the codebook size at `1024`, which corresponds to `10` bits per transmitted token index, and study the main communication-accuracy tradeoff by varying the number of groups `G`. Following your suggestion, we provide additional codebook-size evaluations in the table below.

These results indicate that ASTRA is not overly sensitive to the codebook size within a practical range. Even smaller codebooks can still preserve competitive accuracy, while `K=1024` provides a clean `10`-bit operating point and was therefore chosen in the paper.

| Codebook size `K` | Total bits per token | Compression ratio | ImageNet accuracy of ViT-Base |
|---|---|---|---|
| 256 | [TBD] | [TBD] | [TBD] |
| 512 | [TBD] | [TBD] | [TBD] |
| 1024 | [TBD] | [TBD] | [TBD] |
| 2048 | [TBD] | [TBD] | [TBD] |
