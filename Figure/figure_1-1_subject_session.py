# Scatter plot to show the distribution of age and sex of subject at baseline and follow-up sessions.
# Author: Chenyu Gao
# Date: Jan 20, 2023

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv')

# Baseline age
list_df_sub = []
list_df_sex = []
list_df_age_base = []

for sub in np.unique(df['Subject_ID'].values):
    age_base = df.loc[df['Subject_ID'] == sub].sort_values(by=['Age'])['Age'].values[0]
    
    # Make sure that the sex of a subject does not change
    if np.unique(df.loc[df['Subject_ID'] == sub,'Sex'].values).shape[0] != 1:
        print('The subject changed sex!')
        exit()
    sex = df.loc[df['Subject_ID'] == sub,'Sex'].values[0]  
    
    list_df_sub.append(sub)
    list_df_sex.append(sex)
    list_df_age_base.append(age_base)

# Save to dataframe
d = {'Subject_ID': list_df_sub, 'Sex':list_df_sex, 'Age': list_df_age_base}
df_base = pd.DataFrame(data=d)


# Figure_1-1
fig, ax = plt.subplots(figsize=(15, 20),dpi=300)
c_male = 'blue'
c_female = 'red'

# Loop through every subject, from young to old according to baseline age
i = 0  # pseudo subject id for plotting
first_male = True
first_female = True

for index,row in df_base.sort_values(by='Age').iterrows():
    i += 1
    # store x,y cordinates
    X = []
    Y = []

    for age in np.unique(df.loc[df['Subject_ID']==row['Subject_ID']].sort_values(by=['Age'])['Age'].values):
        X.append(age)
        Y.append(i)
    
    # Line plot
    if row['Sex'] == 1:
        ax.plot(X, Y, alpha=0.3, linewidth=0.5, c=c_male)
    else:
        ax.plot(X, Y, alpha=0.3, linewidth=0.5, c=c_female)
    
    # scatter plot
    if row['Sex'] == 1:
        if first_male:
            ax.scatter(x=X, y=Y, s=2, alpha=1, c=c_male, label='Male')
            first_male = False
        else:
            ax.scatter(x=X, y=Y, s=2, alpha=1, c=c_male)
    else:
        if first_female:
            ax.scatter(x=X, y=Y, s=2, alpha=1, c=c_female, label='Female')
            first_female = False
        else:
            ax.scatter(x=X, y=Y, s=2, alpha=1, c=c_female)
    
ax.set_title('Age of Subject in Baseline Session and Follow-Up Sessions') #TODO
ax.set_xlabel('Age (Year)')
ax.set_ylabel('Subject')
ax.set_xlim(left=20, right=105)
ax.set_ylim(bottom=0-5, top=1036+5)
ax.set_yticks([])
ax.legend(loc='lower right')

fig.savefig('./figs/figure_1-1_subject_session.png')