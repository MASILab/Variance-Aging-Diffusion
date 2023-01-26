import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

path_folder_part = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/part')
path_folder_spaghetti = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/spaghetti')

# Loop through every .csv file
for fn in path_folder_part.iterdir():
    if fn.name.endswith('.csv') and len(fn.name.split('-'))==3:
        df = pd.read_csv(fn)
        
        # Parse file name
        s_atlas = fn.name.split('-')[0]
        s_region_id = fn.name.split('-')[1]
        s_measure = fn.name.split('-')[2].replace('.csv','')
        

# Prepare dataframe
list_df_sub = []
list_df_sex = []
list_df_ses = []
list_df_age = []
list_df_val = []
list_df_val_base = []

for sub in df['Subject_ID'].unique():
    # Skip the subject that has only 1 session
    if df.loc[df['Subject_ID']==sub, 'Session'].unique().shape[0] < 2:
        continue

    # Loop through sessions of the subject, from the earliest to the latest
    for (i,ses) in enumerate(df.loc[df['Subject_ID']==sub].sort_values(by=['Age','Session','DTI_ID'],ascending=True)['Session'].unique()):
        sex = df.loc[df['Session']==ses, 'Sex'].values[0] # Sex
        age = df.loc[df['Session']==ses].sort_values(by=['DTI_ID'])['Age'].values[0] # Age
        val = df.loc[df['Session']==ses].sort_values(by=['DTI_ID'])[s_measure].values[0] # value for s_measure, DTI_1 is the first option
        if i == 0:
            val_base = val
        list_df_sub.append(sub)
        list_df_sex.append(sex)
        list_df_ses.append(ses)
        list_df_age.append(age)
        list_df_val.append(val)
        list_df_val_base.append(val_base)

# Create DataFrame from list
d = {"Subject_ID": list_df_sub,
     "Sex": list_df_sex,
     "Session": list_df_ses,
     "Age": list_df_age,
     s_measure: list_df_val,
     "{0}_base".format(s_measure): list_df_val_base}

df_plot = pd.DataFrame(data=d)

# New column: change of value w.r.t. baseline
df_plot["{0}_change".format(s_measure)] = df_plot[s_measure] - df_plot["{0}_base".format(s_measure)]

print(df_plot)

# params for plotting
markersz = 30
markeralpha = 0.5
linealpha = 0.3
linewidth = 1
linestyle = 'solid'
list_color = ['red','blue']
list_label = ['Female','Male']
fig, ax = plt.subplots(figsize=(12,12),dpi=300)

# Scatter plots (female and male)
for i,c in enumerate(list_color):
    x = df_plot.loc[df_plot['Sex']==i]['Age'].values # 0: female, 1: male
    y = df_plot.loc[df_plot['Sex']==i]["{0}_change".format(s_measure)].values
    ax.scatter(x,y,
               s =markersz,
               c =c,
               marker='.',
               alpha= markeralpha,
               linewidths=0,
               label=list_label[i]
               )

# Line up the scatters from the same subject
for i,c in enumerate(list_color):
    for sub_id in df_plot.loc[df_plot['Sex']==i]['Subject_ID'].unique():
        x = df_plot.loc[df_plot['Subject_ID']==sub_id]['Age'].values
        y = df_plot.loc[df_plot['Subject_ID']==sub_id]["{0}_change".format(s_measure)].values
        ax.plot(x,y,
                linestyle=linestyle,
                linewidth=linewidth, 
                markersize=markersz,
                c=c,
                alpha=linealpha
                )

# Horizontal line
ax.axhline(y=0, linewidth=linewidth, c='k', label="Baseline")

# Legend
ax.legend()

# Axis labels
ax.set_xlabel('Age (Year)')
ax.set_ylabel('Change')
ax.set_title("Change in {0} compared to baseline session".format(fn.name.replace('.csv','')))

# Save figure
figure_save = path_folder_spaghetti / "{0}_spaghetti_v2.png".format(fn.name.replace(".csv",""))
plt.savefig(figure_save)