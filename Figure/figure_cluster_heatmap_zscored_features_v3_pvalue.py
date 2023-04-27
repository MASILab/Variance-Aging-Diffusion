import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
import pdb
import scipy.spatial as sp, scipy.cluster.hierarchy as hc


# Output location
path_out_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/clustermap_v3/')

# Load the dataframe
path_coef_heatmap_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_zscore_feature_20230208/stats/coef_heatmap')
list_csv = [fn for fn in path_coef_heatmap_folder.iterdir()]

for fn in list_csv:
    # Load csv
    df = pd.read_csv(fn, index_col=0)
    
    # Split into 2 for each subplot
    df_beta = df.iloc[[0,1,3,2,4]]
    df_pvalue = df.iloc[[5,6,8,7,9]]
    
    # Mask of NAN values
    mask_beta_nan = df_beta.isna()
    mask_pvalue_nan = df_pvalue.isna()
    
    # Linkage for columns (based on beta values)
    df_beta_imp = df_beta.fillna(0)  # Impute missing beta with 0
    df_beta_imp.iloc[[0,1]] = 10 * df_beta_imp.iloc[[0,1]]  # converge unit from year to decade
    col_linkage = hc.linkage(y = df_beta_imp.T, method='average', metric='euclidean', optimal_ordering=True)
    
    # Convert p-values to log
    df_pvalue_imp = df_pvalue.fillna(1)
    print(df_pvalue_imp)
    df_pvalue_imp.replace(to_replace=0, value=5e-300)
    print(df_pvalue_imp)
    for c in df_pvalue_imp.columns:
        df_pvalue_imp[c] = np.log10(df_pvalue_imp[c])
    print(df_pvalue_imp)

    # Clustermap
    
    cmap=plt.cm.get_cmap('Reds').reversed()
    
    g = sns.clustermap(data=df_pvalue_imp,
                        figsize=(28,11),
                        row_cluster=False,
                        col_linkage=col_linkage,
                        mask=mask_pvalue_nan,
                        dendrogram_ratio=(0.03, 0),
                        cmap = cmap,
                        vmax = 0,
                        vmin = -25,
                        cbar_pos=(0,.15,.005,.7))
    # Set colorbar ticks
    cbar = g.ax_heatmap.collections[0].colorbar
    cbar.set_ticks([0, -5, -10, -15, -20, -25])
    cbar.set_ticklabels(['1', r'$10^{-5}$', r'$10^{-10}$',r'$10^{-15}$', r'$10^{-20}$',r'$10^{-25}$'])
    
    # cbar.set_ticks([0, -25 , -50, -75, -100,-125,-150,-175,-200])
    # cbar.set_ticklabels(['1', r'$10^{-25}$', r'$10^{-50}$', r'$10^{-75}$', r'$10^{-100}$', r'$10^{-125}$', r'$10^{-150}$', r'$10^{-175}$', r'$10^{-200}$'])
    # cbar.set_ticks([0, -25 , -50])
    # cbar.set_ticklabels(['1', r'$10^{-25}$', r'$10^{-50}$'])

    g.ax_heatmap.yaxis.set_ticks_position("left")
    
    # 
    g.ax_heatmap.set_facecolor('#e4e4e4')
    
    # title
    atlas = fn.name.split('-')[0]
    measure_type = fn.name.split('-')[1].replace('_coef_all.csv','')
    # g.fig.suptitle("p-values of the fixed effects\nDependent variable: {0} (Z-Score), Atlas: {1}".format(measure_type,atlas),
    #                x = 0.5,
    #                y = 0.98,
    #                fontsize =14)

    figure_save = path_out_folder/ 'pvalue_reds_vmin25_heatonly'/ '{0}_{1}_pvalue_clustermap.png'.format(atlas,measure_type)
    plt.savefig(figure_save,dpi=300)
    