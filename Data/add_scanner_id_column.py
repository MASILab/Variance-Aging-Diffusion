import pandas as pd

df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv')

df['Scanner_ID'] = df['Session'].str.split('_').str[-1]


df = df[['Subject_ID', 'Session_ID', 'Scanner_ID', 'Session', 'Sex', 'Age', 'DTI_ID', 'DTI_ID_Full', 'Motion']]
print(df)
print(df.loc[df['Scanner_ID']!='10'])

df.to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109_w_scanner_id.csv', index=False)