# 01_replicas — faithful replicas of the paper models

Each subfolder rebuilds paper models exactly as they were trained, with no new training:
- the historical files needed (copied unchanged from `code/`, i.e. the `~/uav` working tree, or from a paper-era git revision when the working tree differs);
- an adapted `config.py`, with every change marked `# REPLICA:`;
- byte-identical local copies of the paper checkpoints in `weights/` (git-ignored; source paths and hashes in the README);
- a `validate_paper_metrics` notebook that must reproduce the published numbers.

A replica is "trusted" only after its validation reproduces the paper. Audit and revision work build on trusted replicas.

| Replica | Paper results | Status |
|---|---|---|
| `mobilenet_paper/` | MobileNetV2 Nano FP32 and Brevitas QAT (Tables 5, 7, 8) | Validated 2026-10-04: exact (max abs diff 0 vs logs) |
| `bed_paper/` | BED stages (Tables 3, 4, 7) | Not started |

**Using a replica from another folder:** `common.replicas.use('<name>', model=...)`. It puts the replica first on `sys.path` and returns its `config`; the replica's `modules` are then importable. One replica per process.
