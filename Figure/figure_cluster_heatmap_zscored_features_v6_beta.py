import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
from matplotlib.font_manager import FontProperties
import scipy.spatial as sp, scipy.cluster.hierarchy as hc
import re

# Hyperparameters
figuresz = (7.8, 3.3)  #TODO
dpi = 600 #TODO
fontsz = 10
fontsz_cbar = 8
fontsz_xticks = {'BrainColor': 8,
                 'EveType1': 8,
                 'EveType2': 8,
                 'EveType3': 8}

xticklabels = {'BrainColor': 2,
                 'EveType1': 2,
                 'EveType2': 2,
                 'EveType3': 2}

# Output location
path_out_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/clustermap_v6/') #TODO

# Load the dataframe
path_coef_heatmap_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/stats/coef_heatmap')
list_csv = [fn for fn in path_coef_heatmap_folder.iterdir() if fn.name.endswith('_pval_adjusted.csv')]

for fn in list_csv:
    # Parse filename
    atlas = fn.name.split('-')[0]
    measure_type = fn.name.split('-')[1].replace('_coef_all_pval_adjusted.csv','')

    df = pd.read_csv(fn, index_col=0)
    lut = pd.read_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr/{0}_LUT.csv".format(atlas)) # LUT for renaming
    column_mapping = dict(zip(lut['ROI'], lut['ROI_abbr']))
    df.rename(columns=column_mapping, inplace=True)
    
    # Split into 2 for each subplot
    df_beta = df.iloc[[0,1,3,2,4]]
    df_pvalue = df.iloc[[5,6,8,7,9]]
    
    # Mask of i) NANs; ii) corresponding p-value > 0.05
    mask_nan = df_beta.isna()
    mask_pvalue = df_pvalue > 0.05
    mask_together = pd.DataFrame(np.logical_or(mask_nan.values, mask_pvalue.values), 
                                 columns=df_beta.columns, 
                                 index=df_beta.index)
    
    # Impute missing beta with 0 for calculating hierarchical cluster
    df_beta_imp = df_beta.fillna(0)
    
    # compute distances and linkage manually
    col_linkage = hc.linkage(y = df_beta_imp.T, method='average', metric='euclidean', optimal_ordering=True)
    
    # Clustermap
    print(df_beta_imp)
    g = sns.clustermap(data=df_beta_imp,
                       figsize=figuresz,
                       row_cluster=False,
                       col_linkage=col_linkage,
                       mask=mask_together,
                       dendrogram_ratio=(0, 0.3),
                       cmap = 'RdBu',
                       center = 0,
                       vmin=-2,
                       vmax=2,
                       cbar_pos=None,
                       xticklabels=xticklabels[atlas],
                       yticklabels=['Baseline', 'Interval', 'Sex', 'Motion', 'Rescan']
                       )
    
    g.ax_heatmap.tick_params(pad=-2, axis='y')
    g.ax_heatmap.tick_params(pad=1, axis='x')
    g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_yticklabels(),
                                 verticalalignment='top',
                                 rotation =115,
                                 fontproperties=FontProperties(family='Ubuntu Condensed', 
                                                               size=fontsz))
    g.ax_heatmap.set_xticklabels(g.ax_heatmap.get_xticklabels(),
                                 fontproperties=FontProperties(family='Ubuntu Condensed', 
                                                               size=fontsz_xticks[atlas]))

    # color for "bad pixels"
    g.ax_heatmap.set_facecolor('#e4e4e4')


    plt.tight_layout(pad=0.00)

    figure_save = path_out_folder/ 'beta'/ '{0}_{1}_beta_clustermap.png'.format(atlas,measure_type)
    plt.savefig(figure_save, dpi=dpi)
    