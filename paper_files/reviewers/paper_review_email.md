Dear Prof. Lopez-Vallejo:

I am writing to you regarding manuscript # Access-2026-39017 entitled "Hardware-Aware Optimization for Low-Power FPGA-Based Wildfire Classification in UAV Edge AI" which you submitted to IEEE Access.

Your article was peer reviewed with interest but has not been recommended for publication in its current form.  We strongly encourage you to address the reviewers’ concerns, which can be found at the bottom of this letter, and resubmit your article to IEEE Access once you have updated it accordingly.
 
Please note that IEEE Access has a binary peer review process. Therefore, to uphold quality to IEEE standards, an article is rejected even if it requires minor edits.
 
When updating your manuscript, you should elaborate on your points and clarify with references, examples, data, etc. If you disagree with any technical points the reviewers have made, please include your counterarguments in your response to the reviewers (more information detailed below) and work this into the updated manuscript. 

Also, note that if a reviewer suggested references, you should only add those that are relevant to your work if you feel they strengthen your article. Recommending references to specific publications is not appropriate for reviewers and you should report excessive cases to ieeeaccessEIC@ieee.org.  Authors are not obligated to cite articles that are recommended by the reviewers, and the final decision on the article will not be influenced by whether or not authors cite these suggested references.
 
IEEE Access allows one opportunity to resubmit. If the updated manuscript is determined not to have addressed all of the previous reviewers’ concerns, or if the Associate Editor still has substantial technical concerns, the article will be rejected and no further resubmissions will be allowed.
 
When you are ready to resubmit your updated article, you can do so in the IEEE Author Portal.  When you log into the IEEE Author Portal you will see the title of the rejected article and the option to “Start Resubmission”.

https://ieee.atyponrex.com/submission/submissionBoard/REX-PROD-2-3CECE135-784A-4A9D-A131-8A19D2B4FA11-B6A52D9D-C72C-47ED-B635-427E0B06F60F-63365/current?idtype=external
 
Upon resubmission you will be asked to upload the following 3 files:

1) A document containing your response to reviewers from the previous peer review.  The “response to reviewers” document (template attached) should have the following regarding each comment: a) Reviewer’s concern, b) your response to the concern, c) your action to remedy the concern. The document should be uploaded with your manuscript files under "Author's Response Files.”

2) Your updated manuscript with all your individual changes highlighted, including grammatical changes (e.g. preferably with the yellow highlight tool within the pdf file). This file should be uploaded with your manuscript files as “Highlighted PDF.”

3) A clean copy of the final manuscript (without highlighted changes) submitted as a Word or LaTeX file, and as a PDF, both submitted as the “Main Manuscript.”

**IMPORTANT: Please see the attached Resubmission Checklist that details all the items listed above.  Please utilize this checklist to ensure you have made the necessary edits to your manuscript, and to ensure you have all the necessary files prepared prior to resubmission.

*** AUTHOR LIST CHANGES: If your revised manuscript has an updated author list, you will need to submit a formal request to the Editor by completing the attachment labelled ‘Request for Byline Change,’ and uploading it as 'Request for byline change form.' This should include a DETAILED justification explaining each author’s contribution(s) to the work. You will also need to provide the justification for the author change during the submission process.  Change in the author list is considered rare and exceptional, and the decision to allow such changes rests with the Editor. Once the list and order of authors has been established, the list and order of authors should not be altered without permission of all living authors of that article.

We sincerely hope you will update your manuscript and resubmit soon. Please contact me if you have any questions.

Thank you for your interest in IEEE Access.

Sincerely,

Dr. Guillermo Valencia-Palomo
Associate Editor, IEEE Access
gvalencia@hermosillo.tecnm.mx, chinovp@gmail.com

Reviewers' Comments to Author:

Reviewer: 1

Comments:
The paper addresses a relevant problem, the deployment of an FPGA acceleration device to a UAV as a first-stage wildfire detection trigger. The authors present a complete pipeline, from model training to FPGA implementation. The manuscript is concise but raises some concerns, mainly due to lack of justification and key metrics.  

# Abstract
1. The abstract must be written as one paragraph and use no abbreviations, as per IEEE Access guidelines.
2. The abstract should also mention the BED architecture and the comparison of the FPGA acceleration device with the "CPU baselines", since a significant part of the manuscript is dedicated to its acceleration.

