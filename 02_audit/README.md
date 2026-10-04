# 02_audit — analyses of the paper's own artifacts (no training)

These analyses measure problems in the published results using the historical checkpoints, logs and predictions as they are. They never train models. Background: `paper_files/discussions/01_dataset.md`; tracking: `paper_files/reviewers/response_matrix.md`.

| Folder | Question | Reviewer items |
|---|---|---|
| `f0_selection_bias/` | How much did selecting the checkpoint on the test set inflate the reported metrics? (`best_mean_F1` vs `best_loss` vs `last` checkpoints) | R3-1 (preliminary evidence) |
| `f1_duplicates/` | Are there duplicate or near-duplicate images between train and test, and what is their impact? Produces `dataset_review_split/test_clean.txt` | R2-M2 |
