# Author Notes

Use this file for strategy, reviewer-specific attitude, and unfinished ideas that should guide drafting but should not automatically be treated as rebuttal facts.

## Paper-level guidance
- Main acceptance case: 我们有三个正分，这很好，所以一定要让这三个人满意，大部分问题都是可以用数据和分析直面回答的，要有礼貌地、坚定地回答他的问题，也要体现我们的价值，尽量取悦他们，但不能堆砌感谢的词汇。
- Main risks: 主要就是第一个审稿人yS5Y的态度很重要，一定不能惹怒他，而是要让他理解我们。
- Tone preference: professional, to-the-point, with evidence/numbers
- Claims to push strongly: 我们和KV cache compression确实在compress了KV这一点上是可比的，但是我们的target完全不一样，它们是memory我们是communication，这也使得已有的KV cache compression方法用在本文的limited-bandwidth的scenarios时并不是strong的baselines。
- Claims to handle cautiously: 我们的方法确实需要训练，因为需要align VQ codebook，不过是训练时长没有那么长，所以我们的方法确实不能说是plug-and-play，我们也没有这么claim；对于generation tasks，我们确实只能加速encoding/prefill阶段，也就是所谓的TTFT，这对于提高response效率、提高用户体验很有帮助，而对于TPOT也就是decoding时间确实没有加速，我们应该让论文的Table 7更明确的指出这是TTFT才对。
- Rebuttal structure：每个审稿人的weaknesses和questions有很多是对应的，应该放在一起回复，比如yS5Y的W3和Q1其实是一个，而不同的审稿人也有很多问题是一样的，比如关于我们只能加速prefill的，这些一样的问题在回答的时候基本逻辑是可以复用的，但是因为不同审稿人可能会有不同的侧重点或附加问题，所以回答的时候一定要注意对这些附加问题进行回复。

## Unfinished / in-progress experiments
- Experiment: 不同的codebook size会怎么样
  - Current status: 用ViT-Base做了更多实验还在跑，目前发现codebook size 256的时候对accuracy影响也不大
  - What you expect / current sense: 即使codebook size比较小的时候我们也有比较好的accuracy，其实论文里选择了1024是因为它是10bits
  - Can it be mentioned now?: yes，可以leave some space来之后填写细节结果，markdown表格也可以准备好
  - Notes:

## Reviewer-specific notes

### Reviewer yS5Y
关于W1，我其实很无奈，我们的结果在NLP task的结果挺好的，PPL没怎么drop，downstream tasks也work，但是确实是在zero-shot的时候有比较大的损失，这主要是因为codebook限制了representation space的多样性，更容易学习到train set的pattern而不好generalize了，这一点Appendix H limitation和future work里我们也提到了，我也不知道怎么回答这个weakness能让人觉得作为future work也没关系，其实这个审稿人也说我们在future work里提及了，但是他非要说一定要在这篇文章里提出mitigation techniques，我觉得他真的很mean。
关于W2/Q3，我也同意KV cache compression是相关的，我们应该在related work里讨论一下它们，但是要注意这些方法是target for save memory for long context的，它们并不能"directly addresses the same communication bottleneck that ASTRA targets"。具体来说，这个审稿人提到的[1,2,3]这三篇相关论文，[1]是achieve 3-bit quantization也就是32/3差不多10倍，[2]是3.5-4.3x倍的kv大小减少，[3]是40%也就是1.6倍的kv大小减少，而我们的方法在group为32的情况下也有至少76倍的压缩率，这意味着在limited bandwidth时，它们的communication time是我们的好几倍，我们可以在related work里加上这些讨论，但是我们认为它们不是我们这个scenario的strong baselines。也许这里也可以加一个表格更清楚？
关于W3/Q1,我们确实需要fine-tune来align codebook，像Appendix D detailed training settings里提到的那样，具体到GPU hours的话，我们是在L40S上fine-tune的，我们可以列一个表，列出ViT-Base, GPT2-S, GPT2-M, Llama-3-8B的时间，并承诺会加到论文中去。
关于W4，我是真不知道怎么回答，“more significant models sizes tested ”当然是很好，但是我们没有时间啊，论文里已经尽量涵盖不同的模型、不同的数据集、也测试了像8B这样的模型等等。
关于W5，3.1的假设是比较宽松，这个我们只能承认，“Some explanation on the sensitivity of this theoretical guarantee when this assumption does not hold”需要你来帮我想想怎么分析，有没有可能分析？
关于Q2，是的我们目前只能加速encoding/prefill，这个我们在section 3.1的最后一段也写了，但是确实我们没有在实验的部分尤其是LLAMA的部分explicitly的写出来，这里我们强调我们是减少了TTFT，对于TPOT没有加速，当然baselines也没有，因此我们在对比latency加速的时候也就是table 7其实是TTFT的speedup，这个我们在revise paper会更正。
关于Q4，我们加了一组在ViT-Base上的实验，我们这里加一个表格，总结当固定其他hyperparameters、不同codebook size下的Total Bits per Token、Compression Ratio、accuracy on ImageNet，类似于Tabel 1，然后根据结果给一些总结。