# Introduction
1. The authors should support Section I, Paragraph 4 with references.
2. The introduction fails to explain the importance of deploying low-power acceleration devices and lightweight, high-accuracy neural network architectures on UAVs.
3. The authors should clearly state the purpose of the presented research in the introduction.
4. The authors should explicitly state that their research prioritizes low power consumption over throughput, and justify their decision accordingly.

# Methodology and Data
1. Please provide references for all external tools used (e.g. PyTorch) and their versions.
2. Please attribute reference [23] as the source of Figure 2 in its caption.
3. Spatial SVD is a technique independent of the AIMET framework and should be cited accordingly.
4. In Section II.C.1, how is structural simplification performed? Is it an automated procedure? Is there a systematic approach in applying the mentioned network width and depth? Elaborate.
5. In Section II.C.2, please specify if channel pruning is applied on kernels, feature maps or both. Moreover, elaborate on the order that spatial SVD and channel pruning is applied and if the order has an impact on the end result.
6. In Section II.C.4.a, Equations (5) and (7) assume square kernels, but earlier in the same section, it was established that spatial SVD is used, where kernels are rectangular. Please clarify.
7. "Adaptive fps Scaling" suggests the clock frequency of operation can be altered during runtime. Please clarify.
8. Please justify the choice of the simplified models as the baseline for the compression stage.

# Results
1. In Table 3, please clarify the MAC metric; specifically the BED FPGA reports the effective MAC count, while the raw MAC count has increased.
2. In Figure 6.a, is the reported resources utilization for all model variations other than the FPGA based on 32-bit floating point arithmetics or 2/4/8-bit fixed point arithmetics? Please clarify.
3. Please state the configurations, the chipset, the RAM size, frequency of operation and the instruction set used in Raspberry Pi 3A+ and Pi 5, as the operating system and the hardware specifications significantly affect the reported inference times of Figure 9.a.
4. In Table 9, the use of "Latency" and "Throughput" is misleading. Please consider renaming the columns to "Initial" and "Average" under "Inference Execution Time". Moreover, please provide the standard deviation of the average values.
5. Please add energy efficiency (GOPS/W) to the comparison table for both the FPGA and the CPU baselines. This is a standard metric in FPGA accelerator literature and directly relates to the UAV flight autonomy motivation.
6. In Figure 8, please consider providing the percentage of channels that are all-zero valued.
7. Please extend the reported metrics with all classification metrics provided in Section II.E.
8. Please expand on the F1 drop in the quantization step at both neural network architectures.

# Discussion and Future Work
1. The authors should discuss whether the reported F1-macro metric of all FPGA implementations is acceptable for the deployment scenario.
2. It would strengthen the discussion section to relate the reported power consumption to expected UAV flight autonomy, by estimating how throughput scales with available battery budget.
3. If UAV deployment acts as the sole first-stage trigger for wildfire detection, this constitutes a mission-critical scenario. Please clarify the intended role of the UAV in the detection chain, and, if it is the primary trigger, please discuss reliability and fault tolerance.
4. What are the limitations of this study?
5. What were the criteria in using the BED and MobileNet architectures?
6. What were the criteria in choosing the FPGA board?

Additional Questions:
Please confirm that you have reviewed all relevant files, including supplementary files and any author response files, which can be found in the "View Author's Response" link above (author responses will only appear for resubmissions): Yes, all files have been reviewed

1) Does the paper contribute to the body of knowledge?: Yes The paper addresses a relevant problem, the deployment of an FPGA acceleration device to a UAV as a first-stage wildfire detection trigger. The authors present a complete pipeline, from model training to FPGA implementation. The manuscript is concise but raises some concerns, mainly due to lack of justification and key metrics.

2) Is the paper technically sound?: Yes, the authors present a complete pipeline, from model training to FPGA implementation.

3) Is the subject matter presented in a comprehensive manner?: Yes, the manuscript is concise.

4) Are the references provided applicable and sufficient?: Yes

5) Are there references that are not appropriate for the topic being discussed?: No

5a) If yes, then please indicate which references should be removed.:


Reviewer: 2

