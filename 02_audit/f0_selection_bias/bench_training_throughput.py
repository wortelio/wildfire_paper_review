"""F0 (T5) — Measure the training throughput of the historical pipeline, to estimate F3 run times.

Runs N training steps (train loader with the historical augmentation + forward/backward/Adam step on GPU)
of the MobileNetV2 Nano replica and reports images/s, s/epoch and h/run (100 or 150 epochs), together with
the GPU utilization and the CPU load of the machine during the measurement. No checkpoint is written.

The augmentation is the one of the replica's dataloaders.py (= ~/uav HEAD). The paper's Nano FP32 run used an
older, slightly lighter augmentation (Nov 2024; blur 3x3 instead of 17x17), so this is an upper bound for that run.

Usage (from this folder):
    /opt/conda/envs/pytorch_23/bin/python bench_training_throughput.py --model fp32 [--steps 300] [--tag single]
Run two instances at the same time with different --tag to measure concurrent throughput.
"""
import argparse
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from common import env_capture, paths, replicas  # noqa: E402

TRAIN_IMAGES = 117567     # Table 1 training pool (DFire train + FASDD UAV/CV train + val)


def gpu_util(samples, stop):
    while not stop.is_set():
        out = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,memory.used', '--format=csv,noheader,nounits'],
                             capture_output=True, text=True).stdout.strip()
        try:
            u, m = out.split(',')
            samples.append((float(u), float(m)))
        except ValueError:
            pass
        time.sleep(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', choices=('fp32', 'brevitas'), default='fp32')
    ap.add_argument('--steps', type=int, default=300)
    ap.add_argument('--warmup', type=int, default=20)
    ap.add_argument('--tag', default='single')
    args = ap.parse_args()

    config = replicas.use('mobilenet_paper', model=args.model)
    import torch
    from modules.dataloaders import get_train_loader
    from modules.loss import BCE_LOSS
    if args.model == 'fp32':
        from modules.model_mobilenetv2_mini_Resnet import MobileNetV2_MINI_RESNET
    else:
        from modules.brevitas.model_mobilenetv2_mini_Resnet_Brevitas import MobileNetV2_MINI_RESNET

    loader = get_train_loader()
    model = MobileNetV2_MINI_RESNET().to(config.DEVICE).train()
    opt = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE, weight_decay=config.WEIGHT_DECAY)
    loss_fn = BCE_LOSS(device=config.DEVICE, smoke_precision_weight=config.SMOKE_PRECISION_WEIGHT)

    samples, stop = [], threading.Event()
    th = threading.Thread(target=gpu_util, args=(samples, stop), daemon=True)
    load0 = os.getloadavg()
    it = iter(loader)
    n_img, t0 = 0, None
    for step in range(args.warmup + args.steps):
        if step == args.warmup:
            torch.cuda.synchronize(); t0 = time.time(); th.start()
        x, y = next(it)
        x, y = x.to(config.DEVICE, non_blocking=True), y.to(config.DEVICE, non_blocking=True)
        opt.zero_grad()
        loss = loss_fn(ground_truth=y, predictions=model(x))
        loss.backward(); opt.step()
        if step >= args.warmup:
            n_img += x.shape[0]
    torch.cuda.synchronize()
    dt = time.time() - t0
    stop.set(); th.join(timeout=5)
    ips = n_img / dt
    s_epoch = TRAIN_IMAGES / ips
    res = {'model': args.model, 'tag': args.tag, 'steps': args.steps, 'batch_size': config.BATCH_SIZE,
           'num_workers': config.NUM_WORKERS, 'images': n_img, 'seconds': round(dt, 1),
           'images_per_s': round(ips, 1), 'seconds_per_epoch': round(s_epoch),
           'hours_100_epochs': round(100 * s_epoch / 3600, 2), 'hours_150_epochs': round(150 * s_epoch / 3600, 2),
           'gpu_util_mean_pct': round(sum(u for u, _ in samples) / len(samples), 1) if samples else None,
           'gpu_mem_mb_max': max((m for _, m in samples), default=None),
           'loadavg_before': load0, 'loadavg_after': os.getloadavg(), 'cpus': os.cpu_count(),
           'env': env_capture.capture()}
    out = paths.results_dir('f0_selection_bias', 'throughput') / f'{args.model}__{args.tag}.json'
    out.write_text(json.dumps(res, indent=2, default=str) + '\n')
    print(json.dumps({k: v for k, v in res.items() if k != 'env'}, indent=1))


if __name__ == '__main__':
    main()
