# This script generates spaghetti plots for qualitative analysis.
# It will loop through 2224 csv files which stores the data that LME fits,
# and corresponding csv files which stores the summary of the fitted LME model.
# It will generate hundreds of small figures. 
# Each is a spaghetti plot of either y~age, or y~motion.
# 
# version 1
# 
# Author: Chenyu Gao
# Date: May 10, 2023

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
import random
from tqdm import tqdm

random.seed(0)
num_samples_to_plot = 100

dpi = 300
figsize = (2,2)

fontdict={'fontsize':9}

path_part_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/part') # contains input data, example file: BrainColor-4-AD_std.csv
path_coef_sum_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/stats/coef_sum') # contains coefficients, standard errors... example file: BrainColor-4-AD_std_coef_summary.csv
path_lut_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr')
path_figure_output = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/qualitative_regression/v1/figs/')

list_input_csv = [fn for fn in path_part_folder.iterdir() if fn.name.endswith('_std.csv')]
for input_csv in tqdm(list_input_csv, total=len(list_input_csv)):
    
    # Parse the file name
    atlas = input_csv.name.split('-')[0]  # Atlas: "EveType1", "BrainColor"
    roi_id = input_csv.name.split('-')[1]  # ROI number: "4"
    dvariable = input_csv.name.split('-')[2].replace('.csv','') # dependent variable: "FA_std"
    
    # Load dataframe of input data and regression summary of the fixed effects
    coef_sum_csv = path_coef_sum_folder / input_csv.name.replace('.csv','_coef_summary.csv')
    df_input = pd.read_csv(input_csv)
    df_coef_sum = pd.read_csv(coef_sum_csv, index_col=0)
    
    # Drop rows from rescan, for visualization purpose
    df_input.drop(df_input[df_input['DTI_ID']==2].index, inplace=True)
    
    # ##### Figure 1: Y ~ Age (interval) #####
    # Regression line
    try:
        slope = df_coef_sum.loc['Interval', 'Estimate']
        stderr = df_coef_sum.loc['Interval', 'Std. Error']
    except:
        continue
    
    fig, ax = plt.subplots(1,1,figsize=figsize)
    
    list_male_interval = []
    list_male_y = []
    list_female_interval = []
    list_female_y = []
    
    for subject in df_input['Subject_ID'].unique():
        
        # skip subject with only one session
        if len(df_input.loc[df_input['Subject_ID']==subject].index)==1:
            continue
        
        # Record values to list
        if df_input.loc[df_input['Subject_ID']==subject, 'Sex'].values[0]==1:
            list_male_interval.append(df_input.loc[df_input['Subject_ID']==subject, 'Interval'].values)
            list_male_y.append(df_input.loc[df_input['Subject_ID']==subject, dvariable].values)
        else:
            list_female_interval.append(df_input.loc[df_input['Subject_ID']==subject, 'Interval'].values)
            list_female_y.append(df_input.loc[df_input['Subject_ID']==subject, dvariable].values)
    
    random_indices = random.sample(range(len(list_male_interval)), num_samples_to_plot)
    for i in random_indices:
        x = list_male_interval[i]
        y = list_male_y[i] - list_male_y[i][0]
        
        ax.plot(x, y, color='tab:blue', alpha=0.3, linestyle='-', linewidth=1, zorder=2*i+1)
        ax.scatter(x, y, color='tab:blue', alpha=0.5, s=2, marker='.', zorder=2*i+1)
        
    random_indices = random.sample(range(len(list_female_interval)), num_samples_to_plot)
    for i in random_indices:
        x = list_female_interval[i]
        y = list_female_y[i] - list_female_y[i][0]
        
        ax.plot(x, y, color='tab:red', alpha=0.3, linestyle='-', linewidth=1, zorder=2*i)
        ax.scatter(x, y, color='tab:red', alpha=0.5, s=2, marker='.', zorder=2*i)
    
    # Plot regression line
    x = np.array([0, df_input['Interval'].max()])
    y = x*slope
    ax.plot(x,y, color='tab:orange', linewidth=2, zorder=99999)
    
    # Set title: region name
    lut = pd.read_csv(path_lut_folder/"{}_LUT.csv".format(atlas))
    roi_name_abbr = lut.loc[lut['id']==int(roi_id), 'ROI_abbr'].values[0]
    
    ax.set_title(roi_name_abbr, fontdict=fontdict)
    ax.set_xlabel("Interval (decade)",fontdict=fontdict)
    ax.set_ylabel(r'$σ - σ_{0}$ (z-score)',fontdict=fontdict)
    ax.set_xticks(ticks=[0,0.4,0.8,1.2])
    
    fn_figure = path_figure_output / 'interval' / "{}_{}_{}_vs_interval_slope:{:.3f}_stderr:{:.3f}.png".format(atlas, roi_id, dvariable, slope, stderr)
    fig.savefig(fn_figure, dpi=dpi, bbox_inches='tight')
    plt.close()

