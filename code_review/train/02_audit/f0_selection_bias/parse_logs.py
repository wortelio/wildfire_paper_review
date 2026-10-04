"""F0 — Selection bias from the historical training logs (no GPU, no model loading).

Every historical run logged, after each epoch, the metrics on the *test* set
("VAL Stats"): the LR scheduler monitored that loss, and the checkpoint with
the best mean F1 was the one reported. This script parses those per-epoch
test metrics and measures how much the selected checkpoint differs from
selection-free alternatives (last epoch, mean of the last 10 epochs) and from
the best-loss checkpoint.

Usage (from this folder, any Python >= 3.8, standard library only):
    python parse_logs.py
Outputs:
    results/epochs/<run>.csv          per-epoch test metrics parsed from the log
    results/f0_log_summary.json       per-run summary
    results/f0_log_summary.md         table
"""
import csv
import json
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / 'common' / '__init__.py').exists())))   # code_review/
from common import paths, write_guard  # noqa: E402

UAV_CODE = paths.UAV_CODE

# Paper runs identified in the provenance audit (2026-10-03/04) plus candidates for
# Table 2 / MobileNetV3 Mini, whose provenance is checked here by matching the value.
RUNS = [
    # name, paper item, paper F1-Macro (%), log folder (relative to ~/uav/code), provenance status
    ('nano_fp32', 'Table 5/7/8 MobileNetV2 Nano FP32', 95.93,
     'classifier_my_mobilenetv2/experiments/test_v04_mini_resnet_70k_full_ds', 'VERIFIED (replica)'),
    ('nano_qat', 'Table 5/7/8 MobileNetV2 Nano quantized', 95.45,
     'classifier_my_mobilenetv2/experiments_brevitas/test_v05_mini_resnet_70k_full_ds', 'VERIFIED (replica)'),
    ('nano_eca', 'Table 5 MobileNetV2 Nano ECA', 95.83,
     'classifier_my_mobilenetv2/experiments/test_v11_ECA_70k_full_ds', 'STRONG EVIDENCE'),
    ('mbv2_width01', 'Table 5 MobileNetV2 Width Mult = 0.1', 93.22,
     'classifier_my_mobilenetv2/experiments/test_v21_Original_width_mult_01_full_ds', 'STRONG EVIDENCE'),
    ('nano_qat_relu6', 'Table 5 Quantized MobileNetV2 Nano ReLU6', 94.19,
     'classifier_my_mobilenetv2/experiments_brevitas/test_v41_mini_resnet_70k_relu6_full_ds', 'STRONG EVIDENCE'),
    ('nano_qat_4binp', 'Table 5 Quantized MobileNetV2 Nano 4b Input', 94.44,
     'classifier_my_mobilenetv2/experiments_brevitas/test_v71_mini_resnet_4bitINP_full_ds', 'STRONG EVIDENCE'),
    ('nano_qat_160', 'Table 10 160x160', 94.31,
     'classifier_my_mobilenetv2/experiments_brevitas/test_v21_mini_resnet_70k_160_full_ds', 'STRONG EVIDENCE'),
    ('nano_qat_112', 'Table 10 112x112', 93.81,
     'classifier_my_mobilenetv2/experiments_brevitas/test_v23_mini_resnet_70k_112_full_ds', 'STRONG EVIDENCE'),
    ('bed_original', 'Table 3 BED Original', 95.97,
     'classifier_brevitas_2_finn/experiments_bed_evolution/01_original__full_ds', 'STRONG EVIDENCE'),
    ('bed_simplified', 'Table 3 BED Simplified', 95.89,
     'classifier_brevitas_2_finn/experiments_bed_evolution/11_downto_28__full_ds', 'STRONG EVIDENCE'),
    ('bed_quantized', 'Table 3 BED Quantized', 94.70,
     'classifier_brevitas_2_finn/experiments_bed_evolution/41_brevitas__full_ds', 'INFERENCE'),
    ('bed_fpga', 'Table 3/7 BED FPGA (quantized)', 94.54,
     'classifier_brevitas_2_finn/experiments_bed_evolution/71_brevitas__230_manual_old_SmallBig__full_ds', 'INFERENCE'),
    # Candidates (provenance unknown before this script). The transfer-learning logs contain two sessions:
    # (0) 20 epochs training only the head with a frozen pretrained backbone, (1) full fine-tuning.
    # The paper values correspond to session 1 (index given as 6th field).
    ('ref_mbv2?', 'Table 2 MobileNetV2', 97.65,
     'classifier_transfer_learning/experiments/test_v07_mobilenetv2_full_ds', 'candidate', 1),
    ('ref_mbv3?', 'Table 2 MobileNetV3', 97.07,
     'classifier_transfer_learning/experiments/test_v01_mobilenetv3_full_ds', 'candidate', 1),
    ('ref_mbv3deep?', 'Table 2 MobileNetV3', 97.07,
     'classifier_transfer_learning/experiments/test_v05_mobilenetv3Deep_full_ds', 'candidate', 1),
    ('ref_shufflenet?', 'Table 2 ShuffleNetV2', 94.95,
     'classifier_transfer_learning/experiments/test_v03_shufflenet_full_ds', 'candidate', 1),
    ('ref_mobilevit?', 'Table 2 MobileViTV3', 95.87,
     'classifier_vision_transformer/experiments/test_v11_MobileViTv3_v1_full_ds', 'candidate'),
    ('mbv3_mini?', 'Table 5 MobilenetV3 Mini', 95.37,
     'classifier_my_mobilenetv3/experiments/test_v01_full_ds', 'candidate'),
]

