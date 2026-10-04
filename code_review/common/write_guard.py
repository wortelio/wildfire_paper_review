"""Abort any attempt to write inside protected directories.

Protected by default:
  - ~/uav            (historical evidence, read-only)
  - <repo>/code      (byte-identical copy of the historical code; never edited)

Implemented with a Python audit hook (PEP 578). It covers every write that
goes through Python (open, os.mkdir/remove/rename/..., shutil, torch.save,
logging.FileHandler, matplotlib, PIL, ...) and is inherited by forked
DataLoader workers. Limitation: writes done directly by C code without the
Python I/O layer (e.g. cv2.imwrite) are not intercepted; the audit code must
not use them on protected paths.

Usage (as early as possible in every audit entry point):
    from common import write_guard
    write_guard.install()
"""
import os
import sys

from . import paths

_DEFAULT_PROTECTED = (paths.UAV_ROOT, paths.REPO_ROOT / 'code')
_protected = []
_installed = False

_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
_PATH_EVENTS = {
    # event name -> indices of path arguments that must not be protected
    'os.mkdir': (0,), 'os.rmdir': (0,), 'os.remove': (0,), 'os.unlink': (0,),
    'os.rename': (0, 1), 'os.replace': (0, 1), 'os.symlink': (1,), 'os.link': (1,),
    'os.truncate': (0,), 'os.chmod': (0,), 'os.chown': (0,), 'os.utime': (0,),
    'shutil.copyfile': (1,), 'shutil.copytree': (1,), 'shutil.move': (0, 1),
    'shutil.rmtree': (0,), 'shutil.make_archive': (0,),
}


class ProtectedWriteError(PermissionError):
    pass


def _real(p):
    if isinstance(p, int) or p is None:
        return None
    if isinstance(p, bytes):
        p = os.fsdecode(p)
    return os.path.realpath(os.fspath(p))


def is_protected(path):
    rp = _real(path)
    if rp is None:
        return False
    for root in _protected:
        if rp == root or rp.startswith(root + os.sep):
            return True
    return False


def is_write_open(mode, flags):
    if isinstance(mode, str) and any(c in mode for c in 'wax+'):
        return True
    if isinstance(flags, int) and flags & _WRITE_FLAGS:
        return True
    return False


def _hook(event, args):
    if event == 'open':
        path, mode, flags = (tuple(args) + (None, None, None))[:3]
        if is_write_open(mode, flags) and is_protected(path):
            raise ProtectedWriteError(f'[write_guard] blocked write ({mode or flags}) to protected path: {path}')
    elif event in _PATH_EVENTS:
        for i in _PATH_EVENTS[event]:
            if i < len(args) and is_protected(args[i]):
                raise ProtectedWriteError(f'[write_guard] blocked {event} on protected path: {args[i]}')


def install(extra_protected=()):
    """Install the hook once per process. Extra roots can be added later calls."""
    global _installed
    for root in (*_DEFAULT_PROTECTED, *extra_protected):
        rp = os.path.realpath(os.fspath(root))
        if rp not in _protected:
            _protected.append(rp)
    if not _installed:
        sys.addaudithook(_hook)
        _installed = True
    return list(_protected)
