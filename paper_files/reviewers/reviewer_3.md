# Reviewer 3 — original comments

Source: `paper_files/reviewers/paper_review_email.md`, lines 208–311 (manuscript Access-2026-39017, IEEE Access).
The block below is a verbatim copy, extracted by script and unedited. Do not modify it.

Comment IDs used in `response_matrix.md`: R3-<n> (comments 1-20 as numbered by the reviewer); R3-Q (answers to Additional Questions).

---

<!-- BEGIN VERBATIM -->

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

<!-- END VERBATIM -->
