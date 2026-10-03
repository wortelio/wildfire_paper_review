# Response matrix — Access-2026-39017

Manuscript: "Hardware-Aware Optimization for Low-Power FPGA-Based Wildfire Classification in UAV Edge AI" (IEEE Access).
Decision: reject with encouragement to resubmit. **Only one resubmission is allowed.** Every concern must be addressed, or rebutted with arguments.

Sources:
- Reviewer text: `reviewer_1.md`, `reviewer_2.md`, `reviewer_3.md` (verbatim copies of `paper_review_email.md`).
- Manuscript: `../original.pdf` (authoritative) and `../paper.md` (transcription).
- Author-detected issues: `../paper_comments.md`.

Created: 2026-10-03. This is a first-pass triage: high-level actions and rough estimates for planning only. No resolution work has been done yet.

**Resubmission deliverables required by the editor:**
1. Response-to-reviewers document, giving for each comment: (a) the concern, (b) the response, (c) the action taken.
2. Highlighted PDF showing every change, including grammatical ones.
3. Clean manuscript as LaTeX/Word plus PDF.

---

## 1. Legend

**Type** (the action classes from `claude_instructions/02_review_objective.md`):

| Code | Meaning | Code | Meaning |
|---|---|---|---|
| ED | Editorial-only change | RR | Re-run existing experiment / re-evaluate checkpoints |
| CL | Methodological clarification | NX | New experiment or analysis |
| DS | Expanded discussion | ST | Additional statistical analysis |
| JU | Justification of a design decision | FG | Figure modification |
| IC | Correction of an inconsistency | TB | Table modification |
| VR | Verification of a result | CD | Code modification |
| RH | Recovery of a historical experiment / provenance | SY | New FPGA synthesis / FINN build |
| RF | References / literature work | MS | New hardware measurement (power, latency, throughput) |

**Effort** (human work, in person-days `pd`; compute time is listed separately):
- XS ≤ 0.5 pd
- S ≈ 1 pd
- M = 2–3 pd
- L = 4–7 pd
- XL > 7 pd

**Priority:**
- P1: required for acceptance (major comment, internal inconsistency, or a claim that could be judged incorrect).
- P2: should be addressed.
- P3: minor, or a suggestion.

**Status:** Open → In progress → Done (evidence + commit) → Response drafted.

**Evidence levels:** VERIFIED / STRONG EVIDENCE / INFERENCE / HYPOTHESIS / UNKNOWN.

---

## 2. Work packages (WP)

Most comments overlap. Each is assigned to one work package, so that duplicated concerns are handled once.

| WP | Theme | Comments | Human effort | Compute / hardware |
|---|---|---|---|---|
| WP1 | Editorial, abstract, references, small fixes | R1-Abs-1/2, R1-Meth-1/2/3, R2-m4/m6/m7, R3-11/13/14/15/18/19, A-1, A-2 | 4 pd | — |
| WP2 | Positioning, novelty, related work, comparison table with prior FPGA/MCU work | R2-G, R2-M1, R2-M7, R3-7, R1-Intro-1..4 | 8–10 pd | — |
| WP3 | Methodology clarifications and design justifications | R1-Meth-4..8, R1-Res-1/2, R1-Disc-5/6, R2-m1/m2/m3, R3-6 | 5–6 pd | — |
| WP4 | Evaluation protocol: validation vs test, duplicates, class imbalance | **R3-1**, R2-M2, R3-12, A-3, A-4, A-5 | 2 pd (disclosure only) to 10–12 pd (re-train) | 0 to 3–4 GPU-days |
| WP5 | Statistical robustness (multiple seeds) | R2-M3 | 3–4 pd | 4–9 GPU-days |
| WP6 | Classification metrics: per-label, FPGA output, threshold | R1-Res-7/8, R1-Disc-1, R2-M4, R2-m8 | 4–6 pd | < 1 GPU-day (re-evaluation); FPGA/board TBD |
| WP7 | Hardware-result consistency and timing methodology | **R3-2, R3-3, R3-4**, R3-16, R1-Res-4, R1-Meth-7, R2-m5 | 5–8 pd | + 3–5 pd if board re-measurement is needed |
| WP8 | Power reporting and low-power claim | **R3-8**, R3-9, R3-17, R3-20, R2-M5, R1-Res-5, R1-Disc-2 | 3–4 pd | + 3–5 pd for a PYNQ-Z1 board-level measurement |
| WP9 | Cross-platform comparison | R3-10, R1-Res-3 | 1 pd (specs) to 3–4 pd (Nano on RPi) | RPi 3A+ and RPi 5 hardware |
| WP10 | MobileNetV2 Nano stage-by-stage trajectory | R3-5 (+ R1-Meth-4) | 2–4 pd | possibly FINN estimates only (fast) |
| WP11 | Sparsity / streaming-bottleneck analysis | R2-M6, R1-Res-6 | 3–4 pd | — (existing FINN reports) |
| WP12 | Discussion: limitations, deployment role, acceptability | R1-Disc-3/4, R1-Intro-2 | 2–3 pd | — |
| WP13 | Response letter, highlighted PDF, final consistency pass | all | 4–5 pd | — |

