<!--
TRANSCRIPTION NOTES (not part of the manuscript)
- Source: paper_files/original.pdf (15 pages, pdfTeX, CreationDate 2026-08-16). The PDF is authoritative; if this file and the PDF disagree, the PDF wins.
- Faithful transcription: wording, numbers, units, model names, references and typos are kept as printed. Nothing has been corrected or reworded.
- Running headers ("IEEE Access"), footers ("VOLUME 11, 2023") and page numbers are omitted; page boundaries are marked with HTML comments of the form "Page N".
- Line-end hyphenation has been resolved: syllable breaks are joined (e.g. "detec-tion" -> "detection"); genuine compound hyphens are kept (e.g. "co-design", "PYNQ-Z1", "Z-7020", "F1-Macro").
- Two-column reading order has been linearised. Floats (tables/figures) are placed close to where they appear in the PDF.
- Tables with two-level headers are flattened into single-row Markdown headers ("Train: Empty", etc.). Bold cells in the PDF are rendered in **bold**.
- Figures: only captions, sub-captions and text printed inside the figure are transcribed. Visual content is NOT transcribed unless stated.
- Equations are in LaTeX; multi-letter italic variables use \mathit{}.
- Markers used: [FIGURE N: ...] and [UNCERTAIN TRANSCRIPTION: ...].
-->

<!-- Page 1 -->

Received March 25, 2026; revised XXX; accepted XXX; date of publication XXX; date of current version XXX.

Digital Object Identifier 10.1109/ACCESS.XXXX.XXXXXXX

# Hardware-Aware Optimization for Low-Power FPGA-Based Wildfire Classification in UAV Edge AI

**GONZALO MORENO, PABLO ITUERO, (Member, IEEE) and MARISA LOPEZ-VALLEJO, (Senior Member, IEEE)**

Laboratorio de Sistemas Integrados, Information Processing Telecommunication Center (IPTC), Escuela Técnica Superior de Ingeniería de Telecomunicación, Universidad Politécnica de Madrid, España.

Corresponding author: Pablo Ituero (e-mail: pablo.ituero@upm.es).

This research was funded by the MCIN/AEI/10.13039/501100011033 Spanish Ministry of Science and Innovation within project PID2022-141391OB-C21.

**ABSTRACT** We present a low-power wildfire classification system for unmanned aerial vehicles (UAVs) based on image-level classification using convolutional neural networks (CNNs). To meet the strict energy and resource constraints of edge platforms, the proposed solution is implemented on a Field-Programmable Gate Array (FPGA) using the AMD/Xilinx FINN framework, which enables a fully streaming, dataflow architecture where the entire model is mapped on-chip.
The main challenge addressed in this work is the design of compact yet accurate models that can fit entirely within the limited resources of low-cost FPGAs. To this end, we propose a hardware-aware optimization methodology that combines structural simplification, structured pruning, quantization-aware training, and FPGA-oriented adaptation.
As a result, we deploy a MobileNetV2-based model with fewer than 70K parameters, achieving a throughput above 30 frames per second with a Vivado-estimated FPGA power consumption of 144 mW on a PYNQ-Z1 platform, excluding the processing system and external peripherals. The proposed model maintains competitive performance, with an F1-Macro decrease below 2.5 percentage points compared with larger reference models.

**INDEX TERMS** Wildfires, Unmanned Aerial Vehicles, Convolutional Neural Networks, Energy-Efficient Computing, Edge AI, FPGA.

## I. INTRODUCTION

Wildfires are increasingly widespread, destructive, and major drivers of carbon emissions and economic losses—costing Southern Europe alone €13–21 billion annually in production losses [1], [2]. Mitigating this requires climate action and improved prevention, areas in which Unmanned Aerial Vehicles (UAVs) excel by monitoring vast areas for early fire detection [3]. This work addresses this context by investigating a low-complexity FPGA accelerator for image-level wildfire classification, intended as a first-stage trigger for future UAV integration.

Among potential detection signals (e.g., gas emissions, temperature), RGB images enable long-range monitoring using a UAV’s existing hardware. For computer vision-based detection, Convolutional Neural Networks (CNNs) typically focus on classification or object detection. Object detection models, particularly YOLO-based architectures, are widely preferred; for instance, [4] and [5] modify YOLOv8n [6] to reduce parameters and FLOPs. For classification, CNN-Transformer hybrids address complex real-world backgrounds, with lightweight models proposed for real-time processing [7]–[9], though some rely on satellite imagery [7], [8].

However, many of these models remain too resource-intensive for fully on-chip deployment on low-cost edge FPGAs, which require simplified architectures and low-power operations. Existing deployments span microcontrollers, such as the compact YOLOv8n implementation on the GAP9 [10] or MAX78000 microcontrollers [11], and FPGAs. FPGA approaches typically rely on either full-model mapping via custom dataflow pipelines (also known as streaming) [12], [13] or hardware accelerators such as systolic arrays [14].

Numerous lightweight convolutional neural networks (CNNs) and field-programmable gate array (FPGA) implementations have been proposed for wildfire monitoring. In

<!-- Page 2 -->

many deployment workflows, architectural design, compression, quantization, and hardware mapping are performed as successive stages. Under strict FPGA resource constraints, however, decisions made at one stage can strongly affect the feasibility and efficiency of subsequent stages. We therefore adopt an iterative, constraint-guided co-design workflow in which architectural and numerical transformations are evaluated with the target FPGA implementation in mind.

Our implementation uses a fully streaming dataflow architecture in which model weights, parameters, and intermediate feature-map transfers between layers remain on chip. This avoids repeated off-chip accesses for weights and intermediate activations, while input images and classification outputs are transferred through DMA. The host processor allocates the shared input and output buffers, configures the accelerator, and initiates execution; an interrupt can be used to signal completion.

The main contributions of this work are as follows:

- We present a constraint-guided hardware-aware co-design workflow for balancing classification performance, computational complexity, and FPGA resource utilization under specific deployment constraints.
- We develop a hardware-aware optimization pipeline combining structural simplification, structured pruning, quantization-aware training, and FPGA adaptation. For MobileNetV2, the parameter count decreases from 2.22 million to 68,882, while the deployed model achieves an F1-Macro of 95.32%, 2.33 percentage points below the FP32 reference.
- We implement and validate two optimized CNN architectures (BED and MobileNetV2 Nano) on fully streamed FINN-based FPGA accelerators operating near the 30 fps target at a 4 MHz clock frequency.
- We report post-implementation FPGA resources, latency, throughput, and Vivado-estimated programmable-logic power on a PYNQ-Z1, and contextualize the results using straightforward CPU baselines on Raspberry Pi 3A+ and Raspberry Pi 5.

Although demonstrated on wildfire detection, the proposed methodology can be extended to a broad class of embedded vision applications requiring aggressive CNN optimization under FPGA resource constraints.

The remainder of this paper is structured as follows. Section II details the methodology, Section III the experimental results, and Section IV summarizes the findings and outlines directions for future research.

## II. METHODOLOGY AND DATA

In this work, we adopt a hardware-aware end-to-end co-design methodology, where model architecture, optimization techniques, and FPGA deployment are jointly designed under strict constraints of power, latency, and resource utilization. The workflow is presented in Figure 1. The images are preprocessed before being fed into the model’s training pipeline. Then, the proposed pipeline is formulated as a constraint-driven design space exploration process, where transformations are iteratively applied under explicit hardware and performance constraints:

1) Define the baseline model.
2) Apply candidate structural and numerical transformations to reduce parameter count and MAC operations.
3) Retrain to recover model performance metrics.
4) Evaluate resource usage in the FPGA.
5) Iterate until constraints are met and model can be deployed in the FPGA.

We use three design targets to guide the iterative transformations: reducing MAC operations, parameter count, and estimated programmable-logic power while satisfying the following feasibility constraints:

1) $F_1^{\mathrm{baseline}} - F_1^{\mathrm{optim}} \leq \Delta$.
2) *FPGA Resource Usage* $\leq$ *FPGA Resource Available*.
3) *Throughput* $\geq$ *target fps*.

These targets are addressed through a sequence of structured transformations guided by hardware-aware heuristics; the workflow is not intended to provide a globally optimal solution.

The software tools used in the workflow are summarized in Figure 1: Albumentations for data augmentation, PyTorch for model training, AIMET for structured pruning, Brevitas for quantization, and FINN for FPGA compilation and implementation. Separate Python environments are used for model training, AIMET-based compression, Brevitas quantization, and FINN-based FPGA generation in order to satisfy the dependency requirements of each stage.

### A. DATASETS AND PREPROCESSING

Public RGB datasets for wildfire image classification vary substantially in size, label definitions, scene origin, and train–test organization. BoWFire [15] is too small for training the models considered here, while VisiFire [16] contains frames extracted from a limited number of videos and may therefore include highly correlated samples. Other datasets use binary fire labels, include indoor scenes, or do not provide splits suitable for the smoke–fire multi-label task. FIgLib [17] and PyroNear2024 [18] contribute toward more standardized evaluation, but no single benchmark is yet universally adopted.

