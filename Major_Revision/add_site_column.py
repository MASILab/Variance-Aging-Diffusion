import pandas as pd

if __name__ == '__main__':
    
    df = pd.read_csv('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/data.csv')
    df['site'] = None
    
    # BLSA
    df.loc[df['dataset']=='BLSA', 'site'] = 'blsa_' + df.loc[df['dataset']=='BLSA', 'session'].str.split('scanner').str[-1]
    
    # BIOCARD
    df.loc[df['dataset']=='BIOCARD', 'site'] = 'biocard_0'
    
    # ADNI
    info = pd.read_csv('/nfs/masi/gaoc11/projects/BRAID/data/subject_info/raw/ADNI/ADNI_MRI_T1.csv')
    info['subject'] = 'sub-' + info['Subject ID'].str.split('_S_').str[-1]
    info['site'] = 'adni_' + info['Subject ID'].str.split('_S_').str[0]
    info = info[['subject', 'site']].drop_duplicates()
    
    for idx, row in df.loc[df['dataset']=='ADNI'].iterrows():
        if row['subject'] in info['subject'].values:
            df.loc[idx, 'site'] = info.loc[info['subject']==row['subject'], 'site'].values[0]
        else:
            df.loc[idx, 'site'] = 'adni_na'
    
    print(df['site'].value_counts(dropna=False))
    
    df.to_csv('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/data_site.csv', index=False)
    