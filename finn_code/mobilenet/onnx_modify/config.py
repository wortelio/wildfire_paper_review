import os
# ______________________________________________________________________ #
#                                Logs                                    #
# ______________________________________________________________________ #
EXPERIMENTS_FOLDER = 'experiments/'
EXPERIMENTS_FOLDER += '900_FPS_mul8_scale_fixed_mvau_wwidth_max/'
if not os.path.isdir(EXPERIMENTS_FOLDER):
    os.mkdir(EXPERIMENTS_FOLDER)

# RUN_FOLDER = '04_estimates_mvau_rtl_mvau_wwidth_max_36_by_hand_folding/'
# RUN_FOLDER = '03_full_build_mvau_rtl_hls/'
RUN_FOLDER = '05_full_build_json_mvau_rtl_mvau_wwidth_max_36_by_hand_folding/'

RUN_FOLDER = EXPERIMENTS_FOLDER + RUN_FOLDER
if not os.path.isdir(RUN_FOLDER):
    os.mkdir(RUN_FOLDER)
    print(f'Run folder created in: {RUN_FOLDER}')

# ______________________________________________________________________ #
#                        Classes and Dimensions                          #
# ______________________________________________________________________ #
NUM_CLASSES = 2

IMG_H = 224
IMG_W = 224
# IMG_H = 160
# IMG_W = 160
NUM_CHANNELS = 3

