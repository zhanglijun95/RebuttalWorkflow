# Raw Reviews

## Reviewer yS5Y
Summary:
This paper proposes combining sequence parallelism with mixed-precision attention (local tokens processed with full
prevision and non-local tokens utilize low-bit vector-quantization codes). Additional techniques are introduced (1)
Noise-augmented vector quantization injects Gaussian noise to improve generalization and (2) Distributed class
tokens are used to replicate class tokens across devices to improve attention estimation error. Evaluations performed
with ViT/GPT2 and scale to Llama-3-8B with reported 2.64 speedup on single-device inference and 15.25 on multidevices with low bandwidth such as 10 Mbps.
Strengths And Weaknesses:
Strengths:
Sound motivation, assuming high-bandwidth interconnects cannot be assumed for most real-world settings
(besides corporate data-centers). This focus on sub-100 Mbps bandwidths is a practical problem.
Mixed-precision use case is also well-motivated. Local attention at full precision while compressing only crossdevice communication makes sense for sequence parallelism and seems to yield significant compression ratios of
up to 2,500 .
Thorough evaluations across bandwidth, device count, token lengths, model scale, PTQ, and non-ideal network
conditions. Introducing the Llama-3-8B experiments also help address scalability. Even more ablation studies
throughout the Appendix are informative (especially the analyses of noise magnitude and commitment loss
weight).
Weaknesses:
My main concern is the accuracy degradation in generative / zero-shot settings. Both GPT2-S and GPT2-M show
significant perplexity increases on Wikitext. This is a significant limitation in a scenario where the primary use
case is generation. Authors acknowledge this but do not offer any concrete mitigation techniques besides future
work suggestion.
There is a lack of comparisons to KV cache compression literature which similarly addresses communication and
memory cost of attention [1, 2, 3]. [2] in particular targets network transmission cost of KV caches, which makes it
a direct relevant comparison given ASTRA's focus on bandwidth-constrained settings. These approaches are
complementary to ASTRA and could potentially be combined with it, but the paper neither discusses nor
compares against them. This is a significant omission given that KV cache compression directly addresses the
same communication bottleneck that ASTRA targets.
Much of the training cost information is underspecified even though ASTRA requires fine-tuning the model with
VQ modules and noise augmentations. This unclear configuration is a significant issue. (See Questions section for
exact questions).
Claiming applicability to generative tasks needs more backing than just GPT2-S and GPT2-M (which are small by
modern standards). Llama-3-8B only covers perplexity on Wikipedia and classification benchmarks. I would like to
see more significant models sizes tested in order to prove the claim of applicability to generative tasks.
Theorem 3.1 is quite restrictive. Assuming that Gaussian quantization errors across dimensions are IID is very
unlikely to hold in practice as different dimensions within Transformer embeddings carry much different
information. [4] (which was cited in the paper but not explained in this context) actually demonstrate significant
heterogeneity across dimensions. Some explanation on the sensitivity of this theoretical guarantee when this
assumption does not hold is needed.
References:
[1] Coleman, et al. "Kvquant: Towards 10 million context length llm inference with kv cache quantization." NeurIPS,
2024
[2] Liu et al., "CacheGen: KV cache compression and streaming for fast large language model serving". ACM SIGCOMM,
2024
[3] Saxena et al. "Eigen attention: Attention in low-rank space for kv cache compression." EMNLP, 2024
[4] Michel et al., "Are sixteen heads really better than one?" NeurIPS, 2019
[5] Zhong et al., "DistServe: Disaggregating prefill and decoding for goodput-optimized large language model
serving." USENIX OSDI, 2024
Soundness: 2: fair
Presentation: 3: good
Significance: 2: fair
Originality: 2: fair
Key Questions For Authors:
Questions
1. Related to training. How much additional compute is required to finetune ASTRA variants compared to the
original model? For Llama-3-8B what is wall-clock training time and GPU-hours?
2. In Section 3.1 it states that autoregressive decoding is performed on a single device after parallel encoding.
Meaning ASTRA only accelerates prefill phase for generative models (unlike decode phase which often dominates
latency at larger output [5]). What is the fraction of total generation latency (prefill + decoding over many tokens)
ASTRA actually reduces in a realistic generation scenario?
3. Recent work on KV cache compression also reduces memory and communication cost of attention. How does
ASTRA relate to or complement these approaches? A comparison would strengthen your position.
4. Codebook size is fixed to 1024. How sensitive are accuracy and latency w.r.t ? Is there some meaningful
accuracy-communication tradeoff?
Limitations:
Yes
Overall Recommendation: 3: Weak reject: A paper with clear merits, but also some weaknesses, which overall
outweigh the merits. Papers in this category require revisions before they can be meaningfully built upon by others.
Please use sparingly.
Confidence: 3: You are fairly confident in your assessment. It is possible that you did not understand some parts of
the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully
checked.


