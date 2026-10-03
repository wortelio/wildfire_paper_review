"""Provenance record attached to every audit result."""
import datetime
import hashlib
import importlib.metadata as md
import json
import os
import platform
import socket
import subprocess
import sys
from pathlib import Path

from . import paths

PACKAGES = ('torch', 'torchvision', 'brevitas', 'qonnx', 'onnx', 'onnxruntime', 'albumentations',
            'torchmetrics', 'numpy', 'opencv-python', 'opencv-python-headless', 'pillow', 'aimet-torch')
_SKIP_DIRS = {'__pycache__', '.ipynb_checkpoints'}


def _run(cmd, cwd=None):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:  # noqa: BLE001 - provenance must never crash a run
        return f'<error: {e}>'


def _code_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in _SKIP_DIRS)
        for f in sorted(filenames):
            yield Path(dirpath, f).relative_to(root)


def family_integrity(family):
    """Tree hash of the active family code and byte-identity with the historical copy."""
    active, hist = paths.family_dirs(family)
    h = hashlib.sha256()
    differ, missing = [], []
    for rel in _code_files(active):
        a = (active / rel).read_bytes()
        h.update(str(rel).encode() + b'\0' + hashlib.sha256(a).digest())
        hp = hist / rel
        if not hp.exists():
            missing.append(str(rel))
        elif hp.read_bytes() != a:
            differ.append(str(rel))
    return {'family': family, 'active_tree_sha256': h.hexdigest(),
            'identical_to_uav': not differ and not missing,
            'differ': differ, 'missing_in_uav': missing}


def capture(families=(), extra=None):
    info = {
        'timestamp': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
        'host': socket.gethostname(),
        'argv': sys.argv,
        'cwd': os.getcwd(),
        'python': sys.version.split()[0],
        'executable': sys.executable,
        'conda_env': os.environ.get('CONDA_DEFAULT_ENV') or Path(sys.prefix).name,
        'platform': platform.platform(),
        'packages': {},
        'git': {
            'commit': _run(['git', 'rev-parse', 'HEAD'], cwd=paths.REPO_ROOT),
            'branch': _run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=paths.REPO_ROOT),
            'dirty': bool(_run(['git', 'status', '--porcelain'], cwd=paths.REPO_ROOT)),
        },
        'gpu_driver': _run(['nvidia-smi', '--query-gpu=name,driver_version,memory.total', '--format=csv,noheader']),
        'code_integrity': [family_integrity(f) for f in families],
    }
    for p in PACKAGES:
        try:
            info['packages'][p] = md.version(p)
        except md.PackageNotFoundError:
            pass
    if 'torch' in sys.modules or 'torch' in info['packages']:
        try:
            import torch
            info['torch_cuda'] = torch.version.cuda
            info['cudnn'] = torch.backends.cudnn.version()
            info['cuda_available'] = torch.cuda.is_available()
            if torch.cuda.is_available():
                info['gpu'] = torch.cuda.get_device_name(0)
        except Exception as e:  # noqa: BLE001
            info['torch_error'] = str(e)
    if extra:
        info['extra'] = extra
    return info


def write(path, info):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(info, indent=2, default=str) + '\n')
    return path
