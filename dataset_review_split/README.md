# dataset_review_split — canonical file lists

Single source of truth for the image lists used in the review. Paths are relative to `~/uav/datasets/`. Datasets on disk are never modified: every filter is applied through these lists.

| File | Content | Produced by | Status |
|---|---|---|---|
| `test_full.txt` | Paper test set (DFire test + FASDD UAV test + FASDD CV test, 24,371 images), in the exact order of the paper's `get_val_loader()` | `02_audit/f0_selection_bias` | Pending |
| `test_clean.txt`, `test_contaminated.csv` | Test without train↔test duplicates, and the list of removed images with level and reason | `02_audit/f1_duplicates` | Planned |
| `train.txt`, `val.txt` | Group-aware train/validation split of the paper's training pool | `03_revision/f2_splits` | Planned |