Comments:
This manuscript presents a hardware-aware workflow for optimizing compact convolutional neural networks for fully on-chip FPGA inference, demonstrated using wildfire image classification as the target application. The workflow combines structural simplification, structured pruning, quantization-aware training, and FPGA-specific architectural adaptation, and uses AIMET, Brevitas, and FINN to eventually deploy BED- and MobileNetV2-based networks on a PYNQ-Z1 FPGA.

The manuscript addresses the practically relevant problem of deploying a compact wildfire image-classification model in a resource-constrained edge environment. In particular, deploying a complete CNN as a streaming architecture on a relatively resource-constrained Zynq-7020 device is nontrivial, and the authors provide useful insight into the differences between reducing conventional neural-network complexity metrics and obtaining an actually efficient FPGA implementation. The observation that apparently beneficial transformations can produce inconvenient channel dimensions and therefore lead to inefficient folding is particularly useful from a hardware-design perspective. This is a meaningful contribution to FPGA accelerator design, as many studies primarily report reductions in computational complexity or resource utilization without examining how those improvements translate into an efficient hardware architecture and mapping strategy for the target FPGA. The analysis of parameter count, MAC count, FPGA resource utilization, throughput, precision, and estimated power also makes the optimization trajectory relatively easy to follow. The reduction of MobileNetV2 from approximately 2.22 M parameters and 300 M MACs to fewer than 70 K parameters and 42 M MACs, while limiting the F1-Macro degradation to less than 2.5 percentage points, is a meaningful engineering result.

I also appreciate that the manuscript is relatively careful about several limitations. For example, the author does not claim that the sequential optimization stages constitute independent ablation experiments, explicitly notes limitations of the dataset split, and appropriately warns that the FPGA programmable-logic power estimates and Raspberry Pi board measurements cannot be interpreted as a direct board-level energy comparison.

My primary reservation is that the methodological novelty is somewhat limited. Structural simplification, structured pruning, quantization-aware training, low-bit FINN/Brevitas implementations, FPGA-aware architecture adaptation, and constraint-guided DNN/hardware co-design are all well-established individually. Previous work has gone further by jointly optimizing architecture, quantization, and FPGA mapping using formal or automated hardware-aware optimization methods. Therefore, I believe the main contribution should be positioned primarily as a carefully documented practical workflow and case study rather than a fundamentally new co-design methodology.

Major comments

1. The novelty of the proposed hardware-aware workflow should be stated more precisely.
The manuscript presents the combination of architectural simplification, structured pruning, quantization-aware training, and FPGA adaptation as a principal contribution. However, substantial prior work already exists on low-precision FINN implementations, hardware-aware pruning, and joint neural-network/FPGA optimization. FINN itself is explicitly designed for design-space exploration of spatial dataflow architectures, while previous hardware-aware optimization approaches have jointly considered architecture, quantization, and hardware constraints.

The manuscript's genuinely useful contribution appears to be more specific. It demonstrates how these techniques interact in practice on an extremely resource-constrained Z-7020, and particularly how transformations that appear favorable from the perspective of parameter count or MAC count may become unfavorable after FPGA folding and buffering constraints are considered.

I suggest that the authors sharpen this distinction. Rather than emphasizing the novelty of combining the optimization techniques themselves, they could emphasize the experimentally demonstrated optimization trajectory and the lessons concerning FPGA feasibility, folding-factor compatibility, buffering, resource balancing, and mixed-precision adaptation.

This would strengthen the paper because those observations are among its most convincing contributions.

2. Dataset Independence and Possible Duplicate Samples
The authors appropriately acknowledge that the internet-derived source datasets may contain overlapping or near-duplicate samples. While a systematic duplicate or near-duplicate analysis would strengthen confidence in the reported evaluation results, I do not consider such an analysis essential for the present hardware-focused study, particularly given the practical constraints of conducting additional dataset curation and validation.

However, possible duplicates are especially important when they occur across the training and test splits. If identical or near-identical images, frames, or highly similar source samples appear in both partitions, the reported F1-Macro values may be inflated because the test set would not provide an independent assessment of generalization. This concern is particularly relevant for image datasets assembled from internet-derived sources, where related images may originate from the same event, sequence, webpage, or underlying collection even when their filenames differ. The authors should therefore clarify whether duplicate or near-duplicate samples were checked across the dataset partitions, and, if such a check was not performed, explicitly acknowledge this as a limitation of the evaluation.

