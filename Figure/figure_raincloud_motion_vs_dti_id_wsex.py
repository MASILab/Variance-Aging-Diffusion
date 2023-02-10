import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv')

# # Remove sessions with only 1 DTI (where there is no rescan)
# for session in df['Session'].unique():
#     if df.loc[df['Session']==session].shape[0]<2:
#         index_drop = df.loc[df['Session']==session].index
#         df.drop(index_drop, inplace=True)
        
# # Prepare a dataframe for plotting
# list_df_session = []
# list_df_sex = []
# list_df_motion_diff = [] # diff = motion(rescan) - motion(scan)
# list_df_motion_diff_percent = []  # (motion(rescan) - motion(scan)) /motion(scan) 

# for session in df['Session'].unique():
#     motion_rescan = df.loc[(df['Session']==session) & (df['DTI_ID']==2),'Motion'].item()
#     motion_scan = df.loc[(df['Session']==session) & (df['DTI_ID']==1),'Motion'].item()
#     motion_diff = motion_rescan - motion_scan
#     motion_diff_percent = (motion_rescan - motion_scan)/motion_scan*100
#     sex = df.loc[(df['Session']==session) & (df['DTI_ID']==1), 'Sex'].item()
    
#     list_df_session.append(session)
#     list_df_sex.append(sex)
#     list_df_motion_diff.append(motion_diff)
#     list_df_motion_diff_percent.append(motion_diff_percent)
    
# d = {'Session': list_df_session,
#      'Sex': list_df_sex, 
#      'Motion_diff':list_df_motion_diff, 
#      'Motion_diff%': list_df_motion_diff_percent}
# df = pd.DataFrame(data=d)
# df.to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_change_scan_vs_rescan_wsex_20230208.csv', index=False)
df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_change_scan_vs_rescan_wsex_20230208.csv')

# Raincloud plot
# hyperparams for figure
figure_save = '/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/figs/figure_raincloud_motion_vs_dti_wsex_v1.png'

fig_width = 14
fig_height = 10
dpi = 300
font_size = 12
jitter = 0.1 # strip plot
alpha_scatter = 0.5
sns.set_style('white')
# #002FA7
fig, axes = plt.subplots(1,2,figsize=(fig_width,fig_height))

# Violin plot
axes[0] = sns.violinplot(data = df,
                         x = 'Sex',
                         y = 'Motion_diff',
                         cut=0,
                         width=0.5,
                         inner=None,
                         ax=axes[0],
                         color='#396ef7',
                         saturation=1,
                         linewidth=0)

# Clip the right half of each violin.
for item in axes[0].collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height, transform=axes[0].transData))
    
# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(axes[0].collections)
axes[0] = sns.stripplot(data = df,
                        x = 'Sex',
                        y= 'Motion_diff',
                        jitter=jitter,
                        alpha=alpha_scatter,
                        color ='#396ef7',
                        size=2,
                        ax=axes[0])

# Shift each strip plot strictly below the correponding volin.
for item in axes[0].collections[num_items:]:
    item.set_offsets(item.get_offsets() + (0.15,0))

# Create narrow boxplots on top of the corresponding violin and strip plots, with thick lines, the mean values, without the outliers.
axes[0] = sns.boxplot(data = df,
                      x = 'Sex',
                    y='Motion_diff',
                    width=0.08,
                    showfliers=False,
                    boxprops=dict(facecolor=(0,0,0,0),
                                linewidth=2, zorder=2),
                    whiskerprops=dict(linewidth=2),
                    capprops=dict(linewidth=2),
                    medianprops=dict(color= '#ff8121', linewidth=2),
                    ax=axes[0])    

# Horizontal line at 0
axes[0].axhline(y=0, linestyle=':',linewidth=1, color = 'black')

axes[0].grid(linestyle=':', linewidth=0.5)
axes[0].set_xlabel('')
axes[0].set_xticks(ticks=[0,1],labels=['Female','Male'])
axes[0].set_ylabel(r'$Motion_{rescan} - Motion_{first}$ (mm)', fontsize=font_size)
axes[0].set_title("Motion of Brain During the Rescan Compared With the First Scan\n", fontsize=font_size+2, loc='left')
axes[0].tick_params(labelsize=font_size)
axes[0].set_ylim(bottom=-0.6,top=1)


# Subplot-2
# Violin plot
axes[1] = sns.violinplot(data = df,
                         x = 'Sex',
                         y = 'Motion_diff%',
                         cut=0,
                         width=0.5,
                         inner=None,
                         ax=axes[1],
                         color='#396ef7',
                         saturation=1,
                         linewidth=0)

# Clip the right half of each violin.
for item in axes[1].collections:
    x0, y0, width, height = item.get_paths()[0].get_extents().bounds
    item.set_clip_path(plt.Rectangle((x0, y0), width/2, height, transform=axes[1].transData))
    
# Create strip plots with partially transparent points of different colors depending on the group.
num_items = len(axes[1].collections)
axes[1] = sns.stripplot(data = df,
                        x = 'Sex',
                        y= 'Motion_diff%',
                        jitter=jitter,
                        alpha=alpha_scatter,
                        color ='#396ef7',
                        size=2,
                        ax=axes[1])

# Shift each strip plot strictly below the correponding volin.
for item in axes[1].collections[num_items:]:
    item.set_offsets(item.get_offsets() + (0.15,0))

# Create narrow boxplots on top of the corresponding violin and strip plots, with thick lines, the mean values, without the outliers.
axes[1] = sns.boxplot(data = df,
                      x = 'Sex',
                    y='Motion_diff%',
                    width=0.08,
                    showfliers=False,
                    boxprops=dict(facecolor=(0,0,0,0),
                                linewidth=2, zorder=2),
                    whiskerprops=dict(linewidth=2),
                    capprops=dict(linewidth=2),
                    medianprops=dict(color= '#ff8121', linewidth=2),
                    ax=axes[1])    

# Horizontal line at 0
axes[1].axhline(y=0, linestyle=':',linewidth=1, color = 'black')

axes[1].grid(linestyle=':', linewidth=0.5)
axes[1].set_xlabel('')
axes[1].set_xticks(ticks=[0,1],labels=['Female','Male'])
axes[1].set_ylabel(r'$\frac{Motion_{rescan} - Motion_{first}}{Motion_{first}}\times100$ (%)', fontsize=font_size)
# axes[1].set_title("Motion of Brain During the Rescan Compared With the First Scan", fontsize=font_size, loc='left')
axes[1].tick_params(labelsize=font_size)
axes[1].set_ylim(bottom=-420/5*3,top=420)







fig.savefig(figure_save, dpi = dpi)