## Reviewer GzCs
Summary:
This paper proposes ASTRA, a framework for multi-device Transformer inference that targets bandwidth-constrained
environments (e.g., Wi-Fi, edge networks). The core observation is that existing multi-device parallelism strategies
(tensor, sequence, block parallelism) are bottlenecked by inter-device communication at realistic bandwidths (≤100
Mbps). ASTRA builds on sequence parallelism but replaces full-precision embedding exchanges with vector-quantized
(VQ) indices, achieving massive compression ratios (up to ~2500×). To recover accuracy lost from this aggressive
quantization, the paper introduces two techniques: (1) Noise-Augmented Vector Quantization (NAVQ), which injects
Gaussian noise sampled from the quantization residual distribution during training to improve generalization, and (2)
Distributed Class Tokens, which replicate the CLS token across devices so each attends to its local tokens at full
precision, then pools the results. Experiments span ViT-Base, GPT2-S/M, and Llama-3-8B across vision and language
tasks, demonstrating speedups at low bandwidths where all baselines fail to beat single-device inference. Theoretical
results justify NAVQ via Wasserstein distance arguments and distributed CLS tokens via variance reduction.
Strengths And Weaknesses:
Strengths
1 - The paper clearly identifies and quantifies a real bottleneck: at realistic Wi-Fi bandwidths, communication
dominates multi-device inference latency (58–93% of runtime). The latency breakdown in Figure 3 is compelling and
makes the case sharply.
2 - Achieving ~2500× compression on communication with only ~3.5% accuracy drop on CIFAR-100 / ImageNet is a
strong result.
3 - The paper evaluates across multiple axes: bandwidth, device count, sequence length, model scale (up to Llama-3-
8B), heterogeneous devices, non-ideal networks (packet loss, dynamic bandwidth), and compatibility with posttraining quantization. This breadth is appreciated and goes beyond what many systems papers provide.
Weaknesses
1 - ASTRA requires jointly training VQ codebooks and fine-tuning the Transformer. For ViT-Base on ImageNet, this is
feasible, but for Llama-3-8B, the paper fine-tunes on 1M Wikipedia samples with 8-bit quantization. This is a nontrivial requirement that undermines the "plug-and-play" narrative for large models. The baselines (TP, SP, BP) are
training-free; this asymmetry should be discussed more prominently.
2 - The noise injection idea is sensible and well-motivated via VRM, but the empirical gain is 0.86% accuracy on CIFAR100 (Table 12). This is a small delta for what the paper frames as a key contribution. Additionally, the theoretical result
(Theorem 3.1) assumes Gaussian distributions for both the original embeddings and quantization residuals, and the
proof assumes i.i.d. isotropic errors across dimensions (Appendix B). Real token embeddings are not Gaussian, and
quantization errors are typically heteroscedastic across dimensions. The gap between theory and practice should be
acknowledged.
3 - There is a growing literature on compressing KV caches for long-context inference (e.g., quantized KV caches,
token eviction/merging). While these target a different bottleneck (memory), the conceptual overlap with
compressing token representations for transmission is strong. The related work should discuss this connection and
ideally compare against approaches that quantize KV caches to low bits.
4 - For decoder models (GPT2, Llama), ASTRA only parallelizes the prefill/encoding phase. Autoregressive decoding
proceeds on a single device. For many LLM use cases, decoding latency dominates (especially for long generations).
The paper should quantify what fraction of end-to-end generation latency ASTRA actually reduces, not just report
encoding speedup. As stated, the Llama-3-8B latency numbers (Table 7) appear to be encoding (only for 1024 tokens).
This should be made explicit.
5 - A presentation/soundness concern is that, in the main text, the theorems are plausible and aligned with the
intuition of the method, but the review would benefit from clearer exposition of assumptions and how tightly the
theory maps to the practical training/inference pipeline. For example, the paper states theorems for noiseaugmented embeddings and distributed class tokens, but the main text does not make it obvious whether these
results explain the observed gains quantitatively or mainly provide qualitative justification.
Soundness: 2: fair
Presentation: 3: good
Significance: 3: good
Originality: 2: fair
Key Questions For Authors:
Please refer to the weaknesses mentioned above.
Limitations:
Yes.
Overall Recommendation: 4: Weak accept: Technically solid paper that advances at least one sub-area of AI, with a
contribution that others are likely to build on, but with some weaknesses that limit its impact (e.g., limited evaluation).
Please use sparingly.
Confidence: 3: You are fairly confident in your assessment. It is possible that you did not understand some parts of
the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully
checked

