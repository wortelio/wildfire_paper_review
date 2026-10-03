# Reviewer 1 — original comments

Source: `paper_files/reviewers/paper_review_email.md`, lines 43–101 (manuscript Access-2026-39017, IEEE Access).
The block below is a verbatim copy, extracted by script and unedited. Do not modify it.

Comment IDs used in `response_matrix.md`: R1-<Section>-<n>: Abs, Intro, Meth, Res, Disc (numbering as given by the reviewer).

---

<!-- BEGIN VERBATIM -->

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

<!-- END VERBATIM -->
