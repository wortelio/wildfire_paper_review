# 03_revision — new experiments for the resubmission (with training)

These experiments may produce new numbers for the paper. Code is copied from `01_replicas/` and modified copy-on-write, with the diffs documented. File lists come from `dataset_review_split/`. Background and scope: `paper_files/discussions/01_dataset.md` (sections 4–8).

| Folder | Purpose | Reviewer items |
|---|---|---|
| `f2_splits/` | Code that builds the group-aware train/validation split; the lists are written to `dataset_review_split/` | R3-1, A-3 |
| `f3_retrain/` | Re-training of the key models with validation-only selection and fixed seeds | R3-1, R2-M3 |
| `f_aimet/` | AIMET greedy compression-ratio search re-run on the validation split | A-8 |
