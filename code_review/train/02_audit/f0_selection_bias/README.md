# F0 — Selection bias of the reported checkpoints (R3-1, preliminary evidence)

**Question.** Every historical run evaluated the **test** set after each epoch. The LR scheduler (ReduceLROnPlateau) monitored that test loss, and the reported checkpoint was the one with the best test F1-Macro. How much does that selection inflate the published numbers, and does it change any conclusion of the paper?

**Scope.** No training. Uses the historical logs (per-epoch test metrics) and, for MobileNetV2 Nano, the historical checkpoints evaluated with the validated replica `01_replicas/mobilenet_paper`.

**Caveat.** The "selection-free" references below (last epoch, mean of the last 10 epochs) still come from runs whose learning-rate schedule was driven by the test loss. They show the size of the checkpoint-selection effect, but they are not unbiased estimates. The definitive answer requires re-training with a separate validation set (`03_revision/f3_retrain`).

## Files

| File | Content |
|---|---|
| `parse_logs.py` | Parses the per-epoch "VAL Stats" (= test) of each paper run's `logfile.log`. Outputs `results/epochs/<run>.csv`, `results/f0_log_summary.{json,md}` |
| `eval_checkpoints.py` | Evaluates the `best_mean_F1`, `best_loss` and `last` checkpoints of the two Nano runs on the full test set. Checks them against the log. Writes `results/checkpoints/*.json`, per-image predictions in `artifacts/predictions/*.npz`, and the canonical test lists in `dataset_review_split/test_full/` |
| `bench_training_throughput.py` | Training throughput of the historical pipeline (for the F3 time estimates): `results/throughput/*.json` |
| `results/f0_impact_on_comparisons.json` | Effect of the selection on the comparisons used by the paper |

Commands (from this folder):
```bash
python3 parse_logs.py
NO_ALBUMENTATIONS_UPDATE=1 /opt/conda/envs/pytorch_23/bin/python eval_checkpoints.py --model fp32 --write-test-lists
NO_ALBUMENTATIONS_UPDATE=1 /opt/conda/envs/pytorch_brevitas/bin/python eval_checkpoints.py --model brevitas
NO_ALBUMENTATIONS_UPDATE=1 /opt/conda/envs/pytorch_23/bin/python bench_training_throughput.py --model fp32 --steps 300 --tag single
```

## Results (2026-10-04)

### 1. The logs are a faithful record of the checkpoints (VERIFIED)

The six checkpoints of the two Nano runs (`best_mean_F1`, `best_loss`, `last`) were evaluated with the replica on the historical protocol (first 24,320 test images). All reproduce the per-epoch values of the log exactly (max |diff| = 0.0 at 4 decimals):

| Model | Checkpoint | Epoch | F1-Macro, historical protocol | F1-Macro, full test (24,371) | Smoke recall |
|---|---|---|---|---|---|
| FP32 | best_mean_F1 (paper) | 86 | 95.93 | 95.93 | 94.67 |
| FP32 | best_loss | 98 | 95.89 | 95.88 | 94.71 |
| FP32 | last | 99 | 95.78 | 95.78 | 94.39 |
| QAT | best_mean_F1 (paper) | 91 | 95.45 | 95.46 | 93.48 |
| QAT | best_loss | 91 | 95.45 | 95.46 | 93.48 |
| QAT | last | 99 | 95.12 | 95.12 | 94.57 |

So the per-epoch test metrics parsed from the logs can be used directly for every paper run, including those without a replica yet.

### 2. All paper values are recovered from the logs; new provenance (STRONG EVIDENCE)

All 18 runs checked reproduce the paper value from their log: 17 to two decimals, and BED FPGA with 94.53 vs 94.54 printed (a rounding difference). See `results/f0_log_summary.md`. Provenance newly established:

| Paper item | Run (`~/uav/code/...`) | Params (log) |
|---|---|---|
| Table 2 MobileNetV2 (97.65 %, 2.22 M) | `classifier_transfer_learning/experiments/test_v07_mobilenetv2_full_ds`, session 2 | 2,226,434 |
| Table 2 ShuffleNetV2 (94.95 %, 0.37 M) | `classifier_transfer_learning/experiments/test_v03_shufflenet_full_ds`, session 2 | 374,658 |
| Table 2 MobileViTV3 (95.87 %, 0.74 M) | `classifier_vision_transformer/experiments/test_v11_MobileViTv3_v1_full_ds` | 737,474 |
| Table 5 MobilenetV3 Mini (95.37 %, 76,858) | `classifier_my_mobilenetv3/experiments/test_v01_full_ds` | 76,858 |
| Table 2 MobileNetV3 (97.07 %, 1.52 M) | **Inconsistent row:** F1 97.07 = `test_v01_mobilenetv3_full_ds` (945,538 params ≈ 0.95 M); 1.52 M = `test_v05_mobilenetv3Deep_full_ds` (F1 97.16) | — |