The more important point is that this limitation should remain clearly stated when interpreting the reported F1-Macro values. The current results should primarily be viewed as demonstrating the effect of architectural and hardware constraints on the constructed dataset split, rather than as evidence of broad cross-dataset generalization or real-world UAV performance. Therefore, I recommend that the authors retain this limitation prominently and avoid overly broad claims regarding generalization beyond the evaluated dataset.

3. The statistical reliability of the model comparisons could be improved.
Each configuration apparently uses only one training run, and no globally fixed random seed is used. Consequently, run-to-run variability is not quantified.

Several performance differences used to motivate design choices are quite small. For example, some structural transformations are associated with differences of only approximately 0.03–0.10 percentage points in F1-Macro. Without repeated experiments, it is difficult to determine whether differences of this magnitude are caused by the transformation or ordinary optimization variance.

I would not require the authors to repeat every experiment several times because the FPGA compilation workload is substantial. A reasonable compromise would be to repeat selected software-level experiments, especially the baseline, MobileNetV2 Nano, and a few configurations for which differences below roughly 0.2 percentage points influence an architectural conclusion, with several seeds and report mean and standard deviation. This would help distinguish robust trends from training noise.

4. F1-Macro alone is somewhat insufficient for the intended role as an early-warning trigger.
The proposed accelerator is intended to operate continuously as a first-stage trigger that activates a more computationally expensive detector when smoke or fire is observed.

In this application, false negatives and false positives have substantially different operational consequences. Missing early smoke may be considerably more important than a small change in overall F1-Macro, whereas excessive false alarms may unnecessarily activate the second-stage processor and eliminate much of the anticipated energy benefit.

The manuscript reports useful per-label information for the quantized MobileNetV2 Nano and observes that quantization primarily degrades smoke recall, while fire recall remains above 98%. This is actually a particularly important result and deserves more emphasis.

I recommend reporting, if available, smoke/fire precision and recall for the final FPGA output as well, rather than only F1-Macro. False-positive rate, false-negative rate, or precision-recall curves would also be informative.

The fixed 0.5 threshold should additionally be justified. For a first-stage trigger, a threshold selected to prioritize smoke recall could potentially provide a more appropriate operating point.

5. The Raspberry Pi comparison is useful as context, but should not be interpreted as an efficiency comparison.
The FPGA implementation uses quantized custom CNNs and reports Vivado-estimated PL power, whereas the Raspberry Pi platforms execute different FP32 models using ONNX Runtime and report externally measured board-level power.

The authors already acknowledge this mismatch, which substantially reduces my concern. Nevertheless, figures containing these values side by side could still invite an unintended interpretation that the FPGA is several times or an order of magnitude more energy-efficient.

I suggest explicitly labeling the comparison as "deployment context" wherever it appears, and perhaps visually separating PL-estimated power from measured system power.

If feasible, running the same compact model on the Raspberry Pi would also make the inference-time comparison more informative, although I would not regard this as mandatory.

6. The distinction between MAC reduction and actual streaming-accelerator performance is one of the strongest observations and deserves deeper analysis.
The sparsity experiment is particularly interesting. Removing all-zero channels reduces MobileNetV2 Nano from 68,882 to 41,178 parameters and from 42 M to 36 M MACs, yet does not increase maximum throughput because of remaining pipeline and buffering limitations.

This is a useful hardware-design result because it demonstrates why conventional model-compression metrics are not sufficient for streaming FPGA accelerators.

I encourage the authors to analyze this case more deeply. Identifying the actual bottleneck layer before and after pruning, its cycle count, FIFO requirements, and the resulting initiation interval would convert this observation from an anecdotal result into a broadly useful hardware-design insight.

7. The manuscript would benefit from a clearer comparison with previous FPGA CNN optimization and co-design work.
The related-work comparison should extend beyond wildfire-specific applications. The closest methodological comparisons are prior FPGA studies involving hardware-aware neural network optimization, low-precision dataflow accelerators, structured pruning, and FINN-based implementations.

The proposed workflow does not necessarily need to outperform those studies, since the target device, model, and application constraints may be different. However, a concise comparison would help clarify what is distinctive about the present work and how it differs from existing FPGA co-design approaches.

