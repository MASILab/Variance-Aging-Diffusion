import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv')

fig, ax = plt.subplots(figsize=(10,15))

for session in df['Session'].unique():
    if df.loc[df['Session']==session].shape[0]==2:
        x = ['Scan', 'Rescan']
        y = [df.loc[(df['Session']==session) & (df['DTI_ID']==1),'Motion'].item(),
             df.loc[(df['Session']==session) & (df['DTI_ID']==2),'Motion'].item(),
             ]
        
        if y[1] > y[0]:
            ax.plot(x,y, color='g', alpha=0.5,linewidth=0.5)
        elif y[1] < y[0]:
            ax.plot(x,y, color='r', alpha=0.5,linewidth=0.5)
        else:
            ax.plot(x,y, color='k', alpha=0.5,linewidth=0.5)
    
# Axis labels
ax.set_xlabel('')
ax.set_ylabel("Averaged RMS (mm)")
ax.set_title('Root Mean Square (RMS) of Eddy Movement Relative the Previous Volume')


# Save figure
figure_save = '/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/figs/figure_lineplot_motion_vs_dti_id.png'
plt.savefig(figure_save)
