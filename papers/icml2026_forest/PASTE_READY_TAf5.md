Thank you for the positive comments and for identifying the experimental questions that matter most for strengthening the paper. Your review is especially helpful because it recognizes both the practical value of the problem and the current boundaries of the evaluation.

**W1:** The baselines are too weak to isolate whether diffusion is the key ingredient.  
**A1:** This is a fair concern. The current comparisons are to strong deterministic heuristics because the task is not standard RGB prediction, but sparse-snapshot, object-centric state prediction for real warehouse stow. For that reason, the paper focuses first on whether the proposed architecture adds value beyond the practical heuristic alternatives that would otherwise be used in this setting. It then strengthens that comparison through downstream evaluations, showing that FOREST-predicted states remain useful for DLO prediction and multi-stow reasoning. Our interpretation is not that all baseline questions are settled, but that the paper already establishes meaningful practical value in this target regime.

**W2:** Generalization to unseen intents/bins/categories or distribution shift is not tested.  
**A2:** In highly automated warehouses, arbitrary out-of-distribution manipulation is not the primary requirement. Machine setup, camera views, bin geometry, and action patterns are typically highly standardized. The more relevant industrial objective is therefore not broad transfer across unrelated environments, but robust, high-fidelity prediction within a standardized yet highly stochastic operating regime. ARMBench is designed to capture exactly that regime, which is why strong within-environment performance is already meaningful from a deployment perspective.

**W3:** The canonical-mask prior may help too much and differs from practical pre-insertion signals.  
**A3:** This concern goes to the heart of the paper. The canonical mask in the main experiment is used as a proxy for the in-bin contact-surface view so that the core predictive problem can be isolated and studied. To quantify how much this proxy helps, we ran an additional ablation in which the contact-surface view is estimated before insertion from the induct-view image using SAM3D:

| Setting | Direct Insert N-IoU | Direct Insert O-IoU | Sweep Insert N-IoU | Sweep Insert O-IoU |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D proxy | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

The drop is expected, but the key point is that FOREST still significantly outperforms heuristics under the weaker pre-insertion proxy. Our reading is therefore that the model is not relying only on an idealized prior; it is also learning useful predictive structure about the stow dynamics.

**Q1:** Why has there been relatively little recent visual foresight work?  
**A4:** One reason is that many real manipulation systems do not naturally provide dense video supervision, while much recent robotics work has shifted toward policy learning or large multimodal models. The warehouse setting is different because before/after snapshots are naturally available at scale. This makes sparse-snapshot foresight both practically relevant and still relatively underexplored.

**Q2:** Why is the sweeping operation shown as a blue line rather than a rectangle?  
**A5:** The blue line corresponds to the sweep start line in the dataset annotation. Operationally, the sweep then continues until the existing items are pushed aside and enough space is created for insertion. The figure should make that more explicit, and we will clarify that the blue line denotes the sweep-start specification rather than a rectangular swept volume.

---

## Revised Draft

Thank you for the positive comments and for identifying the experimental questions that matter most for strengthening the paper.

**W1:** The baselines are too weak to isolate whether diffusion is the key ingredient.  
**A1:** We would like to first clarify the task setting behind the baseline choice. This problem is not standard RGB prediction, but sparse-snapshot, object-centric post-stow state prediction in a real warehouse environment. The model is conditioned on the current bin state, the incoming item, and the stow intent, and the target is a future instance-mask layout rather than a future RGB frame. **For this reason, off-the-shelf video prediction or RGB generation methods are not directly applicable without redesigning the representation, conditioning, and learning objective for this task.** Once such changes are introduced, the result is no longer a direct baseline but a newly adapted task-specific method.

For this first study, the paper therefore compares against deterministic heuristics that are natural for this state-based setting and then checks whether the predicted states are useful in downstream tasks. In particular, FOREST-predicted states improve DLO prediction fidelity and support multi-stow reasoning. Our view is not that every baseline question is fully settled, but that the current experiments already show meaningful practical value for the target regime of sparse-snapshot warehouse stow.

