import pandas as pd
import numpy as np
from statsmodels.stats.multitest import multipletests
from pathlib import Path

# Iterate through the dataframes for heatmap
path_coef_heatmap_folder = Path('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/stats/coef_heatmap')
list_csv = [fn for fn in path_coef_heatmap_folder.iterdir() if fn.name.endswith('_coef_all.csv')]

for fn in list_csv:

    # Load csv
    df = pd.read_csv(fn, index_col=0)

    # Iterate through rows of pvalues
    for ind in df.index:
        if ind.startswith('p-value:'):
            p_values = df.loc[ind].values

            # Replace NaNs with 1
            p_values_wonan = np.nan_to_num(p_values, nan=1)

            # Perform FDR correction using the Benjamini-Hochberg method
            p_values_adj = multipletests(p_values_wonan, alpha=0.05, method='fdr_bh')[1]
            
            # Replace p-values with Benjamini-Hochberg adjusted p-values
            df.loc[ind] = p_values_adj

    # Save the pvalue-adjusted dataframe to csv
    fn_save = path_coef_heatmap_folder / fn.name.replace('_all.csv', '_all_pval_adjusted.csv')
    df.to_csv(fn_save, index=True)
