# Wildfire Paper Review — Claude Instructions

## Mission

Assist with the scientific revision of a paper on edge AI and FPGA implementation of quantized convolutional neural networks.

The final objective is to address all reviewer comments rigorously while preserving scientific reproducibility and experimental provenance.

## Legacy

This is an investigation finished at March 2025, so it is a long time since it was done and the code has not been reviewed since then. The user has been kept in the remote server and folders and files are untouched, so eveything should work again, unless updates were performed in HW, specially in the CUDA version of the GPU, which could break the use of the libraries in the conda environments.

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

The file `~/wildfire_paper_review/paper_files/discussion.md` will contain information about the paper problems detected by the reviewers and it will be used to discuss the solutions between Claude and Me.


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
