# Collect stats info from /coef_sum (output of lmer fitted on each atlas+region+diff) in preparation for the heatmap.
# Author: Chenyu Gao
# Date: Feb 1, 2023

import pandas as pd
import numpy as np
from pathlib import Path

# list of regions/measurements/values
list_atlas = ['EveType1','EveType2','EveType3','BrainColor']
list_diff_type = ['RD', 'AD', 'FA', 'MD']
list_value_type = ['std']

# Stats info to extract
list_fixed_effects =  ['Age_base','Interval','Motion','Sex1','DTI_ID2']
list_stats_name = ['Estimate','Pr(>|t|)']

# Path of the lookup table, lmer results, output
path_LUT_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/')
path_coef_sum_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/stats/coef_sum/')
path_output = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/stats/coef_heatmap')


for atlas in list_atlas:
    
    # Load the LUT
    path_lut = path_LUT_folder / "{0}_LUT.csv".format(atlas)
    df_lut = pd.read_csv(path_lut)
      
    for diff_type in list_diff_type:
        for value_type in list_value_type:
            
            # Create empty array to store stats info
            d = np.empty(shape=(len(list_fixed_effects)*len(list_stats_name), len(df_lut.index)))
            
            index_col = 0
            
            # Loop through regions
            for _, row in df_lut.iterrows():
                
                roi_id = row['id']
                roi_name = row['ROI']
                
                # load the coef_sum of this region
                fn_csv = path_coef_sum_folder/"{0}-{1}-{2}_{3}_coef_summary.csv".format(atlas, roi_id, diff_type, value_type)
                df_coef = pd.read_csv(fn_csv)
                
                index_row = 0
                
                for stat in list_stats_name:
                    for fix in list_fixed_effects:
                        if df_coef.loc[df_coef['Unnamed: 0']==fix, stat].values.shape[0] == 1:
                            d[index_row, index_col] = df_coef.loc[df_coef['Unnamed: 0']==fix, stat].item()
                            
                        elif df_coef.loc[df_coef['Unnamed: 0']==fix, stat].values.shape[0] == 0:
                            d[index_row, index_col] = np.nan
                            
                        else:
                            print("ERROR")
                        index_row += 1
                index_col += 1
            
            # Save the array as dataframe
            columns_df = [roi for roi in df_lut['ROI']]
            index_df = []
            for stat in list_stats_name:
                for fix in list_fixed_effects:
                    if stat == 'Estimate':
                        pre = "beta"
                    elif stat == 'Pr(>|t|)':
                        pre = "p-value"
                    index_df.append("{0}:{1}".format(pre,fix))
            
            fn_save = path_output / "{0}-{1}_{2}_coef_all.csv".format(atlas, diff_type, value_type)
            
            pd.DataFrame(data=d, index=index_df, columns=columns_df).to_csv(fn_save, index=True)
            
