# code_review — all new code of the review

The original code stays in `../code/` (byte-identical copy of `~/uav`, never edited). Everything written for the review lives here. `train/` and `finn/` mirror `../code/train/` and `../code/finn/`.

```
code_review/
├── common/                # shared infrastructure (importable package), used by train/ and finn/
├── dataset_review_split/  # canonical, versioned file lists (test_full, test_clean, train/val)
├── train/                 # PyTorch / Brevitas
│   ├── 01_replicas/       #   faithful replicas of the paper models (no training)
│   ├── 02_audit/          #   analyses of the paper's own artifacts (no training): f0, f1
│   └── 03_revision/       #   new experiments for the resubmission (training): f2, f3, f_aimet
└── finn/                  # FINN / FPGA (not started)
```

Rules: see the repository `README.md`. Each experiment folder keeps small versioned outputs in `results/` and large git-ignored outputs in `artifacts/`.