#### 1) DFire and FASDD

To support the multi-label classification experiments, we derived a classification dataset by combining two publicly available object-detection datasets: DFire [19] and FASDD [20]. Both datasets provide bounding box annotations and distinguish between fire and smoke, enabling multi-label classification. DFire includes images collected from surveillance cameras, synthetic renderings, and web sources. FASDD consists of three subsets; we used the CV and UAV subsets. The CV subset contains synthetic and web-sourced images, while the UAV subset comprises real images captured by drones and surveillance systems. Both datasets include scenes spanning the absence of visible fire or smoke, smoke-only and fire-only

<!-- Page 3 -->

**FIGURE 1. End-to-end workflow.**

[FIGURE 1: consultar original.pdf; el contenido visual no se ha transcrito. Text printed inside the figure: logos "Albumentations", "PyTorch", "FINN / XILINX", "AIMET / Qualcomm", "Brevitas / XILINX"; blocks "Preprocess" (- Data Augmentation, - Resize, - Normalization), "Training" (- Multi-label classification, - Hyperparameters), "Deployment" (- Model transformation, - Folding setup, - Resource allocation), "Optimization" (- Architecture, Pruning, - Quantization, - FPGA adaptation); arrow labels "METRICS", "WEIGHTS / MAC", "DSP / BRAM / LUT".]

conditions, and the simultaneous presence of smoke and fire, thereby providing examples of the four label combinations considered in the multi-label classification task.

We converted these object detection datasets into classification datasets by removing bounding boxes and using the entire image as input. We acknowledge that transforming object detection into classification removes spatial localization information, which may reduce sensitivity to small or distant smoke regions. As a result, the model is required to rely on global image features, which may not fully represent the underlying localized phenomena. On the other hand, by leveraging datasets with bounding-box annotations, we ensure that positive labels are grounded in localized evidence.

The resulting dataset comprises 141,938 images, with 82.8% used for training and 17.2% for testing, as detailed in Table 1. The original training and test assignments provided by each source dataset are preserved. This facilitates reconstruction of the combined split, although it does not guarantee independence between images originating from different datasets. FASDD provides explicit information about the origin of its images and does not include DFire among its listed sources. However, both datasets are partially based on images collected from the internet, where content reuse is common and difficult to fully trace. As a result, strict independence between datasets cannot be guaranteed, and the presence of overlapping or near-duplicate samples cannot be ruled out. This limitation may lead to optimistic performance estimates and therefore the reported results should be interpreted with caution in terms of generalization.

Cross-dataset generalization is not evaluated in this work. Our primary objective is to assess the in-distribution effect of architectural and hardware constraints on the constructed split. Consequently, the reported metrics should not be interpreted as evidence of generalization to unseen datasets or to the full range of operational wildfire scenarios.

To expose the models to a broader range of appearance variations during training, we applied data augmentation using Albumentations, including:

- Photometric transformations: brightness, contrast, hue, saturation adjustments, and Gaussian blur;
- Geometric transformations: random shift and rotation.

All images were resized to a fixed resolution of 224×224 or 230×230, and normalized to the range [-1, 1].

### B. MODELS

During UAV operation, frames containing wildfire evidence are expected to be relatively infrequent. An object detector must nevertheless compute localization and classification outputs for every input frame, requiring additional prediction heads and feature-map processing even when no event is present. We therefore use image-level classification as a lower-complexity first-stage trigger for the resource-constrained edge device. Furthermore, in a critical application such as wildfire detection, positive classification can trigger a higher-performance processing unit to execute more advanced object detection algorithms, verify the alert, and guide the UAV to the hotspot. Therefore, our approach should be interpreted as a low-power first-stage trigger, and a trade-off between limited resources and precise localization. The goal of this study is not to solve full wildfire localization, but to explore the minimum predictive signal that can be extracted under strict FPGA constraints. Therefore, the dataset should be interpreted as supporting this reduced problem formulation, rather than representing the complete early detection task. However, we carefully selected models that could also serve as the backbone of future object detection research.

<!-- Page 4 -->

**TABLE 1. DFire and FASDD datasets.**

| Dataset | Train: Empty | Train: Smoke | Train: Fire | Train: Both | Train: Total | Test: Empty | Test: Smoke | Test: Fire | Test: Both | Test: Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DFire | 7833 | 4681 | 944 | 3763 | 17221 | 2005 | 1186 | 220 | 895 | 4306 |
| FASDD UAV | 9989 | 4234 | 175 | 6518 | 20916 | 1997 | 846 | 35 | 1303 | 4181 |
| FASDD CV | 32666 | 19512 | 10459 | 16793 | 79430 | 6533 | 3902 | 2091 | 3558 | 15884 |
| Total | 50488 | 28427 | 11578 | 27074 | **117567** | 10535 | 5934 | 2346 | 5556 | **24371** |

We configure the models for a multi-label classification task with two output neurons, enabling the identification of images containing smoke, fire, both, or neither. Binary cross-entropy is the loss function used, applied independently to each output neuron and summed. A fixed threshold of 0.5 is applied independently to the sigmoid output of each neuron to obtain the binary smoke and fire decisions.

Models are trained with Adam using an initial learning rate of $10^{-3}$ and a batch size of 64. A ReduceLROnPlateau scheduler monitors the held-out evaluation loss and multiplies the learning rate by 0.8 after two epochs without an improvement greater than 0.001, down to a minimum of $10^{-6}$. Depending on the optimization stage, the configured schedule comprises 100 or 150 epochs. We do not apply early stopping; checkpoints are stored periodically and when either the evaluation loss or F1-Macro improves, and the checkpoint with the highest F1-Macro is retained for the reported comparison. The experiments use one training run per configuration without a globally fixed random seed; consequently, the reported results do not quantify run-to-run variability.

We evaluated with two models: BED [21] and MobileNetV2 [13].

#### 1) BED

BED is a lightweight object detection model designed for low-power, resource-constrained microcontrollers. Its architecture is simple and shallow, inspired by SqueezeNet’s strategy [22] of using 1x1 convolutions to reduce the number of input channels before applying more computationally expensive 3x3 convolutions. The model employs max pooling, ReLU activation, and average pooling before the final dense layers. To adapt BED for classification, we removed its detection head and replaced it with fully connected layers, culminating in an output layer with two neurons.

#### 2) MobileNetV2

MobileNetV2 is a more advanced model built around inverted residual bottlenecks, a block illustrated in Figure 2 from the original paper. It is designed to reduce computational cost while preserving rich feature representations. The block architecture follows these steps:

1) Pointwise convolution (1x1 kernel): Expands the number of input channels, followed by ReLU6.
2) Depthwise convolution (3x3 kernel): Applies a separate filter to each input channel, reducing the number of parameters and computational complexity. This step is also followed by ReLU6 activation.

**FIGURE 2. Inverted Residual Block.**

[FIGURE 2: consultar original.pdf; el contenido visual no se ha transcrito. Text printed inside the figure: "3x3", "Relu6, Dwise", "Relu6, 1x1", "+".]

3) Pointwise-linear convolution: Controls the number of block output channels.
4) Skip connections: If input and output have the same number of channels, a residual connection is added, allowing the network to learn identity mappings. This helps mitigate the vanishing/exploding gradient problem.

#### 3) Reference Architectures

As reference architectures, we train MobileNetV2, MobileNetV3 [23], and ShuffleNetV2 [24] using transfer learning with pretrained weights. We also train the MobileViTV3-v1 architecture [25] from scratch to include a CNN–Transformer architecture in the comparison. Its implementation follows the MobileViTV3-v1 configuration with MobileViTV3 fusion blocks rather than the original MobileViT architecture.

### C. DESIGN RULES FOR HARDWARE-AWARE OPTIMIZATION

We organize the optimization procedure into coarse- and fine-grained transformations. Coarse structural changes first reduce network depth and width to define a feasible architectural region. Structured pruning, quantization-aware training, and FPGA-oriented adaptation are then applied to refine the candidate model while monitoring classification performance and implementation constraints.

Finally, in Section II-C5, we introduce two additional optimizations, applied only to MobileNetV2 Nano: reducing input image dimensions and pruning based on model sparsity.

#### 1) Structural Simplification

Structural simplification first reduces network width and depth, including the removal of complete blocks. The specific transformations are selected iteratively by comparing

<!-- Page 5 -->

**FIGURE 3. Spatial SVD.**

[FIGURE 3: consultar original.pdf; el contenido visual no se ha transcrito. Text printed inside the figure: "3x3", "Width", "Height", "Out Channels"; arrow down; "3x1", "Width", "Height", "Mid Channels", "+", "1x3", "Width", "Height", "Out Channels".]

F1-Macro, parameter count, MAC operations, and estimated FPGA feasibility rather than by applying a fixed compression ratio.

Early layers operate on large feature maps, so increasing their channel width has a substantial effect on MAC operations. Deeper layers operate on smaller spatial dimensions but commonly use more channels, increasing parameter storage. We therefore evaluate reductions in both width and depth rather than assuming that either dimension can be minimized independently.

