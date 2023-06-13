# Report beta and p-values of opposite pairs of Motion and Interval
#
# Author: Chenyu Gao
# Date: Jun 13, 2023

import pandas as pd
import math

df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/stats/coef_heatmap/EveType1-FA_std_coef_all_pval_adjusted.csv', index_col=0)
LUT = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr/EveType1_LUT.csv')
threshold = -0.1 # smaller value leads to less rows presented but more significant results

list_df_roi_rename = []
list_df_beta_interval = []
list_df_p_interval = []
list_df_beta_motion = []
list_df_p_motion = []

for col in df.columns:
    beta_interval = df.loc['beta:Interval', col]
    beta_motion = df.loc['beta:Motion', col]

    p_interval = df.loc['p-value:Interval', col]
    p_motion = df.loc['p-value:Motion', col]
    
    # if (beta_interval*beta_motion <= threshold) or ((beta_interval < 0) and (beta_motion > 0)):
    if (beta_interval*beta_motion <= threshold):
        list_df_roi_rename.append(LUT.loc[LUT['ROI']==col, 'ROI_rename'].item())
        list_df_beta_interval.append("{0:.3f}".format(beta_interval))
        list_df_p_interval.append("{:.1e}".format(p_interval))
        list_df_beta_motion.append("{0:.3f}".format(beta_motion))
        list_df_p_motion.append("{:.1e}".format(p_motion))

d = {'ROI':list_df_roi_rename, 
     'beta_interval': list_df_beta_interval, 
     'p-value_interval': list_df_p_interval,
     'beta_motion': list_df_beta_motion,
     'p-value_motion': list_df_p_motion}
report = pd.DataFrame(data=d)

# Remove "Left " and "Right " prefixes to create a 'clean' column
report['ROI_clean'] = report['ROI'].str.replace('Left ', '').str.replace('Right ', '').str.replace('Inferior ', '').str.replace('Lateral ', '').str.replace('Middle ', '').str.replace('Superior ', '')
report['ROI_clean_l'] = report['ROI'].str.replace('Left ', '').str.replace('Right ', '')

# Sort first by 'Region_clean' and then by 'Region'
report = report.sort_values(by=['ROI_clean', 'ROI_clean_l', 'ROI'])

# Remove the 'Region_clean' column as it's no longer needed
report = report.drop('ROI_clean', axis=1)
report = report.drop('ROI_clean_l', axis=1)

print(report)

report.to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Experiments/report_beta_p-value_ROI.csv', index=False)
report.to_excel('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Experiments/report_beta_p-value_ROI.xlsx', index=False)