A comparison table could focus on a small number of representative dimensions, such as:
target FPGA and network,
optimization and quantization strategy,
degree of hardware-aware or automated design exploration,
reported hardware performance and resource usage.

This would make the contribution and positioning of the manuscript clearer without requiring an extensive benchmark against unrelated platforms or applications.

Minor comments

The following issues are relatively small, but addressing them would improve the manuscript.
- The feasibility constraint involving the optimized-to-baseline performance ratio should be checked carefully. If the objective is to constrain performance degradation, a formulation such as F_opt divided by F_baseline being less than or equal to Delta may be counterintuitive depending on how Delta is defined. The authors should clarify whether Delta represents the maximum allowable degradation, the minimum retained performance, or another quantity.
- Equation (7), describing matrix-multiplication cycles, should be checked and explained carefully. From the summarized expression, the placement of PE and the definition of "In Vectors" are not immediately intuitive. A derivation or reference to FINN's folding formulation would help readers reproduce the calculation.
- The rationale for preferring channel counts that are multiples of eight, rather than merely four, could be quantified. For example, the authors could show how this affects allowable SIMD and PE combinations or DSP packing.
- The use of 2-bit precision for two computationally dominant BED layers is interesting and should probably be described explicitly as mixed-precision quantization rather than simply as part of the FPGA adaptation process.
- It would be useful to report whether the 4 MHz and lower-than-1-MHz configurations were physically executed at those clock frequencies on the FPGA, or whether throughput was extrapolated from the 100 MHz implementation while only the frequency in the power model was changed. The distinction is important, particularly when discussing measured inference time.
- The approximately 109 mW power result at 100 kHz is described as an approximate static-power floor. It might be clearer to report Vivado's static and dynamic power components directly rather than infer static power using an extremely low clock frequency.
- The manuscript appropriately describes classification as a reduced version of the wildfire-detection problem rather than claiming that it performs localization. This wording should be retained consistently. Image-level classification inevitably loses information about small or distant smoke regions when bounding-box annotations are discarded.
- Given that reducing the input resolution from 224x224 to 160x160 and 112x112 decreases F1-Macro by approximately 1.14 and 1.64 percentage points, respectively, it would be interesting to report smoke recall separately. Small or distant smoke regions are likely to be more sensitive to resolution reduction than clearly visible fire regions.

Overall, I find the manuscript technically meaningful and practically relevant, particularly in demonstrating how conventional model optimization metrics translate into actual FPGA implementation constraints and design choices. The main concerns relate to the positioning of the methodological novelty, the reliability and interpretation of the reported model-performance results, and the need for clearer comparison with prior FPGA co-design work. These issues appear addressable without fundamentally changing the proposed architecture or experimental framework. I therefore believe the manuscript would be suitable for publication after appropriate revision.

Additional Questions:
Please confirm that you have reviewed all relevant files, including supplementary files and any author response files, which can be found in the "View Author's Response" link above (author responses will only appear for resubmissions): Yes, all files have been reviewed

1) Does the paper contribute to the body of knowledge?: Yes. This paper contributes to the body of knowledge by demonstrating a practical hardware-aware optimization workflow for mapping compact CNN models onto a highly resource-constrained FPGA.

2) Is the paper technically sound?: Yes.

3) Is the subject matter presented in a comprehensive manner?: Yes, very well presented.

4) Are the references provided applicable and sufficient?: N/A

5) Are there references that are not appropriate for the topic being discussed?: No

5a) If yes, then please indicate which references should be removed.:


Reviewer: 3

Comments:
This manuscript presents a hardware-aware optimization workflow for implementing MobileNetV2 and BED as fully on-chip FINN accelerators on a PYNQ-Z1. The engineering work is promising, and the manuscript is generally transparent about its limitations. However, several methodological and reporting issues should be addressed before publication.

Major Comments

1. Clarify the relationship between the evaluation and test sets.

Table 1 defines only training and test partitions, while Section II-B refers to a held-out evaluation set used for learning-rate scheduling and checkpoint selection based on F1-Macro. Please clarify whether this is a separate validation set. If so, report its size in Table 1. If it is the test set, the reported test metrics may be affected by model selection.

