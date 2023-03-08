import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from pathlib import Path
import time
import subprocess
import sys
import pandas as pd
from functions import reorder_nifti_data

# Options
seed = 21  # 9, 17, 21, 28, 61, 65, 97 for increasing motion and age
scalar = 'fa'
slice_loc = [40, 40, 40]
SAVE_NIFTI = False
cropsz = [35, 35, 35]

"""
# Prepare a dataframe (session, age, motion) that we can sample from
fn_csv = '/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv'
df = pd.read_csv(fn_csv)
print(df)
list_df_session = []
list_df_age = []
list_df_motion_1 = []
list_df_motion_2 = []

for session in df['Session'].unique():
    # skip scanners that are not 10
    scanner = session.split('_')[-1]
    if scanner != '10':
        continue
    # skip session with only 1 scan
    if len(df.loc[df['Session']==session].index) !=2:
        continue
    # skip session with NAN age or motion
    if df.loc[df['Session']==session].isnull().values.any():
        continue
    age = df.loc[(df['Session']==session)&(df['DTI_ID']==1), 'Age'].item()
    motion_1 = df.loc[(df['Session']==session)&(df['DTI_ID']==1), 'Motion'].item()
    motion_2 = df.loc[(df['Session']==session)&(df['DTI_ID']==2), 'Motion'].item()
    
    list_df_session.append(session)
    list_df_age.append(age)
    list_df_motion_1.append(motion_1)
    list_df_motion_2.append(motion_2)

d = {'Session': list_df_session, 
     'Age':list_df_age, 
     'Motion_DTI1': list_df_motion_1, 
     'Motion_DTI2': list_df_motion_2}
df = pd.DataFrame(data=d)
df.to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/noisy_scalar_maps/session_age_motion_info.csv', index=False)
"""

# Sample 3 sessions, with increasing age and motion
df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/noisy_scalar_maps/session_age_motion_info.csv')

row_1 = df.loc[df['Age']<=40].sample(random_state=seed)
row_2 = df.loc[(df['Age'] > 55) & (df['Age'] <70)].sample(random_state=seed)
row_3 = df.loc[df['Age'] > 85].sample(random_state=seed)
list_sessions = [row_1['Session'].item(),
                 row_2['Session'].item(),
                 row_3['Session'].item()]

# Path of the BLSA dataset
path_blsa_dataset = Path('/nfs2/harmonization/BLSA/')

# Make folder to store scalar maps used in this script
path_cache_fd = Path('/home-local/Data/BLSA_Scalar_Maps')
# local_time = time.localtime()
# str_time = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)
path_cache_fd = path_cache_fd / "seed_{0}".format(seed)

subprocess.run(['mkdir',
                '-p',
                path_cache_fd
                ])


fig, axes = plt.subplots(3,3,figsize=(8,8))

for id_col, session in enumerate(list_sessions):
    if id_col == 0:
        age = row_1['Age'].item()
        motion_1 = row_1['Motion_DTI1'].item()
        motion_2 = row_1['Motion_DTI2'].item()
    elif id_col == 1:
        age = row_2['Age'].item()
        motion_1 = row_2['Motion_DTI1'].item()
        motion_2 = row_2['Motion_DTI2'].item()
    elif id_col == 2:
        age = row_3['Age'].item()
        motion_1 = row_3['Motion_DTI1'].item()
        motion_2 = row_3['Motion_DTI2'].item()
        
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
                path_img_1_save = path_cache_fd / "{0}_DTI{1}_dwmri_tensor_{2}.nii.gz".format(session, dti_id, scalar)
                if SAVE_NIFTI:
                    subprocess.run(['cp', path_img_1, path_img_1_save])
                
            elif dti_id == 2:
                path_img_2 = assessor / 'SCALARS' / 'dwmri_tensor_{0}.nii.gz'.format(scalar)
                path_img_2_save = path_cache_fd / "{0}_DTI{1}_dwmri_tensor_{2}.nii.gz".format(session, dti_id, scalar)
                if SAVE_NIFTI:
                    subprocess.run(['cp', path_img_2, path_img_2_save])
    
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
    im_dti1 = axes[0,id_col].imshow(data_1_re[0+cropsz[0]:-1-cropsz[0],0+cropsz[0]:-1-cropsz[0],slice_loc[id_col]], cmap='gray', interpolation='nearest', vmin=0, vmax=2)
    # axes[0,id_col].set_title("{0}\nAge: {1} years".format(session,age), loc='center', fontdict={'fontsize': 10})
    axes[0,id_col].set_title("Age: {0} years".format(age), loc='left', fontdict={'fontsize': 10})
    axes[0,id_col].axis('off')
    axes[0,id_col].text(x=0, y=245, s= 'Motion: {0:.4} mm'.format(motion_1),color='white', fontdict={'fontsize': 10})
    axes[0,id_col].text(-20, 120, r'$DTI1$', va='center', rotation='vertical', fontsize=10)
    
    # DTI2
    im_dti2 = axes[1,id_col].imshow(data_2_re[0+cropsz[1]:-1-cropsz[1],0+cropsz[1]:-1-cropsz[1],slice_loc[id_col]], cmap='gray', interpolation='nearest', vmin=0, vmax=2)
    axes[1,id_col].axis('off')
    axes[1,id_col].text(x=0, y=245, s= 'Motion: {0:.4} mm'.format(motion_2),color='white', fontdict={'fontsize': 10})
    axes[1,id_col].text(-20, 120, r'$DTI2$', va='center', rotation='vertical', fontsize=10)

    # DTI1-DTI2
    # axes[2,id_col].imshow(data_diff[0+cropsz:-1-cropsz,0+cropsz:-1-cropsz,slice_loc[id_col]], cmap='RdBu', vmin=-0.5, vmax=0.5)
    img_diff = axes[2,id_col].imshow(data_diff_abs[0+cropsz[2]:-1-cropsz[2],0+cropsz[2]:-1-cropsz[2],slice_loc[id_col]], cmap='hot', vmin=0, vmax=0.5, interpolation='nearest')
    axes[2,id_col].axis('off')
    axes[2,id_col].text(-20, 120, r'$|DTI1 - DTI2|$', va='center', rotation='vertical', fontsize=10)

# colorbars
cax = fig.add_axes([0.905, 0.64, 0.01, 0.22])
fig.colorbar(im_dti1, cax=cax)
cax = fig.add_axes([0.905, 0.38, 0.01, 0.22])
fig.colorbar(im_dti2, cax=cax)
cax = fig.add_axes([0.905, 0.12, 0.01, 0.22])
fig.colorbar(img_diff, cax=cax)

fig.subplots_adjust(wspace=0.01, hspace=0.01)

fig.savefig('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/noisy_scalar_maps/save/seed_{0}.png'.format(seed), dpi = 300, bbox_inches="tight")