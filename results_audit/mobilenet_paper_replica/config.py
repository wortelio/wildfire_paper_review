import os
import torch

# REPLICA: copy of code/train/mobilenet/config.py (= ~/uav HEAD, sha256 30d158a2...) adapted to
# reproduce the MobileNetV2 Nano paper runs (Tables 5, 7 and 8). Values taken from each run's
# logs/logfile.log header. Every modified line is marked "# REPLICA:". See README.md for the full diff.
# The model is selected with the environment variable REPLICA_MODEL (default 'fp32'):
#   fp32     -> experiments/test_v04_mini_resnet_70k_full_ds          (FP32, epoch 86;  conda env pytorch_23)
#   brevitas -> experiments_brevitas/test_v05_mini_resnet_70k_full_ds (QAT,  epoch 91;  conda env pytorch_brevitas)
UAV_DATASETS = os.path.expanduser('~/uav/datasets/')   # REPLICA: absolute, read-only dataset root
REPLICA_MODEL = os.environ.get('REPLICA_MODEL', 'fp32')  # REPLICA
assert REPLICA_MODEL in ('fp32', 'brevitas'), REPLICA_MODEL  # REPLICA
PAPER_RUNS = {  # REPLICA: paper runs and local byte-identical copies of their best-F1 checkpoints (see README)
    'fp32': {
        'run_dir': os.path.expanduser('~/uav/code/classifier_my_mobilenetv2/experiments/test_v04_mini_resnet_70k_full_ds/'),
        'model_name': 'MY_MBLNET_V2',
        'weights': 'MY_MBLNET_V2_classifier__best_mean_F1.pt',
        'sha256': 'c8385799d1771c5e9f055d9a9c19f66f7bb3606b2d2cbf655723b1733ad607f6',
    },
    'brevitas': {
        'run_dir': os.path.expanduser('~/uav/code/classifier_my_mobilenetv2/experiments_brevitas/test_v05_mini_resnet_70k_full_ds/'),
        'model_name': 'MY_MBLNET_V2_RESNET',
        'weights': 'MY_MBLNET_V2_RESNET_classifier__best_mean_F1.pt',
        'sha256': '5418b2467e7e22f3eb9fdf31a4eca9b7a84139c0ce881b122a06b28d4716b65d',
    },
}
PAPER_RUN_DIR = PAPER_RUNS[REPLICA_MODEL]['run_dir']  # REPLICA

# ______________________________________________________________________ #
#                                Logs                                    #
# ______________________________________________________________________ #
RUN_FOLDER = 'outputs/'  # REPLICA: local, git-ignored (was experiments_comparison/figlib_dataset/test_v21_...)
if not os.path.isdir(RUN_FOLDER):
    os.mkdir(RUN_FOLDER)
LOGS_FOLDER = RUN_FOLDER + 'logs/'
if not os.path.isdir(LOGS_FOLDER):
    os.mkdir(LOGS_FOLDER)
PLOTS_FOLDER = RUN_FOLDER + 'plots/'
if not os.path.isdir(PLOTS_FOLDER):
    os.mkdir(PLOTS_FOLDER)
WEIGHTS_FOLDER = RUN_FOLDER + 'weights/'
if not os.path.isdir(WEIGHTS_FOLDER):
    os.mkdir(WEIGHTS_FOLDER)
ONNX_FOLDER = RUN_FOLDER + 'onnx/'
if not os.path.isdir(ONNX_FOLDER):
    os.mkdir(ONNX_FOLDER)
# ______________________________________________________________________ #
#                        Classes and Dimensions                          #
# ______________________________________________________________________ #
FOG = 0
FOUR_CLASSES = 0
SICILIA = 0
FIGLIB = 0  # REPLICA: paper uses DFire + FASDD (the final `else` branch below); was 1

# REPLICA: assertion added after the paper runs (FIgLib/FOG/SICILIA experiments); it forbids DFire+FASDD.
# assert FOG+SICILIA+FIGLIB == 1, f'FOG {FOG} + SICILIA {SICILIA} + FIGLIB {FIGLIB} should be 1'

if FOG:
    if FOUR_CLASSES:
        CLASSES = ["non_smokefog", "non_smoke", "smokefog", "smoke"]
        NUM_CLASSES = len(CLASSES)
    else:
        # Binary Classification
        CLASSES = ["non_smoke", "smoke"]
    # Do not disturb metrics
    NUM_CLASSES = 2
