# Generate summary of the demographics of BLSA used for this study.
#
# Author: Chenyu Gao
# Date: May 11, 2023

import pandas as pd

csv = '/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109_w_scanner_id.csv'

df = pd.read_csv(csv)

# Number of subjects
num_subject_female = len(df.loc[df['Sex']==0,'Subject_ID'].unique())
num_subject_male = len(df.loc[df['Sex']==1,'Subject_ID'].unique())
num_subject_total = len(df['Subject_ID'].unique())
print('total number of subjects: {}\nnumber of females: {}\nnumber of males: {}'.format(num_subject_total, num_subject_female, num_subject_male))

# Age at baseline
df['Age_baseline'] = -9999
for subject in df['Subject_ID'].unique():
    df.loc[df['Subject_ID']==subject,'Age_baseline'] = df.loc[df['Subject_ID']==subject,'Age'].min()

# range
print('\nAge at baseline\nRange')
print('Female:{} - {}'.format(df.loc[df['Sex']==0,'Age_baseline'].min(),
                              df.loc[df['Sex']==0,'Age_baseline'].max()))
print('Male:{} - {}'.format(df.loc[df['Sex']==1,'Age_baseline'].min(),
                            df.loc[df['Sex']==1,'Age_baseline'].max()))

# Mean and SD
print("\nMean and SD")
print('Female: {} ({})'.format(df.loc[df['Sex']==0,'Age_baseline'].mean(),
                               df.loc[df['Sex']==0,'Age_baseline'].std()))
print('Male: {} ({})'.format(df.loc[df['Sex']==1,'Age_baseline'].mean(),
                             df.loc[df['Sex']==1,'Age_baseline'].std()))

# Sessions
print('\nSessions')
print('Total number of sessions (female): {}'.format(len(df.loc[df['Sex']==0,'Session'].unique())))
print('Total number of sessions (male): {}'.format(len(df.loc[df['Sex']==1,'Session'].unique())))

print('sessions w/ rescan (female): {}'.format(len(df.loc[(df['Sex']==0) & (df['DTI_ID']==2),'Session'].unique())))
print('sessions w/ rescan (male): {}'.format(len(df.loc[(df['Sex']==1) & (df['DTI_ID']==2),'Session'].unique())))

# Number of subject by #sessions
#female
max_total = 0
for subject in df['Subject_ID'].unique():
    if len(df.loc[df['Subject_ID']==subject, 'Session'].unique()) > max_total:
        max_total = len(df.loc[df['Subject_ID']==subject, 'Session'].unique())

counts_female = [0 for _ in range(max_total)]
counts_male = [0 for _ in range(max_total)]

for subject in df['Subject_ID'].unique():
    num_sessions = len(df.loc[df['Subject_ID']==subject,'Session'].unique())
    if df.loc[df['Subject_ID']==subject,'Sex'].values[0]==0:
        counts_female[num_sessions-1] += 1
    else:
        counts_male[num_sessions-1] += 1

for i in range(max_total):
    print('{}\t{}\t{}'.format(i+1,
                              counts_female[i],
                              counts_male[i]))

# Check if every subject has at least 2 scans
print("Following subjects have only 1 DTI scan:")
num = 0
for subject in df['Subject_ID'].unique():
    if len(df.loc[df['Subject_ID']==subject,]) ==1:
        num += 1
        print(subject)
print("total: {}".format(num))

# df.to_csv('./temp.csv', index=False)