EPOCH_RE = re.compile(r'^=== EPOCH (\d+)/(\d+) ===')
# e.g. '-----------|----------|----------|    Smoke  |0.9546   |0.9566   |0.9467   |0.9516   |'
#      '11.07      |7.07      |3.99      |    Fire   |0.9782   |0.9524   |0.9820   |0.9670   |'
ROW_RE = re.compile(r'^([^|]*)\|([^|]*)\|([^|]*)\|\s*(Smoke|Fire)\s*\|'
                    r'\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|')
SAVE_F1_RE = re.compile(r'Saving model with best Mean F1: ([\d.]+)')
SAVE_LOSS_RE = re.compile(r'Saving model with new best validation loss: ([\d.]+)')


PARAMS_RE = re.compile(r'^(Trainable|Total) parameters = (\d+)')


def split_sessions(lines):
    """Split a log into training sessions. Each session ends at '***Script finished' and includes the
    header printed before it (model summary, parameter counts). A trailing unfinished session is kept."""
    sessions, cur = [], []
    for line in lines:
        cur.append(line)
        if line.startswith('***Script finished'):
            sessions.append(cur)
            cur = []
    if any(EPOCH_RE.match(l) for l in cur):
        sessions.append(cur)
    return sessions


def parse_log(path, session=0):
    """Parse one training session of a log (0 = first). Returns (epochs, n_sessions, params)."""
    all_lines = Path(path).read_text(errors='replace').splitlines()
    sess = split_sessions(all_lines)
    lines = sess[session] if sess else []
    params = {}
    for l in lines:
        m = PARAMS_RE.match(l)
        if m:
            params[m.group(1).lower()] = int(m.group(2))
    epochs, cur, section = [], None, None
    for line in lines:
        m = EPOCH_RE.match(line)
        if m:
            cur = {'epoch': int(m.group(1)), 'n_epochs': int(m.group(2)) + 1, 'saved_best_f1': None,
                   'saved_best_loss': None}
            epochs.append(cur)
            section = None
            continue
        if cur is None:
            continue
        if line.startswith('TRAIN Stats'):
            section = 'train'
        elif line.startswith('VAL Stats'):
            section = 'val'
        elif section == 'val':
            r = ROW_RE.match(line)
            if r:
                cls = r.group(4).lower()
                if cls == 'fire':          # loss columns are printed on the Fire row
                    try:
                        cur['val_loss'], cur['val_loss_smoke'], cur['val_loss_fire'] = (float(g) for g in r.group(1, 2, 3))
                    except ValueError:
                        pass
                acc, prec, rec, f1 = map(float, r.group(5, 6, 7, 8))
                cur.update({f'{cls}_acc': acc, f'{cls}_prec': prec, f'{cls}_rec': rec, f'{cls}_f1': f1})
        m = SAVE_F1_RE.search(line)
        if m:
            cur['saved_best_f1'] = float(m.group(1))
        m = SAVE_LOSS_RE.search(line)
        if m:
            cur['saved_best_loss'] = float(m.group(1))
    complete = [e for e in epochs if 'smoke_f1' in e and 'fire_f1' in e]
    for e in complete:
        e['f1_macro'] = (e['smoke_f1'] + e['fire_f1']) / 2
    return complete, len(sess), params


