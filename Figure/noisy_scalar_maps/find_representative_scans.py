# pick 3 subjects from young to old

import pandas as pd
import numpy as np

fn_csv = '/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv'
df = pd.read_csv(fn_csv)


# Create simplified dataframe
list_df_session = []
list_df_scanner = []
list_df_age = []
list_df_motion = []
for _,row in df.iterrows():
    session = row['Session']
    scanner_id = session.split('_')[-1]
    age = row['Age']
    motion = row['Motion']
    
    list_df_session.append(session)
    list_df_scanner.append(scanner_id)
    list_df_age.append(age)
    list_df_motion.append(motion)

d = {'Session': list_df_session, 'Scanner':list_df_scanner, 'Age': list_df_age, 'Motion': list_df_motion}
df = pd.DataFrame(data=d)

df.sort_values(by=['Age', 'Session'], inplace=True)

# # for seed in range(50):
# #     print("seed: {0}".format(seed))
# #     print(df.loc[(df['Scanner']=='10') & (df['Age'] <= 45)].sample(random_state=seed))
# #     print(df.loc[(df['Scanner']=='10') & (df['Age'] > 65) & (df['Age'] <75)].sample(random_state=seed))
# #     print(df.loc[(df['Scanner']=='10') & (df['Age'] > 85)].sample(random_state=seed))

for seed in range(50):
    print("seed: {0}".format(seed))
    print(df.loc[(df['Scanner']=='10') & (df['Age'] <= 40)].sample(random_state=seed))
    print(df.loc[(df['Scanner']=='10') & (df['Age'] > 55) & (df['Age'] <70)].sample(random_state=seed))
    print(df.loc[(df['Scanner']=='10') & (df['Age'] > 85)].sample(random_state=seed))