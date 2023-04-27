import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
import scipy.spatial as sp, scipy.cluster.hierarchy as hc


# Output location
path_out_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/clustermap_v2/')

# Load the dataframe
path_coef_heatmap_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_zscore_feature_20230208/stats/coef_heatmap')
list_csv = [fn for fn in path_coef_heatmap_folder.iterdir()]

for fn in list_csv:
    # Load csv
    df = pd.read_csv(fn, index_col=0)
    print(df)
    
    # Split into 2 for each subplot
    df_beta = df.iloc[[0,1,3,2,4]]
    df_pvalue = df.iloc[[5,6,8,7,9]]
    
    # Mask of NAN values
    mask_beta_nan = df_beta.isna()
    mask_pvalue_nan = df_pvalue.isna()
    
    # Impute missing beta with 0 for calculating hierarchical cluster
    df_beta_imp = df_beta.fillna(0)
    
    # compute distances and linkage manually
    df_beta_imp.iloc[[0,1]] = 10*df_beta_imp.iloc[[0,1]] # converge unit from year to decade
    col_linkage = hc.linkage(y = df_beta_imp.T, method='average', metric='euclidean', optimal_ordering=True)
    
    # Clustermap
    g = sns.clustermap(data=df_pvalue,
                        figsize=(28,15),
                        row_cluster=False,
                        col_linkage=col_linkage,
                        mask=mask_pvalue_nan,
                        dendrogram_ratio=(0.03, .4),
                        cmap = 'Blues',
                        vmin=0,
                        vmax=0.05,
                        cbar_pos=(0,.15,.005,.5))

    g.ax_heatmap.yaxis.set_ticks_position("left")
    
    # 
    g.ax_heatmap.set_facecolor('#e4e4e4')
    # title
    atlas = fn.name.split('-')[0]
    measure_type = fn.name.split('-')[1].replace('_coef_all.csv','')
    g.fig.suptitle("p-values of the fixed effects\nDependent variable: {0} (Z-Score), Atlas: {1}".format(measure_type,atlas),
                   x = 0.5,
                   y = 0.98,
                   fontsize =14)

    figure_save = path_out_folder/ 'pvalue'/ '{0}_{1}_pvalue_clustermap.png'.format(atlas,measure_type)
    plt.savefig(figure_save,dpi=300)
    
    