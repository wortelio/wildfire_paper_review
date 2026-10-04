# dataset_review_split — canonical file lists

Single source of truth for the image lists used in the review. Paths are relative to `~/uav/datasets/`. Datasets on disk are never modified: every filter is applied through these lists.

| File | Content | Produced by | Status |
|---|---|---|---|
| `test_full/` (`dfire_test.tsv`, `fasdd_uav_test.tsv`, `fasdd_cv_test.tsv`, `manifest.json`) | Paper test set (24,371 images: file, smoke, fire), split per source so each file stays < 1 MB. Concatenated in the manifest order, they give the exact order of the paper's `get_val_loader()`. Label counts reproduce Table 1, with FASDD CV test "Both" = 3358 (A-10) | `02_audit/f0_selection_bias/eval_checkpoints.py` | Done 2026-10-04 |
| `test_clean.txt`, `test_contaminated.csv` | Test without train↔test duplicates, and the list of removed images with level and reason | `02_audit/f1_duplicates` | Planned |
| `train.txt`, `val.txt` | Group-aware train/validation split of the paper's training pool | `03_revision/f2_splits` | Planned |
