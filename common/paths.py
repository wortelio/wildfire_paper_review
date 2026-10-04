"""Absolute paths for the review work.

Repository layout:
  code/                  byte-identical copy of the historical code (never edited)
  common/                shared infrastructure (this package)
  dataset_review_split/  canonical, versioned file lists (test_full, test_clean, train, val)
  01_replicas/           faithful replicas of the paper models (no training)
  02_audit/              analyses of the paper's own artifacts (no training): f0, f1
  03_revision/           new experiments for the resubmission (training): f2, f3, f_aimet

The historical repository (~/uav) is read-only evidence: datasets and
checkpoints are read from there, never written. Outputs live under
<experiment>/{results,artifacts}: results/ is versioned, artifacts/ is git-ignored.
"""
from pathlib import Path

HOME = Path.home()
UAV_ROOT = (HOME / 'uav').resolve()
UAV_CODE = UAV_ROOT / 'code'
UAV_DATASETS = UAV_ROOT / 'datasets'

REPO_ROOT = Path(__file__).resolve().parents[1]
CODE_TRAIN = REPO_ROOT / 'code' / 'train'
COMMON_DIR = REPO_ROOT / 'common'
SPLITS_DIR = REPO_ROOT / 'dataset_review_split'
REPLICAS_DIR = REPO_ROOT / '01_replicas'
AUDIT_DIR = REPO_ROOT / '02_audit'
REVISION_DIR = REPO_ROOT / '03_revision'

# Active (byte-identical copy) code folder -> historical folder in ~/uav.
# Identity verified with `cmp` on 2026-10-03; re-checked by env_capture.
FAMILIES = {
    'mobilenet': {
        'active': CODE_TRAIN / 'mobilenet',
        'historical': UAV_CODE / 'classifier_my_mobilenetv2',
    },
    'bed': {
        'active': CODE_TRAIN / 'bed',
        'historical': UAV_CODE / 'classifier_brevitas_2_finn',
    },
    'transfer_learning': {
        'active': CODE_TRAIN / 'baseline_transfer_learning',
        'historical': UAV_CODE / 'classifier_transfer_learning',
    },
    'vision_transformer': {
        'active': CODE_TRAIN / 'baseline_vision_transformer',
        'historical': UAV_CODE / 'classifier_vision_transformer',
    },
}

# Experiment name -> folder. results_dir()/artifacts_dir() resolve through this map.
EXPERIMENTS = {
    'common': COMMON_DIR,
    'f0_selection_bias': AUDIT_DIR / 'f0_selection_bias',
    'f1_duplicates': AUDIT_DIR / 'f1_duplicates',
    'f2_splits': REVISION_DIR / 'f2_splits',
    'f3_retrain': REVISION_DIR / 'f3_retrain',
    'f_aimet': REVISION_DIR / 'f_aimet',
}


def family_dirs(family):
    if family not in FAMILIES:
        raise KeyError(f'Unknown family {family!r}; expected one of {sorted(FAMILIES)}')
    return FAMILIES[family]['active'], FAMILIES[family]['historical']


def replica_dir(name):
    d = REPLICAS_DIR / name
    if not (d / 'config.py').exists():
        raise FileNotFoundError(f'No replica {name!r} in {REPLICAS_DIR}')
    return d


def results_dir(experiment, *sub):
    """Small, versioned outputs (JSON/CSV/tables/plots)."""
    return _exp_dir(experiment, 'results', *sub)


def artifacts_dir(experiment, *sub):
    """Large, git-ignored outputs (checkpoints, predictions, embeddings, big logs)."""
    return _exp_dir(experiment, 'artifacts', *sub)


def _exp_dir(experiment, kind, *sub):
    if experiment not in EXPERIMENTS:
        raise KeyError(f'Unknown experiment {experiment!r}; expected one of {sorted(EXPERIMENTS)}')
    d = EXPERIMENTS[experiment] / kind
    if sub:
        d = d / Path(*sub)
    d.mkdir(parents=True, exist_ok=True)
    return d
