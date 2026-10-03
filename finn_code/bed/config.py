import os
# ______________________________________________________________________ #
#                                Logs                                    #
# ______________________________________________________________________ #
EXPERIMENTS_FOLDER = 'experiments_evolution_ori_to_fpga/'
# EXPERIMENTS_FOLDER += 'SmallBig/'
EXPERIMENTS_FOLDER += '03_fpga_4bits_mul8/'
# EXPERIMENTS_FOLDER += '750_FPS/'

if not os.path.isdir(EXPERIMENTS_FOLDER):
    os.mkdir(EXPERIMENTS_FOLDER)

RUN_FOLDER = '01_estimates_mvau_rtl_hls_mvau_wwidth_max_108/'
# RUN_FOLDER = '07_full_build_json_mvau_rtl_hls_mvau_wwidth_max_108_by_hand_folding/'

RUN_FOLDER = EXPERIMENTS_FOLDER + RUN_FOLDER
if not os.path.isdir(RUN_FOLDER):
    os.mkdir(RUN_FOLDER)
    print(f'Run folder created in: {RUN_FOLDER}')

# ______________________________________________________________________ #
#                        Classes and Dimensions                          #
# ______________________________________________________________________ #
NUM_CLASSES = 2

# IMG_H = 230
# IMG_W = 230
IMG_H = 224
IMG_W = 224
# IMG_H = 160
# IMG_W = 160
NUM_CHANNELS = 3

