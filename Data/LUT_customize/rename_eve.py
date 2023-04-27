import pandas as pd
import sys

exit() # There is some manual work after this script. Rerunning would overwrite those efforts!

# I mannually renamed Eve-1 labels
df_eve1 = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/EveType1_LUT.csv')

# Lets transfer label names to Eve-2
df_eve2 = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/EveType2_LUT.csv')
df_eve2['ROI_rename'] = ''

for index, row in df_eve2.iterrows():
    try:
        df_eve2.loc[index,'ROI_rename'] = df_eve1.loc[df_eve1['ROI']==row['ROI'],'ROI_rename'].values[0]
    except:
        print(row['ROI'])
df_eve2.to_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/EveType2_LUT.csv", index=False)

# Lets transfer label names to Eve-3
df_eve3 = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/EveType3_LUT.csv')
df_eve3['ROI_rename'] = ''

for index, row in df_eve3.iterrows():
    try:
        df_eve3.loc[index,'ROI_rename'] = df_eve1.loc[df_eve1['ROI']==row['ROI'],'ROI_rename'].values[0]
    except:
        print(row['ROI'])
df_eve3.to_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/EveType3_LUT.csv", index=False)