2. Describe how the PYNQ-Z1 inference times in Table 9 were obtained.

The Raspberry Pi timing protocol is clearly described, but no equivalent methodology is provided for the PYNQ-Z1. Please state whether the reported latency and throughput were measured on the board, obtained from simulation, or derived from cycle counts; how many inferences were used; and whether DMA/data-transfer overhead is included.

3. Reconcile the BED results in Tables 3 and 7.

Table 3 reports BED Quantized at 94.70% and BED FPGA at 94.54%, consistent with Section III-A2. However, Section III-B1 attributes the full 1.26 percentage-point reduction to quantization, corresponding to 94.54%. Please reconcile the table labels, values, and accompanying text.

4. Clarify the throughput results in Table 9.

For MobileNetV2 Nano, the reported throughput times scale consistently with clock frequency, whereas the BED values do not despite unchanged folding factors. Please explain this discrepancy or correct the reported values. In addition, Section III-B2 reports a theoretical maximum of 784 fps for MobileNetV2 Nano at 100 MHz, while the 1.19 ms throughput in Table 9 corresponds to approximately 840 fps. Please clarify which values are theoretical estimates and which are measured results.

5. Provide a stage-by-stage optimization trajectory for MobileNetV2 Nano.

The workflow is presented as the principal contribution, but only BED has a complete optimization trajectory in Table 3. Please provide an equivalent progression for MobileNetV2 Nano, including parameters, MAC operations, and F1-Macro at the major optimization stages. This would make the proposed methodology more transparent and reproducible. Please also clarify the specific architectural changes included in the BED structural-simplification stage.

6. Explain the selection of MobileNetV2 as the optimization baseline.

Table 2 suggests that MobileNetV3 offers substantially lower computational cost with only a modest reduction in F1-Macro. The later discussion of FINN operator limitations appears relevant to the choice of MobileNetV2 but is not explicitly connected to it. Please state the rationale for selecting MobileNetV2 and explain why MobileNetV3 Mini was evaluated but not deployed.

7. Add a quantitative comparison with prior implementations.

The manuscript cites related FPGA and microcontroller implementations but provides no quantitative comparison with them. A table comparing relevant metrics such as classification performance, throughput, resource utilization, and power, while clearly noting differences in datasets, tasks, and measurement boundaries, would better establish the contribution relative to prior work.

8. Reconsider the low-power claim and cross-platform power comparison.

The title emphasizes a low-power FPGA implementation and the abstract highlights 144 mW. However, this value is a Vivado-estimated programmable-logic power at 4 MHz and excludes the processing system, peripherals, and board-level components. As currently presented, the 144 mW headline figure could therefore be misinterpreted as measured PYNQ-Z1 board-level power. In contrast, the Raspberry Pi values are externally measured board-level power, yet Figure 9b presents these values on the same axis.

Please either provide PYNQ-Z1 board-level power measurements using a measurement boundary comparable to that used for the Raspberry Pi platforms, or remove the direct cross-platform power comparison and clearly qualify the PYNQ-Z1 result as an accelerator-level power estimate in the title, abstract, and conclusion. At minimum, the abstract should explicitly state that the 144 mW value is Vivado-estimated PL power obtained at 4 MHz.

9. Report power consistently with the stated optimization objectives.

Estimated PL power is identified as a design target, but power is reported only for the final FPGA designs. Please either report estimated power across the major optimization stages or revise the description of the design objectives accordingly. Reporting energy per frame would also help relate power to throughput.

10. Strengthen the cross-platform performance comparison.

The current comparison uses different models on the PYNQ-Z1, Raspberry Pi 3A+, and Raspberry Pi 5, which confounds model and platform differences. Please consider additionally evaluating MobileNetV2 Nano across all three platforms to provide a controlled reference point.

11. Clarify the evaluation setting for Table 2.

Please identify the dataset and test split used to obtain the F1-Macro values in the Table 2 caption. The text should also note that the reference models were not all trained under identical initialization conditions, since three use pretrained weights while MobileViTV3 is trained from scratch.

12. Discuss class imbalance in the constructed dataset.

Table 1 shows substantial class imbalance, particularly in the FASDD UAV subset. Please state whether class weighting or threshold adjustment was considered and discuss how the imbalance may affect the per-label results in Table 8.

