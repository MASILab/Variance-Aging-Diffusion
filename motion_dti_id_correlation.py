# R-Squared to measure the correlation between Motion and DTI_ID
# Pseudocode provided by Dr. Landman.
#
# Author: Chenyu Gao, Bennett Landman
# Date: Jan 31, 2023

import pandas as pd
import numpy as np

# Import the dataframe
df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv')

# Remove sessions with only 1 DTI (where there is no rescan)
for session in df['Session'].unique():
    if df.loc[df['Session']==session].shape[0]<2:
        index_drop = df.loc[df['Session']==session].index
        df.drop(index_drop, inplace=True)

# Compute mean values
motion_mean_all = np.nanmean(df['Motion'].values)
motion_mean_1 = np.nanmean(df.loc[df['DTI_ID']==1, 'Motion'].values)
motion_mean_2 = np.nanmean(df.loc[df['DTI_ID']==2, 'Motion'].values)

# Add columns to dataframe
df['Motion_correct_all'] = df['Motion'] - motion_mean_all

df['Motion_correct_group'] = np.nan
df.loc[df['DTI_ID']==1,'Motion_correct_group'] = df.loc[df['DTI_ID']==1,'Motion'] - motion_mean_1 
df.loc[df['DTI_ID']==2,'Motion_correct_group'] = df.loc[df['DTI_ID']==2,'Motion'] - motion_mean_2

# Compute R-squared
rss = np.var(df['Motion_correct_group'].values)
tss = np.var(df['Motion_correct_all'].values)

r_squared = 1 - rss/tss

print('R2: ', r_squared)