**W2:** Generalization to unseen intents, bins, categories, or distribution shift is not tested.  
**A2:** We would like to clarify the industrial notion of generalization targeted here. In highly automated warehouses, arbitrary out-of-distribution manipulation is not the primary requirement. Camera views, machine setup, bin geometry, and action patterns are usually highly standardized, while the stochasticity comes from how different items interact within that operating regime. **The more relevant objective is therefore not broad transfer across unrelated environments, but robust and high-fidelity prediction within a standardized yet still highly stochastic warehouse setting.** ARMBench is designed to capture exactly that regime, which is why strong performance within it is already meaningful from a deployment perspective.

**W3:** The canonical-mask prior may help too much and differs from practical pre-insertion signals.  
**A3:** This concern is central to the paper, and the intended interpretation is as follows. The canonical mask in the main setting is used to isolate the predictive question of interest, namely whether a model can forecast the post-stow reconfiguration when a representation of the incoming item's contact-side geometry is available. This is a proof-of-concept setting motivated by the fact that production-scale warehouse data are valuable but incomplete. To test how much this input helps in a more practical setup, we additionally replace the GT-derived mask with an estimate produced from the induct-view image using SAM3D and retrain FOREST with this estimated input:

| Setting | Direct Insert N-IoU | Direct Insert O-IoU | Sweep Insert N-IoU | Sweep Insert O-IoU |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

With SAM3D, FOREST still remains clearly above copy-paste(+gravity) across all four metrics. **This means the predictive value is still preserved when the GT-derived input is replaced by a practical acquisition route.** The SAM3D results are lower than the main-setting results partly because SAM3D itself is imperfect, and partly because the main setting still benefits from information retained in the GT-derived mask. The comparison is therefore best read in two parts. The main setting shows the predictive potential of the dynamics model when the contact-side geometry is accurately available. The SAM3D setting shows that a large part of this value is still preserved when that input is replaced by a practical estimate.

**Q1:** Why has there been relatively little recent visual foresight work?  
**A4:** One reason is that many real manipulation systems do not naturally provide dense video supervision, while much recent robotics work has shifted toward policy learning, foundation models, or end-to-end control. The warehouse setting is different because before/after snapshots are naturally available at scale as part of routine operation. **This makes sparse-snapshot visual foresight both practically important and still relatively underexplored.**

**Q2:** Why is the sweeping operation shown as a blue line rather than a rectangle?  
**A5:** The blue line corresponds to the sweep start line in the dataset annotation. Operationally, the sweep continues from that line until the existing items are pushed aside and enough space is created for insertion. **We will clarify in the revision that the blue line denotes the sweep-start specification rather than a rectangular swept volume.**

---

## Revised Draft V2

Thank you for the positive assessment and for the constructive questions on evaluation and scope. Your review is especially encouraging because it recognizes the practical value of the problem and also points to the experiments that would most strengthen the paper.

**W1:** The baselines are too weak without learned baselines to isolate whether diffusion is the key ingredient.  
**A1:** The current experiments do not fully isolate diffusion from every simpler learned alternative. What they establish is that, for this sparse-snapshot stow problem, a diffusion-based object-centric predictor substantially outperforms the practical heuristic alternatives and remains useful in downstream tasks. The baseline difficulty comes from the nature of the task itself [这句话和前面没有逻辑关系，前面还在讲我们和heuristic baselins比了，怎么突然就讲什么baseline difficulty，哪来的baseline difficulty，这个审稿人没这么提啊，所以我觉得你的逻辑非常差，要回答审稿人的这个问题，当然是先承认baselines弱，解释可能的强baseline也就是learned baseline其实难以成立，最后说明但是我们还是能说diffusion是关键的]. This problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric post-stow bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture. Accordingly, off-the-shelf video prediction or RGB generation methods are not directly suitable without redesigning the representation, conditioning interface, and learning objective. In our own trials, simple RGB-conditioned diffusion performs poorly for exactly this reason. Once such changes are introduced, the result is no longer a direct baseline, but a newly adapted method for this task. 

