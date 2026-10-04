# Common infrastructure (T1)

Scripts run with their own folder as working directory and find the repository root from their own path. Use the conda environment of the historical run:
- scripts: `cd <experiment folder> && /opt/conda/envs/<env>/bin/python <script>.py`;
- the self-test: `cd <repo root> && /opt/conda/envs/<env>/bin/python -m common.selftest`.

Numbered folders (`01_replicas`, `02_audit`, `03_revision`) are not Python packages. Scripts in them add the repository root to `sys.path` and import `common`. Replicas are loaded with `common.replicas.use()`.

| Module | Purpose |
|---|---|
| `paths.py` | Absolute paths: `~/uav` (read-only), `code/train/<family>` (active copy), per-phase `results/` (versioned) and `artifacts/` (git-ignored) |
| `write_guard.py` | Python audit hook (PEP 578) that aborts any write under `~/uav` or `<repo>/code`. Call `write_guard.install()` first. It does not intercept writes from C code that bypasses Python I/O (e.g. `cv2.imwrite`) |
| `config_shim.py` | `build_config(family, run_dir, fixed, code_root)` executes the historical `config.py` unchanged, ignoring assignments to `fixed` keys and resolving relative paths against the historical folder in `~/uav`. `load_family()` registers it as `config` and exposes the original `modules` package (one family per process; no `__pycache__` written) |
| `snapshot.py` | `materialize(family, rev)` extracts the family code at a `~/uav` git revision (read-only `git archive`) into `artifacts/snapshots/`. `PAPER_ERA_REV = 455f115` |
| `replicas.py` | `use(name, model)`: makes `01_replicas/<name>` importable (its `config` and `modules`) from any working directory; one replica per process |
| `env_capture.py` | Provenance record: git commit/dirty, conda env, package versions, CUDA/cuDNN/GPU, and byte-identity of `code/train/<family>` with `~/uav` |
| `selftest.py` | Infrastructure self-test (see results below) |

## Conda environment per historical run (STRONG EVIDENCE)

The notebook kernel Python version maps one-to-one to a conda environment:

| Kernel Python | Environment | Used by | Key versions |
|---|---|---|---|
| 3.10.9 | `pytorch_brevitas` | `train_brevitas.ipynb`, `train_bed_evol_brevitas.ipynb`, `train_ECA.ipynb` (QAT runs) | torch 2.1.2+cu121, brevitas 0.10.2, albumentations 1.3.1, cv2 4.5.3 |
| 3.10.13 | `pytorch_23` | `train.ipynb` (mobilenet, bed, transfer learning, ViT), `train_bed_evol.ipynb` (FP32 runs) | torch 2.3.1+cu121, albumentations 1.4.10, cv2 4.10.0 |

Note: FP32 and QAT runs therefore used **different Albumentations / OpenCV versions**. This must be kept when re-running (F3).

Both environments see the RTX 4070 Ti with the current driver (555.42.02, CUDA 12.5), so the CUDA risk mentioned in the CLAUDE.md "Legacy" section does not materialize (VERIFIED 2026-10-03).

## Self-test results (2026-10-03, `results/selftest/selftest_<env>.json`)

- **write_guard (VERIFIED):** blocks `open('w'/'a')`, `os.open(O_CREAT)` and `mkdir` on a protected scratch root; reading `~/uav` is still allowed. `~/uav` and `code/` are reported as protected. A `find -newer` check after the runs showed **no file written under `~/uav` or `code/`**.
- **Paper-era snapshot `455f115`:** all four families build their config, resolve the dataset paths to `~/uav/datasets`, import the original modules and load a test batch, in both environments.
- **Active copy (`code/train`, = `~/uav` working tree, 2026-10-03): it is NOT usable as-is for the paper runs (VERIFIED):**
  1. `mobilenet/config.py` asserts `FOG + SICILIA + FIGLIB == 1`, an assertion added after the paper. It cannot select the DFire+FASDD dataset.
  2. `bed/modules/models_bed_evolution/bed_05_brevitas_fpga_old_small_big.py` now defines an "all 4-bit / multiples of 8" variant (conv1 16 ch, conv3.4 Mid 48, ...). The deployed BED FPGA architecture of Table 4 (conv1 12 ch, conv3.4 Mid 44, 2-bit layers) exists only in `455f115`, and is commented out in the current file.
  3. `baseline_transfer_learning/modules/dataset_dfire.py` was not copied to the active repo (`ModuleNotFoundError`).

  Consequence: audits of paper runs use `snapshot.materialize(family, '455f115')` by default. Whether `455f115` is exactly the code of each run is checked by the T3 sanity gate (strict state-dict loading + reproduction of the logged metrics).
- **Evaluation detail (VERIFIED, all families):** the historical `get_val_loader()` uses `drop_last=True` with batch size 64 (128 in the last BED config). The historical test metrics were therefore computed on 24,320 of the 24,371 test images (Table 1); the same last 51 images (`shuffle=False`) are always excluded. T3 reproduces this setting; later evaluations will also report the full test set.