13. Correct and complete the references.

FINN is central to the implementation but is not cited. Please add appropriate references for FINN/FINN-R and consider citing other core software components such as PyTorch and Albumentations. In addition, reference [13] (MobileNetV2) does not support the FPGA dataflow claim for which it is cited in the Introduction and should be removed from that statement or replaced with an appropriate reference. Reference [13] remains appropriate where it is cited in Section II-B as the source of the MobileNetV2 architecture.

Minor Comments

14. Please check the input notation for Conv4.4 in Table 4.

15. Please use consistent terminology for the same optimization stage, which is labeled “MANUAL” in Figure 6a and “Simplified” in Table 3.

16. Please verify the F1-Macro value in the first row of Table 10, where FPGA power and clock are reported alongside what appears to be the quantized software result.

17. Please verify that the PYNQ-Z1 bar in Figure 9b corresponds to the 144 mW value reported in Table 9.

18. Please correct the rendering of the euro symbol in Section I.

19. Please carefully review the reference list for bibliographic and formatting errors, including [1], [8], [13], [16], [20], [24], and [29].

20. If Figure 9b is retained, please clearly distinguish the PYNQ-Z1 programmable-logic estimate from the Raspberry Pi board-level measurements within the figure.

Additional Questions:
Please confirm that you have reviewed all relevant files, including supplementary files and any author response files, which can be found in the "View Author's Response" link above (author responses will only appear for resubmissions): Yes, all files have been reviewed

1) Does the paper contribute to the body of knowledge?: Yes, with qualifications.

The paper presents a useful hardware-aware optimization and FPGA implementation of lightweight CNNs on a resource-constrained Zynq platform. The resulting MobileNetV2 Nano achieves substantial reductions in parameters and MAC operations with a limited loss in F1-Macro. However, because the proposed constraint-guided workflow is the main claimed contribution, its stage-by-stage application to MobileNetV2 Nano should be documented more clearly.

2) Is the paper technically sound?: Partially.

The overall technical approach is appropriate, but several aspects of the quantitative evaluation require clarification or correction.

The FINN-based implementation, quantization, folding, and FPGA resource and power analysis are technically reasonable. However, the relationship between the validation and test sets is unclear, and several reported results are internally inconsistent, including the BED quantization results in Tables 3 and 7 and the throughput values in Table 9. In addition, the methodology used to obtain the PYNQ-Z1 inference times is not sufficiently described, including whether the values are measured or estimated and whether DMA transfers are included. These issues should be resolved to establish the reliability and reproducibility of the reported hardware results.

3) Is the subject matter presented in a comprehensive manner?: Partially.

The manuscript is generally well structured and clearly describes the dataset construction, quantization settings, FPGA design constraints, and limitations of the evaluation. However, several aspects of the proposed methodology require more complete presentation. In particular, the optimization trajectory of MobileNetV2 Nano is not documented stage by stage, and the rationale for selecting MobileNetV2 as the base architecture is not clearly connected to the FINN implementation constraints. In addition, the effect of the optimization process on power is not shown across stages, and no quantitative comparison with prior FPGA-based implementations is provided. These additions would make the proposed hardware-aware methodology and its benefits easier to assess.

4) Are the references provided applicable and sufficient?: Partially.

The references generally provide adequate coverage of wildfire detection and model compression. However, FINN, which is central to the FPGA implementation methodology, is not cited, despite repeated use throughout the manuscript. PyTorch and Albumentations are also used without references. In addition, several references contain incorrect or inconsistent bibliographic information, including the venue/year information for MobileNetV2 [13] and ECA-Net [29], and some entries rely on preprint versions where peer-reviewed publications are available. The reference list should therefore be carefully reviewed for completeness, accuracy, and consistency.

5) Are there references that are not appropriate for the topic being discussed?: Yes

5a) If yes, then please indicate which references should be removed.: Yes, in one case.

In the Introduction, the claim that FPGA approaches typically rely on full-model mapping through custom dataflow pipelines is supported by references [12] and [13]. However, [13] is the MobileNetV2 architecture paper and does not support this FPGA-specific claim. It should therefore be removed from this statement or replaced with an appropriate reference on FPGA dataflow implementations.

I did not identify other references that appear inappropriate to the topics they are used to support.