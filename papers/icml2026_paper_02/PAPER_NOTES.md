# Paper Notes

## One-paragraph summary

ASTRA targets multi-device Transformer inference in bandwidth-constrained environments, where existing tensor/sequence/block parallel approaches become communication-bound and often fail to outperform single-device inference. The method builds on sequence parallelism and introduces mixed-precision attention, where local tokens remain full precision while non-local tokens are transmitted as low-bit vector-quantized codes. To preserve accuracy under aggressive communication compression, ASTRA adds Noise-Augmented Vector Quantization (NAVQ) and Distributed Class Tokens. Across ViT, GPT2, and Llama-3-8B, the paper reports large low-bandwidth latency gains while largely preserving in-domain task quality, but it also explicitly exposes weaker zero-shot generalization for GPT models and only accelerates the parallel prompt-encoding / prefill stage for decoder-style generation.

## Main claims
- C1: Existing multi-device Transformer inference methods are impractical at realistic low bandwidth because communication dominates runtime.
- C2: ASTRA reduces communication by combining sequence parallelism with mixed-precision attention and vector-quantized transmission of non-local token embeddings.
- C3: NAVQ and Distributed Class Tokens improve robustness / accuracy under aggressive compression.
- C4: ASTRA achieves substantial end-to-end latency speedups in low-bandwidth settings while maintaining reasonably strong task performance across vision and language models.
- C5: ASTRA remains compatible with weight quantization and shows robustness under heterogeneous devices and non-ideal network conditions.

## Key evidence already in the paper
- E1: Figure 1 / Figure 3 / Table 4 show large latency gains over TP, SP, and BP under 10-100 Mbps, where baseline communication dominates runtime.
- E2: Table 1 shows ViT-Base accuracy remains close to the original model under 76.8-2457.6× communication compression.
- E3: Table 3 shows GPT2 in-domain PPL remains competitive under compression, but zero-shot PPL degrades more strongly.
- E4: Table 6 / Table 7 / Table 10 / Table 11 show ASTRA scales to Llama-3-8B, preserves downstream task quality reasonably well, and remains robust under packet loss / dynamic bandwidth.
- E5: Theorem 3.1, Theorem 3.2, Table 12, and Table 13 provide theory plus ablations for NAVQ and Distributed Class Tokens.

## Important quantitative results
- Figure 1 / Table 4:
  - What it shows: low-bandwidth latency speedup against multi-device baselines on 4 devices, 1024 tokens
  - Exact numbers: ASTRA reaches 1.27-2.74× speedup at 20 Mbps while all baselines are below single-device; speedup over SP is up to 171.82× and over BP+AG(Nb=1) up to 15.25×.
- Table 1:
  - What it shows: ViT-Base accuracy under communication compression
  - Exact numbers: original ViT-Base is 92.53 / 80.32 on CIFAR-100 / ImageNet; ASTRA G=32 reaches 91.64 / 80.28 at 76.8× compression; ASTRA G=1 reaches 88.95 / 77.39 at 2457.6× compression.
- Table 3:
  - What it shows: GPT2 PPL and compression ratios
  - Exact numbers: GPT2-M on Wikitext-103 increases from 14.8 to 16.84 at G=32 with 102.4× compression; GPT2-M zero-shot PPL rises from 43.22 to 62.29; GPT2-S zero-shot rises from 58.91 to 76.24 at G=32.
- Table 5:
  - What it shows: compatibility with 8-bit / 4-bit quantization
  - Exact numbers: ASTRA G=32 + 8-bit reaches 80.26 ImageNet accuracy with 1.35× speedup over 8-bit single-device ViT-Base; ASTRA G=32 + 4-bit reaches 79.78 with 1.81× speedup.
- Table 6:
  - What it shows: Llama-3-8B perplexity and communication compression
  - Exact numbers: original PPL 5.8118; ASTRA G=32 PPL 7.4360 at 51.2× compression; ASTRA G=1 PPL 7.7336 at 1638.4× compression.
- Table 7:
  - What it shows: Llama-3-8B latency under different bandwidths
  - Exact numbers: single-device Llama-3-8B latency is 4.578s; ASTRA G=1 is 1.563s at 10 Mbps and 1.540s at 500 Mbps; BP Nb=4 is 4.642s at 10 Mbps and 1.485s at 500 Mbps.