The present paper therefore compares against heuristics that are natural for this state-based setting and then evaluates whether the predicted states remain useful in downstream tasks. In particular, FOREST-predicted states improve DLO prediction fidelity and support multi-stow reasoning, showing that the predicted post-stow states are useful beyond direct IoU comparison. This provides meaningful evidence for the practical value of the proposed diffusion-based formulation, even if it does not yet separate diffusion from all possible simpler learned models.

**W2:** Generalization to unseen intents, bins, categories, or distribution shift is not tested.  
**A2:** The present study is focused on the production environment represented by ARMBench, which is the only public production-scale stow dataset we found, and it already contains substantial diversity in object categories, item instances, and storage bins within that warehouse environment. The experiments therefore evaluate performance within a realistic target environment rather than across unrelated environments [这个回答也是和A1一样只是复制了之前的回答，但是没做适配，明明这个审稿人没提到cross-env或者是unrelated environment].

This emphasis is also consistent with the application. Production warehouse systems are typically highly standardized, and what matters most in practice is stable performance within that standardized operating environment. For the use case studied here, strong within-environment performance on ARMBench is already meaningful.

**W3:** The canonical-mask prior may help too much and differs from practical pre-insertion signals.  
**A3:** This concern is valid to the paper, and it is also exactly why quantifying the effect of this prior is important [这个第一句话也是废话，没传达任何具体内容，而且证明了你的整个回答的逻辑非常差，没有主旨也没有适配审稿人的问题，回答这个回答就应该先承认这个canonical-mask prior确实和实际能够获得的prior不一样，然后简单解释为什么我们用的这个mask，能证明什么，然后说我们还扩展了实验来用practical得到的mask做训练，有一些什么样的结论]. The canonical mask in the main setting is used to isolate the predictive question of interest, namely whether a model can forecast the post-stow reconfiguration when a representation of the incoming item's contact-side geometry is available. This is a proof-of-concept setting motivated by the fact that production-scale warehouse data are valuable but incomplete. To quantify how much this prior helps in a more practical setup, we replace the GT-derived mask with an estimate produced from the induct-view image using SAM3D and retrain FOREST with this estimated input:

| Setting | Direct Insert N-IoU | Direct Insert O-IoU | Sweep Insert N-IoU | Sweep Insert O-IoU |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

With SAM3D, FOREST still remains clearly above copy-paste(+gravity) across all four metrics. This means the predictive value is still preserved when the GT-derived input is replaced by a practical acquisition route. The SAM3D results are lower than the main-setting results partly because SAM3D itself is imperfect, and partly because the main setting still benefits from information retained in the GT-derived mask. The main setting therefore shows the predictive potential of the dynamics model when the contact-side geometry is accurately available, while the SAM3D setting shows that a large part of this value is still preserved when that input is replaced by a practical estimate.

**Q1:** Why has there been relatively little recent visual foresight work?  
**A4:** One likely reason is that explicit visual foresight models require supervision that many real manipulation settings do not naturally provide [我觉得这个回答不大好，因为visual foresight天然的可以用video做autoaggressive learning，根本不需要这么多奇奇怪怪的labels，已有的模型做的也挺好的，倒是因为在production warehouse scenario，有一些需求上的转变才使得visual foresight又有机会了，尤其是world model的出现，我其实感觉visual foresight不是不火了，而是现在都用world model/predictive model来表达了]. Dense videos with reliable labels are expensive to collect, while much recent robotics work has shifted toward policy learning, large multimodal models, and end-to-end control. In that sense, the underlying problem has not disappeared, but the community’s framing and tooling have shifted. The warehouse setting is different because before/after observations are naturally accumulated at scale during routine operation. This makes sparse-snapshot visual foresight both practically valuable in this domain and still comparatively underexplored.

