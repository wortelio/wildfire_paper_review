"""F0 — Evaluate alternative checkpoints of the MobileNetV2 Nano paper runs with the validated replica.

For each model (fp32: test_v04, brevitas: test_v05) this evaluates, on the full paper test set
(24,371 images, single pass, drop_last=False):
    best_mean_F1  (the checkpoint reported in the paper; selected on the test set)
    best_loss     (selected on the test loss; also test-dependent)
    last          (last epoch; no checkpoint selection, but the LR scheduler still monitored the test loss)
Metrics are computed on the full test set and on the first 24,320 images (= the historical
drop_last=True protocol), and the latter are compared with the per-epoch values parsed from the log
(4 decimals), which checks that log epoch <-> checkpoint file mapping is right.

Checkpoints are read in place from ~/uav (read-only; write_guard is active).
Resumable: a checkpoint whose results JSON exists is skipped.

Usage (from this folder, in the conda env of the original training run):
    /opt/conda/envs/pytorch_23/bin/python eval_checkpoints.py --model fp32 [--write-test-lists]
    /opt/conda/envs/pytorch_brevitas/bin/python eval_checkpoints.py --model brevitas
"""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / 'common' / '__init__.py').exists())))   # code_review/
from common import env_capture, paths, replicas  # noqa: E402
import parse_logs  # noqa: E402  (same folder)

RUNS = {
    'fp32': {'log_run': 'nano_fp32', 'env': 'pytorch_23',
             'files': {'best_mean_F1': 'MY_MBLNET_V2_classifier__best_mean_F1.pt',
                       'best_loss': 'MY_MBLNET_V2_classifier__best_loss.pt',
                       'last': 'last_MY_MBLNET_V2_classifier.pt'}},
    'brevitas': {'log_run': 'nano_qat', 'env': 'pytorch_brevitas',
                 'files': {'best_mean_F1': 'MY_MBLNET_V2_RESNET_classifier__best_mean_F1.pt',
                           'best_loss': 'MY_MBLNET_V2_RESNET_classifier__best_loss.pt',
                           'last': 'last_MY_MBLNET_V2_RESNET_classifier.pt'}},
}
N_PAPER = 24320   # 380 batches x 64 (drop_last=True), the historical evaluation protocol


def metrics(y, p, thr=0.5):
    import numpy as np
    out = {}
    for i, c in enumerate(('smoke', 'fire')):
        yp = (p[:, i] > thr).astype(int); yt = y[:, i].astype(int)
        TP = int((yp & yt).sum()); FP = int((yp & (1 - yt)).sum())
        TN = int(((1 - yp) & (1 - yt)).sum()); FN = int(((1 - yp) & yt).sum())
        prec = TP / (TP + FP); rec = TP / (TP + FN)
        out[c] = {'TP': TP, 'FP': FP, 'TN': TN, 'FN': FN, 'Accuracy': (TP + TN) / len(yt),
                  'Precision': prec, 'Recall': rec, 'F1': 2 * prec * rec / (prec + rec)}
    out['F1_macro'] = (out['smoke']['F1'] + out['fire']['F1']) / 2
    return out


