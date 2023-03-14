import random
from pathlib import Path
import pandas as pd

selected_stat = 'coef_sum'
num_comparison = 3


path_b1_stats = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/stats')
path_b1_statfd = path_b1_stats / selected_stat
path_b2_stats = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_zscore_feature_20230208/stats')
path_b2_statfd = path_b2_stats / selected_stat

list_pool = [fn.name for fn in path_b1_statfd.iterdir()]

#  randomly sample several 
list_sample = random.sample(list_pool, k=num_comparison)

for csv in list_sample:
    print(csv)
    print('Data_20230309')
    fn = path_b1_statfd / csv
    df = pd.read_csv(fn)
    print(df)
    print('------------')  
    print('Data_zscore_feature_20230208')  
    fn = path_b2_statfd / csv
    df = pd.read_csv(fn)
    print(df)
    print('============================')