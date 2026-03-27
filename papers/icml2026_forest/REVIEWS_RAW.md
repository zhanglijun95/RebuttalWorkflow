# Raw Reviews

## Reviewer Dwiz
Summary:
The paper focuses on the problem of accurately predicting changes in the bin layout after an item is placed into a storage bin in real-world robotic stow scenarios, where only sparse snapshot supervision is available. To this end, it proposes FOREST, a visual foresight diffusion-based world model for robotic stow. The method first extracts and aligns instance masks from pre- and post-stow images to construct an item-aligned, slot-structured bin state. It then takes the pre-stow bin state, canonical new-item mask, pre-stow RGB image, and stow intent as conditional inputs, and uses a Transformer-based latent diffusion model to predict the post-stow bin state, thereby enabling structured prediction of the bin layout after stowing. Experiments are mainly conducted on the real-world warehouse dataset ARMBench, with both direct evaluation and downstream-task evaluation performed under two stow modes: direct insert and sweep insert.

Strengths And Weaknesses:
Paper Strengths

The paper focuses on the visual foresight problem in real-world robotic stow scenarios, which is more aligned with practical industrial environments characterized by sparse supervision and complex object interactions.
The paper proposes FOREST, a framework centered on an item-aligned bin-state representation, which integrates instance alignment, conditional modeling, and latent diffusion prediction into a unified pipeline; the overall method is clearly structured and shows a certain degree of engineering feasibility.
Weaknesses

The proposed FOREST method heavily relies on upstream modules to establish the pre/post alignment relationship. Although the paper mentions mitigating this issue through filtering and consistency checks, it does not actually demonstrate how much supervisory noise affects the final model performance. It would therefore be beneficial to include additional experiments analyzing the robustness of the slot-aligned state when instance segmentation is incorrect, matching fails, or some objects are missed.
The paper assumes that, in a single-step stow setting, the change in instance count can be used to identify the newly added item and establish one-to-one correspondence. This is a relatively strong assumption. It would be beneficial to further evaluate the method under more realistic scenarios, such as increased occlusion, partially visible objects, coupled movements among multiple items, or missed detections.
The authors formulate the problem as a latent diffusion world model, but the motivation appears to rely more on the success of diffusion models in other domains rather than directly demonstrating their unique advantage for this task. The paper does not clearly show what diffusion offers here compared with alternative approaches, and it would be helpful to include additional experiments to better justify this design choice.
Soundness: 3: good
Presentation: 3: good
Significance: 2: fair
Originality: 2: fair
Key Questions For Authors:
The paper uses a large vision-language model to filter samples with inconsistent matching, but the implementation details are not sufficiently described. It would be helpful if the authors could further clarify the type of VLM used, the input prompts, and whether any manual verification was involved.

The paper introduces six item attributes—rigid, round, square, conveyable, foldable, and fragile—as part of the conditioning information. It would be helpful if the authors could clarify the rationale for choosing these specific attributes, and explain whether they were selected based on domain knowledge, dataset availability, or empirical effectiveness. In particular, it remains unclear whether these six properties are sufficient to capture the key factors that influence post-stow dynamics.

Limitations:
Yes

Overall Recommendation: 3: Weak reject: A paper with clear merits, but also some weaknesses, which overall outweigh the merits. Papers in this category require revisions before they can be meaningfully built upon by others. Please use sparingly.
Confidence: 3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.

## Reviewer gfXd
Summary:
This paper presents FOREST, a model intended to provide warehouse robots with visual foresight by predicting how a storage bin will appear after an item is placed inside. The approach takes three inputs: the pre-stow bin observation, a representation of the item to be inserted, and the stow intent describing where the item will be placed. The goal is to allow the robot to simulate the outcome of a planned stow action before executing it, enabling better decisions about placement to improve space utilization or avoid destabilizing existing items. Since large-scale fulfillment systems typically record only sparse “before” and “after” snapshots rather than continuous video, the model is trained to infer object rearrangements from these temporally sparse observations.

