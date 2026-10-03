# mobilenet_paper_replica — MobileNetV2 Nano FP32

Minimal, self-contained copy of the historical code needed to rebuild the **MobileNetV2 Nano FP32** model reported in the paper, load its weights and evaluate it on the paper test set. It is the trusted baseline for later automation; code duplication with `code/train/mobilenet` and `results_audit/common` is intentional at this stage.

**Paper results:**
- Table 5, row "MobileNetV2 Nano (Ours)": 68,882 parameters, F1-Macro 95.93 %.
- Table 8, row "FP32": smoke P/R/F1 95.66 / 94.67 / 95.16; fire 95.24 / 98.20 / 96.70.

## Provenance

| Item | Value | Evidence |
|---|---|---|
| Historical run | `~/uav/code/classifier_my_mobilenetv2/experiments/test_v04_mini_resnet_70k_full_ds` | STRONG EVIDENCE: the logged per-class P/R/F1 equal Table 8 FP32 to all printed decimals |
| Checkpoint | `MY_MBLNET_V2_classifier__best_mean_F1.pt` (see "Weights" below) | — |
| Epoch | 86 | **VERIFIED:** `epoch = 86`, and all 188 tensors are identical to `…smoke__precision=0.9566__recall=0.9467__epoch=86.pt`. The log saves "best Mean F1: 0.9593" at epoch 86 and never again |
| Training dates | 2024-11-05 18:54 → 2024-11-06 04:35 (9 h 40 min), 100 epochs | log |
| Training kernel / env | Python 3.10.13 → conda env `pytorch_23` (torch 2.3.1, albumentations 1.4.10) | STRONG EVIDENCE (only env with 3.10.13) |
| Model class | `modules/model_mobilenetv2_mini_Resnet.py :: MobileNetV2_MINI_RESNET` | INFERENCE. Basis: run name "mini_resnet"; at `~/uav@f8d1ede` (2024-11-07) the notebook had moved on to the next run, `test_v05_mini_No_resnet` (`model_mobilenetv2_mini`), with the `_Resnet` import commented just above. The model file has not changed since its first commit `f8d1ede`. **Caveat:** the no-skip variant has the same 68,882 parameters and state-dict shapes, so strict loading does not discriminate. Evaluation A is the decisive check (the wrong class cannot reproduce the logged metrics) |

## Weights

`weights/MY_MBLNET_V2_classifier__best_mean_F1.pt` is a byte-identical copy (`cp -p`, 2026-10-03; `cmp` OK) of:

```
/home/gmoreno/uav/code/classifier_my_mobilenetv2/experiments/test_v04_mini_resnet_70k_full_ds/weights/MY_MBLNET_V2_classifier__best_mean_F1.pt
```

| Property | Value |
|---|---|
| Size | 998,822 bytes |
| Original mtime | 2024-11-06 03:19:56.975639702 +0100 (written at the end of epoch 86) |
| sha256 | `c8385799d1771c5e9f055d9a9c19f66f7bb3606b2d2cbf655723b1733ad607f6` |
| md5 | `45b0df5fdf6b9f0073e3a500d29e5b15` |
| Content | dict with `epoch` (= 86), `model_state_dict` (188 tensors, 68,882 parameters), `optimizer_state_dict`, `scheduler_state_dict` |
| Equivalent file in the same folder | `MY_MBLNET_V2_classifier__smoke__precision=0.9566__recall=0.9467__epoch=86.pt` (different file, md5 `0386bb97…`, but identical `epoch` and `model_state_dict` tensors) |

`config.py` loads the local copy (`LOAD_MODEL_FILE = 'weights/…'`) and records the source path (`ORIGINAL_MODEL_FILE`) and the sha256 (`MODEL_FILE_SHA256`). The notebook aborts if the hash of the loaded file differs. The file is versioned in git (an exception in `.gitignore`); it is about 1 MB.

## Files

All copied from `code/train/mobilenet/` (= `~/uav` HEAD; sha256 and identity in `SOURCES.sha256`).

| File | Changed? | Notes |
|---|---|---|
| `config.py` | **Yes** (every line marked `# REPLICA:`) | Changes listed below |
| `modules/dataloaders.py`, `dataset_dfire.py`, `dataset_fasdd.py`, `dataset_clouds.py` | No | `dataset_clouds` is only imported by `dataloaders` |
| `modules/model_mobilenetv2_mini_Resnet.py` | No | Unchanged since `~/uav@f8d1ede` |
| `modules/metrics.py`, `val_epoch.py`, `loss.py`, `utils.py` | No | Exactly the functions used during training |
| `weights/MY_MBLNET_V2_classifier__best_mean_F1.pt` | Copied unchanged | Paper checkpoint (see "Weights") |
| `validate_paper_metrics.ipynb` | New | Derived from `validate_metrics.ipynb`, keeping only the paper test set and the FP32 model |

**`config.py` changes** (all other values, i.e. LR 1e-3, scheduler 0.8 / 2 / 0.001 / 1e-6, batch 64, 8 workers, 224×224, loss BCE with smoke `pos_weight` 0.8, already equal the `test_v04` log header):
1. `RUN_FOLDER = 'outputs/'`: local and git-ignored. `config.py` still creates `outputs/{logs,plots,weights,onnx}` on import.
2. `FIGLIB = 0` and the post-paper `assert FOG+SICILIA+FIGLIB == 1` commented out, so the DFire+FASDD branch (`CLASSES = ["smoke", "fire"]`, `LOSS_FN = "BCE"`) is selected.
3. Dataset paths: `'../../datasets/...'` → `~/uav/datasets/...` (absolute, read-only).
4. `MODEL = "MY_MBLNET_V2"`, `WEIGHT_DECAY = 1e-3`, `EPOCHS = 100`: log values, kept for documentation (not used by the evaluation).
5. `LOAD_MODEL_FILE = 'weights/MY_MBLNET_V2_classifier__best_mean_F1.pt'` (local copy of the paper checkpoint); `ORIGINAL_MODEL_FILE` and `MODEL_FILE_SHA256` added for traceability.

## How to run

```bash
cd ~/wildfire_paper_review/results_audit/mobilenet_paper_replica
NO_ALBUMENTATIONS_UPDATE=1 /opt/conda/envs/pytorch_23/bin/jupyter nbconvert --to notebook --execute \
    --output validate_paper_metrics.executed.ipynb validate_paper_metrics.ipynb
```

- `NO_ALBUMENTATIONS_UPDATE=1` stops albumentations 1.4.10 from checking online for a newer version at import.
- The notebook installs `results_audit/common/write_guard`, so any write to `~/uav` or `code/` aborts.
- Outputs go to `results/` (metrics + provenance JSON, per-image predictions CSV).

**Acceptance criteria:**
- **A.** `modules.val_epoch.eval_fn` on `get_val_loader()` (batch 64, `drop_last=True`, 24,320 of 24,371 images, the training protocol) reproduces the logged epoch-86 metrics (`max |diff| ≲ 1e-5`).
- **B.** The independent numpy TP/FP/TN/FN computation, restricted to the same 24,320 images, equals A. Its full-test (24,371) values are reported separately.

## Status

- 2026-10-03: prepared. Imports, configuration, strict weight loading (epoch 86, 68,882 parameters) and a forward pass checked in `pytorch_23`. **The evaluation has not been run yet** (next phase).
