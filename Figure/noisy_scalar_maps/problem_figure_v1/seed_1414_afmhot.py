# This script takes screenshots of the FA scalar maps of DTI1 and DTI2 and their difference.
# The selection of samples are defined in ../compare_fa_maps_aging_subjects_loop_seeds.py

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from pathlib import Path
import subprocess
import pandas as pd
from functions import reorder_nifti_data

# Options
seed = 1414
scalar = 'fa'
cropsz = [35, 35, 35]
df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/noisy_scalar_maps/session_age_motion_info.csv')
path_blsa_dataset = Path('/nfs2/harmonization/BLSA/')

# Sample 3 sessions, with increasing age and motion
row_1 = df.loc[df['Age']<=40].sample(random_state=seed)
row_2 = df.loc[(df['Age'] > 55) & (df['Age'] <70)].sample(random_state=seed)
row_3 = df.loc[df['Age'] > 85].sample(random_state=seed)

list_rows = [row_1, row_2, row_3]

for row in list_rows:
    session = row['Session'].item()
    age = row['Age'].item()
    motion_1 = row['Motion_DTI1'].item()
    motion_2 = row['Motion_DTI2'].item()

    ASSESSORS_fd = path_blsa_dataset / session / 'ASSESSORS' # path of the /ASSESSORS folder
    for assessor in ASSESSORS_fd.iterdir():
        if '-dtiQA_synb0_v7-x-' in assessor.name:
            # Check if it's DTI1 or DTI2
            OUTLOG_fd = assessor / 'OUTLOG'
            OUTLOG_txt = OUTLOG_fd / (assessor.name + '.txt')
            try:
                with open(OUTLOG_txt, 'r') as f:
                    content = f.read()
                    if ('DTI1' in content) and ('DTI2' not in content):
                        dti_id = 1
                    elif ('DTI2' in content) and ('DTI1' not in content):
                        dti_id = 2
                    else:
                        print("Can not determine if it's DTI1 or DTI2: ", assessor)
                        break
            except:
                print("Can not determine if it's DTI1 or DTI2: ", assessor)
                break
            
            # path to the scalar maps
            if dti_id == 1:
                path_img_1 = assessor / 'SCALARS' / 'dwmri_tensor_{0}.nii.gz'.format(scalar)
            elif dti_id == 2:
                path_img_2 = assessor / 'SCALARS' / 'dwmri_tensor_{0}.nii.gz'.format(scalar)
                
    # Load images
    img_1 = nib.load(path_img_1)
    data_1 = img_1.get_fdata() 
    affine_code_1 = nib.aff2axcodes(img_1.affine)
    data_1_re = reorder_nifti_data(data_1, affine_code_1)
    
    img_2 = nib.load(path_img_2)
    data_2 = img_2.get_fdata() 
    affine_code_2 = nib.aff2axcodes(img_2.affine)
    data_2_re = reorder_nifti_data(data_2, affine_code_2)
    
    data_diff = data_1_re - data_2_re
    data_diff_abs = np.abs(data_diff)
    
    # DTI1
    fig, ax = plt.subplots(1,1,figsize=(5,4))
    im_dti1 = ax.imshow(data_1_re[0+cropsz[0]:-1-cropsz[0],0+cropsz[0]:-1-cropsz[0], 40], cmap='gray', interpolation='nearest', vmin=0, vmax=1)
    ax.axis('off')
    plt.colorbar(im_dti1, ax=ax, ticks=[0,0.5,1,1.5])
    fig.savefig('./screenshots/{0}_age_{1}years_DTI1_motion_{2:.4}mm_fa.png'.format(session, age, motion_1), dpi = 300, bbox_inches="tight")
    
    # DTI2
    fig, ax = plt.subplots(1,1,figsize=(5,4))
    im_dti2 = ax.imshow(data_2_re[0+cropsz[1]:-1-cropsz[1],0+cropsz[1]:-1-cropsz[1], 40], cmap='gray', interpolation='nearest', vmin=0, vmax=1)
    ax.axis('off')
    plt.colorbar(im_dti2, ax=ax, ticks=[0,0.5,1,1.5])
    fig.savefig('./screenshots/{0}_age_{1}years_DTI2_motion_{2:.4}mm_fa.png'.format(session, age, motion_2), dpi = 300, bbox_inches="tight")

    # DTI1-DTI2
    fig, ax = plt.subplots(1,1,figsize=(5,4))
    img_diff = ax.imshow(data_diff_abs[0+cropsz[2]:-1-cropsz[2],0+cropsz[2]:-1-cropsz[2], 40], cmap='afmhot', vmin=0, vmax=0.5, interpolation='nearest')
    ax.axis('off')
    plt.colorbar(img_diff, ax=ax, ticks=[0,0.25,0.5])
    fig.savefig('./screenshots/{0}_age_{1}years_diff_fa.png'.format(session, age), dpi = 300, bbox_inches="tight")