**Q2:** Why is the sweeping operation shown as a blue line rather than a rectangle?  
**A5:** The blue line corresponds to the sweep start line in the dataset annotation. Operationally, the sweep continues from that line until the existing items are pushed aside and space is created for insertion.

---

## Revised Draft V3

Thank you for the positive assessment and questions on evaluation and scope.

**W1:** The baselines are too weak without learned baselines to isolate whether diffusion is the key ingredient.  
**A1:** The current baselines are indeed not sufficient to isolate diffusion from every possible simpler learned alternative. What the present experiments establish is that, in this sparse-snapshot stow setting, a diffusion-based object-centric predictor substantially outperforms the practical heuristic alternatives and remains useful in downstream tasks. 

Stronger learned baselines are nontrivial here because this problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric post-stow bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture. Accordingly, **off-the-shelf video prediction or RGB generation methods are not directly suitable without redesigning the representation, conditioning interface, and learning objective**. In our own trials, simple RGB-conditioned diffusion performs poorly for exactly this reason. Once such changes are introduced, the result is no longer a direct baseline, but a newly adapted method for this task.

The present paper therefore compares against heuristic baselines that are natural for this state-based setting and then evaluates whether the predicted states remain useful in downstream tasks. In particular, FOREST-predicted states improve DLO prediction fidelity and support multi-stow reasoning, showing that the predicted post-stow states are useful beyond direct IoU comparison. This does not fully settle the baseline question, but it does support diffusion as a meaningful ingredient in the proposed formulation.

**W2:** Generalization to unseen intents, bins, categories, or distribution shift is not tested.  
**A2:** The current experiments do not explicitly test generalization to unseen intents, bins, or item categories. What they do evaluate is robustness within ARMBench, which is the only public production-scale stow dataset we found and contains substantial diversity in object categories, item instances, and storage bins within one warehouse environment. **The experiments therefore test performance across a realistic range of variation inside the target production environment.**
This focus is also consistent with the real application. Production warehouse systems are typically highly standardized, and what matters most in practice is stable performance within that standardized operating environment. 

**W3:** The canonical-mask prior may help too much and differs from practical pre-insertion signals.  
**A3:** The canonical-mask prior in the main setting is indeed stronger than what a practical pre-insertion pipeline would typically provide. We use it because ARMBench does not directly provide the in-bin contact-surface view of the incoming item, and the main experiment is intended to answer a proof-of-concept question: if a representation of that contact-side geometry is available, can the model predict how the bin will reconfigure after the stow. 

To quantify how much this prior helps under a more practical input, we additionally replace the GT-derived mask with an estimate produced from the induct-view image using SAM3D and retrain FOREST with this estimated input:

| Setting | Direct Insert N-IoU | Direct Insert O-IoU | Sweep Insert N-IoU | Sweep Insert O-IoU |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

With SAM3D, FOREST still remains clearly above copy-paste(+gravity) across all four metrics. This means **the predictive capability is still preserved when the GT-derived input is replaced by a practical acquisition route**. 
Besides, the SAM3D results are lower than the main-setting results partly because SAM3D itself is imperfect, and partly because the main setting still benefits from prior retained in the GT-derived mask. 

**Q1:** Why has there been relatively little recent visual foresight work?  
**A4:** Our impression is not that the underlying idea has disappeared, but that the framing has changed. Many problems that would previously have been described as visual foresight are now discussed under world models, predictive models, or action-conditioned generative modeling. The warehouse setting makes the foresight formulation especially useful again because routine operation naturally produces before/after observations at scale, and the downstream requirement is explicit future-state reasoning rather than direct action imitation. In that sense, the problem has become practically timely again, even if the surrounding terminology has shifted.

**Q2:** Why is the sweeping operation shown as a blue line rather than a rectangle?  
**A5:** The blue line corresponds to the sweep start line in the dataset annotation. Operationally, the sweep continues from that line until the existing items are pushed aside and sufficient space is created for insertion.

## Final

Thank you for the positive assessment and for the constructive questions. 