elif SICILIA:
    if FOUR_CLASSES:
        CLASSES = ["fire", "no_fire", "smoke"]
        NUM_CLASSES = len(CLASSES)
    else:
        # Binary Classification
        CLASSES = ["non_smoke", "smoke"]
    # Do not disturb metrics
    NUM_CLASSES = 2
elif FIGLIB:
    CLASSES = ["non_smoke", "smoke"]
    # Do not disturb metrics
    NUM_CLASSES = 2
else:
    CLASSES = ["smoke", "fire"]
    NUM_CLASSES = len(CLASSES)

#___   Padding Model  ___#
IMG_DIM = {'W':224, 'H':224} # (W, H)
# IMG_DIM = {'W':160, 'H':160} # (W, H)
# IMG_DIM = {'W':112, 'H':112} # (W, H)

#___ No Padding Model ___#
# IMG_DIM = {'W':230, 'H':230} # (W, H)

IMG_H = IMG_DIM['H']
IMG_W = IMG_DIM['W']
NUM_CHANNELS = 3

# ______________________________________________________________________ #
#                        Folders and Datasets                            #
# ______________________________________________________________________ #
dfire_dir = UAV_DATASETS + 'ds2fire/dfire_yolo/'  # REPLICA: was '../../datasets/ds2fire/dfire_yolo/'
DFIRE_TRAIN_IMG_DIR = dfire_dir + 'train/images/'
DFIRE_TRAIN_LABEL_DIR = dfire_dir + 'train/labels/'
DFIRE_TEST_IMG_DIR = dfire_dir + 'test/images/'
DFIRE_TEST_LABEL_DIR = dfire_dir + 'test/labels/'

FASDD_UAV_IMGS_DIR = UAV_DATASETS + 'fasdd/fasdd_uav/images/'  # REPLICA: was '../../datasets/fasdd/fasdd_uav/images/'
FASDD_UAV_TRAIN_LABELS_FILE = UAV_DATASETS + 'fasdd/fasdd_uav/annotations/YOLO_UAV/train.txt'  # REPLICA: was '../../datasets/fasdd/fasdd_uav/annotations/YOLO_UAV/train.txt'
FASDD_UAV_VAL_LABELS_FILE = UAV_DATASETS + 'fasdd/fasdd_uav/annotations/YOLO_UAV/val.txt'  # REPLICA: was '../../datasets/fasdd/fasdd_uav/annotations/YOLO_UAV/val.txt'
FASDD_UAV_TEST_LABELS_FILE = UAV_DATASETS + 'fasdd/fasdd_uav/annotations/YOLO_UAV/test.txt'  # REPLICA: was '../../datasets/fasdd/fasdd_uav/annotations/YOLO_UAV/test.txt'

FASDD_CV_IMGS_DIR = UAV_DATASETS + 'fasdd/fasdd_cv/images/'  # REPLICA: was '../../datasets/fasdd/fasdd_cv/images/'
FASDD_CV_TRAIN_LABELS_FILE = UAV_DATASETS + 'fasdd/fasdd_cv/annotations/YOLO_CV/train.txt'  # REPLICA: was '../../datasets/fasdd/fasdd_cv/annotations/YOLO_CV/train.txt'
FASDD_CV_VAL_LABELS_FILE = UAV_DATASETS + 'fasdd/fasdd_cv/annotations/YOLO_CV/val.txt'  # REPLICA: was '../../datasets/fasdd/fasdd_cv/annotations/YOLO_CV/val.txt'
FASDD_CV_TEST_LABELS_FILE = UAV_DATASETS + 'fasdd/fasdd_cv/annotations/YOLO_CV/test.txt'  # REPLICA: was '../../datasets/fasdd/fasdd_cv/annotations/YOLO_CV/test.txt'

CLOUDS_IMG_DIR = UAV_DATASETS + 'clouds/images/'  # REPLICA: was '../../datasets/clouds/images/'

DS_LEN = None

### DFire Mini ###
dfire_mini_dir = UAV_DATASETS + 'dfire_mini/'  # REPLICA: was '../../datasets/dfire_mini/'
DFIRE_MINI_TRAIN_IMG_DIR = dfire_mini_dir + 'train/images/'
DFIRE_MINI_TRAIN_LABEL_DIR = dfire_mini_dir + 'train/labels/'
DFIRE_MINI_TEST_IMG_DIR = dfire_mini_dir + 'test/images/'
DFIRE_MINI_TEST_LABEL_DIR = dfire_mini_dir + 'test/labels/'