Strengths And Weaknesses:
Strengths
Addresses a practically relevant problem: The paper studies future state prediction in warehouse environments using the current diffusion based model paradigm which is an impactful problem in the real world. Predicting the outcome of object placement actions could potentially help robots reason about space utilization has not been studied well in this kind of stow based setup.
Uses real-world data from a large-scale warehouse dataset: The work evaluates the approach on ARMBench, a dataset collected from real production systems. Studying manipulation dynamics in such realistic settings is valuable, as many prior works on visual foresight focus primarily on simulated environments or controlled laboratory setups.
Weakness
Lack of clarity and poor structural flow, largely stemming from an imprecise and delayed problem formulation. The paper is difficult to follow because the formal setting, specifically the inputs, outputs, and supervision signals, is not clearly defined early in the text, making it challenging to distinguish exactly what information is available to the model during training versus at test time. Furthermore, the description of the proposed method and the data processing pipeline is scattered across multiple sections, which disrupts the narrative and obscures the actual task being solved. To significantly improve readability and clarify the core contributions, the authors must consolidate their methodology and introduce a dedicated, explicit problem statement before diving into the technical architecture.
Questionable characterization as a world model: The paper frames FOREST as a world model, but the formulation does not fully align with common definitions used in the literature. Typically, a world model learns environment dynamics by predicting future states given the current state and an action (or by modeling intermediate transitions along trajectories). In this work, however, the representation of the incoming object is derived from the ground-truth post-stow image and then canonicalized before being used as input. This makes it unclear whether the model is truly predicting future states from the current observation and stow intent, or whether it is primarily learning to place a known object silhouette into the scene.
Use of privileged information derived from the ground-truth post-stow image: The canonicalized mask used as the “new item observation” is extracted from the ground-truth post-stow image. Although canonicalization removes pose and location information, the representation still provides the exact object silhouette from the same viewpoint used in evaluation. Moreover, it is unclear how such a representation would be obtained in practice at test time without access to the final state. This introduces a form of privileged information that simplifies the task and raises concerns about the realism of the evaluation setup.
Potential simplification of the task due to canonicalization: Because the canonicalized mask already contains the object silhouette from the correct camera viewpoint, the model may effectively be learning to predict a placement transform (e.g., position and orientation) for a known mask rather than modeling the underlying dynamics of object interactions. This weakens the claim that the method learns meaningful stow dynamics and makes it difficult to assess whether the model truly captures the physical rearrangement of objects.
Weak baselines and limited comparisons: The experimental evaluation relies primarily on simple heuristic baselines (copy-paste and copy-paste with gravity), which are relatively weak and do not represent strong learning-based alternatives. Furthermore, these baselines are not designed to exploit the same conditioning information available to the proposed method. As a result, the comparisons do not fully isolate the benefits of the proposed architecture. Stronger baselines that receive the same inputs (e.g., learned diffusion or transformer-based predictors) would make the evaluation more convincing.
Limited demonstration of a practical foresight setup: In an ideal formulation, a world model should predict the final bin state given the pre-stow observation and the stow intent, allowing the robot to simulate candidate actions before execution and plan accordingly. Alternatively, if the method requires an explicit object mask as input, the paper should demonstrate the approach in a realistic scenario where such a mask is available before the object is placed (e.g., when the item is outside the bin and visible to an external camera or segmentation system). In the current setup, the mask is derived from the ground-truth post-stow image, which limits the demonstration of how the method would operate in a real deployment.
Soundness: 1: poor
Presentation: 1: poor
Significance: 2: fair
Originality: 2: fair
Key Questions For Authors:
Prediction target formulation. Why does the method focus on predicting instance-mask layouts rather than predicting the final bin image (or a latent image representation) directly from the pre-stow observation and stow intent? For example, recent video or generative world models could potentially be used to predict the post-stow state in image or latent space while leveraging large-scale priors on object appearance and dynamics.
Use of canonical masks derived from the final state. The new-item representation is constructed from the post-stow mask and then canonicalized. Have the authors considered evaluating the method in a setting where the object mask is obtained before insertion (e.g., from an external camera or induction station), or in a synthetic setup where such masks are naturally available? This could better demonstrate the method in a realistic inference scenario.
Practical deployment considerations. In a real robotic system, the post-stow image would not be available at test time since it is precisely the quantity the model aims to predict. Could the authors clarify how the proposed approach would obtain the required item representation in a practical deployment, and whether the method would remain effective without relying on signals derived from the ground-truth post-stow image?
Limitations:
The authors adequately discuss the technical limitations of their work in Appendix G, specifically noting the model's restriction to single-step transitions and its reliance on canonical masks extracted from ground-truth post-stow views rather than true contact-surface views.