---

## 3. Matrix

### Reviewer 1

| ID | Concern (summary) | Paper | Type | WP | High-level action | Effort | Prio | Evidence / notes | Status | Commit |
|---|---|---|---|---|---|---|---|---|---|---|
| R1-Abs-1 | Abstract must be one paragraph with no abbreviations (IEEE Access rule) | Abstract | ED | WP1 | Rewrite as a single paragraph; expand UAV, CNN, FPGA, PYNQ… | XS | P1 | Formal requirement; the current abstract has 3 paragraphs and many acronyms | Open | |
| R1-Abs-2 | Abstract should mention BED and the CPU baselines | Abstract | ED | WP1 | Add one sentence each; combine with the power qualification of R3-8 | XS | P2 | | Open | |
| R1-Intro-1 | Support Sec. I paragraph 4 with references | §I ¶4 ("Numerous lightweight CNNs and FPGA implementations…") | RF | WP2 | Add wildfire-FPGA references; feeds the related-work table | S | P1 | The paragraph currently has no citations | Open | |
| R1-Intro-2 | Explain why low-power accelerators and lightweight, accurate nets matter on UAVs | §I | DS, RF | WP2 | Short motivation (payload, battery, latency) with references | S | P2 | | Open | |
| R1-Intro-3 | State the research purpose clearly | §I | ED | WP2 | Explicit objective statement | XS | P2 | | Open | |
| R1-Intro-4 | State and justify that low power is prioritized over throughput | §I, §II-C4a | JU | WP2 | Explain the design target (≈30 fps at minimum power, i.e. clock scaling) | S | P2 | Consistent with the paper's adaptive-clock strategy | Open | |
| R1-Meth-1 | References and versions for all tools | §II, Fig. 1 | RF, ED | WP1 | Add citations and a versions table | S | P1 | STRONG EVIDENCE (conda envs + FINN checkout): torch 2.1.2, brevitas 0.10.2, qonnx 0.3.0, albumentations 1.3.1 (`pytorch_brevitas`); aimet_torch 1.32.1 (`pytorch_aimet`); FINN v0.10.1; Vivado 2022.2. The FP32 training environment is still to be confirmed (INFERENCE: `pytorch_23`, torch 2.3.1) | Open | |
| R1-Meth-2 | Attribute [23] as the source of Fig. 2 | Fig. 2 caption | ED | WP1 | Fix the caption; check which paper the figure comes from | XS | P1 | INFERENCE: the drawing style matches the MobileNetV3 paper (its Fig. 3 shows the V2 block), so the reviewer is probably right | Open | |
| R1-Meth-3 | Cite spatial SVD independently of AIMET | §II-C2a | RF | WP1 | Cite the original low-rank / spatial-SVD work | XS | P2 | | Open | |
| R1-Meth-4 | How is structural simplification performed? Automated or systematic? | §II-C1 | CL | WP3/WP10 | Describe the manual, heuristic procedure and its decision rules; link to the Nano trajectory (R3-5) | M | P1 | Manual, iterative procedure (STRONG EVIDENCE: historical runs `test_v00_387k` → `test_v02_small_100k` → `test_v04_mini_resnet_70k`) | Open | |
| R1-Meth-5 | Channel pruning on kernels, feature maps or both? Order of SVD/pruning and its impact | §II-C2 | CL, RH | WP3 | Clarify; look for historical runs that tried both orders | S–M | P2 | HYPOTHESIS: `uav/code/quantization/qualcomm_aimet/{pruning_after_spatial_svd, spatial_svd_after_pruning}.ipynb` may already contain the comparison | Open | |
| R1-Meth-6 | Eqs. (5) and (7) assume square kernels, but SVD kernels are rectangular | §II-C4a | CL | WP3 | Generalize to k_h·k_w | XS | P2 | Same family as R2-m2 | Open | |
| R1-Meth-7 | "Adaptive fps scaling" suggests run-time clock change | §II-C4a | CL, ED | WP3/WP7 | Rename to design-time clock scaling; explain how it was evaluated | XS | P1 | Depends on R2-m5 (were the lower clocks physically run?) | Open | |
| R1-Meth-8 | Justify the simplified models as the baseline for compression | §II-C | JU | WP3 | Rationale: feasibility region first, then fine-grained steps | S | P2 | | Open | |
| R1-Res-1 | Table 3 MAC: BED FPGA reports effective MACs while raw MACs increased | Table 3 | CL, VR, TB | WP3 | Recompute MACs with one consistent definition; clarify the column | S | P2 | Check `train/bed/model_MACs*.ipynb`. The 110 M figure comes from the 230×230 no-padding variant | Open | |
| R1-Res-2 | Fig. 6a: are the estimates for FP32 or fixed point? | Fig. 6a | CL, RH, FG | WP3 | State the precision used for each FINN estimate | S | P2 | STRONG EVIDENCE: FINN estimates use quantized ONNX models (`bed_evol_to_finn_driver/models_evolution/*_Bipolar.onnx`, `experiments_bed_evolution_brevitas/`). The bit-width for each stage still needs confirming | Open | |
| R1-Res-3 | Give RPi 3A+ / Pi 5 configuration (SoC, RAM, clock, ISA, OS) | §II-D, Fig. 9a | ED, TB | WP9 | Add a platform table | XS–S | P2 | Needs information from the author (OS image, ONNX Runtime version) | Open | |
| R1-Res-4 | Table 9: rename "Latency/Throughput" to "Initial/Average"; give std | Table 9 | TB, MS | WP7 | Rename; std is only possible if repeated board timings exist | M | P1 | Depends on R3-2 (were the times measured or simulated?) | Open | |
| R1-Res-5 | Add GOPS/W for FPGA and CPU | Table 9 / new table | TB, NX | WP8 | Compute from MACs, throughput and power, with a boundary caveat | S | P2 | Must be qualified (PL estimate vs board measurement), see R3-8 | Open | |
| R1-Res-6 | Fig. 8: percentage of all-zero channels | Fig. 8 | FG | WP11 | Add the percentages | XS–S | P3 | Data in `finn/mobilenet/onnx_modify/` notebooks | Open | |
| R1-Res-7 | Report all §II-E metrics (accuracy, precision, recall, F1) | Tables 2, 3, 5, 7 | TB, RR | WP6 | Re-evaluate the existing checkpoints | M | P2 | Checkpoints and logs exist for most stages (STRONG EVIDENCE, see provenance report) | Open | |
| R1-Res-8 | Expand on the F1 drop at quantization for both nets | §III-A, §III-B1 | DS | WP6 | Per-label analysis (smoke recall) | S | P2 | | Open | |
| R1-Disc-1 | Is the final FPGA F1-Macro acceptable for deployment? | §IV | DS | WP6 | Discuss together with recall-oriented metrics (R2-M4) | S | P2 | | Open | |
| R1-Disc-2 | Relate power to UAV flight autonomy | §IV | DS | WP8 | Back-of-envelope battery-share estimate, clearly caveated | S | P3 | Only meaningful with a board-level boundary (R3-8) | Open | |
| R1-Disc-3 | Role of the UAV in the detection chain; reliability and fault tolerance if it is the primary trigger | §II-B, §IV | DS | WP12 | Clarify the first-stage-trigger concept; add a limitations note | S | P2 | | Open | |
| R1-Disc-4 | What are the limitations? | §IV | DS | WP12 | Dedicated "Limitations" subsection that consolidates the scattered caveats | S | P1 | | Open | |
| R1-Disc-5 | Criteria for choosing BED and MobileNet | §II-B | JU | WP3 | Explicit criteria, merged with R3-6 | XS–S | P2 | | Open | |
| R1-Disc-6 | Criteria for choosing the FPGA board | §II-C4 | JU | WP3 | Cost, FINN support, low-end Zynq | XS | P2 | | Open | |