### FLAME ###
flame_dir = UAV_DATASETS + 'flame'  # REPLICA: was '../../datasets/flame'
FLAME_TEST_IMG_DIR = flame_dir + '/Test'
### FOG ###
fog_dir = UAV_DATASETS + 'fog_dataset'  # REPLICA: was '../../datasets/fog_dataset'
FOG_TRAIN_IMG_DIR = fog_dir + '/train'
FOG_TEST_IMG_DIR = fog_dir + '/test'
### SICILIA ###
sicilia_dir = UAV_DATASETS + 'sicilia_bosque'  # REPLICA: was '../../datasets/sicilia_bosque'
SICILIA_TRAIN_IMG_DIR = sicilia_dir + '/train'
SICILIA_TEST_IMG_DIR = sicilia_dir + '/test'
### FIGLIB ###
figlib_dir = UAV_DATASETS + 'figlib/'  # REPLICA: was '../../datasets/figlib/'
FIGLIB_TRAIN_IMG_DIR = figlib_dir + 'train/'
FIGLIB_VAL_IMG_DIR = figlib_dir + 'val/'
FIGLIB_TEST_IMG_DIR = figlib_dir + 'test/'

# ______________________________________________________________________ #
#                   Hyperparameters and More                             #
# ______________________________________________________________________ #
BREVITAS_MODEL = (REPLICA_MODEL == 'brevitas')  # REPLICA: only selects the Brevitas ONNX-export imports in utils.py; was False
MODEL = PAPER_RUNS[REPLICA_MODEL]['model_name']  # REPLICA: name used by the run's weight files; was "Mobilenetv2_Mini_Resnet"
WIDTH_MULT = 1.0

LEARNING_RATE = 1e-3
# LEARNING_RATE = 5e-4
# Optimizer
# WEIGHT_DECAY = 0.0
# WEIGHT_DECAY = 1e-5
WEIGHT_DECAY = 1e-3  # REPLICA: log "Weight Decay: 0.001"; was 0.0
FACTOR = 0.8
PATIENCE = 2
THRES = 0.001
MIN_LR = 1e-6
# MIN_LR = 1e-7

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 64 
NUM_WORKERS = 8
PIN_MEMORY = True

EPOCHS = 100  # REPLICA: log "Epochs: 100"; was 5

LOAD_MODEL = False
LOAD_MODEL_DIR = 'weights/'  # REPLICA: local byte-identical copy of PAPER_RUN_DIR + 'weights/' (see README); was ./experiments_brevitas/test_v05_.../weights/
LOAD_MODEL_FILE = LOAD_MODEL_DIR + PAPER_RUNS[REPLICA_MODEL]['weights']  # REPLICA: best-F1 checkpoint (fp32: epoch 86, brevitas: epoch 91; VERIFIED identical tensors to the epoch files)
ORIGINAL_MODEL_FILE = PAPER_RUN_DIR + 'weights/' + PAPER_RUNS[REPLICA_MODEL]['weights']  # REPLICA: source of the local copy
MODEL_FILE_SHA256 = PAPER_RUNS[REPLICA_MODEL]['sha256']  # REPLICA: sha256 of both files


if FOG:
    if FOUR_CLASSES:
        LOSS_FN = "CE"
    else:
        LOSS_FN = "FOG_BCE"
elif SICILIA:
    if FOUR_CLASSES:
        LOSS_FN = "CE"
    else:
        LOSS_FN = "FOG_BCE"
elif FIGLIB:
        LOSS_FN = "FOG_BCE"
else:
    LOSS_FN = "BCE"
    SMOKE_PRECISION_WEIGHT = 0.8

# ______________________________________________________________________ #
#                             Quantization                               #
# ______________________________________________________________________ #
FIXED_POINT = True

# WEIGHTS_BIT_WIDTH = 4
# BIG_LAYERS_WEIGHTS_BIT_WIDTH = 2
# ACTIVATIONS_BIT_WIDTH = 8
# BIAS_BIT_WIDTH = 4

##### FINN
WEIGHTS_BIT_WIDTH = 4
BIG_LAYERS_WEIGHTS_BIT_WIDTH = 4
ACTIVATIONS_BIT_WIDTH = 4
BIAS_BIT_WIDTH = 4
