# Reviewer 2 — original comments

Source: `paper_files/reviewers/paper_review_email.md`, lines 102–207 (manuscript Access-2026-39017, IEEE Access).
The block below is a verbatim copy, extracted by script and unedited. Do not modify it.

Comment IDs used in `response_matrix.md`: R2-M<n> (major comments 1-7, numbered by the reviewer); R2-m<n> (minor comments, unnumbered bullets in the original, numbered here 1-8 in order of appearance); R2-G (general assessment).

---

<!-- BEGIN VERBATIM -->

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

<!-- END VERBATIM -->
