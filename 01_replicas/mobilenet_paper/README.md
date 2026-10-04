# 01_replicas/mobilenet_paper — MobileNetV2 Nano (FP32 and Brevitas QAT)

(Until 2026-10-04 this folder was `results_audit/mobilenet_paper_replica/`; earlier results and executed notebooks still show that path.)

Minimal, self-contained copy of the historical code needed to rebuild the two **MobileNetV2 Nano** models reported in the paper, load their weights and evaluate them on the paper test set. It is the trusted baseline for later automation. Code duplication with `code/train/mobilenet` and `results_audit/common` is intentional at this stage.

| Model (`REPLICA_MODEL`) | Paper results |
|---|---|
| `fp32` | Table 5 "MobileNetV2 Nano (Ours)": 68,882 params, F1-Macro 95.93 %. Table 7 FP32 95.93 %. Table 8 FP32: smoke P/R/F1 95.66 / 94.67 / 95.16; fire 95.24 / 98.20 / 96.70 |
| `brevitas` | Table 5 "Quantized - MobileNetV2 Nano": 68,914 params, 95.45 %. Table 7 Quantized 95.45 %. Table 8 "Quantized software": smoke 95.82 / 93.48 / 94.64; fire 94.43 / 98.19 / 96.27. This is also the model exported to QONNX and deployed with FINN (see below) |

## Provenance — FP32 (`fp32`)

| Item | Value | Evidence |
|---|---|---|
| Historical run | `~/uav/code/classifier_my_mobilenetv2/experiments/test_v04_mini_resnet_70k_full_ds` | STRONG EVIDENCE: the logged per-class P/R/F1 equal Table 8 FP32 to all printed decimals |
| Checkpoint / epoch | `MY_MBLNET_V2_classifier__best_mean_F1.pt`, epoch 86 | **VERIFIED:** `epoch = 86`, and all 188 tensors are identical to `…smoke__precision=0.9566__recall=0.9467__epoch=86.pt`. The log saves "best Mean F1: 0.9593" at epoch 86 and never again |
| Training dates | 2024-11-05 18:54 → 2024-11-06 04:35 (9 h 40 min), 100 epochs | log |
| Training env | Python 3.10.13 → conda env `pytorch_23` (torch 2.3.1, albumentations 1.4.10) | STRONG EVIDENCE (only env with 3.10.13) |
| Model class | `modules/model_mobilenetv2_mini_Resnet.py :: MobileNetV2_MINI_RESNET` | **VERIFIED (2026-10-03):** evaluation A reproduces the logged metrics and losses exactly. This was only an INFERENCE before evaluation, because the no-skip variant `model_mobilenetv2_mini` has the same 68,882 parameters and state-dict shapes, so strict loading cannot discriminate. The model file has not changed since its first commit `~/uav@f8d1ede` |

## Provenance — Brevitas QAT (`brevitas`)

| Item | Value | Evidence |
|---|---|---|
| Historical run | `~/uav/code/classifier_my_mobilenetv2/experiments_brevitas/test_v05_mini_resnet_70k_full_ds` | STRONG EVIDENCE: the logged per-class P/R/F1 equal Table 8 "Quantized software". **VERIFIED:** the run's `onnx/MY_MBLNET_V2_RESNET_classifier__best_mean_F1__BIPOLAR_Out__QONNX.onnx` has the same MD5 (`1ef6b83c…`) as the QONNX used by the FINN builds (`my_mblnet_resnet_to_finn_driver/onnx_models/`, `my_mblnet_resnet_onnx_modify/onnx_models/`) |
| Checkpoint / epoch | `MY_MBLNET_V2_RESNET_classifier__best_mean_F1.pt`, epoch 91 | **VERIFIED:** `epoch = 91`, and all 230 tensors are identical to `…smoke__precision=0.9582__recall=0.9348__epoch=91.pt`. The log saves "best Mean F1: 0.9545" at epoch 91 |
| Training dates | 2024-11-07 12:23 → 22:28 (10 h 05 min), 100 epochs, trained from scratch (`Load Model: False`) | log |
| Training env | Python 3.10.9 → conda env `pytorch_brevitas` (torch 2.1.2, brevitas 0.10.2, albumentations 1.3.1) | STRONG EVIDENCE (only 3.10.9 env with Brevitas) |
| Quantization (log header) | Fixed point; weights 4 bit, "big layers" weights 4 bit, bias 4 bit, activations 4 bit. In the model code: 8-bit input `QuantIdentity`, 8-bit per-tensor final linear layer | log, model file |
| Model class | `modules/brevitas/model_mobilenetv2_mini_Resnet_Brevitas.py :: MobileNetV2_MINI_RESNET` (+ `modules/brevitas/common.py`) | **VERIFIED (2026-10-03, before evaluation):** (1) the `torchinfo` summary of this class, 293 lines, is **identical** to the summary printed in the run log; (2) strict state-dict loading works; (3) 68,914 trainable parameters, as in the log |
| Code version | Current file = `~/uav@37a799f` (2024-12-17); unchanged since | git |