Overall Recommendation: 2: Reject: For instance, a paper with technical flaws, weak evaluation, inadequate reproducibility, incompletely addressed ethical considerations, or writing so poor that it is not possible to understand its key claims.
Confidence: 4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.

## Reviewer oQeb
Summary:
This paper studies visual foresight for robotic stow operations in automated warehouses. The task is to predict the post-stow bin configuration given the pre-stow observation, the incoming item, and a high-level stow intent. The authors propose FOREST, a diffusion-based world model that predicts object-level bin layouts using instance masks. The method converts sparse pre/post snapshots into slot-aligned object representations via instance segmentation and item matching, and then trains a latent diffusion transformer conditioned on the stow context to predict the future layout.

The approach is evaluated on ARMBench, a real-world robotic stow dataset containing pre- and post-stow snapshots. The authors conduct (1) direct evaluation of predicted masks using instance IoU and (2) downstream evaluations including Delta Linear Opportunity (DLO) prediction and multi-stow rollout reasoning. Experiments show that FOREST substantially improves prediction accuracy over heuristic baselines and produces predictions that are useful for downstream planning tasks.

Overall, the paper proposes a structured diffusion-based world model for predicting bin reconfiguration in warehouse manipulation tasks under sparse supervision.

Strengths And Weaknesses:
Strengths
Well-motivated real-world problem
The paper addresses an important industrial robotics task: predicting the outcome of stow operations. The problem formulation—visual foresight under sparse snapshot supervision—is practical and relevant to warehouse automation.

Object-centric state representation
The use of slot-aligned instance masks to represent bin states is a reasonable design choice. This abstraction simplifies the dynamics modeling problem and focuses the prediction task on object interactions rather than pixel-level details.

Integration of diffusion world models with manipulation planning
The paper adapts latent diffusion models to predict structured object layouts rather than raw images. The conditioning mechanism using cross-attention and AdaLN for stow intent is technically reasonable and consistent with modern generative modeling practice.

Evaluation beyond raw prediction metrics
The inclusion of downstream tasks (DLO prediction and multi-stow reasoning) strengthens the evaluation. These experiments demonstrate that the predicted layouts are not only visually plausible but also useful for planning-related signals.

Weaknesses
Limited baselines
The empirical comparison is restricted to heuristic baselines (copy-paste and copy-paste with gravity). Given the increasing literature on video prediction, world models, and object-centric dynamics models, it is unclear how the proposed approach compares against stronger learned baselines such as: 1.latent video prediction models, 2.object-centric dynamics models and 3.diffusion world models used in robotics manipulation.

Without such comparisons, it is difficult to assess the relative novelty and performance gain.

Single-step prediction formulation
The method models single-step transitions between pre- and post-stow states. Although multi-step rollouts are demonstrated, the model is not explicitly trained for sequential dynamics. It is unclear whether the framework scales to longer horizons or more complex manipulation sequences.

Dependence on segmentation quality
The approach relies heavily on instance masks extracted by MaskDINO. Errors in segmentation or item matching may propagate into the world model training signal. While the paper mentions filtering heuristics, the impact of segmentation noise is not thoroughly analyzed.

Limited physical reasoning
Although the model predicts rearrangements, it does not explicitly model physical constraints such as contact dynamics or stability. It is possible that some predictions arise from dataset bias rather than genuine physical reasoning.

Dataset-specific evaluation
All experiments are conducted on a single dataset (ARMBench). The paper would benefit from demonstrating generalization to: synthetic manipulation environments different container geometries unseen object distributions

Scores
Soundness: 2 (Fair)
The methodology is reasonable, but the evaluation is limited by weak baselines and reliance on a single dataset. Stronger empirical comparisons would be necessary to convincingly demonstrate the benefits of the proposed approach.

Presentation: 3 (Good)
The paper is clearly structured and the pipeline is well explained. Figures describing the pipeline and evaluation are helpful. However, some implementation details (e.g., segmentation noise handling and matching robustness) could be described more thoroughly.

Significance: 3 (Good)
The problem is practically relevant and the approach could be useful for robotics planning systems. However, the broader impact is somewhat limited due to the narrow evaluation setting and reliance on a specific dataset.

