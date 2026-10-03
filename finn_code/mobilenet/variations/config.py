import os
# ______________________________________________________________________ #
#                                Logs                                    #
# ______________________________________________________________________ #
EXPERIMENTS_FOLDER = 'experiments/'
EXPERIMENTS_FOLDER += 'A_1500_FPS_mvau_wwidth_max/'
EXPERIMENTS_FOLDER += '160/'
if not os.path.isdir(EXPERIMENTS_FOLDER):
    os.mkdir(EXPERIMENTS_FOLDER)

RUN_FOLDER = '05_estimates_mvau_rtl_mvau_wwidth_max_16_by_hand_folding/'
# RUN_FOLDER = '14_full_build_mvau_rtl_hls/'
# RUN_FOLDER = '02_full_build_json_mvau_rtl_mvau_wwidth_max_16_manual_folding_1000ns/'

RUN_FOLDER = EXPERIMENTS_FOLDER + RUN_FOLDER
if not os.path.isdir(RUN_FOLDER):
    os.mkdir(RUN_FOLDER)
    print(f'Run folder created in: {RUN_FOLDER}')

# ______________________________________________________________________ #
#                        Classes and Dimensions                          #
# ______________________________________________________________________ #
NUM_CLASSES = 2

# IMG_H = 224
# IMG_W = 224
# IMG_H = 160
# IMG_W = 160
IMG_H = 112
IMG_W = 112
NUM_CHANNELS = 3