**Caution on the Brevitas code version.** At `~/uav@f8d1ede` (2024-11-07 10:10, about two hours before the run started) this file still defined `MobileNetV2_MINI`, without the quantized-residual logic (`quant_identity_out`, `shared_quant`). The run log shows the class `MobileNetV2_MINI_RESNET`. So the run used an uncommitted working-tree version, first committed in `37a799f`. The identical `torchinfo` summary and the evaluation below confirm that this committed version is the one used. `common.py` differs from that date only in comments and in a class added later (`CommonShiftUintActQuant`), so it is functionally identical.

## Weights

Both files are byte-identical copies (`cp -p`; `cmp` OK). They are **not versioned in git** (too large; `01_replicas/**/*.pt` is ignored), so they must be re-copied from `~/uav` on a fresh clone.

| File in `weights/` | Copied from (full path) | Size | sha256 | md5 | Original mtime |
|---|---|---|---|---|---|
| `MY_MBLNET_V2_classifier__best_mean_F1.pt` | `/home/gmoreno/uav/code/classifier_my_mobilenetv2/experiments/test_v04_mini_resnet_70k_full_ds/weights/MY_MBLNET_V2_classifier__best_mean_F1.pt` | 998,822 B | `c8385799d1771c5e9f055d9a9c19f66f7bb3606b2d2cbf655723b1733ad607f6` | `45b0df5fdf6b9f0073e3a500d29e5b15` | 2024-11-06 03:19:56 +0100 (end of epoch 86) |
| `MY_MBLNET_V2_RESNET_classifier__best_mean_F1.pt` | `/home/gmoreno/uav/code/classifier_my_mobilenetv2/experiments_brevitas/test_v05_mini_resnet_70k_full_ds/weights/MY_MBLNET_V2_RESNET_classifier__best_mean_F1.pt` | 1,276,401 B | `5418b2467e7e22f3eb9fdf31a4eca9b7a84139c0ce881b122a06b28d4716b65d` | `eabe8112fb32c5999b1f34ad11e6d16d` | 2024-11-07 21:42:27 +0100 (end of epoch 91) |

Each file is a dict with `epoch`, `model_state_dict`, `optimizer_state_dict` and `scheduler_state_dict`. `config.py` stores, for each model, the weight file name, the original run folder (`ORIGINAL_MODEL_FILE`) and the sha256 (`MODEL_FILE_SHA256`). The notebook aborts if the hash of the loaded file differs.

## Files

All copied from `code/train/mobilenet/` (= `~/uav` HEAD; sha256 and identity in `SOURCES.sha256`).

| File | Changed? | Notes |
|---|---|---|
| `config.py` | **Yes** (every line marked `# REPLICA:`) | Changes listed below |
| `modules/dataloaders.py`, `dataset_dfire.py`, `dataset_fasdd.py`, `dataset_clouds.py` | No | `dataset_clouds` is only imported by `dataloaders` |
| `modules/model_mobilenetv2_mini_Resnet.py` | No | FP32 model |
| `modules/brevitas/model_mobilenetv2_mini_Resnet_Brevitas.py`, `modules/brevitas/common.py` | No | Brevitas model and its quantizers |
| `modules/metrics.py`, `val_epoch.py`, `loss.py`, `utils.py` | No | Exactly the functions used during training |
| `weights/*.pt` | Copied unchanged, not in git | Paper checkpoints (see "Weights") |
| `validate_paper_metrics.ipynb` | New | Derived from `validate_metrics.ipynb`, keeping only the paper test set and the two paper models |
| `run_validation.sh` | New | Runs the notebook for each model in its original conda environment |

**`config.py` changes.** All other values (LR 1e-3, weight decay 1e-3, scheduler 0.8 / 2 / 0.001 / 1e-6, batch 64, 8 workers, 224×224, 100 epochs, loss BCE with smoke `pos_weight` 0.8, Brevitas bit widths 4/4/4/4) already equal both log headers.
1. `REPLICA_MODEL` (environment variable, `fp32` by default) selects the model. `PAPER_RUNS` holds, per model, the run folder, weight file name and sha256.
2. `RUN_FOLDER = 'outputs/'`: local and git-ignored. `config.py` still creates `outputs/{logs,plots,weights,onnx}` on import.
3. `FIGLIB = 0` and the post-paper `assert FOG+SICILIA+FIGLIB == 1` commented out, so the DFire+FASDD branch (`CLASSES = ["smoke", "fire"]`, `LOSS_FN = "BCE"`) is selected.
4. Dataset paths: `'../../datasets/...'` → `~/uav/datasets/...` (absolute, read-only).
5. `BREVITAS_MODEL = (REPLICA_MODEL == 'brevitas')`: it only enables the Brevitas ONNX-export imports in `utils.py`. `MODEL` = the name used by the run's weight files. `WEIGHT_DECAY = 1e-3` and `EPOCHS = 100` are log values, kept for documentation (not used by the evaluation).
6. `LOAD_MODEL_FILE = 'weights/<file>'` (local copy); `ORIGINAL_MODEL_FILE` and `MODEL_FILE_SHA256` added for traceability.

## How to run