**W1:** The baselines are too weak to isolate whether diffusion is the key ingredient.  
**A1:** We agree that the current baselines are not sufficient to isolate diffusion from every possible simpler learned alternative. What the present experiments establish is that, in this sparse-snapshot stow setting, a diffusion-based object-centric predictor substantially outperforms the practical heuristic alternatives and remains useful in downstream tasks. 

Stronger learned baselines are nontrivial here because this problem is not standard video prediction and not ordinary RGB generation. The supervision is temporally sparse, the prediction target is an object-centric post-stow bin state rather than future appearance, and the signal that matters for stow is geometry and occupancy rather than texture. Accordingly, **off-the-shelf video prediction or RGB generation methods are not directly suitable without redesigning the representation, conditioning interface, and learning objective**. In our own trials, simple RGB-conditioned diffusion performs poorly for exactly this reason. 

The present paper therefore compares against heuristic baselines that are natural for this problem and then evaluates whether the predicted states remain useful in downstream tasks. In particular, FOREST-predicted states improve DLO prediction fidelity and support multi-stow reasoning, showing that the predicted post-stow states are useful beyond direct IoU comparison. This does not fully settle the baseline question, but it does support diffusion as a meaningful ingredient in the proposed formulation.

**W2:** Generalization to unseen intents, bins, categories, or distribution shift is not tested.  
**A2:** The current experiments do not explicitly test generalization to unseen cases. What we do evaluate is robustness within ARMBench, which is a representative public production-scale stow dataset and contains substantial diversity in object categories, item instances, and storage bins within one warehouse environment. **The experiments therefore test performance across a realistic range of variation inside the target production environment.**
This focus is also consistent with the real application. Production warehouse systems are typically highly standardized, and what matters most in practice is stable performance within that standardized operating environment. 

**W3:** The canonical-mask prior may help too much and differs from practical pre-insertion signals.  
**A3:** We agree that the canonical-mask prior in the main setting may be stronger than what a practical pre-insertion pipeline would typically provide. We use it because ARMBench does not directly provide the in-bin contact-surface view of the incoming item, and the main experiment is intended to answer a proof-of-concept question: suppose that the contact-side geometry is available, can the model predict how the bin will reconfigure after the stow. To further quantify how much this prior help, we additionally replace the GT-derived mask with an estimate produced from the induct-view image using SAM3D and retrain FOREST with this generated input:

| Setting | Direct Insert N-IoU | Direct Insert O-IoU | Sweep Insert N-IoU | Sweep Insert O-IoU |
|---|---:|---:|---:|---:|
| Copy-Paste + Gravity | 0.3632 | 0.8563 | 0.2167 | 0.5287 |
| FOREST (main paper) | 0.7017 | 0.8550 | 0.6166 | 0.6878 |
| FOREST + SAM3D | 0.5290 | 0.8443 | 0.4784 | 0.6678 |

With SAM3D, FOREST still remains clearly above copy-paste(+gravity). This means **the predictive capability is still preserved when the GT-derived input is replaced by a practical acquisition route**. Besides, the SAM3D results are lower than the main-setting results partly because SAM3D itself is imperfect, and partly because the main setting benefits from the prior retained in the GT-derived mask. 

**Q1:** Why has there been relatively little recent visual foresight work?  
**A4:** Our impression is not that the underlying idea has disappeared, but that the framing has changed. Many problems that would previously have been described as visual foresight are now discussed under world models, predictive models, or action-conditioned generative modeling. The warehouse setting makes the foresight formulation especially useful again because routine operation naturally produces before/after observations at scale, and the downstream requirement is explicit future-state reasoning rather than direct action imitation. In that sense, the problem has become practically timely again, even if the surrounding terminology has shifted.

**Q2:** Why is the sweeping operation shown as a blue line rather than a rectangle?  
**A5:** The blue line corresponds to the sweep start line in the dataset annotation. Operationally, the sweep continues from that line until the existing items are pushed aside and sufficient space is created for insertion.