By jointly reducing the layer width and model depth, we define a compact baseline architecture that significantly lowers computational cost and memory requirements while maintaining acceptable performance. This simplified architecture serves as the starting point for the subsequent fine-grained optimization stages.

#### 2) Structured Pruning

Next, we apply two consecutive structured pruning strategies to convolutional layers: spatial singular value decomposition (SVD) and channel pruning. We used the Qualcomm AIMET framework to implement these techniques [26].

##### a: Spatial SVD

As Figure 3 shows, spatial SVD decomposes convolution kernels, transforming, for example, a 3×3 kernel into sequential 3×1 and 1×3 kernels. It preserves the number of input and output channels of the original layer, so it does not affect the rest of the model.

The number of weights and multiply-accumulate operations (MAC) of the original convolution, if stride is 1 and padding is applied, are:

$$
\begin{aligned}
W_{Ori} &= k^2 \cdot \mathit{In} \cdot \mathit{Out} \\
\mathit{MAC}_{Ori} &= k^2 \cdot \mathit{In} \cdot \mathit{Out} \cdot h \cdot w
\end{aligned}
\tag{1}
$$

The equations for spatial SVD convolutions are:

$$
\begin{aligned}
W_{SVD} &= k \cdot \mathit{In} \cdot \mathit{Mid} + k \cdot \mathit{Mid} \cdot \mathit{Out} \\
\mathit{MAC}_{SVD} &= (k \cdot \mathit{In} \cdot \mathit{Mid} + k \cdot \mathit{Mid} \cdot \mathit{Out}) \times (h \cdot w)
\end{aligned}
\tag{2}
$$

where:

| Symbol | Meaning |
|---|---|
| $W$ | = number of weights |
| $k$ | = kernel dimensions |
| $\mathit{In}$ | = convolution input channels |
| $\mathit{Mid}$ | = convolution output channels of first spatial SVD convolution |
| $\mathit{Out}$ | = convolution output channels |
| $h$ | = input image height |
| $w$ | = input image width |

In the original convolution, $k_h = k_w = k$, so $k_h \cdot k_w = k^2$. In spatial SVD, $k_h \cdot k_w = k_h \cdot 1 = 1 \cdot k_w = k$. The compression ratio can be calculated as follows:

$$
\frac{W_{SVD}}{W_{Ori}} = \frac{\mathit{MAC}_{SVD}}{\mathit{MAC}_{Ori}} = \frac{\mathit{Mid} \cdot (\mathit{In} + \mathit{Out})}{k \cdot \mathit{In} \cdot \mathit{Out}}
\tag{3}
$$

For the very common case where $\mathit{Out} = 2\mathit{In}$ and $k = 3$, the compression ratio can be simplified and, if $\mathit{Mid} < \mathit{Out}$, the layer is compressed:

$$
\frac{W_{SVD}}{W_{Ori}} = \frac{\mathit{MAC}_{SVD}}{\mathit{MAC}_{Ori}} = \frac{\mathit{Mid}}{\mathit{Out}}
\tag{4}
$$

##### b: Channel Pruning

Channel pruning, on the other hand, completely removes selected input channels from the convolution layer, so the compression ratio is $\mathit{In}_{Pruning}/\mathit{In}_{Ori}$.

#### 3) Quantization

We apply quantization-aware training (QAT) using Brevitas [27], which integrates with the FINN compiler. Uniform affine quantization may use either symmetric or asymmetric ranges [28]. Symmetric quantization fixes the zero point at zero, whereas asymmetric quantization permits a nonzero zero point to better match non-centered value distributions. Although asymmetric quantization can reduce quantization error for some distributions, it requires additional zero-point handling in hardware. We therefore use symmetric quantization to simplify the FPGA implementation.

A second design choice is whether quantization is applied per tensor or per channel. Per-tensor quantization uses one scale and zero point for an entire tensor, whereas per-channel quantization uses separate values for individual channels. The latter can better accommodate the different weight ranges commonly observed across depthwise-convolution channels, at the cost of storing and handling additional scale parameters. We therefore quantize convolutional weights per channel, while activations and fully connected layers use per-tensor quantization. Throughout the Results section, model size is reported as the total parameter count. For quantized models, this count includes additional learned scale parameters introduced by the quantizers where applicable. Consequently, a

<!-- Page 6 -->

quantized model may have a slightly higher reported parameter count than its floating-point counterpart even though the number of convolutional and fully connected weight coefficients is unchanged.

Quantization is also selected with FPGA implementation constraints in mind. For the supported FINN operators and the target DSP-packing configuration, 4-bit inputs and weights can allow up to four low-precision operations to share a DSP, whereas precisions above 4 bits and up to 8 bits can allow up to two operations per DSP. The effective packing depends on the layer dimensions, folding factors, and synthesis mapping.

We apply the following quantization scheme:

- Input image: 8-bit per-tensor quantization.
- Convolution layers: 4-bit per-channel quantization.
- Activations: 4-bit per-tensor quantization.
- Linear layers: 8-bit per-tensor quantization.

#### 4) FPGA Adaptation and Implementation

We implement the models on a PYNQ-Z1 development board, which integrates a Zynq-7000 System-on-Chip (SoC) with an ARM dual-core processor and a Z-7020 FPGA. The implementation follows the operator support available in the FINN toolchain used for this study. In this configuration, stream multiplication required by the MobileNetV3 squeeze-and-excitation block is not supported directly, and the readily supported activation functions are limited to ReLU and HardTanh. [UNCERTAIN TRANSCRIPTION: printed as "Hard-" / "Tanh." across a line break; verificar contra original.pdf whether the intended form is "HardTanh" or "Hard-Tanh"] These constraints influence the selection and adaptation of candidate architectures.

##### a: Design Guidelines for FPGA Deployment

The number of input/output channels and kernel dimensions for each layer are critical, as they need to conform to specific divisibility rules to optimize parallelization and achieve maximum throughput. For example, to translate convolutional layers into HW, they are restructured into a convolutional input generator that performs the image-to-column operation to unroll the convolution, followed by matrix multiplication. Matrix multiplication is the most computationally intensive operation, and parallelization is achieved using two folding factors, SIMD (Single Instruction Multiple Data) and PE (Processing Elements). SIMD defines the number of input elements processed simultaneously and PE the number of output channels computed in parallel. These parameters must satisfy the following equations:

$$
\begin{aligned}
(\mathit{In} \cdot k^2) \bmod \mathit{SIMD} &= 0, \\
\mathit{Out} \bmod \mathit{PE} &= 0.
\end{aligned}
\tag{5}
$$

For matrix-multiplication layers using 4-bit inputs and weights, the estimated DSP allocation under the target packing configuration is given by:

$$
\begin{aligned}
\mathit{DSP} &= \lceil \mathit{PE}/4 \rceil \cdot \mathit{SIMD}, \\
\mathit{PE} \bmod 4 &= 0.
\end{aligned}
\tag{6}
$$

In a streaming dataflow accelerator, steady-state throughput is limited by the layer with the largest cycle count. Matrix-vector units commonly account for a substantial fraction of computation and parameter storage in the evaluated models. For a matrix-multiplication layer, the cycle count is estimated as follows:

$$
\mathit{MatMul\ Cycles} = \frac{\mathit{Out}}{\mathit{PE}} \cdot \frac{\mathit{In} \cdot k^2}{\mathit{SIMD}} \cdot \mathit{In}_{\mathit{Vectors}}
\tag{7}
$$

where $\mathit{In}_{\mathit{Vectors}}$ is related to the input dimensions of the layer.

Gathering all these details, we define hardware-aware design constraints that guide all architectural and optimization decisions. These constraints are implicitly enforced throughout the pipeline, ensuring that intermediate models remain close to feasible FPGA implementations.

1) **Channel Multiplicity**: All input and output channels must be multiples of at least 4, preferably 8, to facilitate efficient configuration of folding factors. This constraint does not apply to input images with three RGB channels or to the final output neurons, which depend on the number of target classes.
2) **Frequency and Throughput**: We use 100 MHz as the initial implementation target. FINN first proposes folding factors that satisfy the divisibility constraints in (5). SIMD is increased to reduce the layer cycle count, followed by PE when additional output-channel parallelism is required. The resulting configuration is then adjusted to improve DSP packing and to keep BRAM, LUT, DSP, and slice utilization within the Z-7020 capacity. Matrix-multiplication layers that cannot be assigned to the available DSPs are mapped to LUTs, convolutional input generators are preferentially allocated to BRAM, and resource margin is reserved for FIFOs, DMA, and AXI infrastructure.
3) **Adaptive fps Scaling**: After generating the 100 MHz implementations, we evaluate lower clock frequencies without changing the folding factors. Throughput scales with clock frequency, while the Vivado-estimated dynamic programmable-logic power decreases and the allocated resources remain unchanged. We select operating points near 30 fps and 5 fps to represent two potential camera-processing rates.

##### b: Power Consumption Estimation

