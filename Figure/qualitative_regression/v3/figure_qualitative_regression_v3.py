# Compared to version 1, this version will pick representative examples 
# for good, medium, and bad fitting.
# Good, medium, bad are measured by Std. Err. from LME.
# y~motion is abandoned because the figure is hard to interpret.
# We will show data and its regression result for y~interval.
# 
# version 3: use full name of ROIs
# 
# Author: Chenyu Gao
# Date: May 11, 2023

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm

random.seed(0)
num_samples_to_plot = 150
num_examples_per_class = 10

dpi = 600
figsize = (2,2)

fontdict={'fontsize':9}

path_part_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/part') # contains input data, example file: BrainColor-4-AD_std.csv
path_coef_sum_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data_20230309/stats/coef_sum') # contains coefficients, standard errors... example file: BrainColor-4-AD_std_coef_summary.csv
path_lut_folder = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr')
path_figure_output = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/qualitative_regression/v3/figs/')

# Loop through all results, prepare a dataframe that has columns: input data csv file name; dti scalar; slope; standard error (as measure of fitting)...
list_df_csv = []
list_df_atlas = []
list_df_roi_id = []  # "4"
list_df_dvariable = []  # "FA_std"
list_df_dti = []  # "FA"
list_df_slope = []
list_df_stderr = []

print('Start preparing the dataframe...')
list_input_csv = [fn for fn in path_part_folder.iterdir() if fn.name.endswith('_std.csv')]
for input_csv in tqdm(list_input_csv, total=len(list_input_csv)):
    # Parse the file name
    atlas = input_csv.name.split('-')[0]  # Atlas: "EveType1", "BrainColor"
    roi_id = input_csv.name.split('-')[1]  # ROI number: "4"
    dvariable = input_csv.name.split('-')[2].replace('.csv','') # dependent variable: "FA_std"
    # Load regression summary
    coef_sum_csv = path_coef_sum_folder / input_csv.name.replace('.csv','_coef_summary.csv')
    df_coef_sum = pd.read_csv(coef_sum_csv, index_col=0)
    try:
        slope = df_coef_sum.loc['Interval', 'Estimate']
        stderr = df_coef_sum.loc['Interval', 'Std. Error']
    except:
        continue
    list_df_csv.append(input_csv.name)
    list_df_atlas.append(atlas)
    list_df_roi_id.append(roi_id)
    list_df_dvariable.append(dvariable)
    list_df_dti.append(dvariable.split('_')[0])
    list_df_slope.append(slope)
    list_df_stderr.append(stderr)
d = {'input_csv': list_df_csv,
     'atlas': list_df_atlas,
     'roi_id': list_df_roi_id,
     'dvariable': list_df_dvariable,
     'dti_scalar':list_df_dti,
     'slope':list_df_slope,
     'std_err':list_df_stderr}
df = pd.DataFrame(data=d)
print('Complete!\nStart looping through DTI scalars and pick representative examples...')

for dti_scalar in df['dti_scalar'].unique():
    print('Start drawing exmaples for {}'.format(dti_scalar))
    df_selected = df.loc[df['dti_scalar']==dti_scalar].sort_values('std_err')
    num_rows = len(df_selected.index)

    # pick representative examples for this DTI scalar, good, medium, bad
    list_representative_rows = list(range(num_examples_per_class)) \
                             + list(range(num_rows//2-num_examples_per_class//2, num_rows//2+num_examples_per_class//2)) \
                             + list(range(num_rows-num_examples_per_class, num_rows))
    
    # Make figure for each example
    for i in tqdm(list_representative_rows, total=len(list_representative_rows)):
        row = df_selected.iloc[[i]]

        # retrieve info from the row
        input_csv = path_part_folder / row['input_csv'].item()
        atlas = row['atlas'].item()
        roi_id = row['roi_id'].item()
        dvariable = row['dvariable'].item()
        dti_scalar = row['dti_scalar'].item()
        slope = row['slope'].item()
        stderr = row['std_err'].item()
        
        # Load data
        df_input = pd.read_csv(input_csv)
        df_input.drop(df_input[df_input['DTI_ID']==2].index, inplace=True)  # Drop rows from rescan, for easier visualization

        # create figure
        fig, ax = plt.subplots(1,1,figsize=figsize)
        
        # Prepare lists for plotting longitudinal data points (spaghetti)
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
        
        # Sample num_samples_to_plot male subjects to plot
        random_indices = random.sample(range(len(list_male_interval)), num_samples_to_plot)
        for j in random_indices:
            x = list_male_interval[j]
            y = list_male_y[j] - list_male_y[j][0]
            
            ax.plot(x, y, color='tab:blue', alpha=0.3, linestyle='-', linewidth=1, zorder=2*j+1)
            ax.scatter(x, y, color='tab:blue', alpha=0.5, s=2, marker='.', zorder=2*j+1)
        
        # Sample num_samples_to_plot male subjects to plot
        random_indices = random.sample(range(len(list_female_interval)), num_samples_to_plot)
        for j in random_indices:
            x = list_female_interval[j]
            y = list_female_y[j] - list_female_y[j][0]
            
            ax.plot(x, y, color='tab:red', alpha=0.3, linestyle='-', linewidth=1, zorder=2*j)
            ax.scatter(x, y, color='tab:red', alpha=0.5, s=2, marker='.', zorder=2*j)
        
        # Plot regression line
        x = np.array([0, df_input['Interval'].max()])
        y = x*slope
        ax.plot(x,y, color='tab:orange', linewidth=2, zorder=99999)
        
        # Set title: region name
        lut = pd.read_csv(path_lut_folder/"{}_LUT.csv".format(atlas))
        roi_name_full = lut.loc[lut['id']==int(roi_id), 'ROI_rename'].values[0]
        
        ax.set_title(roi_name_full, fontdict=fontdict)
        ax.set_xlabel("Interval (decade)",fontdict=fontdict)
        ax.set_ylabel(r'$σ - σ_{0}$ (z-score)',fontdict=fontdict)
        ax.set_xticks(ticks=[0,0.4,0.8,1.2])
        
        fn_figure = path_figure_output / dti_scalar / "{:03d}_{}_{}_{}_vs_interval_slope_{:.3f}_stderr_{:.3f}.png".format(i, atlas, roi_id, dvariable, slope, stderr)
        fig.savefig(fn_figure, dpi=dpi, bbox_inches='tight')
        plt.close()
