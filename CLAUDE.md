# Wildfire Paper Review — Claude Instructions

## Mission

Assist with the scientific revision of a paper on edge AI and FPGA implementation of quantized convolutional neural networks.

The final objective is to address all reviewer comments rigorously while preserving scientific reproducibility and experimental provenance.

## Legacy

This is an investigation finished at March 2025, so it is a long time since it was done and the code has not been reviewed since then. The user has been kept in the remote server and folders and files are untouched, so eveything should work again, unless updates were performed in HW, specially in the CUDA version of the GPU, which could break the use of the libraries in the conda environments.

## State of the copied code (important)

The code in `~/wildfire_paper_review/code/` is a copy of the **last state of `~/uav` before the project was abandoned**, not a snapshot of the paper experiments:

- Each `config.py` holds the settings of the **last experiment run** in that folder (e.g. FIgLib, ShiftReLU or 5-epoch tests). These are not necessarily the settings of the runs reported in the paper. **Never assume a `config.py` reflects a paper result.**
- **Intended design (user, 2026-10-03):** the selection of files copied from `~/uav` should contain everything needed to reconstruct the paper results. The only changes needed should be small edits to the `config.py` settings (dataset flags, model, bit widths, image size, run folder, …). The settings of each paper run must be recovered from its historical log header (`logs/logfile.log`), notebook outputs and Git history.
- **Known exceptions to that design** (VERIFIED by the audit self-test, see `common/README.md`):
  1. `code/train/bed/modules/models_bed_evolution/bed_05_brevitas_fpga_old_small_big.py`: the current file defines a later "all 4-bit / multiples of 8" variant. The deployed BED FPGA architecture of Table 4 is commented out in it and is active only at `~/uav` revision `455f115`. Here a model file differs, not just a `config.py`.
  2. `code/train/mobilenet/config.py`: has an `assert FOG+SICILIA+FIGLIB == 1` added after the paper, so it needs more than a value change to select DFire+FASDD.
  3. `code/train/baseline_transfer_learning/modules/dataset_fasdd.py` exists, but `dataset_dfire.py` was not copied.
  4. The FINN build folder of the deployed MobileNetV2 Nano (`~/uav/finn/notebooks/uav_finn/classification/my_mblnet_resnet_to_finn_driver`) was not copied. `code/finn/mobilenet/to_finn_driver/my_mblnet_to_finn_driver` uses a different model.
- **Policy:** files in `code/` are kept byte-identical to `~/uav` (provenance evidence). Paper runs are reproduced through `01_replicas/` (adapted copies, validated against the paper) and the infrastructure in `common/` (`common/config_shim.py` overrides `config.py` values without editing the file; `common/snapshot.py` provides the paper-era code `455f115` where needed). Any change to code goes into a copy, with its diff documented.

## Read these project instructions first

Before substantial work, read:

- `claude_instructions/01_paper_pdf_to_markdown.md`
- `claude_instructions/02_review_objective.md`
- `claude_instructions/03_domain_and_tooling.md`
- `claude_instructions/04_claude_agent_spec.md`
- `claude_instructions/05_experimental_provenance.md`
- `claude_instructions/06_reproducibility_and_git.md`
- `claude_instructions/90_old_repo.md`


If these files are stored elsewhere, locate them before proceeding.

## Active repository

The active working repository is expected to be:

`~/wildfire_paper_review`

Verify with:

```bash
pwd
git rev-parse --show-toplevel
```

Changes requested for the review belong in this repository.

## Historical repository

There is an older repository expected to be here:
`~/uav` 

It contains historical experiments and Git history. Its content is explained in /claude_instructions/90_old_repo.md.

Its exact filesystem path must be verified before use.

Treat it as **READ-ONLY historical evidence** unless the user explicitly says otherwise.

Do not modify, move, rename or delete files in the historical repository.

## Paper

The original PDF is authoritative.

A Markdown transcription may be created to make the manuscript easier to inspect and work with, but it must be faithful to the PDF.

Never silently modify scientific content during PDF-to-Markdown conversion.

If the Markdown and PDF disagree, the PDF wins.

## Reviewers

Reviewer comments are requirements to be tracked explicitly.

For each reviewer comment, connect:

reviewer comment
→ paper section/table/figure
→ relevant code
→ relevant historical experiment
→ required action
→ validation evidence
→ final response/change

## Discussion

The folder `~/wildfire_paper_review/paper_files/discussions/` (`00_discussion.md` general overview; one numbered file per topic, e.g. `01_dataset.md`) will contain information about the paper problems detected by the reviewers and it will be used to discuss the solutions between Claude and Me.


## Experimental evidence

Do not assume that the code currently copied into the active repository is exactly the code that generated the published results.

When provenance is uncertain, investigate the historical repository, outputs and Git history.

Always distinguish:

- VERIFIED
- STRONG EVIDENCE
- INFERENCE
- HYPOTHESIS
- UNKNOWN

Never present an inference as a verified fact.

## Technical domain

Act as an expert assistant in:

- Python
- Jupyter notebooks
- PyTorch
- CNN training
- quantization-aware training
- Brevitas
- QONNX / ONNX
- FINN
- AMD/Xilinx FPGA dataflow implementations
- FPGA resource/performance analysis

Pay particular attention to dependency/version compatibility and reproducibility.

## Git commits and large files

- A versioned pre-commit hook (`.githooks/pre-commit`, enabled with `git config core.hooksPath .githooks`) **rejects any commit that adds, modifies or renames a file larger than 1 MB** (staged size). Each blocked attempt is appended to `.git/large_files_blocked.log`.
- When a commit is blocked:
  1. **Do not bypass the hook:** no `--no-verify`, no disabling the hook, no splitting or compressing files to sneak them in, no silently changing `.gitignore` to hide them.
  2. **Do not make that commit.** Leave the changes uncommitted, and keep working on the remaining tasks that do not need it (long runs in tmux keep going).
  3. Report the blocked commit and the large files in the next message to the user. The user decides afterwards: exclude the file (`.gitignore`, `artifacts/`), or explicitly approve committing it.
- Large outputs (weights, predictions, embeddings, executed notebooks with big outputs) belong in git-ignored `artifacts/` folders by design.
- Long tasks run inside the tmux session `review`. Long computations are launched detached (`setsid`/`nohup`) with logs on disk, and scripts are resumable (they skip results that already exist), so an SSH disconnection does not lose work.

## Change policy

Before scientifically meaningful changes:

1. identify the reviewer requirement;
2. identify the affected paper claim/result;
3. establish experimental provenance;
4. explain the proposed change;
5. make the smallest justified change;
6. validate it;
7. inspect the Git diff;
8. record the evidence.

Do not update dependencies automatically.

Do not overwrite historical checkpoints, logs or experimental outputs.

Do not perform large refactors before reproducing/understanding the historical behavior.

## Notebooks

The historical project relies heavily on notebooks.

Be alert to:

- implicit execution order;
- hidden state;
- stored outputs;
- hard-coded paths;
- duplicated code;
- checkpoints;
- configuration embedded in cells.

Do not automatically convert all notebooks to Python modules.

First establish provenance and reproducibility.

## Default behavior under uncertainty

Investigate first.

Show paths, evidence and relevant Git history.

Ask for human judgment only when the decision is scientifically ambiguous or would materially alter the experiment.

Prefer small, reversible and version-controlled changes.
