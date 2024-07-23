import pdb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/BLSA_eddy_movement_rms_average_20221109_w_scanner_id.csv')
df = df[['Subject_ID','Session','Sex','Age']]
df.drop_duplicates(inplace=True)

# collect race information
demog = pd.read_excel('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/sublist_demog.xlsx')
demog['Session'] = demog['labels']
df = df.merge(demog[['Session','race']], on='Session', how='left')

for sex in [1,0]:
    print(f"Race distribution (Sex={sex}, Total={df.loc[df['Sex']==sex, 'Subject_ID'].nunique()})")
    for r in df.loc[df['Sex']==sex, 'race'].unique():
        print(f"\t{r}: {df.loc[(df['Sex']==sex)&(df['race']==r), 'Subject_ID'].nunique()}")


# Visualize age distribution
dict_sex = {1: 'male', 0: 'female'}
df['Sex'] = df['Sex'].map(dict_sex)

fig, ax = plt.subplots(1, 1, figsize=(6.5, 4), tight_layout=True)
sns.histplot(
    data=df, x='Age', hue='Sex',
    binwidth=5, multiple='stack',
    ax=ax,
)
ax.set_xlabel("Age (years)")
ax.set_ylabel(f"Number of sessions (Total={len(df.index)})")

fig.savefig('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/figures/demog/age_distribution.png', dpi=300)