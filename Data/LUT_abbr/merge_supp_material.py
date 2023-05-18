# This script merges the look up tables for Eve1,2,3, SLANT together as a single excel sheet.
# The excel sheet is used as the supplementary material for the paper.
# Author: Chenyu Gao
# Date: May 18, 2023

import pandas as pd
from pathlib import Path

path_lut_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr')
path_output = path_lut_folder / 'ROI_LookUpTable.xlsx'

atlas_to_segmentation_dict = {'BrainColor': 'SLANT',
                            'EveType1': 'EveType1',
                            'EveType2': 'EveType2',
                            'EveType3': 'EveType3'}

# Create empty list to store entries for dataframe
list_df_seg_method = []
list_df_label_id  = []
list_df_abbr = []
list_df_full = []
list_df_original = []

for atlas in atlas_to_segmentation_dict.keys():
    seg_method = atlas_to_segmentation_dict[atlas]
    csv = path_lut_folder / "{}_LUT.csv".format(atlas)
    df = pd.read_csv(csv)
    for _,row in df.iterrows():
        list_df_seg_method.append(seg_method)
        list_df_label_id.append(row['id'])
        list_df_abbr.append(row['ROI_abbr'])
        list_df_full.append(row['ROI_rename'])
        list_df_original.append(row['ROI'])

d = {'Segmentation': list_df_seg_method,
     'Label_ID': list_df_label_id,
     'ROI_Name_Abbreviated': list_df_abbr,
     'ROI_Name_Full': list_df_full,
     'ROI_Name_Original': list_df_original
     }
df_merged = pd.DataFrame(data=d)
df_merged.to_excel(path_output, index=False)