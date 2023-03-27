# This script tests the Benjamini-Hochberg method for False Discovery Rates (FDR) implemented by statsmodels.
# The method itself is well introduced in the following YouTube video:
# https://www.youtube.com/watch?v=K8LQSvtjcEo
# Date: Mar 27, 2023
# Author: Chenyu Gao

import pandas as pd
import numpy as np
from statsmodels.stats.multitest import multipletests

# Load example p-values
df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/stats/coef_heatmap/BrainColor-AD_std_coef_all.csv', index_col=0)
p_values = df.loc['p-value:Interval'].values

# Replace NaNs with 1
p_values_wonan = np.nan_to_num(p_values, nan=1)

# Perform FDR correction using the Benjamini-Hochberg method
p_values_adj = multipletests(p_values_wonan, alpha=0.05, method='fdr_bh')[1]

# Print results and compare, in accending order
sorted_indices = np.argsort(p_values_adj)
for i in sorted_indices:
    amp = p_values_adj[i]/p_values_wonan[i]
    print("{0}\t{1}\t{2}---{3:3.4}".format(p_values[i], p_values_adj[i], amp, p_values_wonan.size/amp))