Finally, we estimate the power consumption of the Z-7020 programmable logic using the Xilinx Vivado power analysis tools. Switching activity is obtained from post-implementation simulations using batches of four images. The reported values include the estimated static and dynamic power associated with the FPGA implementation, but exclude the processing system, external peripherals, and board-level components. Consequently, these results should be interpreted as accelerator-level estimates rather than measurements of the total PYNQ-Z1 board power.

<!-- Page 7 -->

#### 5) Further Optimizations

We next examine two additional modifications to MobileNetV2 Nano. The 4-bit input configuration in Table 5 reduces F1-Macro to 94.44% without providing a sufficient implementation benefit, while reducing the first convolution does not materially improve the observed hardware–accuracy trade-off. We therefore evaluate input-resolution scaling and removal of all-zero convolutional channels:

- **Reducing Input Image Dimensions**: This approach provides a straightforward way to decrease the computational cost while preserving the total number of model parameters.
- **Model Sparsity**: We identify convolutional output channels whose weight coefficients are all zero and remove eligible channels using custom graph-transformation code. To preserve valid FPGA folding factors, some zero-valued channels are retained when the resulting channel count would violate the multiplicity constraints in Section II-C4a. The effect of this transformation is reported in Section II-C5.

### D. BASELINE COMPARISON WITH GENERAL-PURPOSE PROCESSORS

The comparison with general-purpose processors is intended to provide deployment context rather than to establish an intrinsic advantage for either architecture. FPGA dataflow implementations offer application-specific parallelism but require a more specialized development flow, whereas CPU platforms provide greater software flexibility and can benefit from platform-specific optimization. The configurations evaluated here therefore represent particular implementation points rather than the maximum attainable efficiency of each device family.

To contextualize the FPGA implementation, we benchmark the reference and compact CNN models on Raspberry Pi 3A+ and Raspberry Pi 5 in 32-bit floating-point format. In the power-performance comparison, we select for each platform the model with the highest F1-Macro among those capable of operating near or above 30 fps. This results in MobileNetV2 Nano for the PYNQ-Z1, ShuffleNetV2 for the Raspberry Pi 3A+, and MobileNetV3 for the Raspberry Pi 5.

The workload depends on the evaluated metric. Inference timing is measured using repeated synthetic inputs, whereas the Raspberry Pi board-power measurements use a continuous loop that acquires images from a Logitech C270 USB webcam and performs inference. The PYNQ-Z1 programmable-logic power values are obtained from the post-implementation simulation procedure described in Section II-C4b. On the FPGA, the ARM processor configures and triggers the accelerator. On the Raspberry Pi platforms, inference is performed on the CPU in 32-bit floating-point format using ONNX Runtime, which may apply graph-level optimizations such as fusing BatchNorm and convolution operations. We do not apply quantization or explicitly configure multithreading. Consequently, these results represent a straightforward CPU baseline rather than the maximum performance attainable through platform-specific optimization.

For the Raspberry Pi platforms, two metrics are evaluated:

- **Inference Time:** We measured the time to process 5,000 images using a synthetic constant input. The *first-image latency* and the average *throughput time* were recorded separately.
- **Power Consumption:** We used a power meter to measure power while running an infinite inference loop on images captured in real time from the camera. The minimum and maximum power draw observed are reported to account for variance due to background tasks.

This comparison provides a reference for contextualizing the accelerator results, but it should not be interpreted as a direct board-to-board power comparison. The FPGA values correspond to Vivado estimates for the programmable logic, whereas the Raspberry Pi values are obtained through external measurements during camera acquisition and inference. Therefore, the results illustrate the potential efficiency of the custom accelerator, while a conclusive system-level comparison would require measuring all platforms with the same instrumentation and system boundaries.

### E. CLASSIFICATION METRICS

Because the task is formulated as multi-label classification, the smoke and fire outputs are evaluated independently. For each label, true positives (*TP*), false positives (*FP*), true negatives (*TN*), and false negatives (*FN*) are computed after converting the model output into a binary decision. Accuracy measures the proportion of correct binary decisions, precision measures the proportion of predicted positives that are correct, recall measures the proportion of actual positives that are detected, and the F1 score is their harmonic mean.

$$
\begin{aligned}
\mathit{Accuracy} &= \frac{\mathit{TP} + \mathit{TN}}{\mathit{TP} + \mathit{FP} + \mathit{TN} + \mathit{FN}} \\
\mathit{Precision} &= \frac{\mathit{TP}}{\mathit{TP} + \mathit{FP}} \\
\mathit{Recall} &= \frac{\mathit{TP}}{\mathit{TP} + \mathit{FN}} \\
F1 &= 2 \times \frac{\mathit{Precision} \cdot \mathit{Recall}}{\mathit{Precision} + \mathit{Recall}}
\end{aligned}
\tag{8}
$$

To compare the models with a single number, we use F1-Macro:

$$
F1_{\mathit{Macro}} = \frac{F1_{\mathit{Smoke}} + F1_{\mathit{Fire}}}{2}
\tag{9}
$$

## III. RESULTS

This section reports the effect of the successive workflow stages on F1-Macro, parameter count, MAC operations, and FPGA implementation metrics. Because each stage is applied to the output of the preceding stage, the reported differences describe the observed optimization trajectory rather than independent causal ablations.

<!-- Page 8 -->

### A. MODEL OPTIMIZATION

We apply the optimization stages sequentially to BED and MobileNetV2 and report the resulting trajectory in F1-Macro, parameter count, and MAC operations. Established lightweight architectures are first trained as reference models. Structural simplification, structured pruning, quantization, and FPGA adaptation are then evaluated in the order in which they are applied; therefore, differences between rows should not be interpreted as independent ablations.

#### 1) Reference Models

Table 2 presents the trained reference models. MobileNetV2 achieves the highest F1-Macro but is the largest and most computationally intensive model.

**TABLE 2. Reference Models.**

| Model | Parameters | MAC | F1-Macro |
|---|---:|---:|---:|
| MobileNetV2 | 2.22 M | 300 M | 97.65 % |
| MobileNetV3 | 1.52 M | 55 M | 97.07 % |
| ShuffleNetV2 | 0.37 M | 39 M | 94.95 % |
| MobileViTV3\* | 0.74 M | 93 M | 95.87 % |

\* No pre-trained weights, trained from scratch.

**TABLE 3. BED optimization.**

| Model | Parameters | MAC | F1-Macro |
|---|---:|---:|---:|
| BED Original | 292866 | 411 M | 95.97 % |
| BED Simplified | 93266 | 226 M | 95.89 % |
| BED Compressed | | | |
| - Spatial SVD | 57969 | 180 M | 95.86 % |
| - Pruning | 53520 | 153 M | 95.80 % |
| BED Quantized | 53901 | 153 M | 94.70 % |
| **BED FPGA** | 64353 | 110 M | **94.54 %** |

<!-- In the PDF, the whole "BED FPGA" label is bold and the F1-Macro value 94.54 % is bold. -->

#### 2) BED Optimization

Table 3 summarizes the BED optimization sequence. Structural simplification reduces F1-Macro by 0.08 percentage points while substantially decreasing parameters and MAC operations. Spatial SVD and channel pruning introduce additional decreases of 0.03 and 0.06 percentage points, respectively. Quantization produces the largest single decrease, from 95.80% to 94.70%, followed by a further 0.16-point decrease during FPGA-oriented adaptation.

Spatial SVD and channel pruning produce non-standard channel counts, such as 7 or 51, which lead to inefficient folding on the FPGA. We therefore apply an additional adaptation step that makes channel counts multiples of 4 or 8. This increases the parameter count from 53,901 to 64,353, while hardware-oriented architectural changes reduce the MAC count from 153 million to 110 million. Padding is removed to simplify the implementation, and the input resolution is adjusted to 230 × 230. The resulting sequence of valid convolutions reduces the feature map entering the average-pooling layer from 28 × 28 to 20 × 20. Overall, BED FPGA achieves an approximately fourfold reduction in both parameters and MAC operations relative to the original BED model, with an F1-Macro decrease of 1.43 percentage points.

**FIGURE 5. BED architectures.**

- (a) BED Original architecture.
- (b) BED FPGA architecture. Green layers represent structured pruning optimization.

[FIGURE 5: consultar original.pdf; el contenido visual no se ha transcrito (layer diagrams; small in-figure labels are not legible at the rendered resolution). Legible in-figure text in (b) includes "Structured Pruning", "CONV 3.4", "Smoke", "Fire".]

<!-- Note: the PDF contains no figure labelled "FIGURE 4"; figure numbering goes from FIGURE 3 to FIGURE 5. -->

Figure 5 presents a visual comparison between the original BED model and the final BED FPGA model used for deployment. To better illustrate the optimization process, we focus on convolution 3.4. Initially, this layer consisted of a convolution operation with 32 input channels, 64 output channels, and a 3x3 kernel. After applying spatial SVD and channel pruning, it is transformed into two successive convolutions: the first with 32 input channels, 51 output channels, and a 3x1 kernel, followed by a second convolution with 51 input channels, 57 output channels, and a 1x3 kernel. Since this structure is inefficient for FPGA deployment, it is adjusted to a more optimized configuration: a first convolution with 32 input channels, 44 output channels, and a 3x1 kernel, followed by a second convolution with 44 input channels, 64 output channels, and a 1x3 kernel. The compression ratio can be computed with equation 4:

