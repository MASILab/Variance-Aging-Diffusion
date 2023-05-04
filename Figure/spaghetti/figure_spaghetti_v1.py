import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

path_folder_part = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/part')
path_folder_spaghetti = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/spaghetti')

# params for plotting
markersz = 30
markeralpha = 0.8
linealpha = 0.3
linestyle = 'solid'
list_color = ['red','blue']
list_label = ['Female','Male']

for fn in path_folder_part.iterdir():
    if fn.name.endswith('.csv') and len(fn.name.split('-'))==3:
        
        # Parse file name
        s_atlas = fn.name.split('-')[0]
        s_region_id = fn.name.split('-')[1]
        s_measure = fn.name.split('-')[2].replace('.csv','')
        
        # Load dataframe
        df = pd.read_csv(fn)
        df = df.loc[df['DTI_ID']==1]
        
        fig, ax = plt.subplots(figsize=(12,12),dpi=300)

        # Scatter plots (female and male)
        for i,c in enumerate(list_color):
            x = df.loc[df['Sex']==i]['Age'].values # 0: female, 1: male
            y = df.loc[df['Sex']==i][s_measure].values
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
            for sub_id in df.loc[df['Sex']==i]['Subject_ID'].unique():
                x = df.loc[df['Subject_ID']==sub_id]['Age'].values
                y = df.loc[df['Subject_ID']==sub_id][s_measure].values
                ax.plot(x,y,
                        linestyle=linestyle,
                        linewidth=1, 
                        markersize=markersz,
                        c=c,
                        alpha=linealpha
                        )
        # Legend
        ax.legend()

        # Axis labels
        ax.set_xlabel('Age (year)')
        ax.set_ylabel(s_measure)
        ax.set_title(fn.name.replace('.csv',''))

        # Save figure
        figure_save = path_folder_spaghetti / "v1" / "{0}_spaghetti_v1.png".format(fn.name.replace(".csv",""))
        plt.savefig(figure_save)
        break