### Reviewer 2

R2 recommends publication after revision. The main concerns are novelty positioning, reliability of the model comparisons, and comparison with prior co-design work.

| ID | Concern (summary) | Paper | Type | WP | High-level action | Effort | Prio | Evidence / notes | Status | Commit |
|---|---|---|---|---|---|---|---|---|---|---|
| R2-G | Methodological novelty is limited; position the work as a documented practical workflow / case study | Title, Abstract, §I contributions | DS, ED | WP2 | Same action as R2-M1 | — | P1 | | Open | |
| R2-M1 | State the novelty precisely: lessons on folding, buffering, resource balancing, mixed precision | §I, §IV | DS, ED | WP2 | Rewrite the contributions around the optimization trajectory and the FPGA-feasibility lessons | M | P1 | | Open | |
| R2-M2 | Were duplicates / near-duplicates checked across train/test? If not, acknowledge it | §II-A1 | CL, NX | WP4 | At minimum: state clearly that no check was done. Recommended: perceptual-hash check between train and test, reported in the paper | XS (statement) / M (check) | P1 | No duplicate check was found in the historical repo (UNKNOWN; to confirm) | Open | |
| R2-M3 | Single run without fixed seed; repeat selected software experiments (baseline, Nano, configurations with < 0.2 pp differences) and report mean ± std | §II-B, Tables 3, 5 | ST, RR | WP5 | 3–5 seeds on about 3–4 configurations (FP32 and QAT only; no FINN) | L | P1 | STRONG EVIDENCE (file timestamps): ≈12 h per Nano FP32 run, ≈10 h per Nano QAT run, ≈14 h per BED-FPGA QAT run on a shared RTX 4070 Ti, so roughly 90–210 GPU-h. Should be combined with the R3-1 decision | Open | |
| R2-M4 | F1-Macro is insufficient for a trigger: report per-label P/R for the FPGA output, FPR/FNR or PR curves; justify the 0.5 threshold | Tables 7, 8; §II-B | TB, FG, NX, DS | WP6 | Per-label metrics for all stages; PR curves from the software models; threshold analysis (recall-oriented operating point) | M (+M for FPGA per-label) | P1 | How the FPGA F1 (95.32/94.38) was obtained still needs to be traced (board run? `validate.py`?). UNKNOWN | Open | |
| R2-M5 | RPi comparison is context, not an efficiency comparison; label it as such and separate PL-estimated from measured power visually | §II-D, §III-C, Fig. 9b | FG, ED | WP8 | Rework Fig. 9b and its wording; merge with R3-8/R3-17/R3-20 | S | P1 | | Open | |
| R2-M6 | Analyse the sparsity case: bottleneck layer, cycles, FIFOs, initiation interval before and after pruning | §III-B6, Fig. 8 | RH, TB, DS | WP11 | Extract per-layer cycle estimates and FIFO depths from the existing FINN builds (original vs pruned) | M | P2 | Builds exist in `uav/finn/.../my_mblnet_resnet_onnx_modify/experiments/` and `my_mblnet_resnet_to_finn_driver/experiments/` (STRONG EVIDENCE) | Open | |
| R2-M7 | Compare with prior FPGA CNN optimization / co-design work (table: FPGA, network, optimization and quantization, automation, HW performance) | §I (related work), new table | RF, TB | WP2 | Literature survey plus a comparison table; shared with R3-7 | L | P1 | | Open | |
| R2-m1 | Clarify Δ in the feasibility constraint (reviewer reads it as an F_opt/F_baseline ratio) | §II, constraint 1 | CL | WP3 | Define Δ explicitly as the maximum allowed F1 degradation in pp | XS | P2 | The paper uses a difference, not a ratio (VERIFIED in `paper.md`); the reviewer may have misread. Clarify politely | Open | |
| R2-m2 | Eq. (7): explain the placement of PE and the meaning of In_Vectors; derive it or cite FINN folding | Eq. (7) | CL, RF | WP3 | Short derivation plus FINN reference | S | P2 | Same family as R1-Meth-6 | Open | |
| R2-m3 | Quantify why multiples of 8 are preferred over 4 | §II-C4a | CL | WP3 | Small example of the allowed SIMD/PE pairs and the DSP packing | S | P3 | | Open | |
| R2-m4 | Call the 2-bit BED layers mixed-precision quantization explicitly | §III-A2, Table 4 | ED | WP1 | Wording | XS | P2 | | Open | |
| R2-m5 | Were 4 MHz and < 1 MHz physically executed, or extrapolated with only the power-model clock changed? | §III-B5, Table 9 | CL, VR, RH | WP7 | Trace the provenance of each Table 9 entry; state the method | M | P1 | STRONG EVIDENCE that some low-clock full builds exist (`experiments_CLK/30_FPS_CLK_200ns`, `1_FPS_CLK_1us`, `0X_FPS_CLK_10us`; BED `30_FPS_200us`, `05_FPS_1us`). No 4 MHz full build was found (only estimates in `30_FPS_250ns`). The paper itself says the "power model" clock was reduced | Open | |
| R2-m6 | Report Vivado static/dynamic components directly instead of inferring a static floor at 100 kHz | §III-B5 | ED, TB | WP8 | Table 9 already splits static/dynamic: remove or reword the 109 mW sentence | XS | P3 | | Open | |
| R2-m7 | Keep the "reduced problem / no localization" wording consistent | throughout | ED | WP1 | Consistency pass | XS | P3 | | Open | |
| R2-m8 | Report smoke recall separately for the 160/112 resolutions | Table 10 | TB, RR | WP6 | Values are already in the logs (`test_v21`, `test_v23`) | S | P2 | STRONG EVIDENCE that per-label metrics are in those logs | Open | |

