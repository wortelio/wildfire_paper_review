# code_review/finn — FINN / FPGA review work

Mirror of `code/finn/` for the review. Not started.

Planned scope: provenance of the hardware numbers (Table 9 latency/throughput, power, Fig. 9b), FPGA F1-Macro (Table 7) on the canonical test lists in `../dataset_review_split/`, and the streaming-bottleneck analysis of the sparsity experiment (R2-M6).

Open decision: FINN runs inside its Docker container, which mounts `~/uav/finn`. Notebooks developed here may later be copied to `~/uav/finn/notebooks/uav_finn/classification_review/` (the only folder of `~/uav` that may be modified; see `claude_instructions/90_old_repo.md`).
