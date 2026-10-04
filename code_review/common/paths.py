"""Absolute paths for the review work.

Repository layout:
  code/                              byte-identical copy of the historical code (never edited)
  code_review/                       all new code of the review
    common/                          shared infrastructure (this package; used by train and finn)
    dataset_review_split/            canonical, versioned file lists (test_full, test_clean, train, val)
    train/01_replicas/               faithful replicas of the paper models (no training)
    train/02_audit/                  analyses of the paper's own artifacts (no training): f0, f1
    train/03_revision/               new experiments for the resubmission (training): f2, f3, f_aimet
    finn/                            FINN / FPGA review work (not started)

Locations are derived from this file and from the repository's .git directory, never from
the working directory or from a fixed number of parent levels, so they survive reorganizations.

The historical repository (~/uav) is read-only evidence: datasets and
checkpoints are read from there, never written. Outputs live under
<experiment>/{results,artifacts}: results/ is versioned, artifacts/ is git-ignored.
"""
from pathlib import Path

HOME = Path.home()
UAV_ROOT = (HOME / 'uav').resolve()
UAV_CODE = UAV_ROOT / 'code'
UAV_DATASETS = UAV_ROOT / 'datasets'

COMMON_DIR = Path(__file__).resolve().parent
CODE_REVIEW_DIR = COMMON_DIR.parent


def _find_repo_root(start):
    for p in (start, *start.parents):
        if (p / '.git').exists():
            return p
    raise RuntimeError(f'No .git directory above {start}')


REPO_ROOT = _find_repo_root(COMMON_DIR)
CODE_TRAIN = REPO_ROOT / 'code' / 'train'
SPLITS_DIR = CODE_REVIEW_DIR / 'dataset_review_split'
TRAIN_REVIEW_DIR = CODE_REVIEW_DIR / 'train'
FINN_REVIEW_DIR = CODE_REVIEW_DIR / 'finn'
REPLICAS_DIR = TRAIN_REVIEW_DIR / '01_replicas'
AUDIT_DIR = TRAIN_REVIEW_DIR / '02_audit'
REVISION_DIR = TRAIN_REVIEW_DIR / '03_revision'

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
