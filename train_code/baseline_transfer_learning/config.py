import os
import torch
# ______________________________________________________________________ #
#                                Logs                                    #
# ______________________________________________________________________ #
RUN_FOLDER = 'experiments/' + 'test_v07_mobilenetv2_full_ds/'
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

# ______________________________________________________________________ #
#                        Classes and Dimensions                          #
# ______________________________________________________________________ #
CLASSES = ["smoke", "fire"]
NUM_CLASSES = len(CLASSES)

#___   Padding Model  ___#
IMG_DIM = {'W':224, 'H':224} # (W, H)

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

DS_LEN = None

# ______________________________________________________________________ #
#                   Hyperparameters and More                             #
# ______________________________________________________________________ #
MODEL = "MOBILENETV2"
# MODEL = "SHUFFLENET"

#### FREEZE
LEARNING_RATE_FREEZE = 1e-3
# Optimizer
WEIGHT_DECAY_FREEZE = 1e-3
### FINE TUNING
LEARNING_RATE_FINETUNING = 1e-5
# Optimizer
WEIGHT_DECAY_FINETUNING = 1e-4
FACTOR = 0.8
PATIENCE = 2
THRES = 0.001
MIN_LR = 1e-6

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 64 
NUM_WORKERS = 8
PIN_MEMORY = True

EPOCHS_FREZZE = 20
EPOCHS_FINETUNING = 80

LOSS_FN = "BCE"
SMOKE_PRECISION_WEIGHT = 0.8