## Reviewer 3uqF
Summary:
The paper addresses the problem on how to make multi-device Transformer inference practical when inter-device
bandwidth is limited. The paper argues that existing distributed inference methods for Transformers are often
communication-bound in low-bandwidth settings, and proposes ASTRA, a framework built on sequence parallelism
with mixed-precision attention, where local tokens are kept in full precision while non-local tokens are communicated
through vector-quantized representations. The paper's main contribution is the combination of this communicationefficient attention scheme with two accuracy-preserving components, Noise-Augmented Vector Quantization and
Distributed Class Tokens. Experiments on ViT, GPT2, and Llama-3-8B suggest that ASTRA can substantially reduce
communication cost and improve end-to-end latency over prior multi-device baselines in bandwidth-constrained
settings, while maintaining reasonably strong task performance in most in-domain evaluations.
Strengths And Weaknesses:
Strengths
multi-device methods can become communication-bound under realistic bandwidth constraints: the paper
makes this bottleneck central. Motivation is clear and relevant.
the design choices make sense: Mixed-Precision Attention, Noise-Augmented Vector Quantization, and
Distributed Class Tokens have the goal of reducing communication while preserving accuracy.
empirical evaluation is broad: results span vision and language models (ViT, GPT2, Llama-3-8B), multiple datasets,
varying bandwidth/device count/token length, non-ideal network conditions, and compatibility with weight
quantization. the non-ideal network experiments (Table 11) are a nice differentiator relative to prior work.
latency results are interesting in the low-bandwidth regime. ASTRA consistently outperforms TP, SP, and BP
variants, and the latency breakdown in Figure 3 directly supports the communication-dominance claim.
Weaknesses
Section 3.1 states that after parallel prompt encoding, decoding proceeds sequentially on a single device. This
means ASTRA only accelerates prefill, which is often not the dominant cost for long-generation tasks. This is a
significant limitation for the paper's LLM claims, and the latency numbers in Table 7 should explicitly state they
measure prefill only.
GPT2-M zero-shot PPL rises from 43.22 to 62.29 (~44% increase) even at G=32, and some Llama-3-8B downstream
tasks show noticeable drops. No mitigation is attempted or discussed, weakening the claim that aggressive
compression broadly preserves model quality.
It is not very clear how bandwidth caps are enforced, whether network stack overhead is included, and whether
codebook lookup and dequantization are accounted for.
the originality of the paper is primarily at the "integration level": sequence parallelism, vector quantization, noise
regularization, and replicated class tokens are individually known. The contribution lies in their combination and
deployment framing rather than a fundamentally new inference primitive.
Soundness: 3: good
Presentation: 3: good
Significance: 4: excellent
Originality: 3: good
Key Questions For Authors:
1. Sec. 3.1 states that decoding proceeds sequentially on a single device after prefill. Do the latency numbers in
Table 7 measure prefill only? What fraction of total inference time does ASTRA actually accelerate for typical
prompt/generation ratios, and is there a credible path to extending the method to the decode phase?
2. could you clarify the exact deployment and networking setup used for latency measurements (e.g.,
communication backend, bandwidth throttling mechanism, whether all methods shared the same
implementation stack)?
3. what is the end-to-end adaptation cost of ASTRA, including codebook initialization and fine-tuning time?
Specifically, is any retraining needed when changing device count or bandwidth regime?
Limitations:
yes
Overall Recommendation: 4: Weak accept: Technically solid paper that advances at least one sub-area of AI, with a
contribution that others are likely to build on, but with some weaknesses that limit its impact (e.g., limited evaluation).
Please use sparingly.
Confidence: 2: You are willing to defend your assessment, but it is quite likely that you did not understand the
central parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were
not carefully checked.

