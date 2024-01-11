import pandas as pd

df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109.csv')

df_demog = pd.read_excel('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/sublist_demog.xlsx')

list_female_subject_ad = []
list_male_subject_ad = []

for session in df['Session'].unique():
    dxatvi = df_demog.loc[df_demog['labels']==session, 'dxatvi'].item()
    ad = df_demog.loc[df_demog['labels']==session, 'ad'].item()
    sex = df_demog.loc[df_demog['labels']==session, 'sex'].item()
    
    if ad != 0:
        if sex==0:
            list_female_subject_ad.append(session.split('_')[1])
        elif sex==1:
            list_male_subject_ad.append(session.split('_')[1])
        else:
            print("No sex info.")
        print(session, sex, dxatvi, ad)
    else:
        continue

print("Number of female with AD: {}".format(len(set(list_female_subject_ad))))
print("Number of male with AD: {}".format(len(set(list_male_subject_ad))))