### Reviewer GzCs
关于W1，我们确实不是"plug-and-play"的方法，我们只是说我们是architecture-agnostic的，我们这里可以像回答yS5Y W3/Q1一样给出具体的fine-tune时间，并表示这个时间不算长。
关于W2，“The gap between theory and practice should be acknowledged.”这个我们肯定是承认的，就像回答yS5Y W5承认这个理论的局限性，分析一下when this assumption does not hold的时候会怎么样，这也确实可能导致在实际使用的时候提升没有那么大，不过还是要说明在CIFAR100上即使是0.86的提升也不是偶然、也不是小数目。
关于W3，基本和回答yS5Y W2是一样的，同意->分析->承认加入revised paper。
关于W4，基本和回答yS5Y Q2是一样的，承认->同意要explicitly地写出来，会改成->分析TTFT的意义，说明baseline也是这样的，所以我们keep fair comparison而且因为generation部分不管多长大家都一样所以就没放进来了
关于W5，我们需要解释theory和practice的联系，我们其实只能承认其实theory只能provide qualitative justification，theory只是我们支撑了我们method这样设计是有意义的，我们想要达成一个目的：比如使得模型不要因为codebook的加入过度overfit到train set上，我们提出：用noise augment这些codebook entries，然后我们证明：这个方案在理想情况下，理论上能帮助达成我们的目的，最后在实际使用中发现empirically是有用的，这些我们会在论文里加以解释。

### Reviewer 3uqF
关于W1/Q1，还是和回答yS5Y Q2一样的，承认->同意要explicitly地写出来，会改成->强调TTFT的意义，虽然dominant cost for long-generation tasks是decoding，但是加速encoding仍然很有意义。-> Q1里还问了"is there a credible path to extending the method to the decode phase"，我觉得我们可以开脑洞回答一下。
关于W2，zero-shot的部分确实只能承认，不过还是要说这主要是因为codebook限制了representation space的多样性，更容易学习到train set的pattern而不好generalize了，这一点limitation和future work里我们也在Appendix H discuss了。然后关于Llama-3-8B downstream tasks，我们在Appendix D Table 10的结果是很好的，在Group在32的时候只比原本LLAMA drop了0.48%-1.67%，consider我们的communication真的压缩了至少51.2倍，我们的结果还是很好的，不过我们不能和审稿人硬着来，还是要委婉一些。
关于W3/Q2，关于具体的networking是怎么设置的，其实就是simulate的，你知道一般simulate bandwidth是怎么做的吗？就是在需要交换数据的时候按设定的bandwidth和应该传输的数据大小来计算communication的时间来等待，其中不包括network stack overhead，这一点对于所有baselines来说都是一样的即all methods shared the same implementation stack，是fair的、也是标准的做法（也许需要引用一些论文来证明这样是模拟式标准的？）；其中包括codebook lookup and dequantization的时间。
关于W4，是关于创新性的，我觉得审稿人也并没有说错，只不过还是要回答一下，证明我们的意义。
关于Q3，类似回答yS5Y W3/Q1一样给出具体的fine-tune时间，并表示这个时间不算长，而这个fine-tune在device count change的时候需要retrain，在bandwidth变了的时候不需要retrain。

## Reviewer PTaj
这是最positive的reviewer，也是最有人味的reviewer，如果可以的话我希望能让他提升到5分，感谢他对于我们的认可，可以给一些简短但有力的认可部分。
关于weakness，他主要提到的两点，一个是novelty，当然他本人也说我们做的system-level integration of existing ideas是fine的，不过我还是觉得可以回复他一下，表示同意的同时给出思考为什么我们觉得我们做的是有意义的，我认为这里的回答不是为了说服谁，而是为了和人沟通我们做研究的理解和想法。
第二个是关于我们只能加速prefill的，还是和回答yS5Y Q2类似，承认当for long generation task的时候decoding才是bottleneck我们的加速可能就不明显了，不过我们再提一下TTFT的意义，对于提高response效率、提高用户体验很有帮助。
也许在最后希望这个审稿人能support我们的工作，我们感谢他的认可和建议。
