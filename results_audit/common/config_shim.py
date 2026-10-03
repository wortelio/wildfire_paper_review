"""Build the `config` module of a historical run without editing code/.

The historical code does `import config` from almost every module. Each
code/train/<family>/config.py holds the state of the *last* experiment run
in that folder, uses paths relative to the historical folder in ~/uav, and
creates directories at import time.

build_config() executes that file unchanged, with three differences:
  1. Keys passed in `fixed` are frozen: any assignment to them inside
     config.py is ignored, so values derived from them (e.g. NUM_CLASSES from
     the dataset flags, LOGS_FOLDER from RUN_FOLDER) are computed consistently
     with the run being audited.
  2. RUN_FOLDER is always frozen to an audit artifacts directory, so the
     mkdir calls in config.py only create folders there.
  3. After execution, every relative path ('./...' or '../...') is resolved
     against the historical folder in ~/uav (so '../../datasets/' -> ~/uav/datasets).

load_family() then registers the module as `config` and makes the original
`modules` package of that family importable. Only one family per process.

code_root selects which copy of the historical code is used: the active copy
in code/train (default, = ~/uav working tree, 2026-10-03) or a paper-era
revision extracted by snapshot.materialize().
"""
import hashlib
import importlib
import os
import sys
import types
from pathlib import Path

from . import paths


class _FrozenNamespace(dict):
    """Locals mapping for exec(): assignments to frozen keys are ignored."""

    def __init__(self, fixed):
        super().__init__(fixed)
        self._fixed = frozenset(fixed)
        self.assigned = set()

    def __setitem__(self, key, value):
        self.assigned.add(key)
        if key in self._fixed:
            return
        super().__setitem__(key, value)


def _resolve_relative(value, base):
    if isinstance(value, str) and (value.startswith('./') or value.startswith('../')):
        trailing = '/' if value.endswith('/') else ''
        return os.path.normpath(os.path.join(base, value)) + trailing
    return value


def build_config(family, run_dir, fixed=None, allow_new=(), code_root=None):
    """Return a module object equivalent to <code_root>/config.py for one run.

    family    : key of paths.FAMILIES
    code_root : folder with config.py and modules/ (default: active copy in code/train;
                use snapshot.materialize(family, rev) for a historical ~/uav revision)
    run_dir   : directory for this run's outputs (inside results_audit/.../artifacts)
    fixed     : {NAME: value} frozen before executing config.py
    allow_new : names in `fixed` that do not exist in config.py (otherwise an error,
                to catch typos that would silently do nothing)
    """
    active_dir, hist_dir = paths.family_dirs(family)
    code_root = Path(code_root) if code_root else active_dir
    src_path = code_root / 'config.py'
    src = src_path.read_text()

    run_dir = Path(run_dir).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    frozen = {'RUN_FOLDER': str(run_dir) + '/'}
    frozen.update(fixed or {})

    ns = _FrozenNamespace(frozen)
    exec_globals = {'__name__': 'config', '__file__': str(src_path), '__builtins__': __builtins__}
    exec(compile(src, str(src_path), 'exec'), exec_globals, ns)

    unknown = set(fixed or {}) - ns.assigned - set(allow_new)
    if unknown:
        raise KeyError(f'Fixed keys never assigned in {src_path}: {sorted(unknown)} '
                       f'(typo? pass them in allow_new if intentional)')

    mod = types.ModuleType('config')
    mod.__file__ = str(src_path)
    for k, v in ns.items():
        if k.startswith('__'):
            continue
        setattr(mod, k, _resolve_relative(v, hist_dir))
    mod.__audit__ = {
        'family': family,
        'code_root': str(code_root),
        'source': str(src_path),
        'source_sha256': hashlib.sha256(src.encode()).hexdigest(),
        'relative_paths_resolved_against': str(hist_dir),
        'fixed': {k: repr(v) for k, v in frozen.items()},
    }
    return mod


def load_family(family, config_module, code_root=None):
    """Register `config_module` as `config` and expose the `modules` package of code_root."""
    root = Path(code_root) if code_root else paths.family_dirs(family)[0]
    loaded = sys.modules.get('modules')
    if loaded is not None:
        loaded_from = list(getattr(loaded, '__path__', []))
        if str(root / 'modules') not in loaded_from:
            raise RuntimeError(f'`modules` already loaded from {loaded_from}; one family per process')
    sys.dont_write_bytecode = True          # keep code/ free of __pycache__
    sys.modules['config'] = config_module
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return importlib.import_module('modules')