def summarize(name, item, paper, rel, status, session=0):
    log = UAV_CODE / rel / 'logs' / 'logfile.log'
    if not log.exists():
        return {'run': name, 'error': f'missing log {log}'}
    ep, sessions, params = parse_log(log, session)
    if not ep:
        return {'run': name, 'error': 'no epochs parsed'}
    out_csv = paths.results_dir('f0_selection_bias', 'epochs') / f'{name.rstrip("?")}.csv'
    keys = ['epoch', 'n_epochs', 'val_loss', 'smoke_prec', 'smoke_rec', 'smoke_f1', 'fire_prec', 'fire_rec',
            'fire_f1', 'f1_macro', 'saved_best_f1', 'saved_best_loss']
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
        w.writeheader()
        w.writerows(ep)

    f1 = [e['f1_macro'] for e in ep]
    saved = [e for e in ep if e['saved_best_f1'] is not None]
    sel = saved[-1] if saved else max(ep, key=lambda e: e['f1_macro'])
    loss_ep = [e for e in ep if 'val_loss' in e]
    best_loss = min(loss_ep, key=lambda e: e['val_loss']) if loss_ep else None
    last = ep[-1]
    last10 = f1[-10:]
    s = {
        'run': name, 'paper_item': item, 'paper_f1_macro': paper, 'provenance': status, 'log': str(log),
        'training_sessions_in_log': sessions, 'session_used': session,
        'trainable_params': params.get('trainable'), 'total_params': params.get('total'),
        'epochs_parsed': len(ep), 'epochs_planned': ep[0]['n_epochs'],
        'selected_epoch': sel['epoch'], 'selected_f1_macro': 100 * sel['f1_macro'],
        'selected_saved_value': sel['saved_best_f1'],
        'last_epoch': last['epoch'], 'last_f1_macro': 100 * last['f1_macro'],
        'last10_mean': 100 * statistics.mean(last10), 'last10_std': 100 * statistics.stdev(last10),
        'last10_min': 100 * min(last10), 'last10_max': 100 * max(last10),
        'best_loss_epoch': best_loss['epoch'] if best_loss else None,
        'best_loss_f1_macro': 100 * best_loss['f1_macro'] if best_loss else None,
        'max_any_epoch_f1_macro': 100 * max(f1),
    }
    s['bias_vs_last'] = s['selected_f1_macro'] - s['last_f1_macro']
    s['bias_vs_last10_mean'] = s['selected_f1_macro'] - s['last10_mean']
    s['bias_vs_best_loss'] = s['selected_f1_macro'] - s['best_loss_f1_macro'] if best_loss else None
    s['paper_minus_selected'] = paper - s['selected_f1_macro']
    s['matches_paper_2dp'] = abs(round(s['selected_f1_macro'], 2) - paper) <= 0.011
    return s


def main():
    write_guard.install()
    summaries = [summarize(*r) for r in RUNS]
    out = paths.results_dir('f0_selection_bias')
    (out / 'f0_log_summary.json').write_text(json.dumps(summaries, indent=2) + '\n')

    hdr = ('| Run | Paper item | Paper | Selected ep. → F1 | Last ep. → F1 | Last-10 mean ± sd | '
           'Best-loss ep. → F1 | Sel − last | Sel − mean10 | Sel − best-loss | Match | Session (of n) | Params (log) |')
    rows = [hdr, '|' + '---|' * 13]
    for s in summaries:
        if 'error' in s:
            rows.append(f"| {s['run']} | {s['error']} |" + ' |' * 11)
            continue
        rows.append(
            f"| {s['run']} | {s['paper_item']} | {s['paper_f1_macro']:.2f} | "
            f"{s['selected_epoch']} → {s['selected_f1_macro']:.2f} | {s['last_epoch']} → {s['last_f1_macro']:.2f} | "
            f"{s['last10_mean']:.2f} ± {s['last10_std']:.2f} | {s['best_loss_epoch']} → {s['best_loss_f1_macro']:.2f} | "
            f"{s['bias_vs_last']:+.2f} | {s['bias_vs_last10_mean']:+.2f} | {s['bias_vs_best_loss']:+.2f} | "
            f"{'yes' if s['matches_paper_2dp'] else 'NO'} | {s['session_used']} (of {s['training_sessions_in_log']}) | "
            f"{s['total_params']} |")
    note = ('\nF1-Macro (%) on the test set, from the per-epoch "VAL Stats" of each log (4-decimal per-class F1, '
            'averaged). "Selected" = last epoch where the log reports "Saving model with best Mean F1". '
            '"Match" = selected value equals the paper value to 2 decimals (±0.01). Generated by parse_logs.py.\n')
    (out / 'f0_log_summary.md').write_text('\n'.join(rows) + '\n' + note)
    print('\n'.join(rows))


if __name__ == '__main__':
    main()
