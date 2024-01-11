# List out numerical values of betas and p-values from the heatmap.
# This will be used for easier reference when writing the result section of the paper.
# Author: Chenyu Gao
# Date: Jun 20, 2023

import pandas as pd
from pathlib import Path

lut_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr')
heatmap_stats_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/stats/coef_heatmap')
output_dir = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/nice_table')

selected_lut = ['BrainColor', 'EveType1']
selected_DTI_scalar = ['FA']

# Loop through csv files and pick the selected ones according to file names
for csv in heatmap_stats_folder.iterdir():
    if not csv.name.endswith('_coef_all_pval_adjusted.csv'):
        continue
    
    atlas = csv.name.split('-')[0]
    DTI_scalar = csv.name.split('-')[1].split('_')[0]

    if (atlas in selected_lut) and (DTI_scalar in selected_DTI_scalar):
        list_roi_name_original = []
        list_roi_name_rename = []
        list_roi_name_abbr = []

        list_age_base_beta = []
        list_age_base_p = []
        list_interval_beta = []
        list_interval_p = []
        list_motion_beta = []
        list_motion_p = []
        list_sex_beta = []
        list_sex_p = []
        list_rescan_beta = []
        list_rescan_p = []

        heatmap = pd.read_csv(csv, index_col=0)

        path_lut = lut_folder / "{}_LUT.csv".format(atlas)
        lut = pd.read_csv(path_lut)

        for _, row in lut.iterrows():
            list_roi_name_original.append(row['ROI'])
            list_roi_name_rename.append(row['ROI_rename'])
            list_roi_name_abbr.append(row['ROI_abbr'])

            # Age_base
            beta = heatmap.loc['beta:Age_base', row['ROI']]
            pvalue = heatmap.loc['p-value:Age_base', row['ROI']]
            if beta != beta:
                list_age_base_beta.append(None)
                list_age_base_p.append(None)
            else:
                list_age_base_beta.append(beta)
                list_age_base_p.append(pvalue)

            # Age_interval
            beta = heatmap.loc['beta:Interval', row['ROI']]
            pvalue = heatmap.loc['p-value:Interval', row['ROI']]
            if beta != beta:
                list_interval_beta.append(None)
                list_interval_p.append(None)
            else:
                list_interval_beta.append(beta)
                list_interval_p.append(pvalue)
            
            # Motion
            beta = heatmap.loc['beta:Motion', row['ROI']]
            pvalue = heatmap.loc['p-value:Motion', row['ROI']]
            if beta != beta:
                list_motion_beta.append(None)
                list_motion_p.append(None)
            else:
                list_motion_beta.append(beta)
                list_motion_p.append(pvalue)
            
            # Sex
            beta = heatmap.loc['beta:Sex1', row['ROI']]
            pvalue = heatmap.loc['p-value:Sex1', row['ROI']]
            if beta != beta:    
                list_sex_beta.append(None)
                list_sex_p.append(None)
            else:
                list_sex_beta.append(beta)
                list_sex_p.append(pvalue)
                
            # Rescan
            beta = heatmap.loc['beta:DTI_ID2', row['ROI']]
            pvalue = heatmap.loc['p-value:DTI_ID2', row['ROI']]
            if beta != beta:
                list_rescan_beta.append(None)
                list_rescan_p.append(None)
            else:    
                list_rescan_beta.append(beta)
                list_rescan_p.append(pvalue)

        d = {'ROI_original':list_roi_name_original,
             'ROI_rename':list_roi_name_rename,
             'ROI_abbr':list_roi_name_abbr,
             'coefficient:Age_base':list_age_base_beta,
             'pvalue:Age_base':list_age_base_p,
             'coefficient:Age_interval':list_interval_beta,
             'pvalue:Age_interval':list_interval_p,
             'coefficient:Motion':list_motion_beta,
             'pvalue:Motion':list_motion_p,
             'coefficient:Sex':list_sex_beta,
             'pvalue:Sex':list_sex_p,
             'coefficient:Rescan':list_rescan_beta,
             'pvalue:Rescan':list_rescan_p}
        
        df = pd.DataFrame(data=d)
        output = output_dir / ('lme_stats_' + csv.name.replace('_std_coef_all_pval_adjusted.csv', '.csv'))
        df.to_csv(output, index=False)
