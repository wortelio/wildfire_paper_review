# results_audit — Audit of the results reported in the paper

Purpose: check, with a rigorous and reproducible protocol, the validity of the results reported in manuscript Access-2026-39017. The main reviewer comments this addresses:

| Comment | Topic |
|---|---|
| R3-1, A-8 | Test set used for model selection and for the AIMET compression search |
| R2-M2 | Possible train/test duplicates |
| R2-M3 | No seeds; run-to-run variability |

Background and decisions: `paper_files/discussions/01_dataset.md` (sections 4–8). Tracking: `paper_files/reviewers/response_matrix.md`.

## Rules

1. **`~/uav` is read-only historical evidence.** Code here may read datasets and checkpoints from `~/uav`, but must never write there. `common/write_guard.py` enforces this at run time.
2. **`code/` is never edited.** `code/train/**` and `code/finn/**` are byte-identical copies of the historical `~/uav` working tree (verified 2026-10-03 with `cmp`), and that identity is part of the provenance evidence. The original modules are imported unchanged, and their global `config` is replaced at import time by `common/config_shim.py`. **The working tree is not the paper-era code** (see `common/README.md`), so paper runs are audited with the code of the `~/uav` revision `455f115`, extracted read-only by `common/snapshot.py`.
3. **Copy-on-write for code changes.** If a phase needs a modified module (e.g. seeds or a validation split in F3), it is copied into that phase's folder and its diff against the original is documented in the phase README.
4. **Every result records its provenance:** git commit, conda environment, package versions, GPU, date, run spec and command (`common/env_capture.py`).
5. **Outputs:**
   - `<phase>/results/` holds small, versioned outputs (JSON, CSV, Markdown tables, plots).
   - `<phase>/artifacts/` holds large outputs that are not versioned (checkpoints, embeddings, logs > 1 MB). It is git-ignored.
6. **Evidence levels** in reports: VERIFIED / STRONG EVIDENCE / INFERENCE / HYPOTHESIS / UNKNOWN.

## Structure

```
results_audit/
├── common/
│   ├── paths.py           # absolute paths (~/uav datasets and checkpoints) and local outputs
│   ├── config_shim.py     # builds the `config` module of each historical run (no mkdir, no relative paths)
│   ├── write_guard.py     # aborts on any write attempt under ~/uav
│   ├── env_capture.py     # provenance record for every result
│   ├── snapshot.py        # historical code at a ~/uav git revision (paper era: 455f115)
│   └── run_specs/         # one spec per historical run used in the paper
├── mobilenet_paper_replica/  # self-contained replica of MobileNetV2 Nano FP32 + Brevitas QAT (paper Tables 5, 7, 8)
├── f0_selection_bias/     # F0: re-evaluate historical checkpoints (sanity gate + best-vs-last bias) and timing
├── f1_duplicates/         # F1: exact / perceptual / embedding near-duplicate analysis (train <-> test)
├── f2_splits/             # F2: group-aware train/val split; versioned file lists
├── f_aimet/               # AIMET greedy ratio search re-run on the validation split
└── f3_retrain/            # F3: re-training with validation-only selection and fixed seeds
```

## Status

| Phase | Status |
|---|---|
| T0 structure | Done |
| T1 common infrastructure | Done (see `common/README.md`: the active code copy is not usable as-is; paper-era snapshot `455f115` is used) |
| mobilenet_paper_replica | Done: MobileNetV2 Nano FP32 and Brevitas QAT (Tables 5, 7, 8) reproduced exactly (VERIFIED, max abs diff = 0 vs logs) |
| F0 | Pending |
| F1, F2, F-AIMET, F3 | Not started; scope decided after F0 |
