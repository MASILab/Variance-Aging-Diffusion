import pandas as pd

# EVE atlas
# EveType1
df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_raw/EveType1_LUT.txt', sep=' ', index_col=False)
df_save = df[['id','ROI']]
df_save.to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/EveType1_LUT.csv', index=False)
# EveType2
df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_raw/EveType2_LUT.txt', sep=' ', index_col=False)
df_save = df[['id','ROI']]
df_save.to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/EveType2_LUT.csv', index=False)
# EveType3
df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_raw/EveType3_LUT.txt', sep=' ', index_col=False)
df_save = df[['id','ROI']]
df_save.to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/EveType3_LUT.csv', index=False)

# SLANT
list_df_id = []
list_df_ROI = []
with open('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_raw/BrainColorLUT.txt') as file:
    for line in file:
        list_df_id.append(line.split()[0])
        list_df_ROI.append(line.split()[1])
d = {"id": list_df_id,
     "ROI": list_df_ROI}
df_save = pd.DataFrame(data=d)
df_save.to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/BrainColor_LUT.csv', index=False)