Originality: 3 (Good)
The combination of object-centric bin representations and diffusion world models for warehouse stow prediction is novel in this specific application domain. However, many components (diffusion world models, slot-based representations, transformer conditioning) are adaptations of existing techniques.

Soundness: 2: fair
Presentation: 3: good
Significance: 3: good
Originality: 3: good
Key Questions For Authors:
1. Baselines
Can the authors compare against stronger learned baselines such as object-centric dynamics models or video prediction models? This would help clarify whether diffusion modeling provides a substantial advantage.

2. Segmentation robustness
How sensitive is the model to errors in instance segmentation and item matching? Have the authors evaluated performance under noisy or imperfect masks?

3. Generalization
Does the model generalize to bins with different geometries or to object categories not present during training?

4. Multi-step dynamics
Would training the model explicitly on multi-step transitions improve long-horizon prediction performance compared to the current single-step training formulation?

5.Physical plausibility
Have the authors evaluated whether predicted configurations obey simple physical constraints (e.g., non-overlapping objects, stability)?

Limitations:
The authors briefly discuss limitations of the proposed approach, including reliance on instance segmentation quality and evaluation on a single dataset. A minor suggestion would be to further clarify potential deployment limitations in real warehouse systems (e.g., robustness to perception errors or domain shifts), although no major negative societal impacts are apparent for this work.

Overall Recommendation: 3: Weak reject: A paper with clear merits, but also some weaknesses, which overall outweigh the merits. Papers in this category require revisions before they can be meaningfully built upon by others. Please use sparingly.
Confidence: 3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.

## Reviewer TAf5
Summary:
This paper studies “visual foresight for stow” in warehouse robotics, predicting post-stow bin layouts from sparse pre- and post-stow RGB snapshots, a new-item observation, and a high-level stow intent. The paper reports large gains in instance IoU for the newly inserted item over copy-paste heuristics. It shows that substituting FOREST-predicted masks into two downstream tasks (DLO prediction and multi-stow rollout) causes only modest degradation relative to using ground-truth masks.

Strengths And Weaknesses:
Strengths

This paper is well-structured, logically organized, and comprehensive in content. It addresses a critical practical challenge in visual foresight for stow by proposing a feasible solution. The problem is clearly formulated for single-step, intent-conditioned post-stow prediction using only sparse supervision, an approach that is practically motivated by the production constraints described by the authors.

Weaknesses

Baselines are too weak for the claimed modeling advance. Only heuristics are compared (copy-paste variants). Without a learned baseline, it is impossible to tell whether diffusion is the key ingredient or whether a simpler conditional model would match the gains.
The paper does not test generalization to unseen intents, bins, or item categories, nor robustness to distribution shift (which is practically relevant for production warehouses).
As described in Sec 3.2 and Appendix C, the model is conditioned on a canonical mask derived from the ground truth, used both at train and test. This sidesteps the hard part of mapping induct-view shape to in-bin contact surface and, more importantly, gives a nearly perfect item silhouette prior. It should be noted that the shapes obtained through the methods mentioned in Appendix C—such as adding additional cameras or performing 3D reconstruction—will inevitably differ from this prior. The paper should more explicitly quantify “how much” this prior helps (e.g., ablate to induct-view only, or add noise or partial occlusion to the canonical mask).
Overall, the solid technical work and practical motivation compensate for the shortcomings in the experiments. I expect these issues can be addressed during revision. At this stage, I am inclined to accept the paper.

Soundness: 3: good
Presentation: 3: good
Significance: 2: fair
Originality: 3: good
Key Questions For Authors:
From the related work, it appears that there has been little to no Visual Foresight research published in recent years. Could you comment on why this might be the case? Is this due to a shift in research focus, emerging challenges in the field, or other factors?

Why is the sweeping operation depicted as a blue line in the diagram rather than a rectangle?

Limitations:
Yes

Overall Recommendation: 4: Weak accept: Technically solid paper that advances at least one sub-area of AI, with a contribution that others are likely to build on, but with some weaknesses that limit its impact (e.g., limited evaluation). Please use sparingly.
Confidence: 2: You are willing to defend your assessment, but it is quite likely that you did not understand the central parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.