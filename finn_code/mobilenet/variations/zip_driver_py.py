import shutil
import os

deploy_file = ('./experiments'
               + '/A_3000_FPS_mvau_wwidth_max/112'
               + '/04_full_build_json_mvau_rtl_mvau_wwidth_max_16_manual_folding'
               + '/output_full_build'
               + '/deploy')

print(os.listdir(deploy_file))

shutil.make_archive('./3000_FPS_112_deploy', 'zip', deploy_file)