$$
\frac{W_{SVD}}{W_{Ori}} = \frac{\mathit{Mid}}{\mathit{Out}} = \frac{44}{64} = 68.75\%
\tag{10}
$$

Thus, the layer retains 68.75% of its original weights, which means that it is compressed by a factor of $1 - 0.6875 = 0.3125$.

The final architecture is detailed in Table 4. All convolution layers and the first fully connected layer are followed by BatchNorm and ReLU. Layers optimized with spatial SVD incorporate a Mid channel and two kernels, forming a block structured as: Convolution1-BatchNorm, Convolution2-BatchNorm-ReLU. To reach the same maximum fps achieved by the MobileNetV2-based model, which will be presented in Section III-A3, two computationally

<!-- Page 9 -->

heavy convolution layers and their preceding activations are quantized to 2 bits.

**TABLE 4. BED architecture optimized and adapted for the FPGA.**

| Input | Layer | Mid | Out | Kernel |
|---|---|---:|---:|---:|
| 230<sup>2</sup>x3 | Conv1 | - | 12 | 3 |
| 228<sup>2</sup>x12 | MaxPool | - | 12 | 2 |
| 114<sup>2</sup>x12 | Conv2 | 24 | 16 | 3x1, 1x3 |
| 112<sup>2</sup>x16 | MaxPool | - | 16 | 2 |
| 56<sup>2</sup>x16 | Conv3.1 | - | 16 | 1 |
| 56<sup>2</sup>x16 | Conv3.2 | 16 | 32 | 3x1, 1x3 |
| 54<sup>2</sup>x32 | Conv3.3 | - | 32 | 1 |
| 54<sup>2</sup>x32 | Conv3.4\* | 44 | 64 | 3x1, 1x3 |
| 52<sup>2</sup>x64 | MaxPool | - | 64 | 2 |
| 26<sup>2</sup>x64 | Conv4.1 | - | 32 | 1 |
| 26<sup>2</sup>x32 | Conv4.2\* | - | 64 | 3 |
| 24<sup>2</sup>x64 | Conv4.3 | - | 32 | 1 |
| 24x32 | Conv4.4 | 44 | 60 | 3x1, 1x3 |
| 22<sup>2</sup>x60 | Conv4.5 | - | 32 | 1 |
| 22<sup>2</sup>x32 | Conv4.6 | 20 | 64 | 3x1, 1x3 |
| 20<sup>2</sup>x64 | AvgPool | - | 64 | 20 |
| 1x1x64 | FC | - | 32 | - |
| 32 | FC | - | 2 | - |

\* Weights and activations quantized with 2 bits.

<!-- The Input entry of the Conv4.4 row is printed as "24x32" (without the superscript 2 used in the other rows); transcribed as printed. -->

#### 3) MobileNetV2 Optimization

Several experiments are conducted to compare different configurations of MobileNetV2 and MobileNetV3:

- MobileNetV2 Nano: Inspired by BED optimizations, we derive a compact variant through progressive scaling of width, depth, and expansion factors under hardware constraints. The design follows MobileNet principles, prioritizing depthwise separable convolutions and channel configurations aligned with FPGA folding requirements.
- ECA attention layers [29] are added to MobileNetV2 Nano to evaluate whether channel attention improves classification performance. Because FINN does not support the required element-wise stream multiplication, this variant is evaluated only at the model level and is not deployed. It does not improve F1-Macro.
- MobileNetV2 width multiplier 0.1: We evaluate the standard MobileNetV2 width-scaling mechanism with a multiplier of 0.1.
- MobileNetV3 Mini: We evaluate a custom compact MobileNetV3 variant with reduced depth and width.

Among the compact architectures in Table 5, MobileNetV2 Nano achieves the highest FP32 F1-Macro at 95.93%. Adding ECA changes the score by −0.10 percentage points, whereas the standard width-multiplier configuration and MobileNetV3 Mini score 2.71 and 0.56 points lower, respectively. After quantization, replacing ReLU with ReLU6 reduces F1-Macro from 95.45% to 94.19%, and using a 4-bit input reduces it to 94.44%. We therefore retain ReLU and 8-bit input quantization. Spatial SVD and channel pruning are not applied to this architecture because its channel counts are already aligned with FPGA folding requirements, while its skip connections complicate graph-consistent channel removal.

**TABLE 5. MobileNetV2 and MobileNetV3 experiments.**

| Model | Parameters | MAC | F1-Macro |
|---|---:|---:|---:|
| MobileNetV2 Nano (Ours) | 68882 | 42 M | **95.93 %** |
| MobilenetV2 Nano ECA (Ours) | 68892 | 42 M | 95.83 % |
| MobileNetV2 Width Mult = 0.1 | 78311 | 12 M | 93.22 % |
| MobilenetV3 Mini (Ours) | 76858 | 26 M | 95.37 % |
| Quantized | | | |
| - MobileNetV2 Nano | 68914 | 42 M | **95.45 %** |
| - MobileNetV2 Nano ReLU6 | 68914 | 42 M | 94.19 % |
| - MobileNetV2 Nano 4b Input | 68914 | 42 M | 94.44 % |

**TABLE 6. MobileNetV2 Nano: t is the expansion factor, c the number of channels, n the block repetitions and s the stride.**

| Input | Operator | t | c | n | s |
|---|---|---:|---:|---:|---:|
| 224<sup>2</sup>x3 | conv2d | - | 32 | 1 | 2 |
| 112<sup>2</sup>x32 | bottleneck | 1 | 8 | 1 | 1 |
| 112<sup>2</sup>x8 | bottleneck | 2 | 16 | 2 | 2 |
| 56<sup>2</sup>x16 | bottleneck | 2 | 24 | 2 | 2 |
| 28<sup>2</sup>x24 | bottleneck | 4 | 32 | 3 | 2 |
| 14<sup>2</sup>x32 | bottleneck | 2 | 64 | 2 | 1 |
| 14<sup>2</sup>x64 | conv2d 1x1 | - | 128 | 1 | 1 |
| 14<sup>2</sup>x128 | avgpool 14x14 | - | - | 1 | - |
| 1x1x128 | conv2d 1x1 | - | 2 | - | - |

### B. FPGA IMPLEMENTATION

We evaluate the deployed BED FPGA and MobileNetV2 Nano accelerators in terms of fixed-point classification performance, post-implementation resource utilization, latency, throughput, and Vivado-estimated programmable-logic power. Resource estimates used during design-space exploration are distinguished from post-implementation utilization reports.

#### 1) Impact of Quantization and Deployment on Model Accuracy

Table 7 compares FP32, quantized-software, and FPGA-deployed F1-Macro. Quantization reduces BED by 1.26 percentage points and MobileNetV2 Nano by 0.48 points. FPGA deployment introduces further decreases of 0.16 and 0.13 points, respectively. MobileNetV2 Nano therefore retains the higher F1-Macro throughout the low-precision deployment stages.

**TABLE 7. F1-Macro across FP32, quantized-software, and FPGA-deployed models.**

| Model | F1-Macro: FP32 | F1-Macro: Quantized | F1-Macro: FPGA |
|---|---:|---:|---:|
| BED FPGA | 95.80 % | 94.54 % | 94.38 % |
| MobileNetV2 Nano | 95.93 % | 95.45 % | **95.32** % |

<!-- In the PDF, only the number "95.32" is bold; the "%" sign is not. -->

Table 8 reports the corresponding per-label software metrics for MobileNetV2 Nano. At the fixed 0.5 decision threshold, quantization primarily reduces smoke recall, while fire

<!-- Page 10 -->

recall remains above 98%. Per-label FPGA precision and recall are not included because F1-Macro is the common metric retained across all deployment stages.

#### 2) BED FPGA Estimated Resource Evolution

Figure 6a shows the estimated Z-7020 resource requirements across the BED optimization stages. The initial mapping requires approximately four times the available DSP capacity. Structural simplification and compression reduce the estimated requirements, but the directly compressed network remains infeasible because its irregular channel counts lead to inefficient folding. The final adaptation enforces channel multiplicity and compatible folding factors before adding FIFO, DMA, and AXI infrastructure.

We anticipate that MobileNetV2 Nano can achieve a theoretical maximum throughput of 784 fps at 100 MHz, if images are continuously fed into the pipeline at that rate. As a final fine-tuning step for BED optimization, to achieve a throughput comparable to that of MobileNetV2 Nano, we apply selective mixed-precision quantization to computationally dominant layers, as presented in Table 4. This quantization greatly reduces the LUTs needed for such layers, compared to the 4-bit version, and highlights the achievable degree of granularity.

Ultimately, estimated resources are below the maximum available, except DSPs, which are exhausted but not needed for missing peripherals. Therefore, there is enough room to incorporate FIFOs, DMA and AXI, and the model deployed achieves 781 fps at a 100 MHz FPGA clock, matching MobileNetV2 Nano, allowing direct comparison of power consumption.

