# Generate clustermap for p-values.
# Author: Chenyu Gao
# Date: July 22, 2024

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
from matplotlib.font_manager import FontProperties
import scipy.spatial as sp, scipy.cluster.hierarchy as hc
import re

# Hyperparameters
figuresz = (7.8, 3.3)
dpi = 600
fontsz = 10
fontsz_cbar = 8
fontsz_xticks = {'EveType1': 8}
xticklabels = {'EveType1': 2}

# Output location
path_out_folder = Path('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/figures/clustermap_v7/')

# Load the dataframe
path_coef_heatmap_folder = Path('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/stats/coef_heatmap')
list_csv = [fn for fn in path_coef_heatmap_folder.iterdir() if fn.name.endswith('_pval_adjusted.csv')]

for fn in list_csv:

    # Parse filename
    atlas = fn.name.split('-')[0]
    measure_type = fn.name.split('-')[1].replace('_coef_all_pval_adjusted.csv','')

    # Load csv and rename ROIs
    df = pd.read_csv(fn, index_col=0)
    lut = pd.read_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr/{0}_LUT.csv".format(atlas)) # LUT for renaming
    column_mapping = dict(zip(lut['ROI'], lut['ROI_abbr']))
    df.rename(columns=column_mapping, inplace=True)
    
    # Split into 2 for each subplot
    df_beta = df.iloc[[0,1,3,2]]
    df_pvalue = df.iloc[[4,5,7,6]]
    
    # Calculate hierarchical cluster based on beta values
    df_beta_imp = df_beta.fillna(0)
    col_linkage = hc.linkage(y = df_beta_imp.T, method='average', metric='euclidean', optimal_ordering=True)
    
    # -log(P)
    df_pvalue_imp = df_pvalue.fillna(1)
    df_pvalue_imp.replace(to_replace=0, value=5e-300, inplace=True) # replace 0 with a very small value
    for c in df_pvalue_imp.columns:
        df_pvalue_imp[c] = -np.log10(df_pvalue_imp[c])
    
    # Clustermap
    g = sns.clustermap(data=df_pvalue_imp,
                       figsize=figuresz,
                       row_cluster=False,
                       col_linkage=col_linkage,
                       dendrogram_ratio=(0, 0.3),
                       cmap = 'hot',
                       vmin=0,
                       vmax=50,
                       cbar_pos=None,
                       cbar_kws={'ticks': [0, 25, 50]},
                       tree_kws={'linewidths':0},
                       xticklabels=xticklabels[atlas],
                       yticklabels=['Baseline', 'Interval', 'Sex', 'Motion']
                       )
    
    # Font
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

    plt.tight_layout(pad=0.00)

    figure_save = path_out_folder/ 'pvalue'/ '{0}_{1}_pvalue_clustermap.png'.format(atlas,measure_type)
    plt.savefig(figure_save, dpi=dpi)
    