def write_test_lists(loader):
    """dataset_review_split/test_full/: the paper test set in the exact loader order, one file per source."""
    d = paths.SPLITS_DIR / 'test_full'
    d.mkdir(parents=True, exist_ok=True)
    root = str(paths.UAV_DATASETS) + '/'
    manifest, offset = [], 0
    def leaves(ds):   # get_val_loader builds ConcatDataset(ConcatDataset(dfire, uav), cv)
        return [x for d in ds.datasets for x in leaves(d)] if hasattr(ds, 'datasets') else [ds]
    parts = leaves(loader.dataset)
    assert len(parts) == 3, len(parts)
    for name, ds in zip(('dfire_test', 'fasdd_uav_test', 'fasdd_cv_test'), parts):
        lines = ['file\tsmoke\tfire']
        for f, lab in zip(ds.images_path, ds.labels):
            rel = os.path.normpath(str(f)).replace(os.path.normpath(root) + '/', '')
            lines.append(f'{rel}\t{int(lab[0])}\t{int(lab[1])}')
        text = '\n'.join(lines) + '\n'
        (d / f'{name}.tsv').write_text(text)
        manifest.append({'file': f'{name}.tsv', 'images': len(lines) - 1, 'loader_offset': offset,
                         'sha256': hashlib.sha256(text.encode()).hexdigest()})
        offset += len(lines) - 1
    (d / 'manifest.json').write_text(json.dumps({
        'description': 'Paper test set (Table 1) in the exact order of get_val_loader(): DFire test, '
                       'FASDD UAV test, FASDD CV test (concatenated in this order). Paths relative to ~/uav/datasets/. '
                       'The historical metrics used drop_last=True: only the first 24,320 images.',
        'total_images': offset, 'historical_protocol_images': N_PAPER, 'parts': manifest,
        'generated_by': 'code_review/train/02_audit/f0_selection_bias/eval_checkpoints.py'}, indent=2) + '\n')
    print(f'test lists written to {d} ({offset} images)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', choices=RUNS, required=True)
    ap.add_argument('--write-test-lists', action='store_true')
    args = ap.parse_args()
    spec = RUNS[args.model]

    config = replicas.use('mobilenet_paper', model=args.model)
    import numpy as np
    import torch
    from modules.dataloaders import get_val_loader
    if args.model == 'fp32':
        from modules.model_mobilenetv2_mini_Resnet import MobileNetV2_MINI_RESNET
    else:
        from modules.brevitas.model_mobilenetv2_mini_Resnet_Brevitas import MobileNetV2_MINI_RESNET

    res_dir = paths.results_dir('f0_selection_bias', 'checkpoints')
    art_dir = paths.artifacts_dir('f0_selection_bias', 'predictions')
    log_runs = {r[0]: r for r in parse_logs.RUNS}
    log_rel = log_runs[spec['log_run']][3]
    log_epochs, _, _ = parse_logs.parse_log(paths.UAV_CODE / log_rel / 'logs' / 'logfile.log', 0)
    by_epoch = {e['epoch']: e for e in log_epochs}
    last_epoch = log_epochs[-1]['epoch']

    loader = None
    for tag, fname in spec['files'].items():
        out_json = res_dir / f'{args.model}__{tag}.json'
        if out_json.exists():
            print(f'skip {out_json.name} (exists)')
            continue
        if loader is None:
            loader = get_val_loader(return_img_filename=True, drop_last=False)
            assert len(loader.dataset) == 24371
            if args.write_test_lists:
                write_test_lists(loader)
        ckpt_path = Path(config.PAPER_RUN_DIR) / 'weights' / fname
        ckpt = torch.load(ckpt_path, map_location=config.DEVICE)
        state = ckpt['model_state_dict'] if 'model_state_dict' in ckpt else ckpt
        epoch = ckpt.get('epoch', last_epoch) if 'model_state_dict' in ckpt else last_epoch
        model = MobileNetV2_MINI_RESNET().to(config.DEVICE)
        model.load_state_dict(state)          # strict
        model.to(config.DEVICE).eval()         # Brevitas leaves quantizer scales on CPU after loading
        t0 = time.time()
        ys, ps, files = [], [], []
        with torch.no_grad():
            for x, y, f in loader:
                ps.append(torch.sigmoid(model(x.to(config.DEVICE))).cpu().numpy())
                ys.append(y.numpy()); files.extend(f)
        y = np.concatenate(ys); p = np.concatenate(ps)
        full, hist = metrics(y, p), metrics(y[:N_PAPER], p[:N_PAPER])
        log_row = by_epoch.get(epoch)
        check = None
        if log_row:
            diffs = [abs(round(hist[c][k], 4) - log_row[f'{c}_{lk}'])
                     for c in ('smoke', 'fire') for k, lk in (('Precision', 'prec'), ('Recall', 'rec'), ('F1', 'f1'))]
            check = {'log_epoch': epoch, 'max_abs_diff_4dp': max(diffs), 'matches_log': max(diffs) <= 1e-4 + 1e-9,
                     'log_f1_macro': log_row['f1_macro']}
        np.savez_compressed(art_dir / f'{args.model}__{tag}.npz', y=y, p=p, files=np.array(files))
        rec = {'model': args.model, 'checkpoint': tag, 'file': str(ckpt_path),
               'sha256': hashlib.sha256(ckpt_path.read_bytes()).hexdigest(), 'epoch': epoch,
               'historical_protocol_24320': hist, 'full_test_24371': full, 'check_vs_log': check,
               'seconds': round(time.time() - t0, 1),
               'env': env_capture.capture(extra={'replica_model': args.model})}
        out_json.write_text(json.dumps(rec, indent=2, default=str) + '\n')
        print(f'{args.model} {tag} epoch {epoch}: F1-macro hist {100*hist["F1_macro"]:.2f} '
              f'full {100*full["F1_macro"]:.2f} | log check {check}')


if __name__ == '__main__':
    main()