- Table 10:
  - What it shows: Llama-3-8B downstream-task accuracy
  - Exact numbers: original 0.7615 / 0.8426 / 0.8374 / 0.7970 on CoLA / SST2 / AG News / QQP; ASTRA G=32 gives 0.7539 / 0.8314 / 0.8325 / 0.7803.
- Table 11:
  - What it shows: robustness under 5% packet loss
  - Exact numbers: Llama-3-8B ASTRA G=32 changes from 7.4360 PPL to 7.4431 under 5% packet loss.
- Table 12:
  - What it shows: impact of NAVQ noise magnitude
  - Exact numbers: validation accuracy improves from 89.91 at λ=0.0 to 90.77 at λ=1.0, while train/val gap drops from 10.07 to 9.21.
- Table 13:
  - What it shows: distributed vs single class token
  - Exact numbers: gains range from 0.37% to 7.13% depending on groups and commitment weight.
- Table 14:
  - What it shows: commitment-loss sensitivity
  - Exact numbers: best settings outperform β=0 and β=0.25; for G=32, best is 91.64 vs 91.42 at β=0 and 89.97 at β=0.25.

## Baselines / comparisons already covered

- Original model on a single device
- Tensor Parallelism (TP)
- Sequence Parallelism (SP)
- Block Parallelism (BP), including BP+AllGather and BP+SequenceParallel with different Nb
- 8-bit quantized variants for Llama-3-8B latency comparison

Not currently covered in the paper:

- KV-cache compression methods as explicit baselines
- stronger learned / training-based communication-compression baselines beyond the ASTRA design itself

## Limitations we can acknowledge safely

- Decoder-style generation only accelerates the parallel prompt-encoding / prefill stage; autoregressive decoding proceeds on a single device.
- Zero-shot generalization degrades more strongly than in-domain evaluation for GPT models.
- ASTRA is not training-free; it requires fine-tuning with VQ modules.
- Theorem 3.1 uses Gaussian/Wasserstein analysis and Appendix B adds an independent-identically-distributed quantization-error assumption for analytical clarity.
- The theory supports the design qualitatively; it does not tightly quantify the full practical gain.
- The paper does not report wall-clock fine-tuning time or GPU-hours.
- The paper currently omits discussion / comparison of KV-cache compression literature.

## Review-sensitive facts
- novelty anchors:
  - the claimed novelty is system-level integration for low-bandwidth multi-device inference, not a brand-new Transformer primitive
  - the paper already combines known ingredients: sequence parallelism, VQ, noise regularization, distributed class tokens
  - the value claim is that this combination materially lowers the bandwidth needed for useful multi-device speedup
- theoretical assumptions:
  - Theorem 3.1 relies on Gaussian distribution analysis
  - Appendix B explicitly states that, for analytical clarity, quantization errors are assumed independent and identically distributed across dimensions: ε_k i.i.d. ~ N(0, σ^2)
  - Theorem 3.2 provides a 1/N expected error reduction for distributed class tokens
- runtime / complexity:
  - environment: PyTorch 2.5, training on a single L40S GPU (40GB)
  - deployment: simulated distributed inference on personal laptops with NVIDIA 1660Ti GPUs
  - network conditions are emulated via bandwidth caps
  - main latency results use 4 devices and 1024 input tokens unless stated otherwise
- ablations:
  - noise magnitude λ in {0.0, 0.1, 0.3, 1.0}
  - commitment loss weights β in {0.0001, 0.0002, 0.0005}; controls in Appendix F include β=0 and β=0.25
  - grouped VQ uses G in {1, 16, 32}
- dataset / setup details:
  - vision: CIFAR-100, ImageNet-1K
  - NLP: English Wikipedia and Wikitext-103
  - zero-shot setting = train on Wikipedia, evaluate directly on Wikitext-103 validation
  - decoder setting in Section 3.1: after parallel encoding, autoregressive decoding proceeds on a single device
  - Appendix D: pre-trained weights come from HuggingFace; ViT is fine-tuned for 32 epochs on CIFAR-100 and 4 epochs on ImageNet-1K; NLP models are fine-tuned for 1 epoch on 1M Wikipedia samples and the full Wikitext-103 dataset
