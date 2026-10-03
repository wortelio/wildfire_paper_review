# First Claude Code session — recommended script

Use this after Claude Code has access to the active repository and, if desired, the historical repository as an additional directory.

## Phase 1 — Orientation only

Start with:

```text
We are beginning the revision of a scientific paper.

Do not modify any files yet.

First read CLAUDE.md and all referenced project instructions.

Then:

1. Verify the root of the active repository.
2. Describe its current directory structure.
3. Locate the original paper PDF and any existing Markdown transcription.
4. Locate reviewer comments, if already present.
5. Verify whether the historical `uav` repository is accessible.
6. Confirm its actual filesystem path.
7. Treat the historical repository as read-only.
8. Identify the Conda environment(s) and dependency information available.
9. Identify the main notebooks/scripts for:
   - training;
   - Brevitas quantization;
   - model export;
   - FINN processing/build;
   - evaluation;
   - generation of paper tables/figures.
10. Report uncertainties. Do not guess.

Return an orientation report with file paths and evidence.
```

## Phase 2 — Paper transcription

If `paper.md` does not exist or has not been verified:

```text
Read the PDF-to-Markdown instructions.

Create a faithful Markdown working representation of the scientific paper.

Do not rewrite, correct, summarize or improve the paper.

Preserve numerical values, equations, tables, captions, references and technical terminology.

Mark anything uncertain.

After conversion, perform a second verification pass against the original PDF and report remaining uncertainties.
```

## Phase 3 — Reviewer requirements

After reviewer reports are available:

```text
Read all reviewer reports.

Create a reviewer response matrix.

For each substantive comment identify:
- the exact requirement;
- affected manuscript section/table/figure;
- whether existing evidence is sufficient;
- code/experiment likely involved;
- whether historical provenance must be investigated;
- required action;
- validation criterion.

Do not implement changes yet.
```

## Phase 4 — Experimental provenance audit

Then:

```text
Audit the provenance of the paper's important quantitative results.

Do not modify files.

For each important table, figure and quantitative claim, establish as much as possible of:

paper result
→ historical experiment
→ notebook/script
→ configuration
→ dataset/split
→ seed
→ checkpoint
→ log/output
→ FINN artefacts if relevant
→ Git commit/version
→ corresponding code in the active repository

Search the historical repository when needed.

Do not assume that similar numerical results prove identity.

Classify conclusions as VERIFIED, STRONG EVIDENCE, INFERENCE, HYPOTHESIS or UNKNOWN.

Flag discrepancies between the active repository and the historical code.
```

## Phase 5 — Plan the revision

Only after orientation/provenance:

```text
Build a revision plan ordered by dependency and risk.

Separate:
- editorial-only changes;
- clarifications;
- reproducibility fixes;
- historical experiment recovery;
- experiments that must be rerun;
- genuinely new experiments;
- FPGA/FINN rebuilds;
- tables/figures to update.

For every proposed technical change, link it to the reviewer comment and paper result it addresses.

Do not start large refactors unless they are necessary for a reviewer requirement or reproducibility.
```

## Phase 6 — Execute incrementally

For each task:

```text
Before editing:
1. state the evidence;
2. state the intended change;
3. state how it will be validated.

Then implement the smallest justified change.

Afterward:
1. run the relevant validation;
2. show/summarize git diff;
3. record outputs and experiment metadata;
4. update reviewer/provenance tracking.
```
