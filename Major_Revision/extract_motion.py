import csv
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm

def extract_eddy_motion_from_prequal(path_prequal):
    eddy_movement_rms_txt = path_prequal / 'EDDY' / 'eddy_results.eddy_movement_rms'
    second_column = []
    try:
        with open(eddy_movement_rms_txt, 'r') as f:
            c = csv.reader(f, delimiter=' ')
            for line in c:
                second_column.append(float(line[2]))
    except:
        print("Error loading movement txt: ", eddy_movement_rms_txt)
    motion = np.nanmean(second_column[1:])

    return motion


if __name__ == '__main__':
    df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/data_site.csv')
    df['prequal_folder_updated'] = None
    df['motion'] = None

    for idx, row in tqdm(df.iterrows(), total=len(df.index), desc='Extracting motion'):
        # reformat prequal folder path
        if row['dataset'] == 'BLSA':
            path_prequal = Path(row['prequal_folder'].replace('DTI','run-'))
        elif row['dataset'] == 'BIOCARD':
            path_prequal = Path(row['prequal_folder'].replace('run-0','run-'))
        else:
            path_prequal = Path(row['prequal_folder'])
        
        if not path_prequal.exists():
            alternative_path = [d for d in path_prequal.parent.iterdir() if ('PreQual' in d.name) and d.is_dir()]
            if len(alternative_path) > 0:
                print(f"Alternative path found for {path_prequal}:\n{alternative_path[0]}")
                path_prequal = alternative_path[0]
            else:
                print(f"Can't find any PreQual: {path_prequal.parent}")
                continue

        # extract motion
        motion = extract_eddy_motion_from_prequal(path_prequal)
        df.at[idx, 'prequal_folder_updated'] = str(path_prequal)
        df.at[idx, 'motion'] = motion
        
    df.to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/data_site_motion.csv', index=False)