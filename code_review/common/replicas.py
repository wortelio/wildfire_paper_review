"""Load a paper replica (code_review/train/01_replicas/<name>) from any working directory.

A replica keeps the historical code unchanged: its modules do `import config`
and `import modules.<x>` as top-level imports. use() therefore puts the
replica folder first on sys.path and imports its `config`. Only one replica
can be loaded per process (two replicas would collide on `config`/`modules`);
use one process per replica/model, as 01_replicas/*/run_validation.sh does.

Usage (first lines of an audit script):
    import sys; from pathlib import Path
    HERE = Path(__file__).resolve().parent
    sys.path.insert(0, str(next(p for p in HERE.parents if (p / 'common' / '__init__.py').exists())))
    from common import replicas
    config = replicas.use('mobilenet_paper', model='fp32')
    from modules.model_mobilenetv2_mini_Resnet import MobileNetV2_MINI_RESNET
"""
import importlib
import os
import sys

from . import paths, write_guard

_loaded = None


def use(name, model=None, guard=True):
    """Make replica `name` importable and return its config module.

    model : value for the REPLICA_MODEL environment variable read by the replica's
            config.py (e.g. 'fp32' or 'brevitas' for mobilenet_paper); None keeps the default.
    """
    global _loaded
    if guard:
        write_guard.install()
    rdir = paths.replica_dir(name)
    key = (name, model)
    if _loaded is not None:
        if _loaded != key:
            raise RuntimeError(f'Replica {_loaded} already loaded in this process; cannot load {key}. '
                               f'Use one process per replica/model.')
        return sys.modules['config']
    for mod in ('config', 'modules'):
        if mod in sys.modules:
            raise RuntimeError(f'A module named {mod!r} is already imported '
                               f'({getattr(sys.modules[mod], "__file__", "?")}); cannot load replica {name!r}.')
    if model is not None:
        os.environ['REPLICA_MODEL'] = model
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(rdir))
    config = importlib.import_module('config')
    if os.path.dirname(os.path.abspath(config.__file__)) != str(rdir):
        raise RuntimeError(f'Imported config from {config.__file__}, expected {rdir}')
    _loaded = key
    return config