### Reviewer 3

R3 judges the paper "technically sound: partially", with several internal inconsistencies. **This is the most demanding report.**

| ID | Concern (summary) | Paper | Type | WP | High-level action | Effort | Prio | Evidence / notes | Status | Commit |
|---|---|---|---|---|---|---|---|---|---|---|
| R3-1 | Is the "held-out evaluation set" a separate validation set? If it is the test set, model selection biases the test metrics | §II-B, Table 1 | IC, CL, RR | WP4 | **Decision required (D1).** Option A: disclose and add a limitation. Option B: re-train the final models with a validation set held out from training, report test metrics and compare with the original | XS (A) / L–XL (B) | **P1 critical** | **VERIFIED** (`modules/dataloaders.py` in both `train/mobilenet` and `train/bed`): the scheduler and best-F1 checkpoint use the test splits. **VERIFIED**: the official FASDD `val.txt` was merged into training (UAV 12550 + 8364 ≈ 20916; CV 47660 + 31769 ≈ 79430 in Table 1). The paper's "original training and test assignments are preserved" is therefore inaccurate for FASDD (A-3) | Open | |
| R3-2 | How were the PYNQ-Z1 inference times obtained (board, simulation, cycle counts)? How many inferences? Is DMA included? | Table 9, §III-B5 | CL, RH | WP7 | Trace the method and write a protocol paragraph | M | P1 | UNKNOWN. Candidates: board driver (`driver.py`/`validate.py` in `deploy/`) or xsim testbench (`verilog_stitched_sim/`). Needs investigation | Open | |
| R3-3 | Reconcile the BED numbers in Tables 3 and 7 and the text (the 1.26 pp attributed to quantization) | Tables 3, 7; §III-B1 | IC, TB | WP7 | Relabel Table 7 rows (FP32 = compressed model, "Quantized" = FPGA-adapted QAT) or recompute | S | P1 | STRONG EVIDENCE: BED Quantized = run `41_brevitas__full_ds` (94.69); BED FPGA = `71_…SmallBig__full_ds` (94.53). Table 7 "FP32 95.80" equals the *Pruning* row, not FP32 of the FPGA architecture (`31_fpga` = 95.17). INFERENCE | Open | |
| R3-4 | Table 9: BED throughput does not scale with clock (Nano does); 784 fps vs 1/1.19 ms ≈ 840 fps | Table 9, §III-B2 | IC, VR, RH | WP7 | Recompute and trace each value; separate theoretical from measured values | M | P1 | **VERIFIED (arithmetic):** BED 1.28 ms × 25 = 32.0 ms vs 36.55 reported; × 150 = 192 ms vs 212.62. Nano 1.19 × 25 = 29.75 vs 29.80; × 150 = 178.5 vs 178.93 (consistent). 1/1.19 ms = 840 fps ≠ 784 | Open | |
| R3-5 | Give a stage-by-stage trajectory for MobileNetV2 Nano (params, MAC, F1); clarify the BED simplification changes | §III-A3, new table | RH, TB | WP10 | Rebuild from historical logs (387k → 100k → 70k…) | M | P1 | STRONG EVIDENCE that logs exist: `uav/code/classifier_my_mobilenetv2/experiments/test_v00_387k … test_v04` | Open | |
| R3-6 | Why MobileNetV2 and not MobileNetV3 (cheaper)? Why was V3 Mini not deployed? | §II-B, §II-C4, Table 5 | JU | WP3 | Connect explicitly to the FINN limitations (SE stream multiplication, h-swish) | S | P1 | `z_paper_tests/01_test_mulstream`, `03_activation_complexity` (STRONG EVIDENCE of prior tests) | Open | |
| R3-7 | Quantitative comparison with prior implementations | new table | RF, TB | WP2 | Same action as R2-M7 | — | P1 | | Open | |
| R3-8 | The "low-power" claim and 144 mW headline could be read as board power; measure PYNQ-Z1 board power or requalify title, abstract and conclusion | Title, Abstract, Fig. 9b, §IV | MS or ED | WP8 | **Decision D2/D4.** Minimum: qualify "Vivado-estimated PL power at 4 MHz" everywhere. Better: board-level measurement with the same meter used for the RPi | S (requalify) / M (measure) | **P1 critical** | | Open | |
| R3-9 | Power is a design target but is reported only for the final designs; report it across stages, or revise the objectives; add energy per frame | §II, §III | DS, TB, (SY) | WP8 | Revise the objectives text and add energy per frame. Post-implementation power for intermediate stages is impossible (they do not fit the device, Fig. 6), so argue this | S | P2 | INFERENCE: intermediate stages exceed Z-7020 resources, so only estimates exist | Open | |
| R3-10 | Run MobileNetV2 Nano on all three platforms as a controlled reference | §III-C, Fig. 9 | NX, MS | WP9 | FP32 ONNX of Nano on RPi 3A+ and RPi 5 with the same protocol | M | P2 | Needs the RPi hardware (D2) | Open | |
| R3-11 | Table 2: which dataset and split? Note pretrained vs scratch | Table 2 caption | ED | WP1 | Edit the caption | XS | P2 | | Open | |
| R3-12 | Class imbalance: was class weighting or threshold adjustment considered? Effect on Table 8 | §II-A, Table 8 | DS, CL, VR | WP4 | Discuss; check the loss actually used | S | P2 | **Potential discrepancy:** the logs say "Weighted for Precision" (`SMOKE_PRECISION_WEIGHT = 0.8` in config), while the paper says plain BCE summed. Verify `modules/loss.py` (A-4) | Open | |
| R3-13 | Cite FINN/FINN-R, PyTorch, Albumentations; [13] does not support the FPGA dataflow claim in §I | References, §I | RF | WP1 | Add citations; replace [13] in §I with a dataflow-FPGA reference | S | P1 | VERIFIED in `paper.md`: FINN has no reference | Open | |
| R3-14 | Table 4 Conv4.4 input notation | Table 4 | ED | WP1 | `24x32` → `24²x32` | XS | P1 | = `paper_comments.md` #3 | Open | |
| R3-15 | "MANUAL" (Fig. 6a) vs "Simplified" (Table 3) | Fig. 6a | FG, ED | WP1 | Harmonize the terms | XS | P2 | | Open | |
| R3-16 | Table 10 row 1 F1 (95.45) is the quantized software value, not the FPGA value | Table 10 | IC, TB | WP7 | Clarify the column (all three rows are software QAT values) or add the FPGA F1 | S–M | P1 | STRONG EVIDENCE: 94.31 and 93.81 match the software QAT logs `test_v21`/`test_v23`; FPGA F1 for 160/112 is UNKNOWN | Open | |
| R3-17 | Check that the PYNQ-Z1 bar in Fig. 9b equals 144 mW | Fig. 9b | IC, FG, RH | WP8 | Find the source data; fix the figure | S | P1 | = `paper_comments.md` #5. The bar looks like ≈2.5 W (HYPOTHESIS, visual reading only) | Open | |
| R3-18 | Euro symbol rendering in §I | §I | ED | WP1 | Use `\texteuro` / eurosym with a proper font | XS | P2 | The PDF text layer contains "=C" (VERIFIED with pdftotext) | Open | |
| R3-19 | Bibliographic errors in [1], [8], [13], [16], [20], [24], [29]; prefer peer-reviewed versions over preprints | References | RF, ED | WP1 | Full bibliography audit | S | P1 | Partly covered by `paper_comments.md` #6 ([13], [29]). Also [1] "K. e. a. Bowman" | Open | |
| R3-20 | If Fig. 9b is kept, separate the PL estimate from board-level measurements inside the figure | Fig. 9b | FG | WP8 | Merge with R2-M5 / R3-8 / R3-17 | S | P1 | | Open | |
| R3-Q | References "partially sufficient"; some preprints (e.g. [22], [24], [28]) have peer-reviewed versions | References | RF | WP1 | Included in R3-19 | — | P2 | | Open | |

