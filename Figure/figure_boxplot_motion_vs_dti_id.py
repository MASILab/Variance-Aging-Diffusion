import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv')
print(df)

# Remove sessions with only 1 DTI (where there is no rescan)
for session in df['Session'].unique():
    if df.loc[df['Session']==session].shape[0]<2:
        index_drop = df.loc[df['Session']==session].index
        df.drop(index_drop, inplace=True)

# Rename labels    
df.loc[df['DTI_ID']==1, 'DTI_ID'] = 'Scan'
df.loc[df['DTI_ID']==2, 'DTI_ID'] = 'Rescan'

# Boxplot
fig,ax = plt.subplots(figsize=(8, 8))
sns.boxplot(data=df, x='DTI_ID', y= 'Motion',orient="v", ax=ax)

# Axis labels
ax.set_xlabel('')
ax.set_ylabel("Averaged RMS (mm)")
ax.set_title('Root Mean Square (RMS) of Eddy Movement Relative the Previous Volume')

# Save figure
figure_save = '/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/figs/figure_boxplot_motion_vs_dti_id.png'
plt.savefig(figure_save)