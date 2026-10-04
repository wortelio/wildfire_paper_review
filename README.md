# wildfire_paper_review

Revision of manuscript Access-2026-39017, "Hardware-Aware Optimization for Low-Power FPGA-Based Wildfire Classification in UAV Edge AI" (IEEE Access). Working instructions for Claude: `CLAUDE.md` and `claude_instructions/`.

## Layout

```
wildfire_paper_review/
├── code/                  # byte-identical copy of the historical code in ~/uav (never edited)
├── paper_files/           # original PDF, paper.md, reviewers/ (comments + response matrix),
│                          #   discussions/ (00_discussion.md, 01_dataset.md, ...), paper_comments.md
├── common/                # shared infrastructure (importable package): paths, write_guard, config_shim,
│                          #   snapshot, env_capture, replicas.use(), selftest
├── dataset_review_split/  # canonical, versioned file lists: test_full, test_clean (F1), train/val (F2)
├── 01_replicas/           # faithful replicas of the paper models (historical code + config + weights);
│   └── mobilenet_paper/   #   validated against the paper. Next: bed_paper/
├── 02_audit/              # analyses of the paper's own artifacts, no training
│   ├── f0_selection_bias/
│   └── f1_duplicates/
└── 03_revision/           # new experiments for the resubmission, with training
    ├── f2_splits/         #   code that generates the train/val lists (written to dataset_review_split/)
    ├── f3_retrain/
    └── f_aimet/
```

Dependency order: `01_replicas` (trusted base) → `02_audit` (uses the replicas' models and predictions) → `03_revision` (copies and modifies the replicas' code; uses audit outputs). `common/` and `dataset_review_split/` are shared by all three.

## Rules

1. **`~/uav` is read-only historical evidence.** Datasets and checkpoints are read from `~/uav`, never written. `common/write_guard.py` enforces this at run time; it also protects `code/`.
2. **`code/` is never edited.** `code/train/**` and `code/finn/**` are byte-identical copies of the `~/uav` working tree (verified 2026-10-03), and that identity is part of the provenance evidence. **That working tree is the last state of the project, not the paper-era code** (see `CLAUDE.md`, "State of the copied code").
3. **Replicas** (`01_replicas/<model>_paper/`) copy the needed historical files unchanged, adapt only `config.py` (every change marked `# REPLICA:`), keep byte-identical local copies of the paper weights (git-ignored), and must reproduce the published numbers before being used.
4. **Copy-on-write for code changes.** Any modified module lives in the experiment folder that needs it, with its diff against the original documented in that folder's README.
5. **Every result records its provenance:** git commit, conda environment, package versions, GPU, date, and the exact command or notebook (`common/env_capture.py`).
6. **Outputs.** Each experiment folder has:
   - `results/`: small, versioned outputs (JSON, CSV summaries, Markdown tables, plots);
   - `artifacts/`: large, git-ignored outputs (weights, per-image predictions, embeddings, big logs).

   Commits of files > 1 MB are blocked by `.githooks/pre-commit`.
7. **How to run.** Scripts and notebooks run with their own folder as working directory. They find the repository root from their own path, so they never depend on the working directory for data. One replica (one historical `config`/`modules`) per process: `common.replicas.use(name, model)`. Long runs go in the tmux session `review`, detached (`setsid`/`nohup`), and are resumable.
8. **Evidence levels** in reports: VERIFIED / STRONG EVIDENCE / INFERENCE / HYPOTHESIS / UNKNOWN.

## Status

| Item | Status |
|---|---|
| Paper transcription (`paper_files/paper.md`) | Done |
| Reviewer comments + response matrix | Triaged (`paper_files/reviewers/response_matrix.md`) |
| `common/` infrastructure | Done (self-test: `common/results/selftest/`) |
| `01_replicas/mobilenet_paper` | Done: MobileNetV2 Nano FP32 and Brevitas QAT (Tables 5, 7, 8) reproduced exactly (VERIFIED; max abs diff = 0 vs logs) |
| `01_replicas/bed_paper` | Not started |
| `02_audit/f0_selection_bias` | Done 2026-10-04: selection effect +0.03–0.71 pp (larger for QAT/from-scratch models); conclusions keep their sign, but the "< 2.5 pp" headline is not robust (A-13); canonical test lists written |
| `02_audit/f1_duplicates` | Planned (`paper_files/discussions/01_dataset.md`, P0–P7) |
| `03_revision/*` | Not started; scope decided after F0/F1 |

History: until 2026-10-04 everything under `common/`, `01_replicas/`, `02_audit/` and `03_revision/` lived in `results_audit/` (see git history). JSON results and executed notebooks produced before the move still record the old paths. They are historical records and were left unchanged.
