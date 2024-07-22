import subprocess
import numpy as np
import pandas as pd
import nibabel as nib
from tqdm import tqdm
from pathlib import Path
from multiprocessing import Pool

def create_job_tuples(df, tmp_dir):
    assert 'prequal_folder_updated' in df.columns, "'prequal_folder_updated' not in df.columns"
    tmp_dir = Path(tmp_dir)

    list_job_tuples = []
    for idx, row in df.iterrows():
        prequal = row['prequal_folder_updated']
        wmatlas = Path(prequal.replace('PreQual', 'WMAtlasEVE3'))
        fa = wmatlas / "dwmri%fa.nii.gz"
        if fa.exists():
            save_csv = tmp_dir / f"{idx}.csv"
            save_fa_seg = tmp_dir / f"{idx}_fa_seg.nii.gz"

            if save_csv.exists() and save_fa_seg.exists():
                continue
            
            list_job_tuples.append((prequal, wmatlas, save_csv, save_fa_seg))
        else:
            print(f"fa not found: {fa}")
    print(f"Total jobs: {len(list_job_tuples)}")

    return list_job_tuples


def extract_fa_std_eve_type1(job_tuple):
    global lut_csv, path_atlas_seg
    
    prequal, wmatlas, save_csv, save_fa_seg = job_tuple
    
    # Transform Eve Type 1 segmentation to FA space
    fa = wmatlas / 'dwmri%fa.nii.gz'
    
    t_t1tob0 = wmatlas / 'dwmri%ANTS_t1tob0.txt'
    t_affine = wmatlas / 'dwmri%0GenericAffine.mat'
    t_warpinv = wmatlas / 'dwmri%1InverseWarp.nii.gz'

    ants_command = [
        'antsApplyTransforms', '-d', '3', 
        '-i', path_atlas_seg, '-r', fa, '-o', save_fa_seg,
        '-n', 'NearestNeighbor',
        '-t', t_t1tob0, '-t', f'[{t_affine},1]', '-t', t_warpinv]
    subprocess.run(ants_command)

    # Extract FA std from ROIs
    lut = pd.read_csv(lut_csv)

    img_seg = nib.load(save_fa_seg)
    img_fa = nib.load(fa)
    data_seg = img_seg.get_fdata()
    data_fa = img_fa.get_fdata()

    data = {
        'prequal_folder_updated': [prequal],
        'wmatlas_folder': [str(wmatlas)],
    }
    for roi_id in lut['id'].values:
        if np.sum(data_seg == roi_id) > 1:
            data[f"EveType1-{roi_id}-FA_std"] = [np.nanstd(data_fa[data_seg == roi_id])]
            data[f"EveType1-{roi_id}-SNR"] = [np.nanmean(data_fa[data_seg == roi_id]) / np.nanstd(data_fa[data_seg == roi_id])]
        else:
            print(f"Warning: ROI-{roi_id} has less than 2 voxels:\n{wmatlas}\n{save_fa_seg}\nUse NaN for FA_std and SNR")
            data[f"EveType1-{roi_id}-FA_std"] = [None]
            data[f"EveType1-{roi_id}-SNR"] = [None]
    
    df = pd.DataFrame(data)
    df.to_csv(save_csv, index=False)


def merge_csv(df_main, tmp_dir, final_csv):
    is_first = True
    for idx in df_main.index:
        single_csv = Path(tmp_dir) / f"{idx}.csv"

        if single_csv.exists():
            if is_first:
                df = pd.read_csv(single_csv)
                is_first = False
            else:
                row = pd.read_csv(single_csv)
                df = pd.concat([df, row], axis=0)                
        else:
            print(f"single_csv not found: {single_csv}")
    
    df_main = df_main.merge(df, on=['prequal_folder_updated'], how='left')
    df_main.to_csv(final_csv, index=False)


if __name__ == '__main__':

    # Parallel processing for extracting FA std and SNR from EVE Type 1 ROIs
    global lut_csv, path_atlas_seg
    lut_csv = '/home-local/gaoc11/fa_std_roi_eve3type1/input/EveType1_LUT.csv'
    path_atlas_seg = '/home-local/gaoc11/fa_std_roi_eve3type1/input/Atlas_JHU_MNI_SS_WMPM_Type-I.nii.gz'

    tmp_dir = '/home-local/gaoc11/fa_std_roi_eve3type1/output/'
    df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/data_site_motion.csv')
    list_job_tuples = create_job_tuples(df, tmp_dir)
    
    with Pool(processes=10) as pool:
        for _ in tqdm(pool.imap(extract_fa_std_eve_type1, list_job_tuples, chunksize=1), total=len(list_job_tuples)):
            pass

    # Combine single csv to one
    merge_csv(df, tmp_dir, '/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/data_site_motion_fa-std_snr.csv')
