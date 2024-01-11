# Scatter plot to show the distribution of age and sex of subject at baseline and follow-up sessions.
# version 2: larger fontsize; change color
#
# Author: Chenyu Gao
# Date: May 11, 2023

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# figure_size = (3.75, 3.4)
figure_size = (3.75, 3.5)
dpi = 750
fontsize=7
fontdict={'fontsize':7}
figure_save = '/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/figs/figure_1-1_subject_session_v2.png'

# Dataframe with session and age information
df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109_w_scanner_id.csv')

# Age at baseline
df['Age_baseline'] = -9999
for subject in df['Subject_ID'].unique():
    df.loc[df['Subject_ID']==subject,'Age_baseline'] = df.loc[df['Subject_ID']==subject,'Age'].min()


fig, ax = plt.subplots(1,1,figsize=figure_size)

# Loop through every subject, from young to old according to baseline age
i = 0  # pseudo subject id for y axis
first_male = True # for adding legend
first_female = True

for subject in df.sort_values(by='Age_baseline')['Subject_ID'].unique():
    i += 1
    X = []
    Y = []
    for session in df.loc[df['Subject_ID']==subject].sort_values(by='Age')['Session'].unique():
        age = df.loc[df['Session']==session,'Age'].values[0]
        X.append(age)
        Y.append(i)

    # Line plot
    if df.loc[df['Subject_ID']==subject,'Sex'].values[0] == 1:
        ax.plot(X, Y, alpha=0.5, linewidth=0.3, c='tab:blue')
    else:
        ax.plot(X, Y, alpha=0.5, linewidth=0.3, c='tab:red')
    
    # scatter plot
    if df.loc[df['Subject_ID']==subject,'Sex'].values[0] == 1:
        if first_male:
            ax.scatter(x=X, y=Y, s=0.2, alpha=0.75, c='tab:blue', label='Male')
            first_male = False
        else:
            ax.scatter(x=X, y=Y, s=0.2, alpha=0.75, c='tab:blue')
    else:
        if first_female:
            ax.scatter(x=X, y=Y, s=0.2, alpha=0.75, c='tab:red', label='Female')
            first_female = False
        else:
            ax.scatter(x=X, y=Y, s=0.2, alpha=0.75, c='tab:red')
    
# ax.set_title('Age of Subject in Baseline Session and Follow-Up Sessions') 
ax.set_xlabel('Age (year)', fontdict=fontdict, labelpad=-2)
ax.set_ylabel('Subject (sorted by age at baseline)', fontdict=fontdict, labelpad=-2)
ax.set_xlim(left=20, right=105)
ax.set_ylim(bottom=0-5, top=1036+5)
ax.set_yticks([])
ax.tick_params(axis='x', labelsize=fontsize, length=2, bottom=True, pad=1)
ax.legend(loc='lower right', fontsize=fontsize)

fig.savefig(figure_save, dpi=dpi, bbox_inches='tight')