import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
import pdb
from matplotlib.colors import LogNorm
import math

# Output location
path_out_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/clustermap/')

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
    
    # fig, axes = plt.subplots(2,1,figsize=(25,30),gridspec_kw={'height_ratios': [2, 1]})
    
    df_beta_imp.iloc[[0,1]] = 10*df_beta_imp.iloc[[0,1]]
    
    # Subplot-1
    g = sns.clustermap(data=df_beta_imp,
                       method='average',
                       metric='euclidean',
                        figsize=(28,12),
                        row_cluster=False,
                        mask=mask_beta_nan,
                        dendrogram_ratio=(0.03, .4),
                        cmap = 'RdBu',
                        center = 0,
                        vmin=-2,
                        vmax=2,
                        cbar_pos=(0,.15,.005,.5))
    # g.ax_heatmap.set_title('HEATMAT')
    # g.ax_col_dendrogram.set_title('Heeelllooo')
    g.ax_heatmap.yaxis.set_ticks_position("left")
    # title
    atlas = fn.name.split('-')[0]
    measure_type = fn.name.split('-')[1].replace('_coef_all.csv','')
    g.fig.suptitle("Coefficients of the fixed effects\nDependent variable: {0} (Z-Score), Atlas: {1}".format(measure_type,atlas),
                   x = 0.5,
                   y = 0.98,
                   fontsize =14)

    # # Subplot-2
    # log_norm = LogNorm(vmin=np.nanmin(df_pvalue.values), vmax=np.nanmax(df_pvalue.values))
    # cbar_ticks = [math.pow(10, i) for i in range(math.floor(math.log10(np.nanmin(df_pvalue.values))), 1+math.ceil(math.log10(np.nanmax(df_pvalue.values))))]
    
    # axes[1] = sns.heatmap(data = df_pvalue,
    #                       square='equal',
    #                       ax = axes[1],
    #                       norm = log_norm,
    #                       cbar_kws={"ticks":cbar_ticks}
    #                       )
    # axes[1].imshow(df_pvalue.values, norm=LogNorm())
    
    print(df_beta)
    print(df_pvalue)
    print(mask_beta_nan)
    print(mask_pvalue_nan)
    print(df_beta_imp)
    # print(df_pvalue.values)
    
    
    figure_save = path_out_folder/'{0}_{1}_v1.png'.format(atlas,measure_type)
    plt.savefig(figure_save,dpi=300)
    break