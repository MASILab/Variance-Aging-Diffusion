import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Output location
path_out_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/heatmap/')

# Load the dataframe
path_coef_heatmap_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/stats/coef_heatmap')
list_csv = [fn for fn in path_coef_heatmap_folder.iterdir()]

for fn in list_csv:
    df = pd.read_csv(fn, index_col=0)
    
    # distribution of the data
    for idx in df.index:
        print("{0}\tmean: {1}\tstd: {2}".format(idx, np.nanmean(df.loc[[idx]].values), np.nanvar(df.loc[[idx]].values)))
    
    # modify the values
    df_mod = df.apply(lambda x: (x-x.mean())/x.std(), axis = 1)
    
    # Heatmap
    fig, ax = plt.subplots(figsize=(25,10))
    hm = ax.imshow(df_mod.values, cmap='RdBu')
    # hm = ax.imshow(df_mod.values, cmap='seismic')
    
    ax.set_yticks(ticks=range(df.values.shape[0]), labels=df.index)
    ax.set_xticks(ticks=range(df.values.shape[1]), labels= df.columns, rotation='vertical')

    # title
    atlas = fn.name.split('-')[0]
    measure_type = fn.name.split('-')[1].replace('_coef_all.csv','')
    ax.set_title("Information of Fixed Effects\n(Dependent Variable: {0}, Atlas: {1})".format(measure_type, atlas))

    # colorbar
    fig.colorbar(hm, ax=ax,location='right',fraction=0.025,shrink=0.5)

    # Save figure
    figure_save = path_out_folder / 'zscore' / fn.name.replace('_all.csv','_zscore_RdBu.png')
    plt.savefig(figure_save)