### Author-identified issues (not raised by the reviewers, but they must be fixed or disclosed)

Sources: `../paper_comments.md` and the provenance audit of 2026-10-03.

| ID | Issue | Paper | Type | WP | Action | Effort | Prio | Evidence | Status | Commit |
|---|---|---|---|---|---|---|---|---|---|---|
| A-1 | FIGURE 4 is missing (numbering jumps from 3 to 5) | Figures | ED | WP1 | Renumber | XS | P1 | VERIFIED (`paper_comments.md` #1) | Open | |
| A-2 | §II-C5 refers to itself ("reported in Section II-C5") | §II-C5 | ED | WP1 | Point to §III-B6 | XS | P1 | VERIFIED (`paper_comments.md` #2) | Open | |
| A-3 | "Original training and test assignments preserved" is inaccurate: the FASDD val split was merged into training | §II-A1 | IC | WP4 | Correct the text; resolve together with R3-1 | XS | P1 | VERIFIED (label-file line counts vs Table 1) | Open | |
| A-4 | Training details missing or inconsistent with the logs: weight decay (0.001 / 1e-5 / 0), smoke-precision-weighted loss, epochs 100–150 | §II-B | IC, VR | WP4 | Verify in the code and logs, then report accurately | S | P1 | STRONG EVIDENCE from `logfile.log` headers | Open | |
| A-5 | Normalization: the paper says [-1, 1], the dataloader divides by 255 to give [0, 1] | §II-A | VR, IC | WP4 | Check whether a model-level or FINN pre-processing node rescales | S | P2 | INFERENCE / HYPOTHESIS (`prepro_node.onnx`, TensorNorm) | Open | |
| A-6 | Parameter counts in the paper vs logs: ReLU6 68914 vs 68893; Width-0.1 78311 vs 78258 | Table 5 | VR, TB | WP10 | Re-check and fix | XS | P2 | STRONG EVIDENCE (logs `test_v41`, `test_v21_Original`) | Open | |
| A-7 | The augmentation list in §II-A is incomplete. The real pipeline also has HorizontalFlip, CLAHE, RGBShift and scale; Blur 17×17 is applied at full resolution before Resize; a silent `try/except` falls back to other transforms | §II-A | IC, CL | WP4 | Describe the actual pipeline | XS | P2 | VERIFIED (`train/mobilenet/modules/dataloaders.py` `get_train_loader`, `dataset_dfire.py` `__getitem__`) | Open | |
| A-8 | AIMET greedy compression-ratio search and channel-pruning reconstruction for BED used 2048 **test** images (`aimet_val_loader`) | §II-C2, Table 3 | IC, RR | WP4 | Disclose. Re-run the greedy search on the new validation split and compare the per-layer ratios (see `discussion.md` §7–8) | M | P1 | VERIFIED (`train/bed/aimet_spatial_svd_then_pruning_fasdd.ipynb`) | Open | |

---

## 4. Effort scenarios (rough planning estimates — INFERENCE)

These assume a single author at about 1 FTE (5 pd per week) with Claude assistance. GPU jobs run in the background on the shared RTX 4070 Ti, so the plan is limited by human time rather than compute.

| Scenario | Content | Human effort | Compute / HW | Calendar |
|---|---|---|---|---|
| **S1 – Minimum viable** | Every comment handled through text, historical recovery and re-evaluation of existing checkpoints. R3-1 disclosed as a limitation (Option A). R2-M3 answered with a small seed study (Nano FP32 only, 3 seeds). PYNQ power requalified (no board measurement) | ≈ 38–45 pd | ≈ 2 GPU-days | **8–9 weeks** |
| **S2 – Recommended** | S1, plus: train/test near-duplicate check; re-training of the final models (Nano FP32 + QAT, BED-FPGA QAT) with a proper validation split held out from training, 3 seeds each (covers R3-1 and R2-M3 together, reported as a protocol-sensitivity analysis while the deployed hardware is kept); PYNQ-Z1 board-level power and timing measurement; Nano on both RPis | ≈ 52–62 pd | ≈ 8–12 GPU-days, plus PYNQ-Z1 and RPi hardware, power meter | **11–13 weeks** |
| **S3 – Full re-run** | S2, plus: re-train complete BED and Nano trajectories under the new protocol, new FINN builds of the deployed designs with the new weights, and new post-implementation power/latency numbers | ≈ 75–90 pd | weeks of GPU time plus Vivado synthesis (hours per build) | 16+ weeks |

**Recommendation: S2.** One resubmission is allowed and R3 is strict. R3-1 (test set used for selection) and R3-4/R3-3/R3-16/R3-17 (internal inconsistencies) are the comments most likely to cause rejection if answered only with text. The R3-1 re-training also directly addresses R2-M3.

---

## 5. Critical path and suggested order

1. **Week 1 — Decisions and hardware provenance** (blocking).
   - Decisions D1–D5 below.
   - WP7: trace how every Table 9 number, the FPGA F1 values and Fig. 9b were produced. These may change numbers used throughout the paper.
2. **Weeks 1–2 — Start the long GPU jobs** (WP4/WP5, if S2 is chosen) in the background, using a copy of the training code in the active repository with outputs under `results/review_2026/`. Nothing is written into `uav`.
3. **Weeks 2–5 — Historical recovery and analyses:** WP10 (Nano trajectory), WP11 (sparsity bottleneck), WP6 (metrics, PR curves, threshold), WP9/WP8 measurements if hardware is available.
4. **Weeks 3–8 — Writing:** WP2 (positioning plus comparison table: literature-heavy, can run in parallel), WP3, WP12, WP1.
5. **Final 1.5 weeks — WP13:** response letter in the (a)/(b)/(c) format, highlighted PDF, clean source, and a final cross-check of every number against its evidence.

## 6. Decisions needed from the authors

| ID | Decision | Affects |
|---|---|---|
| D1 | R3-1 / R2-M3: disclose only (A), or re-train the final models with a held-out validation set and seeds (B)? If B, keep the deployed FPGA designs and report re-training as a sensitivity analysis, or redeploy? | WP4, WP5, timeline |
| D2 | Are the PYNQ-Z1 board, RPi 3A+, RPi 5, the power meter and the Logitech C270 still available? | R3-8, R3-10, R3-2, R1-Res-4 |
| D3 | Where is the LaTeX source of the manuscript? It is not in the repository and is needed for the highlighted and clean versions. | WP13 and all edits |
| D4 | Keep "Low-Power" in the title (with qualification), or retitle? | R3-8, R2-M1 |
| D5 | Target resubmission date or time budget (the email states no deadline). | Choice of scenario |