# ##### Figure 2: Y ~ Motion #####
    # Regression line
    try:
        slope = df_coef_sum.loc['Motion', 'Estimate']
        stderr = df_coef_sum.loc['Motion', 'Std. Error']
    except:
        continue
    
    fig, ax = plt.subplots(1,1,figsize=figsize)
    
    list_male_motion = []
    list_male_y = []
    list_female_motion = []
    list_female_y = []
    
    for subject in df_input['Subject_ID'].unique():
        
        # skip subject with only one session
        if len(df_input.loc[df_input['Subject_ID']==subject].index)==1:
            continue
        
        # Sort the sub-dataframe according to Motion column
        df_sort = df_input.loc[df_input['Subject_ID']==subject].sort_values("Motion")
        
        # Record values to list
        if df_input.loc[df_input['Subject_ID']==subject, 'Sex'].values[0]==1:
            list_male_motion.append(df_sort['Motion'].values)
            list_male_y.append(df_sort[dvariable].values)
        else:
            list_female_motion.append(df_sort['Motion'].values)
            list_female_y.append(df_sort[dvariable].values)
    
    random_indices = random.sample(range(len(list_male_motion)), num_samples_to_plot)
    for i in random_indices:
        x = list_male_motion[i]
        y = list_male_y[i] - list_male_y[i][0]
        
        ax.plot(x, y, color='tab:blue', alpha=0.3, linestyle='-', linewidth=1, zorder=2*i+1)
        ax.scatter(x, y, color='tab:blue', alpha=0.5, s=2, marker='.', zorder=2*i+1)
        
    random_indices = random.sample(range(len(list_female_motion)), num_samples_to_plot)
    for i in random_indices:
        x = list_female_motion[i]
        y = list_female_y[i] - list_female_y[i][0]
        
        ax.plot(x, y, color='tab:red', alpha=0.3, linestyle='-', linewidth=1, zorder=2*i)
        ax.scatter(x, y, color='tab:red', alpha=0.5, s=2, marker='.', zorder=2*i)
    
    # Plot regression line
    x = np.array([0, 1])
    y = x*slope
    ax.plot(x,y, color='tab:orange', linewidth=2, zorder=99999)
    
    # Set title: region name
    lut = pd.read_csv(path_lut_folder/"{}_LUT.csv".format(atlas))
    roi_name_abbr = lut.loc[lut['id']==int(roi_id), 'ROI_abbr'].values[0]
    
    ax.set_title(roi_name_abbr, fontdict=fontdict)
    ax.set_xlabel("Motion (mm)",fontdict=fontdict)
    ax.set_ylabel(r'$σ - σ_{0}$ (z-score)',fontdict=fontdict)
    # ax.set_xticks(ticks=[0,0.4,0.8,1.2])
    ax.set_xlim(left=0, right=1)
    fn_figure = path_figure_output / 'motion' / "{}_{}_{}_vs_motion_slope:{:.3f}_stderr:{:.3f}.png".format(atlas, roi_id, dvariable, slope, stderr)
    fig.savefig(fn_figure, dpi=dpi, bbox_inches='tight')
    plt.close()