Training details revealed by the logs (to report in §II-B):
- The transfer-learning references were trained in **two phases**: 20 epochs with a frozen pretrained backbone (head only), then 100 epochs of full fine-tuning.
- The `test_v04` log contains a second, later session appended to the same file. Only the first session is the paper run.

### 3. Size of the selection effect (F1-Macro, percentage points)

| Group | Selected − mean of last 10 epochs | Selected − last epoch |
|---|---|---|
| References, transfer learning (MobileNetV2, MobileNetV3, ShuffleNetV2) | +0.03 to +0.15 | 0.00 to +0.10 |
| From-scratch FP32 (Nano, ECA, width 0.1, MobilenetV3 Mini, MobileViTV3, BED Original/Simplified) | +0.18 to +0.36 | +0.11 to +0.25 |
| QAT (Nano, ReLU6, 4b input, 160, 112, BED Quantized/FPGA) | +0.33 to +0.71 | +0.22 to +1.29 |

The checkpoint selected on the test F1 is usually also the best-test-loss checkpoint, or close to it (difference 0.00–0.13 pp).

### 4. Effect on the paper's comparisons (INFERENCE; proxy = mean of the last 10 epochs)

| Comparison (drop in pp) | Paper | Last epoch | Mean last 10 |
|---|---|---|---|
| Nano FP32 → QAT | 0.48 | 0.66 | 0.63 |
| Nano QAT ReLU → ReLU6 | 1.26 | 2.22 | 1.65 |
| Nano QAT 8b → 4b input | 1.01 | 1.43 | 1.24 |
| Nano 224 → 160 / 112 | 1.14 / 1.64 | 1.04 / 2.15 | 1.30 / 1.86 |
| Nano → ECA | 0.10 | 0.14 | 0.12 |
| Nano → width 0.1 / MobilenetV3 Mini | 2.71 / 0.56 | 2.80 / 0.53 | 2.79 / 0.60 |
| BED Original → Simplified | 0.08 | 0.18 | 0.24 |
| BED Quantized → BED FPGA | 0.16 | 0.07 | 0.20 |
| **Headline: reference MobileNetV2 − deployed Nano** | **2.33 (claim "< 2.5")** | **2.67** | **2.57** |

- Every comparison keeps its sign, so the qualitative conclusions hold.
- Quantization and ReLU6 / 4-bit-input penalties are somewhat larger than reported.
- **The headline claim "F1-Macro decrease below 2.5 percentage points" (Abstract, §I, §IV) is not robust to the selection effect.** With selection-free proxies the gap is 2.57–2.67 pp. The reason is that the from-scratch and QAT models gain more from test-set selection than the transfer-learning references.
- This makes F3 (re-training with validation-only selection) necessary to state that number honestly.

### 5. Training throughput today (T5, for the F3 estimates)

`bench_training_throughput.py`: Nano FP32, historical training pipeline (replica `dataloaders.py`, batch 64, 8 workers, Adam), 300 steps after 20 warm-up steps, `pytorch_23`, RTX 4070 Ti, shared server (load average ≈ 8–10 from other processes before starting).

| Setting | img/s | s/epoch | h / 100 epochs | h / 150 epochs | GPU util. |
|---|---|---|---|---|---|
| 1 process | 153 | 769 | 21.4 | 32.0 | 20 % |
| 2 concurrent processes (each) | 176–188 | 626–666 | 17.4–18.5 | 26.1–27.8 | 26–28 % |

- **About 2× slower than the historical runs** (≈ 10 h per 100 epochs ≈ 337 img/s, from the logs). Probable causes (INFERENCE): the current augmentation is heavier (Blur 17×17 at full resolution, vs 3×3 in the Nov-2024 version used by the Nano FP32 run), and the server is shared.
- **Running 2 processes almost doubles the total throughput** (≈ 364 img/s), with the GPU still below 30 %. The bottleneck is per-process data loading (8 workers), not the machine, so F3 should run 2 or more jobs in parallel.
- **Building the training dataset took ≈ 45–50 min** before the first step: a fixed cost per run that F3 should cache (file list only, no change to the training semantics).
- **Revised F3 estimate (Tier 1, 12 runs):** ≈ 9.5 days sequential, ≈ 5 days with 2 jobs in parallel (previous estimate: 6 / 3–4 days).

## Status

- Done (2026-10-04): log analysis of 18 runs, checkpoint check of the two Nano runs, canonical test lists (`dataset_review_split/test_full/`), training throughput.
- Not done: selection-bias check of the AIMET stages (BED SVD / Pruning), whose logs have no final metrics, and of the remaining BED checkpoints with weights (needs `01_replicas/bed_paper`).
