import os
import torch

# ______________________________________________________________________ #
#                                Logs                                    #
# ______________________________________________________________________ #
RUN_FOLDER = 'experiments_comparison/figlib_dataset/' + 'test_v21_TransferLearning__MICRO__Binary__full_ds/'
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
FIGLIB = 1

assert FOG+SICILIA+FIGLIB == 1, f'FOG {FOG} + SICILIA {SICILIA} + FIGLIB {FIGLIB} should be 1'

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
dfire_dir = '../../datasets/ds2fire/dfire_yolo/'
DFIRE_TRAIN_IMG_DIR = dfire_dir + 'train/images/'
DFIRE_TRAIN_LABEL_DIR = dfire_dir + 'train/labels/'
DFIRE_TEST_IMG_DIR = dfire_dir + 'test/images/'
DFIRE_TEST_LABEL_DIR = dfire_dir + 'test/labels/'

FASDD_UAV_IMGS_DIR = '../../datasets/fasdd/fasdd_uav/images/'
FASDD_UAV_TRAIN_LABELS_FILE = '../../datasets/fasdd/fasdd_uav/annotations/YOLO_UAV/train.txt'
FASDD_UAV_VAL_LABELS_FILE = '../../datasets/fasdd/fasdd_uav/annotations/YOLO_UAV/val.txt'
FASDD_UAV_TEST_LABELS_FILE = '../../datasets/fasdd/fasdd_uav/annotations/YOLO_UAV/test.txt'

FASDD_CV_IMGS_DIR = '../../datasets/fasdd/fasdd_cv/images/'
FASDD_CV_TRAIN_LABELS_FILE = '../../datasets/fasdd/fasdd_cv/annotations/YOLO_CV/train.txt'
FASDD_CV_VAL_LABELS_FILE = '../../datasets/fasdd/fasdd_cv/annotations/YOLO_CV/val.txt'
FASDD_CV_TEST_LABELS_FILE = '../../datasets/fasdd/fasdd_cv/annotations/YOLO_CV/test.txt'

CLOUDS_IMG_DIR = '../../datasets/clouds/images/'

DS_LEN = None

### DFire Mini ###
dfire_mini_dir = '../../datasets/dfire_mini/'
DFIRE_MINI_TRAIN_IMG_DIR = dfire_mini_dir + 'train/images/'
DFIRE_MINI_TRAIN_LABEL_DIR = dfire_mini_dir + 'train/labels/'
DFIRE_MINI_TEST_IMG_DIR = dfire_mini_dir + 'test/images/'
DFIRE_MINI_TEST_LABEL_DIR = dfire_mini_dir + 'test/labels/'

### FLAME ###
flame_dir = '../../datasets/flame'
FLAME_TEST_IMG_DIR = flame_dir + '/Test'
### FOG ###
fog_dir = '../../datasets/fog_dataset'
FOG_TRAIN_IMG_DIR = fog_dir + '/train'
FOG_TEST_IMG_DIR = fog_dir + '/test'
### SICILIA ###
sicilia_dir = '../../datasets/sicilia_bosque'
SICILIA_TRAIN_IMG_DIR = sicilia_dir + '/train'
SICILIA_TEST_IMG_DIR = sicilia_dir + '/test'
### FIGLIB ###
figlib_dir = '../../datasets/figlib/'
FIGLIB_TRAIN_IMG_DIR = figlib_dir + 'train/'
FIGLIB_VAL_IMG_DIR = figlib_dir + 'val/'
FIGLIB_TEST_IMG_DIR = figlib_dir + 'test/'

# ______________________________________________________________________ #
#                   Hyperparameters and More                             #
# ______________________________________________________________________ #
BREVITAS_MODEL = False
MODEL = "Mobilenetv2_Mini_Resnet"
WIDTH_MULT = 1.0

LEARNING_RATE = 1e-3
# LEARNING_RATE = 5e-4
# Optimizer
WEIGHT_DECAY = 0.0
# WEIGHT_DECAY = 1e-5
# WEIGHT_DECAY = 1e-3
FACTOR = 0.8
PATIENCE = 2
THRES = 0.001
MIN_LR = 1e-6
# MIN_LR = 1e-7

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 64 
NUM_WORKERS = 8
PIN_MEMORY = True

EPOCHS = 5

LOAD_MODEL = False
LOAD_MODEL_DIR = './experiments_brevitas/test_v05_mini_resnet_70k_full_ds/weights/'
LOAD_MODEL_FILE = LOAD_MODEL_DIR + "MY_MBLNET_V2_RESNET_classifier__best_mean_F1.pt"


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
