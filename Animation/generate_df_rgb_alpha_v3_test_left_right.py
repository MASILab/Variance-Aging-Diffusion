# This script intentionally sets the RGB and alpha wrongly 
# so that the left brain appears invisible. 
# This is for us to easily distinguish between left or right 
# so we can label left right correctly.
#
# Author: Chenyu Gao
# Date: May 1, 2023

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
from pathlib import Path
import numpy as np


# Hyperparams
sig_scale = 10
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Helper to retrieve RGB info from matplotlib cmap
class MplColorHelper:
    def __init__(self, cmap_name, start_val, stop_val, is_inverse=False):
        self.cmap_name = cmap_name
        if is_inverse:
            self.cmap = plt.get_cmap(cmap_name).reversed()
        else:
            self.cmap = plt.get_cmap(cmap_name)        
        self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
        self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

    def get_rgb(self, val):
        return self.scalarMap.to_rgba(val)

# 
path_output_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Animation/cmap')
path_heatmap_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/stats/coef_heatmap')
path_LUT_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/')

# 
list_heatmap_csv = [fn for fn in path_heatmap_folder.iterdir() if fn.name.endswith('_coef_all_pval_adjusted.csv')]
for csv in list_heatmap_csv:
    
    # Atlas
    atlas = csv.name.split('-')[0]
    path_lut = path_LUT_folder / "{0}_LUT.csv".format(atlas)
    lut = pd.read_csv(path_lut)
    
    # Measure
    measure = csv.name.split('-')[1].replace('_coef_all_pval_adjusted.csv','')  # "AD_std"
    
    # Summarized dataframe
    df = pd.read_csv(csv, index_col=0)
    
    for stat in df.index.values:
        if stat.split(':')[0]=='beta':
            COL = MplColorHelper(cmap_name='RdBu', start_val=-2, stop_val=2, is_inverse=False)          
        elif stat.split(':')[0] == 'p-value':
            # skip pvalue
            continue
        
        # get max and min values 
        top3 = df.loc[stat].nlargest(3)
        pos_top3 = top3[top3 > 0]
        if len(pos_top3) > 0:
            average_pos_top3 = np.mean(pos_top3)
        else:
            average_pos_top3 = 0
        
        bottom3 = df.loc[stat].nsmallest(3)
        neg_bottom3 = bottom3[bottom3 < 0]   # select only negative values
        if len(neg_bottom3) > 0:
            average_neg_bottom3 = np.mean(neg_bottom3)
        else:
            average_neg_bottom3 = 0   
        
        # Loop through regions of brain
        list_df_roi_id = []
        list_df_roi_name = []
        list_df_r = []
        list_df_g = []
        list_df_b = []
        list_df_alpha = []
        
        for roi_id, roi_name in zip(lut['id'],lut['ROI']):
            # Intentionally set left as invisible
            if ('left' in roi_name) or ('Left' in roi_name):
                val = 0
                pvalue = 1
            else:
                print(roi_name)
                val = df[roi_name].loc[stat]
                pvalue = df[roi_name].loc[stat.replace('beta:','p-value:')]
            
            # if p-value is greater than 0.05, set the alpha as 0
            if pvalue > 0.05:
                alpha = 0
            else:
                if val >=0:
                    alpha = sigmoid(val/average_pos_top3*2*sig_scale - sig_scale)  # TODO
                else:
                    alpha = sigmoid(val/average_neg_bottom3*2*sig_scale - sig_scale)  # TODO
            
            if pd.isnull(val):
                RGB_r, RGB_g, RGB_b, alpha = 0, 0, 0, 0                
            else:
                RGB_r, RGB_g, RGB_b = COL.get_rgb(val)[0], COL.get_rgb(val)[1], COL.get_rgb(val)[2]
                
            list_df_roi_id.append(roi_id)
            list_df_roi_name.append(roi_name)
            list_df_r.append(RGB_r)
            list_df_g.append(RGB_g)
            list_df_b.append(RGB_b)
            list_df_alpha.append(alpha)
        
        # Save to csv
        d = {'ROI_ID': list_df_roi_id,
             'ROI_Name': list_df_roi_name,
             'R': list_df_r,
             'G': list_df_g,
             'B': list_df_b,
             'Alpha': list_df_alpha}
             
        fn_save = path_output_folder / "{0}-{1}-{2}-{3}.csv".format(atlas, measure, stat.split(':')[0], stat.split(':')[1])
        pd.DataFrame(data=d).to_csv(fn_save,index=False)