#### 3) MobileNetV2 FPGA Estimated Resource Requirements

As shown in Figure 6b, the original MobileNetV2 has an estimated maximum throughput of 500 fps under maximum unfolding, but would require 414 BRAMs, 72,095 LUTs, and 505 DSPs. These values correspond to 296%, 136%, and 230% of the Z-7020 resources, respectively, making the design infeasible on the target FPGA. MobileNetV2 Nano reduces the MAC count from 300 million to 42 million and brings the estimated resource requirements within the device capacity. Parameter counts are omitted from Figure 6b because they cannot be displayed clearly on the same scale as MAC operations; they decrease from 2.22 million to 68,882.

**FIGURE 6. Resources throughout optimization steps.**

- (a) BED: estimated resource use across optimization stages.
- (b) MobileNetV2: estimated resource use across optimization stages.

[FIGURE 6: consultar original.pdf; el contenido visual (bar/line values) no se ha transcrito. Text printed inside the figure:
(a) Title "Xilinx Z-7020: BED / Resources Utilization % - Weights (K) & MAC (M)"; left axis "RESOURCES (%)" (0–450); right axis "WEIGHTS (K) & MAC (M)" (0–400); categories "ORIGINAL", "MANUAL", "COMPRESSED", "FPGA"; legend "LUT 53200", "BRAM 140", "DSP 220", "Weights", "MAC".
(b) Title "Xilinx Z-7020: MobileNetV2 / Resources Utilization % - MAC (M)"; left axis "RESOURCES (%)" (0–300); right axis "MAC (M)" (0–300); categories "ORIGINAL", "NANO"; legend "LUT 53200", "BRAM 140", "DSP 220", "MAC".]

#### 4) Post-Implementation Resource Utilization

Figure 7 shows the post-implementation resource utilization of both accelerators, including FIFOs, DMA, and AXI infrastructure. BED FPGA uses all 220 available DSPs, so additional matrix-multiplication operations are mapped to LUTs. MobileNetV2 Nano uses 111 DSPs, consistent with its lower computational load of 42 million MAC operations compared with 110 million for BED FPGA. Most MobileNetV2 Nano convolutions are 1 × 1 pointwise operations, while its 3 × 3 depthwise convolutions are mapped to LUT-based vector operations in this FINN implementation.

MobileNetV2 Nano uses more BRAM than BED FPGA because its skip connections require larger inter-layer FIFOs to prevent pipeline stalls. Individual BRAM blocks may have unused capacity because weights are partitioned across memories to provide parallel access to multiple output channels. This capacity overhead is a consequence of the selected parallelism and DSP-packing strategy. Slice utilization is close to the device limit for both accelerators, constraining further increases in unfolding or peripheral logic.

<!-- Page 11 -->

**TABLE 8. Per-label software metrics for MobileNetV2 Nano at a decision threshold of 0.5.**

