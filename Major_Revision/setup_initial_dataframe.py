import pandas as pd

if __name__ == '__main__':
    qa =  pd.read_csv('/nfs/masi/gaoc11/GDPR/masi/gaoc11/BRAID/data/quality_assurance/databank_dti_v1_after_pngqa_after_adspqa.csv')

    # update the control_label column with the latest version, add prequal path column
    braid_databank = pd.read_csv('/nfs/masi/gaoc11/GDPR/masi/gaoc11/BRAID/data/dataset_splitting/spreadsheet/databank_dti_v2.csv')    
    qa = qa[[c for c in qa.columns if c != 'control_label']]
    qa = qa.merge(braid_databank[['dataset','subject','session','scan','control_label','prequal_folder']], on=['dataset','subject','session','scan'], how='left')

    # keep cognitively normal subjects from BLSA, BIOCARD, and ADNI
    qa = qa.loc[qa['dataset'].isin(['BLSA','BIOCARD','ADNI']), ]
    qa = qa.loc[qa['scan']==1, ]
    qa = qa.loc[qa['control_label']==1, ]
    qa[['dataset','subject','session','sex','age','prequal_folder']].to_csv('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/data.csv', index=False)
