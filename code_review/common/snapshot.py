"""Materialize the historical code of a family at a given ~/uav git revision.

The active copy in code/ equals the ~/uav working tree, which was committed
on 2026-10-03 (5cd2012) together with post-paper changes. Some of those
changes alter files used by the paper runs: for example,
bed_05_brevitas_fpga_old_small_big.py no longer defines the deployed BED FPGA
architecture of Table 4. Audits of paper runs therefore import code from a
paper-era revision, extracted read-only with `git archive` into
common/artifacts/snapshots/<rev>/ (git-ignored).

Known revisions:
  455f115  2025-02-28  "Code folder updated: BED evol, all MobilenetV2 last experiments"
                        (first commit after the last paper runs, Feb 2025; mobilenet
                        config.py points to run test_v23)
  f8d1ede  2024-11-07  "MobileNet Resnet through FINN flow" (around Nano runs test_v04/v05)
  5cd2012  2026-10-03  working-tree dump = active copy in code/
"""
import io
import subprocess
import tarfile

from . import paths

PAPER_ERA_REV = '455f115'


def _git(*args):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(paths.UAV_ROOT), *args],
                          capture_output=True, check=True)


def resolve(rev):
    return _git('rev-parse', '--verify', f'{rev}^{{commit}}').stdout.decode().strip()


def materialize(family, rev=PAPER_ERA_REV):
    """Return the family code folder (containing config.py and modules/) at `rev`."""
    _, hist_dir = paths.family_dirs(family)
    rel = hist_dir.relative_to(paths.UAV_ROOT).as_posix()
    full = resolve(rev)
    dest_root = paths.artifacts_dir('common', 'snapshots', full[:12])
    dest = dest_root / rel
    marker = dest / '.complete'
    if marker.exists():
        return dest
    tar_bytes = _git('archive', '--format=tar', full, '--', rel).stdout
    with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as tf:
        members = [m for m in tf.getmembers() if m.name.startswith(rel + '/') or m.name == rel]
        tf.extractall(dest_root, members=members)
    marker.write_text(f'{full}\n')
    return dest