| Stage | Smoke (%): Precision | Smoke (%): Recall | Smoke (%): F1 | Fire (%): Precision | Fire (%): Recall | Fire (%): F1 | F1-Macro (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| FP32 | 95.66 | 94.67 | 95.16 | 95.24 | 98.20 | 96.70 | 95.93 |
| Quantized software | 95.82 | 93.48 | 94.64 | 94.43 | 98.19 | 96.27 | 95.45 |

**FIGURE 7. BED FPGA and MobileNetV2 Nano resources**

[FIGURE 7: consultar original.pdf; el contenido visual (bar values) no se ha transcrito. Text printed inside the figure: title "BED FPGA vs MobilenetV2 Nano: Resources Utilization %"; y axis 0–100; categories "Slice 13300", "LUT 53200", "LUTRAM 17400", "FF 106400", "BRAM 140", "DSP 220"; legend "BED FPGA", "MobileNetV2 Nano".]

#### 5) FPGA Power Consumption and Inference Times

After evaluating the maximum throughput at 100 MHz, we reduce the FPGA clock frequency in the power model, as shown in Table 9. At 4 MHz, the estimated static power dominates the programmable-logic consumption. A separate Vivado power estimate at 100 kHz produced a total of 109 mW, indicating the approximate static-power floor of the implementation. Reducing the frequency to 666.67 kHz further decreases the estimated dynamic power while maintaining operation near 5 fps for both models.

MobileNetV2 Nano has lower estimated programmable-logic power than BED FPGA, primarily because it uses fewer DSPs and LUTs. The difference is most pronounced in the estimated dynamic power at 100 MHz and becomes smaller as the clock frequency is reduced and static power dominates.

Inference time is assessed through first-image latency and throughput for subsequent images.

At 4 MHz, the measured throughput times correspond to approximately 27.4 fps for BED FPGA and 33.6 fps for MobileNetV2 Nano. Thus, the 4 MHz configuration represents operation near the 30 fps target rather than an identical throughput for both models.

#### 6) Further Optimizations: Image Dimensions and Sparsity

Focusing on MobileNetV2 Nano, additional optimizations are explored: input image dimensions and model sparsity.

Table 10 evaluates MobileNetV2 Nano at three input resolutions while adjusting the FPGA clock to remain near the 30 fps target. Reducing the input from 224 × 224 to 160 × 160 and 112×112 decreases the MAC count from 42 million to 21 million and 10 million, respectively, without changing the parameter count. The estimated dynamic programmable-logic power decreases from 31 mW to 14 mW and 6 mW, while F1-Macro decreases by 1.14 and 1.64 percentage points.

Figure 8 identifies convolutional output channels whose weight coefficients are all zero. Graph-level removal of these channels, while retaining channel counts required for FPGA folding, reduces the parameter count from 68,882 to 41,178 and the MAC count from 42 million to 36 million. The reported F1-Macro is unchanged, but the 14% MAC reduction does not increase the maximum throughput beyond the original implementation. Additional FIFO requirements also offset part of the resource reduction. These results show that parameter removal alone does not necessarily improve a streaming accelerator when the critical path and inter-layer buffering remain limiting factors.

### C. RASPBERRY PI COMPARISON: INFERENCE AND POWER

Figure 9a reports FP32 inference times on Raspberry Pi 3A+ and Raspberry Pi 5. Sustaining 30 fps requires an output interval no greater than 33.33 ms. ShuffleNetV2 is the only evaluated model below this limit on Raspberry Pi 3A+, whereas several models meet it on Raspberry Pi 5; MobileNetV3 has the highest F1-Macro among those candidates.

Figure 9b places the Vivado-estimated programmable-logic power of MobileNetV2 Nano near 30 fps alongside measured board-level power for the selected Raspberry Pi models. MobileNetV3 on Raspberry Pi 5 achieves the highest F1-Macro of the three selected configurations. Because the FPGA and Raspberry Pi values use different system boundaries and measurement methods, the absolute power values should not be used for a direct energy-efficiency ranking.

At 100 MHz, the two accelerators produce an output approximately every 1.2–1.3 ms, with Vivado-estimated programmable-logic power between 0.94 W and 1.33 W. The dataflow architecture does not use the ARM cores for convolutional inference, so they remain available in principle for acquisition and control tasks; however, end-to-end processor utilization was not measured. These results demonstrate accelerator-level throughput rather than a complete system-level energy advantage.

<!-- Page 12 -->

**TABLE 9. Vivado-estimated programmable-logic power and FPGA inference times at different clock frequencies.**

| | Estimated PL Power (mW): Static | Estimated PL Power (mW): Dynamic | Estimated PL Power (mW): Total | Inference (ms): Latency | Inference (ms): Throughput |
|---|---:|---:|---:|---:|---:|
| ∼780 fps / 100 MHz | | | | | |
| - BED FPGA | 136 | 1190 | 1327 | 2.02 | 1.28 |
| - MobileNetV2 Nano | 128 | 815 | 943 | 1.99 | 1.19 |
| ∼30 fps / 4 MHz | | | | | |
| - BED FPGA | 112 | 39 | 151 | 52.9 | 36.55 |
| - MobileNetV2 Nano | 112 | 31 | 144 | 49.67 | 29.80 |
| ∼5 fps / 666.67 kHz | | | | | |
| - BED FPGA | 112 | 7 | 119 | 317.48 | 212.62 |
| - MobileNetV2 Nano | 111 | 5 | 116 | 297.86 | 178.93 |

**TABLE 10. Input-dimension experiments operating near the 30 fps target.**

| Input Resolution | MACs | F1-Macro | FPGA Clock | Estimated PL Power (mW): Static | Estimated PL Power (mW): Dynamic | Estimated PL Power (mW): Total |
|---|---:|---:|---:|---:|---:|---:|
| 224 × 224 | 42 M | 95.45 % | 4 MHz | 112 | 31 | 144 |
| 160 × 160 | 21 M | 94.31 % | 2 MHz | 110 | 14 | 124 |
| 112 × 112 | 10 M | 93.81 % | 1 MHz | 119 | 6 | 117 |

**FIGURE 8. MobileNetV2 Nano: Sparsity.**

[FIGURE 8: consultar original.pdf; el contenido visual (bar values) no se ha transcrito. Text printed inside the figure: title "MobileNetV2 Nano Sparsity"; y axis "# Output Channels" (ticks 0, 32, 64, 96, 128); x axis "Convolutional Layer" with categories "Conv0" to "Conv30"; legend "Out Channels", "All Zero Filters".]

## IV. DISCUSSION AND FUTURE WORK

Wildfire monitoring motivates compact onboard inference, and this work evaluates a fully on-chip FPGA accelerator as a first-stage image classifier. At 4 MHz, the deployed BED FPGA and MobileNetV2 Nano designs operate at approximately 27.4 fps and 33.6 fps, respectively. Many general-purpose image-classification networks exceed the resources available for fully on-chip mapping on the Z-7020 and address substantially broader label spaces than the two-output task considered here.

Beyond the specific models implemented, the main contribution of this work lies in demonstrating a practical, constraint-guided workflow that combines architectural simplification, compression, quantization, and FPGA adaptation. The step-by-step results show how these transformations reduce model complexity and affect classification performance and hardware feasibility.

The optimization stages have different roles in the observed trajectory. Structural simplification produces the largest reductions in parameters and MAC operations, quantization enables low-precision FINN mapping, and FPGA adaptation enforces valid channel counts and folding factors. MobileNetV2 Nano requires fewer MAC operations and DSPs than BED FPGA, whereas BED uses less BRAM because it does not require the same skip-connection buffering.

As demonstrated in Section III-A, we successfully optimized a model with 2.22 million parameters and 300 million MAC operations, reducing it to fewer than 70,000 parameters and 42 million MAC operations, achieving a 32× reduction in parameters and a 7× reduction in computation, while maintaining an F1-Macro decrease below 2.5 percentage points.

Although MobileNetV2 Nano achieves the better trade-off, applying the workflow to both MobileNetV2 and BED shows that it can accommodate two structurally different CNN families. Its applicability to a broader range of architectures remains to be evaluated.

<!-- Page 13 -->

**FIGURE 9. Raspberry Pi inference time and comparison between measured Raspberry Pi board power and Vivado-estimated PYNQ-Z1 programmable-logic power.**

- (a) Raspberry Pi inference times.
- (b) Power and F1-Macro of the selected models operating near 30 fps.

[FIGURE 9: consultar original.pdf; bar heights, error bars and line values of (b) are not transcribed.
Text printed inside (a): title "Inference time in Raspberry Pi"; y axis "Inference (ms)" (0–200); groups "Raspi 3A+", "Raspi 5"; legend, in order: "MobileNetV2", "MobileNetV3", "ShuffleNetV2", "MobileViTV3", "BED Compressed", "MobileNetV Nano" (printed this way in the legend). Data labels printed on the bars (transcribed from the rendered figure; verificar contra original.pdf): Raspi 3A+: 209, 91, 28, 179, 48, 41; Raspi 5: 40, 16, 6, 38, 13, 8 (in legend order).
Text printed inside (b): title "Power vs F1-Macro at 30 fps"; left axis "Power (W)" (0–6); right axis "F1-Macro %" (92–98); categories "Raspi 3A+", "Raspi 5", "PYNQ-Z1"; legend "Power", "Best Model at 30 fps".]

The optimization process relies on heuristic transformations and expert knowledge of CNN structure and FPGA constraints, which limits automation and does not guarantee optimality. In the evaluated streaming implementations, reducing MAC operations and feature-map dimensions has a greater effect on throughput and estimated power than reducing parameter count alone. Future work could investigate hardware-aware neural architecture search to automate parts of this process and explore improved trade-offs between classification performance and implementation cost.

Although the programmable-logic power estimates are low, the total PYNQ-Z1 board power was not measured, and ultra-low-power microcontroller systems may provide lower system-level consumption for less demanding throughput targets. At the reduced clock frequencies considered here, static power dominates the estimated programmable-logic consumption. Future work should include board-level measurements with consistent system boundaries and investigate devices that support voltage scaling to reduce static power.

The proposed system shows promise for onboard wildfire detection, but several real-world factors of UAV deployment remain to be evaluated. In operational scenarios, image quality can be impacted by motion blur, rapid viewpoint changes, altitude variations, atmospheric conditions, and variable lighting. Additionally, smoke visibility varies significantly depending on weather conditions and camera orientation. The training pipeline includes photometric and geometric augmentation intended to expose the models to some of these variations, but this does not replace field validation. Future work should therefore evaluate the complete system during representative UAV flights, including changes in altitude, motion, illumination, weather, and camera orientation.

The proposed architecture is intended as a continuously operating first-stage trigger. A positive classification could activate more computationally intensive verification algorithms or adaptive UAV behavior, such as redirecting the platform toward a suspicious region. This cascaded operating concept remains to be validated as part of a complete onboard system.

Finally, the comparison with Raspberry Pi 3A+ and Raspberry Pi 5 provides context for the performance of the proposed accelerator. The PYNQ-Z1 implementation combines competitive F1-Macro with high accelerator throughput and low estimated programmable-logic power. However, because the reported power values were obtained using different methodologies and system boundaries, no definitive board-level energy-efficiency ranking can be established from the present experiments.

This work demonstrates the feasibility of combining architectural optimization and FPGA deployment in a constraint-guided workflow for fully on-chip wildfire classification. The resulting design achieves a compact implementation and high accelerator throughput on the target FPGA. The workflow may also inform other resource-constrained vision applications, although its transferability requires application-specific evaluation.

## CONFLICT OF INTEREST STATEMENT

The authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

## AUTHOR CONTRIBUTIONS

GM carried out the technical work, including model design, optimization, and FPGA implementation, under the supervision of PI. The original idea and project objectives were jointly conceived by GM, PI, and ML-V. GM and PI wrote the manuscript. PI and ML-V secured the funding and provided continuous guidance. All authors contributed to the discussion of the results and reviewed and approved the final manuscript.

## ACKNOWLEDGMENTS

The authors used ChatGPT (OpenAI) to assist with language editing to improve the clarity of parts of the manuscript. The authors developed and verified all technical content, methodology, results, and conclusions.

<!-- Page 14 -->

## DATA AVAILABILITY STATEMENT

The DFire and FASDD source datasets used in this study are publicly available from the sources cited in Section II. The classification dataset was derived from their object-detection annotations while preserving the original training and test splits. Processing scripts, split definitions, and additional materials supporting reproduction of the study are available from the corresponding author upon reasonable request.

## REFERENCES

<!-- Italics used in the PDF for journal/proceedings names are rendered with *...*. Typographic quotes as printed. -->

[1] B. Byrne, J. Liu, and K. e. a. Bowman, “Carbon emissions from the 2023 Canadian wildfires,” *Nature*, vol. 633, pp. 835–839, 2024. [Online]. Available: https://www.nature.com/articles/s41586-024-07878-z

[2] S. Meier, R. Elliott, and E. Strobl, “The regional economic impact of wildfires: Evidence from Southern Europe,” *Journal of Environmental Economics and Management*, vol. 118, p. 102787, 2023. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0095069623000050

[3] S. P. H. Boroujeni, A. Razi, S. Khoshdel, F. Afghah, J. L. Coen, L. O’Neill, P. Fule, A. Watts, N.-M. T. Kokolakis, and K. G. Vamvoudakis, “A comprehensive survey of research towards AI-enabled unmanned aerial systems in pre-, active-, and post-wildfire management,” *Information Fusion*, vol. 108, p. 102369, 2024. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S1566253524001477

[4] L. Lei, R. Duan, F. Yang, and L. Xu, “Low Complexity Forest Fire Detection Based on Improved YOLOv8 Network,” *Forests*, vol. 15, no. 9, p. 1652, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID:272786788

[5] Y. Zheng, F. Tao, Z. Gao, and J. Li, “FGYOLO: An Integrated Feature Enhancement Lightweight Unmanned Aerial Vehicle Forest Fire Detection Framework Based on YOLOv8n,” *Forests*, vol. 15, no. 10, p. 1823, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID:273471397

[6] R. Varghese and M. Sambath, “YOLOv8: A Novel Object Detection Algorithm with Enhanced Performance and Robustness,” in *2024 International Conference on Advances in Data Engineering and Intelligent Computing Systems (ADICS)*, 2024, pp. 1–6.

[7] S. Chaturvedi, C. Shubham Arun, and P. Singh Thakur, “Ultra-lightweight convolution-transformer network for early fire smoke detection,” *Fire Ecology*, vol. 20, no. 83, 2024. [Online]. Available: https://doi.org/10.1186/s42408-024-00304-9

[8] Y. Zheng, G. Zhang, S. Tan, Z. Yang, D. Wen, and H. Xiao, “A forest fire smoke detection model combining convolutional neural network and vision transformer,” *Frontiers in Forests and Global Change*, vol. Volume 6 - 2023, 2023. [Online]. Available: https://www.frontiersin.org/journals/forests-and-global-change/articles/10.3389/ffgc.2023.1136969

[9] H. Yar, Z. A. Khan, T. Hussain, and S. W. Baik, “A modified vision transformer architecture with scratch learning capabilities for effective fire detection,” *Expert Systems with Applications*, vol. 252, p. 123935, 2024. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0957417424008017

[10] J. Moosmann, H. Müller, N. Zimmerman, G. Rutishauser, L. Benini, and M. Magno, “Flexible and Fully Quantized Lightweight TinyissimoYOLO for Ultra-Low-Power Edge Systems,” *IEEE Access*, vol. 12, p. 75093–75107, 2024. [Online]. Available: http://dx.doi.org/10.1109/ACCESS.2024.3404878

[11] A. Dabbous, L. Lazzaroni, F. Bellotti, S. Presentación, A. Pighetti, and R. Berta, “TinyML Acceleration with MAX78000,” in *Proceedings of SIE 2024*, M. Valle, P. Gastaldo, and E. Limiti, Eds. Springer Nature Switzerland, 2025, pp. 468–474.

[12] J. Weixiong, Y. Heng, and H. Yajun, “A High-Throughput Full-Dataflow MobileNetv2 Accelerator on Edge FPGA,” *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, vol. 42, no. 5, pp. 1532–1545, 2023.

[13] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, “MobileNetV2: Inverted Residuals and Linear Bottlenecks,” in *The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2019, pp. 4510–4520.

[14] F. N. Peccia, S. Pavlitska, T. Fleck, and O. Bringmann, “Efficient Edge AI: Deploying Convolutional Neural Networks on FPGA with the Gemmini Accelerator,” in *2024 27th Euromicro Conference on Digital System Design (DSD)*, 2024, pp. 418–426. [Online]. Available: https://api.semanticscholar.org/CorpusID:271865687

[15] D. Y. T. Chino, L. P. S. Avalhais, J. F. Rodrigues, and A. J. M. Traina, “BoWFire: Detection of Fire in Still Images by Integrating Pixel Color and Texture Analysis,” in *2015 28th SIBGRAPI Conference on Graphics, Patterns and Images*. IEEE, 2015, p. 95–102.

[16] A. Cetin, “Computer Vision Based Fire Detection Dataset,” 2014. [Online]. Available: Available online: http://signal.ee.bilkent.edu.tr/VisiFire/ (accessed on 1 February 2024)

[17] A. Dewangan, Y. Pande, H.-W. Braun, F. Vernon, I. Perez, I. Altintas, G. W. Cottrell, and M. H. Nguyen, “FIgLib & SmokeyNet: Dataset and Deep Learning Model for Real-Time Wildland Fire Smoke Detection,” *Remote Sensing*, vol. 14, no. 4, 2022. [Online]. Available: https://www.mdpi.com/2072-4292/14/4/1007

[18] M. Lostanlen, N. Isla, J. Guillen, F. Veith, C. Buc, and V. Barriere, “Scrapping The Web For Early Wildfire Detection: A New Annotated Dataset of Images and Videos of Smoke Plumes In-the-wild,” 2024. [Online]. Available: https://arxiv.org/abs/2402.05349

[19] P. de Venâncio, A. Lisboa, and A. Barbosa, “An automatic fire detection system based on deep convolutional neural networks for low-power, resource-constrained devices,” *Neural Comput & Applic*, vol. 34, p. 15349–15368, 2022. [Online]. Available: https://doi.org/10.1007/s00521-022-07467-z

[20] M. Wang, P. Yue, L. Jiang, D. Yu, T. Tuo, and J. Li, “An open flame and smoke detection dataset for deep learning in remote sensing based fire detection,” *Geo-spatial Information Science*, p. 1–16, 2024.

[21] G. Wang, Z. P. Bhat, Z. Jiang, Y.-W. Chen, D. Zha, A. C. Reyes, A. Niktash, M. G. Ulkar, O. E. Okman, and X. Hu, “BED: A Real-Time Object Detection System for Edge Devices,” *Proceedings of the 31st ACM International Conference on Information and Knowledge Management*, 2022. [Online]. Available: https://api.semanticscholar.org/CorpusID:246863797

[22] F. N. Iandola, M. W. Moskewicz, K. Ashraf, S. Han, W. J. Dally, and K. Keutzer, “SqueezeNet: AlexNet-level accuracy with 50x fewer parameters and <1MB model size,” *ArXiv*, vol. abs/1602.07360, 2016. [Online]. Available: https://api.semanticscholar.org/CorpusID:14136028

[23] A. Howard, M. Sandler, B. Chen, W. Wang, L.-C. Chen, M. Tan, G. Chu, V. Vasudevan, Y. Zhu, R. Pang, H. Adam, and Q. Le, “Searching for MobileNetV3,” in *2019 IEEE/CVF International Conference on Computer Vision (ICCV)*, 2019, pp. 1314–1324.

[24] N. Ma, X. Zhang, H. Zheng, and J. Sun, “ShuffleNet V2: Practical Guidelines for Efficient CNN Architecture Design,” *ArXiv*, vol. abs/1807.11164, 2018. [Online]. Available: https://api.semanticscholar.org/CorpusID:51880435

[25] S. N. Wadekar and A. Chaurasia, “MobileViTv3: Mobile-Friendly Vision Transformer with Simple and Effective Fusion of Local, Global and Input Features,” *arXiv preprint arXiv:2209.15159*, 2022. [Online]. Available: https://arxiv.org/abs/2209.15159

[26] Qualcomm Innovation Center, “AI Model Efficiency Toolkit (AIMET),” https://github.com/quic/aimet, 2024, accessed: 2025-07-01.

[27] G. Franco, A. Pappalardo, and N. J. Fraser, “Xilinx/brevitas,” 2025. [Online]. Available: https://doi.org/10.5281/zenodo.3333552

[28] M. Nagel, M. Fournarakis, R. A. Amjad, Y. Bondarenko, M. van Baalen, and T. Blankevoort, “A White Paper on Neural Network Quantization,” *ArXiv*, vol. abs/2106.08295, 2021. [Online]. Available: https://api.semanticscholar.org/CorpusID:235435934

[29] Q. Wang, B. Wu, P. F. Zhu, P. Li, W. Zuo, and Q. Hu, “ECA-Net: Efficient Channel Attention for Deep Convolutional Neural Networks,” *2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 11 531–11 539, 2019. [Online]. Available: https://api.semanticscholar.org/CorpusID:203902337

<!-- Page 15 -->

## AUTHOR BIOGRAPHIES

<!-- This heading does not exist in the PDF; it is added only to structure the biography block. Author photographs are not transcribed. -->

[PHOTO: Gonzalo Moreno — not transcribed]

**GONZALO MORENO** received the B.Sc. degree in Telecommunication Technologies and Services Engineering and the M.Sc. degree in Electronic Systems Engineering from the Universidad Politécnica de Madrid (UPM), Madrid, Spain, in 2023 and 2024, respectively. From April 2024 to May 2025, he was a Researcher with the Integrated Systems Laboratory, Escuela Técnica Superior de Ingenieros de Telecomunicación, UPM, where he worked on the design, optimization, and deployment of convolutional neural networks on resource-constrained devices, including low-power microcontrollers and FPGAs. Since May 2025, he has been an FPGA Design Engineer in the private sector. His research interests include edge artificial intelligence, energy-efficient deep learning, neural network quantization and compression, FPGA-based neural network acceleration, embedded AI systems, and computer vision for resource-constrained devices.

[PHOTO: Pablo Ituero — not transcribed]

**PABLO ITUERO** received the M.Sc. degree in Electrical Engineering from Universidad Politécnica de Madrid (UPM), Madrid, Spain, and KTH Royal Institute of Technology, Stockholm, Sweden, in 2005, and the Ph.D. degree in Telecommunications Engineering from UPM in 2012.

He is currently an Associate Professor with the Department of Electronic Engineering at UPM, where he is a member of the Integrated Systems Laboratory (LSI) and the Information Processing and Telecommunications Center (IPTC). He is also a Member of the IEEE. His research interests include digital and VLSI design, FPGA-based architectures, variation- and reliability-aware design, and hardware acceleration for artificial intelligence. His current research focuses particularly on neuromorphic computing and spiking neural networks, with an emphasis on efficient hardware architectures for edge and space applications.

[PHOTO: Marisa López-Vallejo — not transcribed]

**MARISA LÓPEZ-VALLEJO** (M’99-SM’20) received the M.S. and Ph.D. degrees from the Universidad Politécnica de Madrid, Madrid, Spain, in 1993 and 1999, respectively. Since 2016 she is a Full Professor at the Department of Electronic Engineering, Universidad Politécnica de Madrid. She was before with Lucent Technologies, Bell Laboratories, Murray Hill, NJ, USA, as a Member of the Technical Staff. During the academic year 2015-2016, she was visiting professor at the Microsystems Technology Lab, MIT, USA.

Her research interests include low-power, radiation and PVT-aware design, computer-aided diagnostic methods and tools, and application-specific high-performance programmable architectures. Last decade she has focused her research on the reliability of CMOS circuits and memristive memories as well as on new architectures to support reliable design beyond 20nm. She has been the coordinator of a set of national and international projects in these areas. She has supervised 14 PhD theses and has published more than 100 papers in journals and conferences in the field.
