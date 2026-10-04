"""Self-test of the audit infrastructure (task T1).

Run from the repository root with each conda environment to be used:
    /opt/conda/envs/pytorch_brevitas/bin/python -m common.selftest
    /opt/conda/envs/pytorch_23/bin/python -m common.selftest

Checks:
  1. write_guard blocks writes to ~/uav and code/ (tested on a scratch root, never on ~/uav itself).
  2. For each family: config.py executes through the shim, dataset paths resolve to ~/uav/datasets,
     the original `modules` package imports unchanged, and one test batch can be loaded.
  3. The active code is still byte-identical to ~/uav; nothing was written to ~/uav or code/.
Each family runs in its own subprocess (one `modules` package per process), once with the
active copy in code/ and once with the paper-era snapshot (snapshot.PAPER_ERA_REV).
Expected finding (2026-10-03): the active mobilenet config.py cannot select DFire+FASDD
(assert FOG+SICILIA+FIGLIB == 1, added after the paper runs).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from . import config_shim, env_capture, paths, snapshot, write_guard

FAMILIES_BY_ENV = {
    'pytorch_brevitas': ('mobilenet', 'bed'),
    'pytorch_23': ('mobilenet', 'bed', 'transfer_learning', 'vision_transformer'),
}
# Dataset selection flags present in some config.py files: force DFire + FASDD.
DATASET_FLAGS = {'mobilenet': {'FOG': 0, 'FOUR_CLASSES': 0, 'SICILIA': 0, 'FIGLIB': 0}}
DATASET_PATH_KEYS = ('DFIRE_TRAIN_IMG_DIR', 'DFIRE_TEST_IMG_DIR', 'DFIRE_TEST_LABEL_DIR',
                     'FASDD_UAV_IMGS_DIR', 'FASDD_UAV_TEST_LABELS_FILE',
                     'FASDD_CV_IMGS_DIR', 'FASDD_CV_TEST_LABELS_FILE')


def check_guard():
    write_guard.install()
    out = {}
    out['uav_protected'] = write_guard.is_protected(paths.UAV_ROOT / 'code' / 'x.txt')
    out['code_protected'] = write_guard.is_protected(paths.REPO_ROOT / 'code' / 'train' / 'x.txt')
    out['audit_not_protected'] = not write_guard.is_protected(paths.AUDIT_DIR / 'x.txt')
    scratch = Path(tempfile.mkdtemp(prefix='wg_selftest_'))
    write_guard.install(extra_protected=[scratch])
    blocked = {}
    for name, fn in {
        'open_w': lambda: open(scratch / 'a.txt', 'w'),
        'open_a': lambda: open(scratch / 'a.txt', 'a'),
        'mkdir': lambda: os.mkdir(scratch / 'd'),
        'os_open_creat': lambda: os.open(scratch / 'b.txt', os.O_WRONLY | os.O_CREAT),
    }.items():
        try:
            fn()
            blocked[name] = False
        except write_guard.ProtectedWriteError:
            blocked[name] = True
    out['blocked_on_scratch'] = blocked
    out['scratch_still_empty'] = not any(scratch.iterdir())
    try:
        with open(paths.UAV_ROOT / 'code' / 'analysis_models.ipynb', 'r') as f:
            f.read(10)
        out['read_uav_allowed'] = True
    except Exception as e:  # noqa: BLE001
        out['read_uav_allowed'] = f'FAILED: {e}'
    return out


def run_family(family, rev=None):
    write_guard.install()
    code_root = snapshot.materialize(family, rev) if rev else None
    run_dir = paths.artifacts_dir('common', 'selftest', f'{family}@{rev or "active"}')
    cfg0 = (code_root or paths.family_dirs(family)[0]) / 'config.py'
    flags = {k: v for k, v in DATASET_FLAGS.get(family, {}).items() if f'{k} =' in cfg0.read_text()}
    fixed = dict(flags)
    fixed.update({'DS_LEN': 64, 'NUM_WORKERS': 2})
    cfg = config_shim.build_config(family, run_dir, fixed=fixed, code_root=code_root)
    res = {'family': family, 'code': rev or 'active', 'code_root': str(code_root or paths.family_dirs(family)[0]),
           'env': os.environ.get('CONDA_DEFAULT_ENV') or Path(sys.prefix).name,
           'NUM_CLASSES': cfg.NUM_CLASSES, 'IMG': (cfg.IMG_H, cfg.IMG_W), 'DEVICE': cfg.DEVICE,
           'RUN_FOLDER': cfg.RUN_FOLDER, 'paths': {}}
    for k in DATASET_PATH_KEYS:
        v = getattr(cfg, k)
        res['paths'][k] = {'value': v, 'exists': os.path.exists(v),
                           'under_uav_datasets': os.path.realpath(v).startswith(str(paths.UAV_DATASETS))}
    config_shim.load_family(family, cfg, code_root=code_root)
    import modules.dataloaders as dataloaders  # noqa: E402  (original, unmodified module)
    import modules.metrics  # noqa: F401,E402
    loader = dataloaders.get_val_loader()
    x, y = next(iter(loader))
    res['val_subset_len'] = len(loader.dataset)
    res['batch'] = {'x_shape': list(x.shape), 'x_min': float(x.min()), 'x_max': float(x.max()),
                    'y_shape': list(y.shape), 'y_unique': sorted(set(y.flatten().tolist()))}
    res['modules_path'] = list(sys.modules['modules'].__path__)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--family')
    ap.add_argument('--rev')
    args = ap.parse_args()
    if args.family:
        print(json.dumps(run_family(args.family, args.rev), default=str))
        return

    env = os.environ.get('CONDA_DEFAULT_ENV') or Path(sys.prefix).name
    families = FAMILIES_BY_ENV.get(env, ('mobilenet', 'bed'))
    report = {'guard': check_guard(), 'families': {}}
    for fam in families:
        for rev in (None, snapshot.PAPER_ERA_REV):
            cmd = [sys.executable, '-m', 'common.selftest', '--family', fam] + (['--rev', rev] if rev else [])
            p = subprocess.run(cmd, cwd=paths.REPO_ROOT, capture_output=True, text=True)
            last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ''
            key = f'{fam}@{rev or "active"}'
            try:
                report['families'][key] = json.loads(last)
            except json.JSONDecodeError:
                err = p.stderr.strip().splitlines()
                report['families'][key] = {'error': err[-1] if err else '', 'returncode': p.returncode,
                                           'stderr_tail': p.stderr[-2000:]}
    report['snapshot_rev'] = snapshot.resolve(snapshot.PAPER_ERA_REV)
    report['env'] = env_capture.capture(families=list(paths.FAMILIES))
    out = paths.results_dir('common', 'selftest') / f'selftest_{env}.json'
    env_capture.write(out, report)
    print(json.dumps(report, indent=2, default=str))
    print(f'\nWritten: {out}')


if __name__ == '__main__':
    main()
