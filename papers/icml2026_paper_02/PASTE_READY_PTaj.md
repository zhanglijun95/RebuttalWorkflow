Thank you for the positive assessment and for recognizing the practical importance of communication-efficient inference under low bandwidth.

**W1:** Novelty mainly lies in the system-level integration of existing ideas.  
**A1:** We think this is a fair reading of the paper, and it is also how we see its main contribution. ASTRA does not claim a fundamentally new Transformer primitive. Its contribution is that sequence parallelism, vector-quantized token exchange, noise-augmented quantization, and distributed class tokens are combined around a concrete deployment bottleneck that existing methods do not address well: multi-device Transformer inference when bandwidth is only `10-100 Mbps`.

What makes this integration meaningful is the regime it enables. The paper shows that ASTRA achieves up to `2.64x` speedup over single-device inference and up to `15.25x` speedup over prior multi-device baselines in the low-bandwidth setting, where those baselines are often slower than simply running on one device. In our view, that shift in the operating region is the main research value of the work.

**W2:** For generative tasks, the current framework primarily benefits prefill rather than full autoregressive inference.  
**A2:** This is correct for the current decoder setting. ASTRA accelerates the prompt-encoding / prefill stage, while autoregressive decoding still proceeds on a single device. We should make that scope boundary more explicit around Table 7.

At the same time, we think the prefill result is still important. Prefill directly affects time-to-first-token, which is a meaningful component of response speed and user experience in interactive settings. The current paper therefore supports a focused but useful claim: ASTRA materially reduces the communication bottleneck in low-bandwidth multi-device prefill, even though it does not yet accelerate the decode phase.

Thank you again for the encouraging review and for recognizing the value of this systems direction. We hope these clarifications further support the case for ASTRA as a meaningful practical contribution.

## V1

Thank you for the positive assessment and for recognizing the practical importance of communication-efficient inference under low bandwidth.

**W1:** Novelty mainly lies in the system-level integration of existing ideas.  
**A1:** We think this is a fair reading of the paper, and it is also how we see its main contribution. ASTRA does not claim a fundamentally new Transformer primitive. Its contribution is that sequence parallelism, vector-quantized token exchange, noise-augmented quantization, and distributed class tokens are combined around a concrete deployment bottleneck that existing methods do not address well, namely multi-device Transformer inference when bandwidth is only `10-100 Mbps`.

What makes this integration meaningful is the regime it enables. The paper shows that ASTRA achieves up to `2.64x` speedup over single-device inference and up to `15.25x` speedup over prior multi-device baselines in the low-bandwidth setting, where those baselines are often slower than simply running on one device. In our view, that shift in the operating region is the main research value of the work.

**W2:** For generative tasks, the current framework primarily benefits prefill rather than full autoregressive inference.  
**A2:** This is correct for the current decoder setting. ASTRA accelerates the prompt-encoding / prefill stage, while autoregressive decoding still proceeds on a single device. We should make that scope boundary more explicit around Table 7.

At the same time, we think the prefill result is still important. Prefill directly affects time-to-first-token, which is a meaningful component of response speed and user experience in interactive settings. The current paper therefore supports a focused but useful claim: ASTRA materially reduces the communication bottleneck in low-bandwidth multi-device prefill, even though it does not yet accelerate the decode phase.

Thank you again for the encouraging review and for recognizing the value of this systems direction. We hope these clarifications further support the case for ASTRA as a meaningful practical contribution.