```bash
cd ~/wildfire_paper_review/01_replicas/mobilenet_paper
./run_validation.sh            # both models; or: ./run_validation.sh fp32 / ./run_validation.sh brevitas
```

- Each model runs in its original training environment: `fp32` → `pytorch_23`, `brevitas` → `pytorch_brevitas`.
- The script sets `NO_ALBUMENTATIONS_UPDATE=1`, which stops albumentations from checking online for a newer version.
- The notebook installs `common/write_guard` (repository root), so any write to `~/uav` or `code/` aborts.
- From other folders (e.g. `02_audit/`), load this replica with `common.replicas.use('mobilenet_paper', model='fp32'|'brevitas')`. `config.py` resolves `weights/` and `outputs/` relative to this folder (`REPLICA_DIR`, added 2026-10-04), so it does not depend on the working directory.
- Outputs:
  - `validate_paper_metrics.executed_<model>.ipynb`;
  - `results/validate_paper_metrics__<model>__<run>__epoch<N>.json` (metrics + provenance, versioned);
  - `results/predictions__…__full_test.csv` (per-image probabilities, git-ignored, regenerable).

**Acceptance criteria:**
- **A.** `modules.val_epoch.eval_fn` on `get_val_loader()` (batch 64, `drop_last=True`, 24,320 of 24,371 images, the training protocol) reproduces the logged metrics of the best-F1 epoch (`max |diff| ≲ 1e-5`).
- **B.** The independent numpy TP/FP/TN/FN computation, restricted to the same 24,320 images, equals A. Its full-test (24,371) values are reported separately.

## Status

- 2026-10-03: FP32 prepared and validated with the first, FP32-only version of the notebook. Paper values reproduced exactly; max |diff| vs log = 0.0.
- 2026-10-04: Brevitas model added and the notebook generalized to both models. One fix was needed: Brevitas 0.10.2 leaves the 130 quantizer scaling parameters (`scaling_impl.value`) on CPU after `load_state_dict`, so the notebook calls `model.to(DEVICE)` again after loading, as the original `validate_metrics.ipynb` did. This is a device move only, and a no-op for FP32.
- **2026-10-04: both models validated with the same notebook version — the paper results are reproduced exactly (VERIFIED).**
  - Run: `./run_validation.sh` on top of commit `83bfab7` plus the uncommitted replica changes (committed right after; the JSON records `dirty: true`).
  - FP32: `pytorch_23` (torch 2.3.1), 3 min 31 s.
  - Brevitas: `pytorch_brevitas` (torch 2.1.2, brevitas 0.10.2), 7 min 38 s.
  - GPU: RTX 4070 Ti.

| Model | Evaluation | Smoke P | Smoke R | Smoke F1 | Fire P | Fire R | Fire F1 | F1-Macro |
|---|---|---|---|---|---|---|---|---|
| FP32 | Paper (Tables 5, 7, 8) | 95.66 | 94.67 | 95.16 | 95.24 | 98.20 | 96.70 | 95.93 |
| FP32 | A: training protocol (24,320 images) | 95.66 | 94.67 | 95.16 | 95.24 | 98.20 | 96.70 | 95.93 |
| FP32 | B: full test (24,371 images) | 95.66 | 94.66 | 95.15 | 95.25 | 98.20 | 96.70 | 95.93 |
| Brevitas | Paper (Tables 5, 7, 8) | 95.82 | 93.48 | 94.64 | 94.43 | 98.19 | 96.27 | 95.45 |
| Brevitas | A: training protocol (24,320 images) | 95.82 | 93.48 | 94.64 | 94.43 | 98.19 | 96.27 | 95.45 |
| Brevitas | B: full test (24,371 images) | 95.83 | 93.47 | 94.64 | 94.44 | 98.19 | 96.28 | 95.46 |

- **A vs the historical logs:** max \|diff\| = **0.0** for both models (all eight per-class metrics).
- **Losses also match the logged "new best validation loss":**
  - FP32: 11.0675 (smoke 7.07, fire 3.99);
  - Brevitas: 12.5129 (smoke 7.96, fire 4.56).
- **B restricted to the same 24,320 images vs A:** max \|diff\| = 2.9e-8 (FP32) and 2.8e-8 (Brevitas), i.e. float32 rounding.
- **Full test set (24,371 images) confusion counts:**

| Model | Smoke TP | Smoke FP | Smoke TN | Smoke FN | Fire TP | Fire FP | Fire TN | Fire FN |
|---|---|---|---|---|---|---|---|---|
| FP32 | 10876 | 494 | 12387 | 614 | 7760 | 387 | 16082 | 142 |
| Brevitas | 10740 | 467 | 12414 | 750 | 7759 | 457 | 16012 | 143 |

- The positive totals (smoke 11,490; fire 7,902) equal Table 1.
- The 51 images excluded by `drop_last=True` (A-9) change the published values by at most 0.01 pp.
- Quantization mainly costs smoke recall: 136 more smoke false negatives (614 → 750). This matches the paper statement in §III-B1.
- No file under `~/uav` or `code/` was modified (`write_guard` active; `~/uav` git status clean).
