# ACCRE

import pandas as pd
import multiprocessing
from tqdm import tqdm
from pathlib import Path

# /nobackup/p_masi/kimm58/projects/WMAtlas/AtlasInputs


def create_job_tuples(df):
    assert 'prequal_folder_updated' in df.columns, "'prequal_folder_updated' not in df.columns"
    
    list_job_tuples = []
    for idx, row in df.iterrows():
            
        wmatlas = Path(row['prequal_folder_updated'].replace('PreQual', 'WMAtlasEVE3'))
        fa = wmatlas / "dwmri%fa.nii.gz"
        
        if fa.exists():
            list_job_tuples.append((idx, fa))
        else:
            print(f"fa not found: {fa}")
    
    return list_job_tuples


if __name__ == '__main__':
    df = pd.read_csv('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/data_site_motion.csv')
    list_job_tuples = create_job_tuples(df)