## Reviewer PTaj
Summary:
ASTRA is a communication-efficient framework designed to enable high-performance Transformer inference in
bandwidth-constrained environments as low as 10 Mbps. Its primary novelty lies in the integration of sequence
parallelism with mixed-precision attention, where non-local token embeddings are compressed into low-bit vectorquantized codes while local computations remain in full precision. To mitigate the accuracy loss typically associated
with such aggressive compression, ASTRA introduces Noise-Augmented Quantization and Distributed Class Tokens,
ensuring architectural robustness across vision (ViT) and language (Llama-3-8B) models. The impact is a
transformative speedup achieving up to 2.64× over single-device inference and 15.25× over existing multi-device
baselines, effectively removing distributed AI performance from the need for high-speed inter-device interconnects.
Strengths And Weaknesses:
Strengths
The work addresses a real challenge in distributed inference for the Transformer model communication overhead
across devices, which becomes critical in bandwidth-constrained environments. Targeting this bottleneck is highly
relevant for edge and multi-device deployments.
The proposed mixed-precision attention mechanism combined with vector-quantized token exchange, significantly
reduces communication cost. By transmitting only low-bit indices instead of full embeddings, the framework provides
a practical method for reducing bandwidth requirements while preserving global attention. Further, the introduction
of Noise-Augmented Vector Quantization (NAVQ) helps mitigate quantization error and improve generalization.
The paper provides theoretical arguments (e.g., Wasserstein distance analysis and variance reduction) supporting the
proposed mechanisms, along with empirical validation through ablations.
Choice of datasets and baselines seems ok.
The results show that ASTRA performs significantly better than baselines, especially when the bandwidth is low. This
is a very important result.
Writing is good.
Lots of additional experiments, including scalability, quantization, and bandwidth-based results.
Weaknesses
Several core components build on existing ideas such as Vector quantization for communication compression, mixedprecision computation, noise-based regularization, token replication for distributed aggregation. While their
combination is useful, the individual techniques are largely adaptations of known strategies rather than
fundamentally new algorithm. The novelty mainly lies in the system-level integration of existing ideas, which is fine.
For generative tasks, the framework still performs sequential decoding on a single device, meaning the
communication-efficient design primarily benefits the encoding stage and may not significantly accelerate full
autoregressive inference.
Soundness: 3: good
Presentation: 3: good
Significance: 4: excellent
Originality: 3: good
Key Questions For Authors:
NA
Limitations:
Impact statements and limitations are present in the appendix, which is great.
Overall Recommendation: 4: Weak accept: Technically solid paper that advances at least one sub-area of AI, with a
contribution that others are likely to build on, but with some weaknesses that limit its impact (e.g., limited evaluation).
Please use sparingly.
Confidence: 4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible,
that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related
work.