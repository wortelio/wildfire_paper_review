"""Absolute paths for the results audit.

The historical repository (~/uav) is read-only evidence: datasets and
checkpoints are read from there, never written. Audit outputs live under
results_audit/<phase>/{results,artifacts}.
"""
from pathlib import Path

HOME = Path.home()
UAV_ROOT = (HOME / 'uav').resolve()
UAV_CODE = UAV_ROOT / 'code'
UAV_DATASETS = UAV_ROOT / 'datasets'

REPO_ROOT = Path(__file__).resolve().parents[2]
CODE_TRAIN = REPO_ROOT / 'code' / 'train'
AUDIT_ROOT = REPO_ROOT / 'results_audit'

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

PHASES = ('f0_selection_bias', 'f1_duplicates', 'f2_splits', 'f_aimet', 'f3_retrain', 'common')


def family_dirs(family):
    if family not in FAMILIES:
        raise KeyError(f'Unknown family {family!r}; expected one of {sorted(FAMILIES)}')
    return FAMILIES[family]['active'], FAMILIES[family]['historical']


def results_dir(phase, *sub):
    """Small, versioned outputs (JSON/CSV/tables/plots)."""
    return _phase_dir(phase, 'results', *sub)


def artifacts_dir(phase, *sub):
    """Large, git-ignored outputs (checkpoints, embeddings, big logs)."""
    return _phase_dir(phase, 'artifacts', *sub)


def _phase_dir(phase, kind, *sub):
    if phase not in PHASES:
        raise KeyError(f'Unknown phase {phase!r}; expected one of {PHASES}')
    d = AUDIT_ROOT / phase / kind / Path(*sub) if sub else AUDIT_ROOT / phase / kind
    d.mkdir(parents=True, exist_ok=True)
    return d
