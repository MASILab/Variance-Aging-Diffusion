# This script generates dataframe(s) that contain RGB parameters of each region in each atlas.
# The color infomation will be used to visualize the 3D moving brain in MATLAB.
# Author: Chenyu Gao
# Date: Feb 14, 2023

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
from pathlib import Path
import numpy as np


# Hyperparams
alpha_max = 0.7 # maximum alpha for set_alpha()
vmax_scale_dict = {"beta:Age_base":1}
alpha_mod_dict = {"beta:Age_base":1}


def set_alpha(val, cbar_center=0, cbar_max=2, alpha_max=0.8, alpha_mod=1):
    """ Set alpha according to beta/p-value (larger beta/pvalue get larger alpha)

    Args:
        val (float): value of the beta or the p-value
        cbar_center (int, optional): value of the center of the colorbar. Defaults to 0.
        cbar_max (int, optional): edge of the colorbar. Defaults to 2.
        alpha_max (float, optional): maximum alpha used for calculation. Can be greater than 1. Defaults to 0.8.
        alpha_mod (float, optional): modification to the alpha. Defaults to 0.

    Returns:
        alpha: alpha value
    """
    alpha = np.abs(val-cbar_center)/np.abs(cbar_max) * alpha_max
    alpha = alpha * alpha_mod
    
    # make sure alpha does not exceed 1 or alpha_max
    if alpha > 1:
        alpha = 1
    if alpha > alpha_max:
        alpha = alpha_max
    
    return alpha


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


# Output location
path_output_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Animation/cmap')

# Location of the summarized LME results
path_heatmap_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_zscore_feature_20230208/stats/coef_heatmap')

# Look-up tables
path_LUT_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/')

# Loop through summarized dataframes
list_heatmap_csv = [fn for fn in path_heatmap_folder.iterdir() if fn.name.endswith('.csv')]
for csv in list_heatmap_csv:
    
    # Atlas
    atlas = csv.name.split('-')[0]
    path_lut = path_LUT_folder / "{0}_LUT.csv".format(atlas)
    lut = pd.read_csv(path_lut)
    
    # Measure
    measure = csv.name.split('-')[1].replace('_coef_all.csv','')  # AD_std
    
    # Summarized dataframe
    df = pd.read_csv(csv, index_col=0)
    
    for stat in df.index.values:
        
        # Hyperparams
        # alpha_mod
        if stat in alpha_mod_dict.keys():
            alpha_mod = alpha_mod_dict[stat]
        else:
            alpha_mod = 1
        # vmin vmax
        if stat in vmax_scale_dict.keys():
            scale = vmax_scale_dict[stat]
        else:
            scale = 1
            
        # Unit Converter
        if stat in ["beta:Age_base","beta:Interval"]:
            # convert years to decades
            unit_convert = 10
            # print(stat, unit_convert)
        else:
            unit_convert = 1
        
        
        # cmaps for beta/p-value
        if stat.split(':')[0]=='beta':
            COL = MplColorHelper(cmap_name='RdBu', start_val=-2*scale, stop_val=2*scale, is_inverse=False)
                        
        elif stat.split(':')[0] == 'p-value':
            COL = MplColorHelper(cmap_name='Reds', start_val=-50*scale, stop_val=0*scale, is_inverse=True)
        
        list_df_roi_id = []
        list_df_roi_name = []
        list_df_r = []
        list_df_g = []
        list_df_b = []
        list_df_alpha = []
        
        # Loop through regions of brain
        for roi_id, roi_name in zip(lut['id'],lut['ROI']):
            
            val = df[roi_name].loc[stat] * unit_convert
            
            if stat.split(':')[0]=='beta':
                if pd.isnull(val):
                    RGB_r = 0
                    RGB_g = 0
                    RGB_b = 0
                    alpha = 0
                else:
                    RGB_r = COL.get_rgb(val)[0]
                    RGB_g = COL.get_rgb(val)[1]
                    RGB_b = COL.get_rgb(val)[2]
                    alpha = set_alpha(val, cbar_center=0, cbar_max=2, alpha_max=alpha_max, alpha_mod=alpha_mod)
                    
            elif stat.split(':')[0] == 'p-value':
                if pd.isnull(val):
                    # print(atlas, measure, roi_id, val)
                    RGB_r = 0
                    RGB_g = 0
                    RGB_b = 0
                    alpha = 0
                elif val == 0:
                    val = 5e-300 # assign a very small p-value to 0s
                    RGB_r = COL.get_rgb(np.log10(val))[0]
                    RGB_g = COL.get_rgb(np.log10(val))[1]
                    RGB_b = COL.get_rgb(np.log10(val))[2]
                    alpha = set_alpha(np.log10(val), cbar_center=0, cbar_max=-50, alpha_max=alpha_max, alpha_mod=alpha_mod)
                else:
                    RGB_r = COL.get_rgb(np.log10(val))[0]
                    RGB_g = COL.get_rgb(np.log10(val))[1]
                    RGB_b = COL.get_rgb(np.log10(val))[2]
                    alpha = set_alpha(np.log10(val), cbar_center=0, cbar_max=-50, alpha_max=alpha_max, alpha_mod=alpha_mod)
            else:
                print('Error')
        
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
             
        fn_save = path_output_folder / "{0}-{1}-{2}-{3}.csv".format(atlas, measure, stat.split(':')[0],stat.split(':')[1])
        pd.DataFrame(data=d).to_csv(fn_save,index=False)